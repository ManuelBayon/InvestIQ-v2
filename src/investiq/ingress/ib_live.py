from ib_insync import Ticker, Future, Stock

from investiq.adapters.ibkr.ib_client import IBClient
from investiq.adapters.ibkr.ib_constants import TRADE_TICK_TYPES

from investiq.core.broker_messages import MarketTrade
from investiq.core.event_queue import EventQueue
from investiq.domain.instrument_spec import InstrumentSpec, FutureSpec, StockSpec


class IBLiveIngress:

    def __init__(
            self,
            ib_client: IBClient,
            run_id: str,
            inbound_queue: EventQueue,
            instrument: InstrumentSpec,
    ):
        self._ib_client = ib_client
        self._run_id = run_id
        self._inbound_queue = inbound_queue
        self._instrument = instrument

    def subscribe_to_stock(
            self,
            symbol: str,
            exchange: str = "SMART",
            currency: str = "USD",
    ) -> None:
        """
        Example : reqMktData(symbol="AMD", exchange= "SMART", currency= "USD")
        """
        self._ib_client.request_market_data(
            contract=Stock(
                symbol=symbol,
                exchange=exchange,
                currency=currency
            )
        )

    def subscribe_to_future(
            self,
            symbol: str,
            local_symbol: str,
            exchange: str = "CME",
            currency: str = "USD",
    ) -> None:
        """
        Example : reqMktData(Future(symbol="NQ", local_symbol="NQU6", exchange"CME"))
        """
        self._ib_client.request_market_data(
            contract=Future(
                symbol=symbol,
                localSymbol=local_symbol,
                exchange=exchange,
                currency=currency
            ),
        )

    def on_pending_ticker(self, tickers: set[Ticker]) -> None:
        for ticker in tickers:
            symbol = ticker.contract.symbol

            for tick in ticker.ticks:
                if tick.tickType in TRADE_TICK_TYPES:
                    event = MarketTrade(
                        run_id=self._run_id,
                        symbol=symbol,
                        timestamp_utc=tick.time,
                        price=tick.price,
                        size=tick.size,
                    )
                    self._inbound_queue.enqueue(event)
                else:
                    continue


    def start(self) -> None:

        self._ib_client.set_market_data_type()

        if isinstance(self._instrument, FutureSpec):
            self.subscribe_to_future(
                symbol=self._instrument.symbol,
                local_symbol=self._instrument.local_symbol,
                exchange=self._instrument.exchange,
                currency=self._instrument.currency,
            )
        elif isinstance(self._instrument, StockSpec):
            self.subscribe_to_stock(
                symbol=self._instrument.symbol,
                exchange=self._instrument.exchange,
                currency=self._instrument.currency,
            )
        else:
            raise NotImplementedError(
                f"Unsupported instrument {type(self._instrument).__name__}"
            )

        self._ib_client.subscribe_pending_tickers(handler=self.on_pending_ticker)
        self._ib_client.run()

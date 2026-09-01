from ib_insync import Ticker, Future, Stock

from investiq.adapters.ibkr.ib_client import IBClient
from investiq.adapters.ibkr.ib_constants import TRADE_TICK_TYPES

from investiq.core.event_factory import CanonicalEventFactory
from investiq.core.event_queue import EventQueue


class IBLiveIngress:

    def __init__(
            self,
            ib_client: IBClient,
            event_factory: CanonicalEventFactory,
            external_event_queue: EventQueue,
    ):
        self._ib_client = ib_client
        self._event_factory = event_factory
        self._external_event_queue = external_event_queue

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
                    event = self._event_factory.create_trade_received(
                        symbol=symbol,
                        timestamp_utc=tick.time,
                        price=tick.price,
                        size=tick.size,
                    )
                    self._external_event_queue.enqueue(event)
                else:
                    continue


    def start(self) -> None:
        self._ib_client.set_market_data_type()
        self.subscribe_to_future(symbol="MNQ", local_symbol="MNQU6")
        self._ib_client.subscribe_pending_tickers(handler=self.on_pending_ticker)
        self._ib_client.run()
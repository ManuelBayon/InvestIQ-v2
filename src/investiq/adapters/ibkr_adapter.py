import asyncio

from ib_insync import IB, Ticker, Stock, Future, Contract, MarketOrder, Trade

from investiq.domain.instruments import StockSpecs
from investiq.domain.models import RawTick
from investiq.domain.order_specs import Side, OrderSpec, MarketOrderSpec
from investiq.events.factory import CanonicalEventFactory
from investiq.runtime.canonical_event_queue import CanonicalEventQueue

class IBKRGatewayAdapter:
    """
    2026-05-21 :
        MVP limitation:
            IB reqMktData delayed ticks are used as proxy ticks.
            TickData.time is treated as tick timestamp for aggregation,
            but this is not guaranteed to be exchange trade-time.
    """
    def __init__(
            self,
            event_factory: CanonicalEventFactory,
            event_queue: CanonicalEventQueue,
    ):
        self._ib = IB()
        self._ib.pendingTickersEvent += self.on_pending_ticker
        self._tickers: dict[str, Ticker] = {}

        self._history: dict[str, list[Ticker]]
        self._event_factory = event_factory
        self._event_queue = event_queue


    def connect(
            self,
            host: str = "127.0.0.1",
            port: int = 4002,
            client_id: int = 1,
            data_type: int = 3,  # 1 = Live / 3 = Delayed
    ) -> None:
        self._ib.connect(host, port, clientId=client_id)
        self._ib.reqMarketDataType(data_type)

    def disconnect(self):
        self._ib.disconnect()

    def subscribe_to_stock(
            self,
            symbol: str,
            exchange: str = "SMART",
            currency: str = "USD",
    ) -> None:
        """
        Example : reqMktData(symbol="AMD", exchange= "SMART", currency= "USD")
        """
        self._tickers[symbol] = self._ib.reqMktData(Stock(symbol, exchange, currency))

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
        self._tickers[symbol] = self._ib.reqMktData(
            contract=Future(
                symbol=symbol,
                localSymbol=local_symbol,
                exchange=exchange,
                currency=currency
            ),
        )

    def run(self) -> None:
        self._loop = asyncio.get_event_loop()
        self._ib.run()

    def on_pending_ticker(
            self,
            tickers: set[Ticker]
    ) -> None:
        """
        2026-05-28 — Adapter boundary:
        - ib_insync.Ticker and ib_insync.TickData do not cross this method.
        - This method converts IB ticks into internal RawTick objects.
        - Current prototype forwards all observed ticks.
        - No deduplication is guaranteed here yet.
        - Ordering is the iteration order received from ib_insync.
        """
        raw_ticks: dict[str, list[RawTick]] = {}
        for t in tickers:

            _symbol = t.contract.symbol
            for tick in t.ticks:

                if tick.tickType != 68:
                    continue

                if _symbol not in raw_ticks:
                    raw_ticks[_symbol] = []

                raw_tick = RawTick(
                    symbol=_symbol,
                    tick_type=tick.tickType,
                    timestamp_utc=tick.time,
                    price=tick.price,
                    size=tick.size,
                )
                raw_ticks[_symbol].append(raw_tick)

        if not raw_ticks:
            return

        event = self._event_factory.create_tick_data_available(
            payload=raw_ticks
        )
        self._event_queue.enqueue(event)

    def place_market_order(
            self,
            order_specs: MarketOrderSpec
    ) -> None:
        instrument = order_specs.instrument
        if isinstance(instrument, StockSpecs):
            contract = Stock(
                symbol=instrument.symbol,
                exchange=instrument.exchange,
                currency=instrument.currency
            )
        else:
            raise NotImplementedError(
                f"Unsupported instrument for market order:{type(instrument).__name__}"
            )

        order = MarketOrder(
            action=order_specs.direction.name,
            totalQuantity=order_specs.quantity
        )
        order.tif = order_specs.tif

        self._loop.call_soon_threadsafe(
            self._place_market_order_on_ib_loop,
            contract,
            order
        )

    def _place_market_order_on_ib_loop(self, contract: Contract, order: MarketOrder) -> None:
        trade = self._ib.placeOrder(contract, order)
        print("[IBKR TRADE CREATED]", trade)
import asyncio

from ib_insync import IB, Ticker, Stock, Future, MarketOrder, Trade, OrderStatus, Fill

from investiq.adapters.mappers import map_ibkr_order_status_to_canonical_event
from investiq.domain.instruments import StockSpecs, FutureSpecs
from investiq.domain.models import RawTick
from investiq.domain.order_specs import MarketOrderSpecs
from investiq.events.factory import CanonicalEventFactory
from investiq.runtime.canonical_event_queue import CanonicalEventQueue


class IBKRAdapter:
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
        self._ib_loop = None
        self._ib.pendingTickersEvent += self.on_pending_ticker
        self._tickers: dict[str, Ticker] = {}

        self._history: dict[str, list[Ticker]]
        self._event_factory = event_factory
        self._event_queue = event_queue


    def connect(
            self,
            host: str = "127.0.0.1",
            port: int = 7497,
            client_id: int = 1,
            data_type: int = 3,  # 1 = Live / 3 = Delayed
    ) -> None:
        self._ib.connect(host, port, clientId=client_id)
        self._ib.reqMarketDataType(data_type)

    def disconnect(self):
        self._ib.disconnect()

    def run(self) -> None:
        self._ib_loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self._ib_loop)

        self.connect()
        self.subscribe_to_future(symbol="MNQ", local_symbol="MNQU6")
        self._ib.run()

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

    def on_pending_ticker(self, tickers: set[Ticker]) -> None:
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

    def _on_status_update(self, trade: Trade) -> None:
        event = map_ibkr_order_status_to_canonical_event(
            status=trade.orderStatus,
            event_factory=self._event_factory
        )
        print(event)

    def _on_fill(self, trade: Trade, fill: Fill) -> None:
        status = trade.orderStatus
        execution = fill.execution
        event = self._event_factory.create_fill_received(
            order_id=status.orderId,
            parent_id=status.parentId,
            client_id=status.clientId,
            broker_perm_id=status.permId,
            timestamp_utc=execution.time,
            account_num=execution.acctNumber,
            qty_executed=execution.shares,
            side=execution.side,
            price=execution.price,
            cumul_qty=execution.cumQty,
        )
        print(event)

    def place_market_order(
            self,
            order_specs: MarketOrderSpecs
    ) -> None:

        instrument = order_specs.instrument

        if isinstance(instrument, StockSpecs):
            contract = Stock(
                symbol=instrument.symbol,
                exchange=instrument.exchange,
                currency=instrument.currency
            )
        elif isinstance(instrument, FutureSpecs):
            contract = Future(
                symbol=instrument.symbol,
                localSymbol=instrument.local_symbol,
                exchange=instrument.exchange,
                currency=instrument.currency,
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
        trade = self._ib.placeOrder(contract, order)
        trade.statusEvent += self._on_status_update
        trade.fillEvent += self._on_fill

    @property
    def ib_loop(self):
        return self._ib_loop
import asyncio

from ib_insync import Stock, Future, MarketOrder, Trade, Fill, CommissionReport

from investiq.adapters.ibkr_client import IBKRClient
from investiq.adapters.ibkr_market_data_adapter import IBKRMarketDataAdapter
from investiq.adapters.mappers import map_ibkr_order_status_to_canonical_event

from investiq.domain.instruments import StockSpecs, FutureSpecs
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
            ibkr_client: IBKRClient,
            ibkr_market_data_adapter: IBKRMarketDataAdapter,
            event_factory: CanonicalEventFactory,
            event_queue: CanonicalEventQueue,
    ):
        self._ibkr_client = ibkr_client
        self._ibkr_market_data_adapter = ibkr_market_data_adapter

        self._event_factory = event_factory
        self._event_queue = event_queue


    def run(self) -> None:
        self._ib_loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self._ib_loop)

        self._ibkr_client.connect()
        self._ibkr_client.set_market_data_type()
        self._ibkr_market_data_adapter.subscribe_to_future(
            symbol="MNQ",
            local_symbol="MNQU6"
        )
        self._ibkr_client.run()

    def _on_status_update(self, trade: Trade) -> None:
        event = map_ibkr_order_status_to_canonical_event(
            status=trade.orderStatus,
            event_factory=self._event_factory
        )
        self._event_queue.enqueue(event)

    def _on_fill(self, trade: Trade, fill: Fill) -> None:
        status = trade.orderStatus
        execution = fill.execution
        event = self._event_factory.create_fill_received(
            order_id=status.orderId,
            parent_id=status.parentId,
            client_id=status.clientId,
            broker_perm_id=status.permId,
            exec_id=execution.execId,
            timestamp_utc=execution.time,
            account_num=execution.acctNumber,
            qty_executed=execution.shares,
            side=execution.side,
            price=execution.price,
            cumul_qty=execution.cumQty,
        )
        self._event_queue.enqueue(event)

    def _on_commission_report(
            self,
            trade: Trade,
            fill: Fill,
            report: CommissionReport
    ) -> None:
        status = trade.orderStatus
        execution = fill.execution
        event = self._event_factory.create_commission_report_received(
            order_id=status.orderId,
            parent_id=status.parentId,
            client_id=status.clientId,
            broker_perm_id=status.permId,
            exec_id=execution.execId,
            commission=report.commission,
            currency=report.currency,
            realized_pnl=report.realizedPNL,
        )
        self._event_queue.enqueue(event)

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
        trade = self._ibkr_client.place_order(contract, order)
        trade.statusEvent += self._on_status_update
        trade.fillEvent += self._on_fill
        trade.commissionReportEvent += self._on_commission_report

    @property
    def ib_loop(self):
        return self._ib_loop
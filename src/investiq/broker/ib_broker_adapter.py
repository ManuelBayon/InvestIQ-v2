from ib_insync import Trade, Fill, CommissionReport, MarketOrder

from investiq.adapters.ibkr.ib_client import IBKRClient
from investiq.adapters.ibkr.ib_contract_mappers import map_stock_specs_to_ib_contract, map_future_specs_to_ib_contract
from investiq.domain.instruments import StockSpecs, FutureSpecs
from investiq.domain.order_specs import MarketOrderSpecs
from investiq.events.factory import CanonicalEventFactory
from investiq.core.event_queue import CanonicalEventQueue


class IBKRBrokerAdapter:

    def __init__(
            self,
            ibkr_client: IBKRClient,
            event_factory: CanonicalEventFactory,
            event_queue: CanonicalEventQueue,
    ):
        self._ibkr_client = ibkr_client
        self._event_factory = event_factory
        self._event_queue = event_queue

    def _on_status_update(self, trade: Trade) -> None:
        status = trade.orderStatus
        event = self._event_factory.create_order_status_updated(
            order_id=status.orderId,
            parent_id=status.parentId,
            status=status.status,
            client_id=status.clientId,
            broker_perm_id=status.permId,
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

    def place_market_order(self, specs: MarketOrderSpecs) -> None:

        instrument_specs = specs.instrument

        if isinstance(instrument_specs, StockSpecs):
            contract = map_stock_specs_to_ib_contract(instrument_specs)

        elif isinstance(instrument_specs, FutureSpecs):
            contract = map_future_specs_to_ib_contract(instrument_specs)

        else:
            raise NotImplementedError(
                f"Unsupported instrument type: {type(instrument_specs).__name__}"
            )

        # Build market order
        order = MarketOrder(action=specs.direction.name, totalQuantity=specs.quantity)
        order.tif = specs.tif

        # Place market order
        trade = self._ibkr_client.place_order(contract=contract, order=order)

        # Subscribe to broker events
        trade.statusEvent += self._on_status_update
        trade.fillEvent += self._on_fill
        trade.commissionReportEvent += self._on_commission_report
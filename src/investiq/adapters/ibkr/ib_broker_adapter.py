from ib_insync import Trade, Fill, CommissionReport, MarketOrder

from investiq.domain.instrument_spec import StockSpec, FutureSpec, InstrumentSpec
from investiq.domain.order_types import MarketOrderSpec
from investiq.adapters.ibkr.ib_client import IBKRClient
from investiq.adapters.ibkr.ib_contract_mappers import map_stock_specs_to_ib_contract, map_future_specs_to_ib_contract
from investiq.core.event_factory import CanonicalEventFactory
from investiq.core.event_queue import EventQueue


class IBKRAdapter:

    def __init__(
            self,
            ib_client: IBKRClient,
            event_factory: CanonicalEventFactory,
            external_event_queue: EventQueue,
    ):

        self._ib_client = ib_client
        self._event_factory = event_factory
        self._external_event_queue = external_event_queue


    def _on_status_update(self, trade: Trade) -> None:
        print("IB CALLBACK STATUS UPDATED") # debug
        status = trade.orderStatus
        event = self._event_factory.create_order_status_updated(
            order_id=status.orderId,
            parent_id=status.parentId,
            status=status.status,
            client_id=status.clientId,
            perm_id=status.permId,
        )
        print(event)
        self._external_event_queue.enqueue(event)


    def _on_fill(self, trade: Trade, fill: Fill) -> None:
        print("IB CALLBACK FILL RECEIVED") # debug
        status = trade.orderStatus
        execution = fill.execution
        event = self._event_factory.create_fill_received(
            order_id=status.orderId,
            parent_id=status.parentId,
            client_id=status.clientId,
            perm_id=status.permId,
            exec_id=execution.execId,
            timestamp_utc=execution.time,
            account_num=execution.acctNumber,
            qty_executed=execution.shares,
            side=execution.side,
            price=execution.price,
            cumul_qty=execution.cumQty,
        )
        print(event)
        self._external_event_queue.enqueue(event)


    def _on_commission_report(
            self,
            trade: Trade,
            fill: Fill,
            report: CommissionReport
    ) -> None:
        print("IB CALLBACK COMMISSION RECEIVED") # debug
        status = trade.orderStatus
        execution = fill.execution
        event = self._event_factory.create_commission_report_received(
            order_id=status.orderId,
            parent_id=status.parentId,
            client_id=status.clientId,
            perm_id=status.permId,
            exec_id=execution.execId,
            commission=report.commission,
            currency=report.currency,
            realized_pnl=report.realizedPNL,
        )
        print(event)
        self._external_event_queue.enqueue(event)


    def place_market_order(
            self,
            contract_spec: InstrumentSpec,
            order_spec: MarketOrderSpec
    ) -> None:

        if isinstance(contract_spec, StockSpec):
            contract = map_stock_specs_to_ib_contract(contract_spec)

        elif isinstance(contract_spec, FutureSpec):
            contract = map_future_specs_to_ib_contract(contract_spec)

        else:
            raise NotImplementedError(
                f"Unsupported instrument type: "
                f"{type(contract_spec).__name__}, "
                f"available are Stock and Future."
            )

        # Build market order
        action = "BUY" if order_spec.quantity > 0 else "SELL"
        order = MarketOrder(
            action=action,
            totalQuantity=abs(order_spec.quantity)
        )
        order.tif = "DAY"

        # Place market order
        trade = self._ib_client.place_order(contract=contract, order=order)

        # Subscribe to broker events
        trade.statusEvent += self._on_status_update
        trade.fillEvent += self._on_fill
        trade.commissionReportEvent += self._on_commission_report
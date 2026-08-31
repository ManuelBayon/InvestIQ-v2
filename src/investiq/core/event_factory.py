from datetime import datetime

from investiq.core.events import TradeReceived, OrderGenerated, OrderStatusUpdated, FillReceived, \
    CommissionReportReceived
from investiq.domain.order_types import Order


class CanonicalEventFactory:

    def __init__(self, run_id: str):
        self._run_id = run_id
        self._next_event_id: int = 1

    def _make_next_event_id(self) -> str:
        event_id =  f"EVT_{self._next_event_id:05d}"
        self._next_event_id += 1
        return event_id

    def create_trade_received(
            self,
            symbol: str,
            timestamp_utc: datetime,
            price: float,
            size: float,
    ) -> TradeReceived:

        event = TradeReceived(
            run_id=self._run_id,
            event_id=self._make_next_event_id(),
            symbol=symbol,
            timestamp_utc=timestamp_utc,
            price=price,
            size=size,
        )
        return event


    def create_order_generated(
            self,
            order: Order
    ) -> OrderGenerated:
        return OrderGenerated(
            run_id=self._run_id,
            event_id=self._make_next_event_id(),
            order=order
        )


    def create_order_status_updated(
            self,
            order_id,
            parent_id,
            status,
            client_id,
            perm_id
    ) -> OrderStatusUpdated:
        event = OrderStatusUpdated(
            run_id=self._run_id,
            event_id=self._make_next_event_id(),
            order_id=order_id,
            parent_id=parent_id,
            status=status,
            client_id=client_id,
            perm_id=perm_id
        )
        return event


    def create_fill_received(
            self,
            order_id,
            parent_id,
            client_id,
            perm_id,
            exec_id,
            timestamp_utc,
            account_num,
            qty_executed,
            side,
            price,
            cumul_qty
    ) -> FillReceived:

        event = FillReceived(
            run_id=self._run_id,
            event_id=self._make_next_event_id(),
            order_id=order_id,
            parent_id=parent_id,
            client_id=client_id,
            perm_id=perm_id,
            exec_id=exec_id,
            timestamp_utc=timestamp_utc,
            account_num=account_num,
            qty_executed=qty_executed,
            side=side,
            price=price,
            cumul_qty=cumul_qty,
        )
        return event


    def create_commission_report_received(
            self,
            order_id,
            parent_id,
            client_id,
            perm_id,
            exec_id,
            commission,
            currency,
            realized_pnl
    ) -> CommissionReportReceived:

        event = CommissionReportReceived(
            run_id=self._run_id,
            event_id=self._make_next_event_id(),
            order_id=order_id,
            parent_id=parent_id,
            client_id=client_id,
            perm_id=perm_id,
            exec_id=exec_id,
            commission=commission,
            currency=currency,
            realized_pnl=realized_pnl
        )
        return event
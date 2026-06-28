from datetime import datetime

from investiq.domain.decision.base import NoOperation, OrderIntent
from investiq.domain.order_specs import OrderSpecs

from investiq.events.intents import IntentGenerated
from investiq.events.market_data import TradeReceived
from investiq.events.orders import OrderSubmitted, ExecutionSkipped, \
    OrderStatusUpdated, FillReceived, CommissionReportReceived


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
            metadata : dict | None = None,
    ) -> TradeReceived:

        if metadata is None:
            metadata = {}

        return TradeReceived(
            run_id=self._run_id,
            event_id=self._make_next_event_id(),
            causation_id=None,
            metadata=metadata,
            symbol=symbol,
            timestamp_utc=timestamp_utc,
            price=price,
            size=size,
        )

    def create_intent_generated(
            self,
            causation_id: str,
            intent: NoOperation | OrderIntent,
            metadata: dict | None = None
    ) -> IntentGenerated:

        if metadata is None:
            metadata = {}

        return IntentGenerated(
            run_id=self._run_id,
            event_id=self._make_next_event_id(),
            causation_id=causation_id,
            metadata=metadata,
            intent=intent
        )

    def create_order_submitted(
            self,
            causation_id: str,
            order: OrderSpecs,
            metadata: dict | None = None
    ) -> OrderSubmitted:

        if metadata is None:
            metadata = {}

        return OrderSubmitted(
            run_id=self._run_id,
            event_id=self._make_next_event_id(),
            causation_id=causation_id,
            metadata=metadata,
            order=order,
        )

    def create_no_order_submitted(
            self,
            causation_id: str,
            reason: str,
            metadata: dict | None = None
    ) -> ExecutionSkipped:

        if metadata is None:
            metadata = {}

        return ExecutionSkipped(
            run_id=self._run_id,
            event_id=self._make_next_event_id(),
            causation_id=causation_id,
            metadata=metadata,
            reason=reason,
        )

    def create_order_status_updated(
            self,
            order_id: int,
            parent_id: int,
            status: str,
            client_id: int,
            broker_perm_id: int,
            metadata: dict | None = None
    ) -> OrderStatusUpdated:

        if metadata is None:
            metadata = {}

        return OrderStatusUpdated(
            run_id=self._run_id,
            event_id=self._make_next_event_id(),
            causation_id=None,
            metadata=metadata,
            order_id=order_id,
            parent_id=parent_id,
            status=status,
            client_id=client_id,
            perm_id=broker_perm_id)

    def create_fill_received(
            self,
            order_id: int,
            parent_id: int,
            client_id: int,
            broker_perm_id: int,
            exec_id: str,
            timestamp_utc: datetime,
            account_num: str,
            qty_executed: float,
            side: str,
            price: float,
            cumul_qty: float,
            metadata: dict | None = None
    ) -> FillReceived:

        if metadata is None:
            metadata = {}

        return FillReceived(
            run_id=self._run_id,
            event_id=self._make_next_event_id(),
            causation_id=None,
            metadata=metadata,
            order_id=order_id,
            parent_id=parent_id,
            client_id=client_id,
            perm_id=broker_perm_id,
            exec_id=exec_id,
            timestamp_utc=timestamp_utc,
            account_num=account_num,
            qty_executed=qty_executed,
            side=side,
            price=price,
            qty_cumul=cumul_qty,
        )

    def create_commission_report_received(
            self,
            order_id: int,
            parent_id: int,
            client_id: int,
            broker_perm_id: int,
            exec_id: str,
            commission: float,
            currency: str,
            realized_pnl: float,
            metadata: dict | None = None
    ) -> CommissionReportReceived:

        if metadata is None:
            metadata = {}

        return CommissionReportReceived(
            run_id=self._run_id,
            event_id=self._make_next_event_id(),
            causation_id=None,
            metadata=metadata,
            order_id=order_id,
            parent_id=parent_id,
            client_id=client_id,
            perm_id=broker_perm_id,
            exec_id=exec_id,
            commission=commission,
            currency=currency,
            realized_pnl=realized_pnl,
        )
from dataclasses import dataclass
from datetime import datetime

from investiq.domain.order_specs import OrderSpecs
from investiq.events.base import CanonicalEvent


@dataclass(frozen=True)
class OrderSubmitted(CanonicalEvent):
    order : OrderSpecs
    def __repr__(self):
        return (
            f"OrderSubmitted(\n"
            f"\trun_id={self.run_id},\n"
            f"\tevent_id={self.event_id},\n"
            f"\tcausation_id={self.causation_id},\n"
            f"\torder={self.order}\n"
            f")"
        )


@dataclass(frozen=True)
class ExecutionSkipped(CanonicalEvent):
    reason: str
    def __repr__(self):
        return (
            f"ExecutionSkipped(\n"
            f"\trun_id={self.run_id},\n"
            f"\tevent_id={self.event_id},\n"
            f"\tcausation_id={self.causation_id},\n"
            f"\treason={self.reason}\n"
            f")"
        )


@dataclass(frozen=True)
class OrderStatusUpdated(CanonicalEvent):
    order_id: int
    parent_id: int
    status: str
    perm_id: int
    client_id: int = 1
    def __repr__(self):
        return (
            f"OrderStatusUpdated(\n"
            f"\trun_id={self.run_id},\n"
            f"\tevent_id={self.event_id},\n"
            f"\tcausation_id={self.causation_id},\n"
            f"\torder_id={self.order_id},\n"
            f"\tparent_id={self.parent_id},\n"
            f"\tstatus={self.status},\n"
            f"\tperm_id={self.perm_id},\n"
            f"\tclient_id={self.client_id},\n"
            f")"
        )





@dataclass(frozen=True)
class FillReceived(CanonicalEvent):
    order_id: int
    parent_id: int
    client_id: int
    account_num: str
    perm_id: int
    exec_id: str
    timestamp_utc: datetime
    side: str
    qty_executed: float
    price: float
    qty_cumul: float
    def __repr__(self):
        return (
            f"FillReceived(\n"
            f"\trun_id={self.run_id},\n"
            f"\tevent_id={self.event_id},\n"
            f"\tcausation_id={self.causation_id},\n"
            f"\torder_id={self.order_id},\n"
            f"\tparent_id={self.parent_id},\n"
            f"\tclient_id={self.client_id},\n"
            f"\taccount_num={self.account_num},\n"
            f"\tperm_id={self.perm_id},\n"
            f"\texec_id={self.exec_id},\n"
            f"\ttimestamp_utc={self.timestamp_utc},\n"
            f"\tside={self.side},\n"
            f"\tqty_executed={self.qty_executed},\n"
            f"\tprice={self.price}\n"
            f"\tcumul_qty={self.qty_cumul}\n"
            f")"
        )


@dataclass(frozen=True)
class CommissionReportReceived(CanonicalEvent):
    order_id: int
    parent_id: int
    client_id: int
    perm_id: int
    exec_id: str
    currency: str
    commission: float
    realized_pnl: float
    def __repr__(self):
        return (
            f"CommissionReportReceived(\n"
            f"\trun_id={self.run_id},\n"
            f"\tevent_id={self.event_id},\n"
            f"\tcausation_id={self.causation_id},\n"
            f"\torder_id={self.order_id},\n"
            f"\tparent_id={self.parent_id},\n"
            f"\tclient_id={self.client_id},\n"
            f"\tbroker_perm_id={self.perm_id},\n"
            f"\texec_id={self.exec_id},\n"
            f"\tcurrency={self.currency},\n"
            f"\tcommission={self.commission},\n"
            f"\trealized_pnl={self.realized_pnl},\n"
            f")"
        )
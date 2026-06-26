from abc import ABC
from dataclasses import dataclass, field
from datetime import datetime

from investiq.domain.decision_layer.base import NoOperation, OrderIntent
from investiq.domain.models import RawTick
from investiq.domain.order_specs import OrderSpecs


@dataclass(frozen=True)
class CanonicalEvent(ABC):
    run_id: str
    event_id: str
    causation_id: str | None
    meta_data: dict

@dataclass(frozen=True)
class TickDataAvailable(CanonicalEvent):
    payload: dict[str, list[RawTick]]
    def __repr__(self):
        return (
            f"TickDataAvailable(\n"
            f"\trun_id={self.run_id},\n"
            f"\tevent_id={self.event_id},\n"
            f"\tcausation_id={self.causation_id},\n"
            f"\tpayload={self.payload}\n"
            f")"
        )

@dataclass(frozen=True)
class IntentGenerated(CanonicalEvent):
    payload: NoOperation | OrderIntent
    def __repr__(self):
        return (
            f"IntentGenerated(\n"
            f"\trun_id={self.run_id},\n"
            f"\tevent_id={self.event_id},\n"
            f"\tcausation_id={self.causation_id},\n"
            f"\tpayload={self.payload}\n"
            f")"
        )

@dataclass(frozen=True)
class OrderSubmitted(CanonicalEvent):
    payload : OrderSpecs
    def __repr__(self):
        return (
            f"OrderSubmitted(\n"
            f"\trun_id={self.run_id},\n"
            f"\tevent_id={self.event_id},\n"
            f"\tcausation_id={self.causation_id},\n"
            f"\tpayload={self.payload}\n"
            f")"
        )

@dataclass(frozen=True)
class ExecutionSkipped(CanonicalEvent):
    payload : dict
    def __repr__(self):
        return (
            f"ExecutionSkipped(\n"
            f"\trun_id={self.run_id},\n"
            f"\tevent_id={self.event_id},\n"
            f"\tcausation_id={self.causation_id},\n"
            f"\treason={self.payload["reason"]}\n"
            f")"
        )

@dataclass(frozen=True)
class OrderStatusUpdated(CanonicalEvent):
    order_id: int
    parent_id: int
    status: str
    broker_perm_id: int
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
            f"\tclient_id={self.client_id},\n"
            f"\tbroker_perm_id={self.broker_perm_id},\n")

@dataclass(frozen=True)
class FillReceived(CanonicalEvent):
    order_id: int
    parent_id: int
    client_id: int
    broker_perm_id: int
    timestamp_utc: datetime
    account_num: str
    shares: float
    avg_price: float

@dataclass(frozen=True)
class CommissionReportReceived(CanonicalEvent):
    pass
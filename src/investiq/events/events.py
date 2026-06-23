from abc import ABC
from dataclasses import dataclass

from investiq.domain.decision_layer.base import NoOperation, OrderIntent
from investiq.domain.models import RawTick
from investiq.domain.order_specs import OrderSpecs


@dataclass(frozen=True)
class CanonicalEvent(ABC):
    run_id: str
    event_id: str
    causation_id: str | None
    meta_data: dict
    payload: object

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
from abc import ABC
from dataclasses import dataclass

from investiq.domain.decision_layer import NoOperation, OrderIntent
from investiq.domain.models import RawTick


@dataclass(frozen=True)
class BaseEvent(ABC):
    run_id: str
    event_id: str
    causation_id: str | None
    meta_data: dict[str, str]

@dataclass(frozen=True)
class TickDataAvailable(BaseEvent):
    payload: dict[str, list[RawTick]]
    def __repr__(self):
        return (
            f"\n"
            f"TickDataAvailable(\n"
            f"\trun_id={self.run_id},\n"
            f"\tevent_id={self.event_id},\n"
            f"\tcausation_id={self.causation_id},\n"
            f"\tpayload={self.payload}\n"
            f")"
        )

@dataclass(frozen=True)
class IntentGenerated(BaseEvent):
    payload: NoOperation | OrderIntent
    def __repr__(self):
        return (
            f"\n"
            f"IntentGenerated(\n"
            f"\trun_id={self.run_id},\n"
            f"\tevent_id={self.event_id},\n"
            f"\tcausation_id={self.causation_id},\n"
            f"\tpayload={self.payload}\n"
            f")"
        )
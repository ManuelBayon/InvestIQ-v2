from abc import ABC
from dataclasses import dataclass

from investiq.domain.models import Bar
from investiq.domain.order_intents import Intent


@dataclass(frozen=True)
class BaseEvent(ABC):
    run_id: str
    event_id: str
    causation_id: str | None
    meta_data: dict[str, str]

@dataclass(frozen=True)
class BarAvailable(BaseEvent):
    bar: Bar

@dataclass(frozen=True)
class DecisionContext:
    bar: Bar
    features: dict[str, float | None]

@dataclass(frozen=True)
class IntentGenerated(BaseEvent):
    context: DecisionContext
    intent: Intent

@dataclass(frozen=True)
class NoOperation(BaseEvent):
    context: DecisionContext
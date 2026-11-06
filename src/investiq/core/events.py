from abc import ABC
from dataclasses import dataclass
from enum import StrEnum, auto

from investiq.domain.orders import OrderSpec


@dataclass(frozen=True)
class CanonicalEvent(ABC):
    run_id: str
    event_id: str


@dataclass(frozen=True)
class InternalEvent(CanonicalEvent):
    ...


@dataclass(frozen=True)
class IntentGenerated(InternalEvent):
    causation_id: str
    spec: OrderSpec
    def __repr__(self) -> str:
        return (
            f"{self.event_id} "
            f"IntentGenerated : "
            f"causation_id={self.causation_id}, "
            f"spec={self.spec}"
        )

class OrderRole(StrEnum):
    ENTRY = auto()
    STOP_LOSS = auto()
    TAKE_PROFIT = auto()


@dataclass(frozen=True, slots=True)
class OrderCreated(InternalEvent):
    intention_id: str
    order_id: int
    parent_id: int | None
    role: OrderRole
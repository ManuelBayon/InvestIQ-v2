from abc import ABC

from dataclasses import dataclass


@dataclass(frozen=True)
class CanonicalEvent(ABC):
    run_id: str
    event_id: str


##################      EXTERNALS      ##################

@dataclass(frozen=True)
class ExternalEvent(CanonicalEvent):...


@dataclass(frozen=True)
class InternalEvent(CanonicalEvent):
    causation_id: str
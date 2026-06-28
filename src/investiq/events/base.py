from abc import ABC
from collections.abc import Mapping
from dataclasses import dataclass


@dataclass(frozen=True)
class CanonicalEvent(ABC):
    run_id: str
    event_id: str
    causation_id: str | None
    metadata: Mapping[str, object]
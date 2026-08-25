from dataclasses import dataclass
from typing import Protocol

from investiq.core.events import CanonicalEvent


@dataclass(frozen=True)
class HandlerResult:
    emitted_events: tuple[CanonicalEvent, ...] = ()

class Handler(Protocol):
    def handle(self, event: CanonicalEvent) -> HandlerResult:
        ...
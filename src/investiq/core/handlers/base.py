from dataclasses import dataclass

from investiq.core.events import CanonicalEvent


@dataclass(frozen=True)
class HandlerResult:
    emitted_events: tuple[CanonicalEvent, ...] = ()

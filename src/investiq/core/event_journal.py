from dataclasses import dataclass
from investiq.core.contracts.events import CanonicalEvent

@dataclass(frozen=True, slots=True)
class EventTransition:
    input_event: CanonicalEvent
    emitted_events: tuple[CanonicalEvent, ...]


class EventTransitionJournal:

    def __init__(self):
        self._journal: list[EventTransition] = []

    def append(self, transition: EventTransition) -> None:
        self._journal.append(transition)
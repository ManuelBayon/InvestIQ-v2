from collections.abc import Iterator

from investiq.core.events import CanonicalEvent


class EventJournal:
    """Ordered canonical facts in memory. Reading the journal has no side effects."""

    def __init__(self) -> None:
        self._events: list[CanonicalEvent] = []
        self._ids: set[tuple[str, str]] = set()

    def append(self, event: CanonicalEvent) -> None:
        key = (event.run_id, event.event_id)
        if key in self._ids:
            raise ValueError(f"Event already journaled: {key}")
        self._events.append(event)
        self._ids.add(key)

    def __iter__(self) -> Iterator[CanonicalEvent]:
        return iter(tuple(self._events))

    def __len__(self) -> int:
        return len(self._events)

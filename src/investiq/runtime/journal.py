from investiq.events.canonical_events import BaseEvent


class CanonicalJournal:

    def __init__(self):
        self._journal: list[BaseEvent] = []

    def append(self, event: BaseEvent) -> None:
        self._journal.append(event)
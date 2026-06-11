from investiq.events.events import CanonicalEvent


class CanonicalJournal:

    def __init__(self):
        self._journal: list[CanonicalEvent] = []

    def append(self, event: CanonicalEvent) -> None:
        self._journal.append(event)
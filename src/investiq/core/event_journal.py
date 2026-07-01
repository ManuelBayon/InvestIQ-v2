from investiq.core.contracts.events import CanonicalEvent


class CanonicalEventJournal:

    def __init__(self):
        self._journal: list[CanonicalEvent] = []

    def append(self, event: CanonicalEvent) -> None:
        self._journal.append(event)
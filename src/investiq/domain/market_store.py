from investiq.domain.models import Bar
from investiq.errors import EventOrderingViolation


class MarketStore:
    """
    2026-05-17: Naive stateful in memory market store.
    """
    def __init__(self):
        self._history: list[Bar] = []

    def ingest(self, bar: Bar) -> None:
        if self._history:
            if bar.timestamp_utc <= self._history[-1].timestamp_utc:
                raise EventOrderingViolation(
                    f"bar.timestamp_utc must be strictly greater than last processed"
                    f"bar.timestamp_utc={bar.timestamp_utc}, "
                    f"last_processed={self._history[-1].timestamp_utc}"
                )
        self._history.append(bar)

    def view(self) -> tuple[Bar, ...]:
        return tuple(self._history)
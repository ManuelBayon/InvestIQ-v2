from investiq.domain.models import Bar, RawTick
from investiq.errors import EventOrderingViolation


class MarketStore:
    """
    2026-06-02
        - using RawTick.
        - RawTicks are grouped by symbol.
        - Key Assumption : RawTicks arrive ordered by timestamp for a given symbol.
        - The current data structure (dict[str, list[RawTick]]) allows
        a future ordering policy without major refactor.

    2026-05-17
        Naive stateful in memory market store.
    """
    def __init__(self):
        self._history: dict[str, list[RawTick]] = {}

    def ingest(self, payload: dict[str, list[RawTick]]) -> None:
        for symbol in payload:
            if symbol not in self._history:
                self._history[symbol] = []
            self._history[symbol].extend(payload[symbol])

    def view(self, symbol: str) -> tuple[RawTick, ...]:
        if symbol not in self._history:
            raise KeyError(
                f"symbol={symbol} is not a valid key in MarketStore. "
                f"Available keys={self._history.keys()}"
            )
        return tuple(self._history[symbol])
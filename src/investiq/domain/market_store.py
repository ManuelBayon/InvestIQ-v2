from copy import deepcopy

from investiq.domain.models import RawTick

class MarketStore:
    """
    2026-06-02
        - using RawTick.
        - RawTicks are grouped by symbol.
        - Key Assumption : RawTicks arrive ordered by timestamp for a given symbol.
        - The current data structure (dict[str, list[RawTick]]) allows
        a future ordering policy without major refactor.
        - view() returns deep copy to validate the data model and causal flow
        do not treat this as a hardened ownership boundary.

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

    def view(self) -> dict[str, list[RawTick]]:
        return deepcopy(self._history)
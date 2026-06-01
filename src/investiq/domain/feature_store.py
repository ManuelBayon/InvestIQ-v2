from investiq.domain.models import Bar


class FeatureStore:
    """
    2026-05-17:
    - FeatureStore is currently a temporary SMA-2 placeholder.
    - No stable invariant beyond deterministic append behavior.
    - Do not over-test until feature contract is clarified.
    """

    def __init__(self):
        self._history: dict[str, list[float]] = {"sma_2": []}

    def update(
            self,
            market_view: tuple[Bar, ...]
    ) -> None:
        if len(market_view) < 2:
            return
        sma_2 = (market_view[-2].close + market_view[-1].close) / 2
        self._history["sma_2"].append(sma_2)

    def view(self) -> tuple[float, ...]:
        return tuple(self._history["sma_2"])
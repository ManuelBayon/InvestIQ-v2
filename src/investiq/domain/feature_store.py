from investiq.domain.models import RawTick


class FeatureStore:
    """
    2026-05-17:
    - FeatureStore is currently a temporary SMA-2 placeholder.
    - No stable invariant beyond deterministic append behavior.
    - Do not over-test until feature contract is clarified.
    """

    def __init__(self):
        self._history: dict[str, dict[str, list[float]]] = {}

    def update(
            self,
            market_view: dict[str, list[RawTick]]
    ) -> None:
        for symbol in market_view:
            if symbol not in self._history:
                self._history[symbol] = {}
            tick_data = market_view[symbol]
            if len(tick_data) >= 2:
                result = (tick_data[-1].price + tick_data[-2].price) / 2
                self._history[symbol].setdefault("sma_2", []).append(result)

    def view(
            self,
            symbol: str | None = None,
            feature: str | None = None,
    ) -> dict[str, dict[str, list[float]]] | dict[str, list[float]] | list[float]:
        if symbol is None:
            return self._history
        if feature is None:
            return self._history[symbol]
        else:
            if feature not in self._history[symbol]:
                raise KeyError(
                    f"feature={feature} is not present in, "
                    f"available features are: {self._history[symbol].keys()}"
                )
            return self._history[symbol][feature]
from investiq.domain.features.point import FeaturePoint


class FeatureStore:

    def __init__(self):
        self._history: list[FeaturePoint] = []


    def update(self, point: FeaturePoint) -> None:
        self._history.append(point)


    @property
    def symbols(self) -> set[str]:
        return set(p.symbol for p in self._history)


    def features_by_symbol(self, symbol: str) -> set[str]:
        if not symbol in self.symbols:
            return set()
        return set(p.feature_name for p in self._history if p.symbol == symbol)


    def has_data(self, symbol: str, feature: str) -> bool:
        return feature in self.features_by_symbol(symbol)


    def latest(self, symbol: str, name: str) -> FeaturePoint:
        if not self.has_data(symbol=symbol, feature=name):
            raise KeyError(f"No feature={name} registered for symbol={symbol}")

        return [p for p in self._history if p.symbol == symbol and p.feature_name == name][-1]
from investiq.domain.features.point import FeaturePoint


class FeatureStore:

    def __init__(self):
        self._history: list[FeaturePoint] = []

    def update(self, point: FeaturePoint) -> None:
        self._history.append(point)

    def latest(self, symbol) -> FeaturePoint:
        points = [p for p in self._history if p.symbol == symbol]
        return points[-1]
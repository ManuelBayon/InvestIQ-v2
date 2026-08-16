from collections.abc import Sequence
from statistics import mean

from investiq.errors import InsufficientHistoryError
from investiq.features.features import Feature, Source


class SimpleMovingAverage:

    def __init__(self, source: Source, window: int):
        self._source = source
        self._window = window
        self._history : list[float] = []


    def compute(self) -> bool:
        try:
            last_prices = self._source.load(self._window)
        except InsufficientHistoryError:
            return False
        self._history.append(mean(last_prices))
        return True


    def load(self, window: int) -> Sequence[float]:
        if window < 1:
            raise ValueError(f"window must be positive, got window={window}")
        series = self._history[-window:]
        if len(series) < window:
            raise InsufficientHistoryError
        return series

    def __repr__(self) -> str:
        return (
            f"\nSimpleMovingAverage("
            f"\nsource={self._source}"
            f"\nwindow={self._window}"
            f"\nhistory={self._history})\n"
        )
from collections.abc import Sequence
from statistics import mean

from investiq.errors import InsufficientHistoryError
from investiq.features.sources import Source


class SimpleMovingAverage:

    def __init__(
            self,
            source: Source,
            window: int,
    ):
        if window < 1:
            raise ValueError(f"window={window} must be a positive integer.")
        self._source = source
        self._window = window
        self._history : list[float] = []

    @property
    def source(self) -> Source:
        return self._source

    @property
    def name(self) -> str:
        return f"sma_{self._window}"

    def compute(self) -> bool:
        try:
            last_prices = self.source.load(self._window)
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

    def latest(self) -> float:
        return self.load(1)[0]
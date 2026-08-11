from typing import Protocol, runtime_checkable
from collections.abc import Sequence
from math import log
from statistics import stdev, mean

from investiq.errors import InsufficientHistoryError

from investiq.domain.market_store import InMemoryMarketStore


class Source(Protocol):
    def load(self, window: int) -> Sequence[float]:
        ...


class PriceSource:
    def __init__(
            self,
            source: InMemoryMarketStore,
            symbol: str
    ):
        self._source = source
        self._symbol = symbol

    def load(self, window: int) -> Sequence[float]:
        return self._source.price_window(self._symbol, window)

@runtime_checkable
class Feature(Protocol):
    def compute(self) -> bool:
        """
        True  : a new observation has been produced.
        False : No new observation.
        """
        ...

    def load(self, window: int) -> Sequence[float]:
        ...

    @property
    def successors(self) -> list["Feature"]:...


class Returns1:
    def __init__(
            self,
            source: Source,
    ):
        self._source = source
        self._history: list[float] = []
        self.successors: list[Feature] = []

    def compute(self) -> bool:
        try:
            series = self._source.load(window=2)
        except InsufficientHistoryError:
            return False

        result = log(series[-1] / series[-2])
        self._history.append(result)
        return True

    def load(self, window: int) -> Sequence[float]:
        if window < 1:
            raise ValueError(f"n must be positive, got n={window}")

        size = len(self._history)
        if size < window:
            raise InsufficientHistoryError(f"requested={window}, available={size}")

        return self._history[-window:]

    @property
    def successors(self) -> list["Feature"]:
        return self.successors


class Volatility:
    def __init__(
            self,
            source: Source,
            window: int
    ):
        self._source = source
        self._window = window
        self._history: list[float] = []
        self.successors: list[Feature] = []

    def compute(self) -> bool:
        try:
            series = self._source.load(self._window)
        except InsufficientHistoryError:
            return False

        result = stdev(series)
        self._history.append(result)
        return True

    def load(self, window: int) -> Sequence[float]:
        if window < 1:
            raise ValueError(f"n must be positive, got n={window}")

        size = len(self._history)
        if size < window:
            raise InsufficientHistoryError(f"requested={window}, available={size}")

        return self._history[-window:]

    @property
    def successors(self) -> list["Feature"]:
        return self.successors


class ZScore:

    def __init__(
            self,
            source: Source,
            window: int,
    ):
        self._source = source
        self._window = window
        self._history: list[float] = []
        self.successors: list[Feature] = []

    def compute(self) -> bool:
        try:
            series = self._source.load(self._window)
        except InsufficientHistoryError:
            return False

        value = series[-1]
        m = mean(series)
        sigma = stdev(series)

        if sigma == 0.0:
            raise ValueError("z_score is undefined when standard deviation is zero.")

        result = (value - m) / sigma
        self._history.append (result)
        return True

    def load(self, window: int) -> Sequence[float]:
        if window < 1:
            raise ValueError(f"n must be positive, got n={window}")

        size = len(self._history)
        if size < window:
            raise InsufficientHistoryError(f"requested={window}, available={size}")

        return self._history[-window:]

    @property
    def successors(self) -> list["Feature"]:
        return self.successors


class Mean:

    def __init__(
            self,
            source: Source,
            window: int
    ):
        self._source = source
        self._window = window
        self._history: list[float] = []
        self.successors: list[Feature] = []

    def compute(self) -> bool:
        try:
            series = self._source.load(self._window)
        except InsufficientHistoryError:
            return False

        result = mean(series)
        self._history.append(result)
        return True

    def load(self, window: int) -> Sequence[float]:
        if window < 1:
            raise ValueError(f"n must be positive, got n={window}")

        size = len(self._history)
        if size < window:
            raise InsufficientHistoryError(f"requested={window}, available={size}")

        return self._history[-window:]

    @property
    def successors(self) -> list["Feature"]:
        return self.successors
from collections import deque
from dataclasses import dataclass

@dataclass(frozen=True)
class SMAFeature:
    symbol: str
    window: int

class SMA:

    def __init__(self, window: int):
        self._window = window
        self._queue: deque[float] = deque(maxlen=self._window)
        self._sum: float = 0.0


    def compute(self, value: float) -> None:
        if len(self._queue) == self._window:
            old_price = self._queue.popleft()
            self._sum -= old_price
        self._sum += value
        self._queue.append(value)

    @property
    def value(self) -> float:
        return self._sum / self._window


    @property
    def is_ready(self) -> bool:
        return len(self._queue) == self._window
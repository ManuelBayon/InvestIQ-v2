from collections import deque
from decimal import Decimal

from investiq.events.market_data import TradeReceived


class SMA:

    def __init__(self, window: int):
        self._window = window
        self._queue: deque[Decimal] = deque(maxlen=window)
        self._sum: Decimal = Decimal(0)

    def compute(self, event: TradeReceived) -> None:
        price = event.price
        if len(self._queue) == self._window:
            old_price = self._queue.popleft()
            self._sum -= old_price
        self._sum += price
        self._queue.append(price)

    @property
    def is_ready(self) -> bool:
        return len(self._queue) == self._window

    @property
    def value(self) -> Decimal:
        return self._sum / self._window
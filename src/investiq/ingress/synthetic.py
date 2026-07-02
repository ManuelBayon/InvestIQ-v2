from datetime import datetime, timezone
from dataclasses import dataclass
from decimal import Decimal

from investiq.events.factory import CanonicalEventFactory
from investiq.core.event_queue import CanonicalEventQueue

@dataclass(frozen=True, slots=True)
class SyntheticTrade:
    symbol: str
    timestamp_utc: datetime
    price: Decimal
    size: Decimal


class SyntheticIngress:


    def __init__(
            self,
            event_queue: CanonicalEventQueue,
            event_factory: CanonicalEventFactory,
            symbol: str,
            n: int,
    ):
        self._symbol = symbol
        if not 1 <= n <= 86400:
            raise ValueError("n must be in [1, 86400]")
        self._n = n

        self._event_queue = event_queue
        self._event_factory = event_factory

    def start(self) -> None:
        for i in range(self._n):
            hour = i // 3600
            min_ = divmod(i, 3600)[1] // 60
            sec = divmod(i, 60)[1]

            _price = Decimal(90) + divmod(i, 21)[1]  # price in [90, 110]
            _size = Decimal(1) + divmod(i, 10)[1]  # size in [1,10]

            trade = self._event_factory.create_trade_received(
                symbol=self._symbol,
                timestamp_utc=datetime(2026, 1, 1, hour, min_, sec, tzinfo=timezone.utc),
                price=_price,
                size=_size,
            )
            self._event_queue.enqueue(trade)
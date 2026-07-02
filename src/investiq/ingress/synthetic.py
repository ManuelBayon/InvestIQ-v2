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


@dataclass(frozen=True, slots=True)
class SyntheticStream:
    symbol: str
    n: int
    min_price: Decimal
    max_price: Decimal
    min_size: Decimal
    max_size: Decimal

    def __post_init__(self):
        one = Decimal("1")

        if not 1 <= self.n <= 86_400:
            raise ValueError("n must be in [1, 86400]")

        if (
                not self.min_price.is_finite()
                or not self.max_price.is_finite()
                or self.min_price != self.min_price.to_integral_value()
                or self.max_price != self.max_price.to_integral_value()
                or not one <= self.min_price <= self.max_price
        ):
            raise ValueError(
                "1 <= min_price <= max_price and both must be finite integrals, "
                f"got min_price={self.min_price}, max_price={self.max_price}"
            )

        if (
                not self.min_size.is_finite()
                or not self.max_size.is_finite()
                or self.min_size != self.min_size.to_integral_value()
                or self.max_size != self.max_size.to_integral_value()
                or not one <= self.min_size <= self.max_size
        ):
            raise ValueError(
                "1 <= min_size <= max_size and both must be finite integrals, "
                f"got min_size={self.min_size}, max_size={self.max_size}"
            )


class SyntheticIngress:


    def __init__(
            self,
            event_queue: CanonicalEventQueue,
            event_factory: CanonicalEventFactory,
            streams: list[SyntheticStream]
    ):
        if not streams:
            raise ValueError("SyntheticIngress requires at least one stream")
        self._streams = tuple(streams)

        self._event_queue = event_queue
        self._event_factory = event_factory

    def start(self) -> None:

        for i in range(max(s.n for s in self._streams)):
            for stream in self._streams:
                if i >= stream.n:
                    continue

                min_price = stream.min_price
                max_price = stream.max_price
                price_delta = max_price - min_price

                min_size = stream.min_size
                max_size = stream.max_size
                size_delta = max_size - min_size

                hour = i // 3600
                min_ = divmod(i, 3600)[1] // 60
                sec = divmod(i, 60)[1]

                price = min_price + divmod(i, price_delta+1)[1]
                size = min_size + divmod(i, size_delta + 1)[1]

                trade = self._event_factory.create_trade_received(
                    symbol=stream.symbol,
                    timestamp_utc=datetime(2026, 1, 1, hour, min_, sec, tzinfo=timezone.utc),
                    price=price,
                    size=size,
                )
                self._event_queue.enqueue(trade)
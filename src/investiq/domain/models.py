from math import isfinite
from dataclasses import dataclass
from datetime import datetime, timezone

from investiq.errors import InvalidBar, InvaliRawTick


@dataclass(frozen=True)
class Bar:
    symbol: str
    timestamp_utc: datetime
    open: float
    high: float
    low: float
    close: float
    volume: int = 0

    def __post_init__(self):
        if self.timestamp_utc.tzinfo is not timezone.utc:
            raise InvalidBar("timestamp must be in UTC use datetime.timezone.utc")

        values = (self.open, self.high, self.low, self.close)
        if any(v < 0 or not isfinite(v) for v in values):
            raise InvalidBar(
                f"Values must be finite and non-negative: "
                f"open={self.open}, high={self.high}, low={self.low}, close={self.close}"
            )
        if self.high < max(self.open, self.low, self.close):
            raise InvalidBar(
               f"bar.high must be >= open, low, close: "
               f"open={self.open}, low={self.low}, close={self.close}"
            )
        if self.low > min(self.open, self.high, self.close):
            raise  InvalidBar(
               f"bar.low must be <= open, close: "
               f"open={self.open}, high={self.high}, close={self.close}"
            )
        if self.volume < 0:
            raise InvalidBar(
                f"volume must be non-negative: volume={self.volume}"
            )

@dataclass(frozen=True)
class RawTick:
    symbol: str
    timestamp_utc: datetime
    tick_type: int
    price: float
    size: float

    def __post_init__(self):
        if self.timestamp_utc.tzinfo is not timezone.utc:
            raise InvaliRawTick("timestamp must be in UTC use datetime.timezone.utc")
        if self.tick_type < 0:
            raise InvaliRawTick(f"tick_type must a non-negative integer, got tick_type={self.tick_type}")
        if self.price < 0 or not isfinite(self.price):
            raise InvaliRawTick(f"price must be a finite non-negative float: price={self.price}")
        if self.size < 0:
            raise InvaliRawTick(f"size must be non-negative: size={self.size}")

    def __repr__(self):
        return (
            f"RawTick("
            f"symbol={self.symbol}, "
            f"timestamp={self.timestamp_utc:%Y-%m-%dT%H:%M:%S.%f}Z, "
            f"type={self.tick_type}, "
            f"price={self.price}, "
            f"size={self.size})"
        )
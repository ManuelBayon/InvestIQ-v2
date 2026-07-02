from dataclasses import dataclass
from datetime import datetime, timezone
from decimal import Decimal
from math import isfinite

from investiq.errors import InvalidTrade
from investiq.events.events import MarketDataEvent


@dataclass(frozen=True)
class TradeReceived(MarketDataEvent):
    symbol: str
    timestamp_utc: datetime
    price: Decimal
    size: Decimal
    def __post_init__(self):
        if self.timestamp_utc.tzinfo is not timezone.utc:
            raise InvalidTrade("timestamp must be in UTC use datetime.timezone.utc")
        if self.price < 0 or not isfinite(self.price):
            raise InvalidTrade(f"price must be a finite non-negative float: price={self.price}")
        if self.size < 0:
            raise InvalidTrade(f"size must be non-negative: size={self.size}")
    def __repr__(self):
        return (
            f"\nTradeReceived(\n"
            f"\trun_id={self.run_id},\n"
            f"\tevent_id={self.event_id},\n"
            f"\tsymbol={self.symbol},\n"
            f"\ttimestamp={self.timestamp_utc:%Y-%m-%dT%H:%M:%S.%f}Z,\n"
            f"\tprice={self.price},\n"
            f"\tsize={self.size}\n"
            f")"
        )
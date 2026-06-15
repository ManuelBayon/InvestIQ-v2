from datetime import datetime, timezone

from investiq.domain.models import RawTick


def make_raw_tick(
        symbol = "symbol",
        timestamp_utc: datetime = datetime(2026,1,1, 12, tzinfo=timezone.utc),
        tick_type: int = 68,
        price: float = 100.0,
        size: float = 1.0,
) -> RawTick:
    return RawTick(
        symbol=symbol,
        timestamp_utc=timestamp_utc,
        tick_type=tick_type,
        price=price,
        size=size,
    )
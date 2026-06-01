from datetime import datetime

from sandbox.tick_aggregation import FakeTickData


def make_fake_tick(
        timestamp_utc: datetime,
        price: float,
        size: float,
        tick_type: int = 68,
) -> FakeTickData:
    return FakeTickData(
        time=timestamp_utc,
        tickType=tick_type,
        price=price,
        size=size
    )
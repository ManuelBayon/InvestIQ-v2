from datetime import datetime

from sandbox.tick_aggregation import FakeTickData, FakeTicker




def make_fake_ticker(
        symbol: str,
        ticks: list[FakeTickData]
) -> FakeTicker:
    return FakeTicker(
        symbol=symbol,
        ticks=ticks,
    )
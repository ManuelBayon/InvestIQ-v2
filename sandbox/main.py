from datetime import datetime

from sandbox.raw_tick_queue import FakeRawMarketDataQueue
from sandbox.tick_aggregation import FakeTickAggregator, FakeTicker
from tests.helpers.tickers import make_fake_ticker, make_fake_tick

def make_ticks_for_ticker_1() -> FakeTicker:
    ticker_1_tick_1 = make_fake_tick(
        timestamp_utc=datetime(2026, 4, 8, 12, 0, 0),
        price=50.0,
        size=1.0
    )
    ticker_1_tick_2 = make_fake_tick(
        timestamp_utc=datetime(2026, 4, 8, 12, 0, 30),
        price=50.0,
        size=2.0
    )
    ticker_1_tick_3 = make_fake_tick(
        timestamp_utc=datetime(2026, 4, 8, 12, 1, 1),
        price=50.0,
        size=1.0
    )
    ticker_1_tick_4 = make_fake_tick(
        timestamp_utc=datetime(2026, 4, 8, 12, 1, 12),
        price=40.0,
        size=2.0
    )
    ticker_1_tick_5 = make_fake_tick(
        timestamp_utc=datetime(2026, 4, 8, 12, 1, 50),
        price=60.0,
        size=3.0
    )
    ticker_1_tick_6 = make_fake_tick(
        timestamp_utc=datetime(2026, 4, 8, 12, 2, 5),
        price=56.0,
        size=4.0
    )
    t1 = make_fake_ticker(
        symbol="TICKER_1",
        ticks=[
            ticker_1_tick_1,
            ticker_1_tick_2,
            ticker_1_tick_3,
            ticker_1_tick_4,
            ticker_1_tick_5,
            ticker_1_tick_6
        ]
    )
    return t1

if __name__ == "__main__":

    aggregator = FakeTickAggregator()
    raw_data_queue = FakeRawMarketDataQueue()

    ticker_1_tick_1 = make_fake_tick(
        timestamp_utc=datetime(2026, 4, 8, 12, 0, 0),
        price=50.0,
        size=1.0
    )
    ticker_2_tick_1 = make_fake_tick(
        timestamp_utc=datetime(2026, 4, 8, 12, 0, 2),
        price=100.0,
        size=1.0
    )
    ticker_1 = make_fake_ticker(
        symbol="TICKER_1",
        ticks=[
            ticker_1_tick_1,
        ]
    )
    ticker_2 = make_fake_ticker(
        symbol="TICKER_2",
        ticks=[
            ticker_2_tick_1,
        ]
    )
    raw_data_queue.push(tickers=[ticker_1, ticker_2])

    ticker_1_tick_2 = make_fake_tick(
        timestamp_utc=datetime(2026, 4, 8, 12, 0, 30),
        price=51.0,
        size=2.0
    )
    ticker_2_tick_2 = make_fake_tick(
        timestamp_utc=datetime(2026, 4, 8, 12, 1, 2),
        price=101.0,
        size=2.0
    )
    ticker_1 = make_fake_ticker(
        symbol="TICKER_1",
        ticks=[ticker_1_tick_2]
    )
    ticker_2 = make_fake_ticker(
        symbol="TICKER_2",
        ticks=[ticker_2_tick_2]
    )
    raw_data_queue.push(tickers=[ticker_1, ticker_2])

    ticker_1_tick_2 = make_fake_tick(
        timestamp_utc=datetime(2026, 4, 8, 12, 1, 3),
        price=52.0,
        size=2.0
    )
    ticker_2_tick_2 = make_fake_tick(
        timestamp_utc=datetime(2026, 4, 8, 12, 1, 20),
        price=102.0,
        size=2.0
    )
    ticker_1 = make_fake_ticker(
        symbol="TICKER_1",
        ticks=[ticker_1_tick_2]
    )
    ticker_2 = make_fake_ticker(
        symbol="TICKER_2",
        ticks=[ticker_2_tick_2]
    )
    raw_data_queue.push(tickers=[ticker_1, ticker_2])



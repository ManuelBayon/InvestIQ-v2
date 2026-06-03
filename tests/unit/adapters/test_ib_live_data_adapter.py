from datetime import datetime, timezone

import pytest
from ib_insync import Ticker, Stock, TickData

from investiq.adapters.ib_live_market_data_feed import IBLiveMarketDataFeed
from investiq.events.canonical_event_factory import CanonicalEventFactory
from investiq.runtime.canonical_event_queue import CanonicalEventQueue
from investiq.events.canonical_events import TickDataAvailable


def test_on_pending_ticker_enqueues_tick_data_available_event() -> None:
    event_factory = CanonicalEventFactory(run_id="test_run_id")
    event_queue = CanonicalEventQueue()
    live_adapter = IBLiveMarketDataFeed(
        event_factory=event_factory,
        event_queue=event_queue,
    )
    tick_1 = TickData(time=datetime(2026, 1, 1, 12, tzinfo=timezone.utc), tickType=68, price=100.0, size=1.0)
    ticker = Ticker(
        contract=Stock('AMD', 'SMART', 'USD'),
        ticks=[tick_1]
    )
    live_adapter.on_pending_ticker(tickers={ticker})

    available_tick = event_queue.dequeue()
    with pytest.raises(IndexError):
        event_queue.dequeue()

    assert isinstance(available_tick, TickDataAvailable)

    tick = available_tick.payload['AMD'][0]
    assert tick.symbol == "AMD"
    assert tick.timestamp_utc == tick_1.time
    assert tick.tick_type == tick_1.tickType
    assert tick.price ==  tick_1.price
    assert tick.size == tick_1.size
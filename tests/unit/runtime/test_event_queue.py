from datetime import datetime, timezone

from investiq.domain.models import RawTick
from investiq.events.events import TickDataAvailable
from investiq.runtime.canonical_event_queue import CanonicalEventQueue


def test_enqueue_single_event():
    queue = CanonicalEventQueue()
    event = TickDataAvailable(
        run_id="run_id",
        event_id="event_id",
        causation_id=None,
        meta_data={},
        payload={
            "symbol":[
                RawTick(
                    symbol="symbol",
                    timestamp_utc=datetime(2026,1,1, tzinfo=timezone.utc),
                    tick_type=68, price=100.0, size=1.0
                )
            ]
        }
    )
    queue.enqueue(event)
    assert queue.dequeue_nowait() == event

def test_enqueue_two_events():
    queue = CanonicalEventQueue()
    event_1 = TickDataAvailable(
        run_id="run_id",
        event_id="event_1",
        causation_id=None,
        meta_data={},
        payload={
            "symbol":[
                RawTick(
                    symbol="symbol",
                    timestamp_utc=datetime(2026,1,1, tzinfo=timezone.utc),
                    tick_type=68, price=100.0, size=1.0
                )
            ]
        }
    )
    event_2 = TickDataAvailable(
        run_id="run_id",
        event_id="event_2",
        causation_id=None,
        meta_data={},
        payload={
            "symbol": [
                RawTick(
                    symbol="symbol",
                    timestamp_utc=datetime(2026, 1, 2, tzinfo=timezone.utc),
                    tick_type=68, price=100.0, size=1.0
                )
            ]
        }
    )
    queue.enqueue(event_1)
    queue.enqueue(event_2)
    assert queue.dequeue_nowait() == event_1
    assert queue.dequeue_nowait() == event_2

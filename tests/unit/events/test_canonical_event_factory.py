from datetime import datetime, timezone

from investiq.domain.models import RawTick
from investiq.events.factory import CanonicalEventFactory


def test_canonical_event_tick_data_available():
    factory = CanonicalEventFactory("test_run_id")
    payload = {
        "MNQ": [
            RawTick(
                symbol="MNQ",
                timestamp_utc=datetime(2026, 1, 1, 12, tzinfo=timezone.utc),
                tick_type=68,
                price=100.0,
                size=1.0
            )
        ]
    }
    event = factory.create_tick_data_available(payload=payload)
    assert event.run_id == factory._run_id
    assert event.causation_id is None
    assert event.event_id == "EVT_00001"
    assert event.meta_data == {}
    assert event.payload == payload
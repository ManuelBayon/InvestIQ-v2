from datetime import datetime, timezone

from investiq.domain.feature_store import FeatureStore
from investiq.domain.models import RawTick


def test_feature_store_ingest_two_valid_ticks():
    store = FeatureStore()
    market_view = {
        "TEST_SYMBOL": [
            RawTick(
                symbol="TEST_SYMBOL",
                timestamp_utc=datetime(2026,1,1, tzinfo=timezone.utc),
                tick_type=68,
                price=100.0,
                size=1.0,
            ),
            RawTick(
                symbol="TEST_SYMBOL",
                timestamp_utc=datetime(2026, 1, 2, tzinfo=timezone.utc),
                tick_type=68,
                price=102.0,
                size=2.0,
            ),
        ]
    }
    store.update(market_view)
    assert store.view() == {'TEST_SYMBOL': {'sma_2': [101.0]}}
    assert store.view("TEST_SYMBOL") == {'sma_2': [101.0]}
    assert store.view("TEST_SYMBOL", "sma_2") == [101.0]


from datetime import datetime, timezone

from investiq.domain.feature_store import FeatureStore
from investiq.domain.market_store import MarketStore
from investiq.domain.models import RawTick


def test_market_feature_store_one_symbol_valid_update():
    market_store = MarketStore()
    feature_store = FeatureStore()
    payload = {
        "TEST_SYMBOL": [
            RawTick(
                symbol="TEST_SYMBOL",
                timestamp_utc=datetime(2026,1,1, tzinfo=timezone.utc),
                tick_type=68,
                price=100.0,
                size=1.0,
            ),
        ]
    }
    market_store.ingest(payload=payload)
    print(f"\n{market_store.view()}")
    feature_store.update(market_store.view())
    print(f"\n{feature_store.view("TEST_SYMBOL")}")
    payload = {
        "TEST_SYMBOL": [
            RawTick(
                symbol="TEST_SYMBOL",
                timestamp_utc=datetime(2026, 1, 2, tzinfo=timezone.utc),
                tick_type=68,
                price=112.0,
                size=2.0,
            ),
        ]
    }
    market_store.ingest(payload=payload)
    print(f"\n{market_store.view()}")
    feature_store.update(market_store.view())
    print(f"\n{feature_store.view("TEST_SYMBOL")}")

def test_market_feature_store_two_symbols_valid_updates():
    market_store = MarketStore()
    feature_store = FeatureStore()
    payload = {
        "SYMBOL_1": [
            RawTick(
                symbol="SYMBOL_1",
                timestamp_utc=datetime(2026,1,1, tzinfo=timezone.utc),
                tick_type=68,
                price=100.0,
                size=1.0,
            ),
        ],
        "SYMBOL_2": [
            RawTick(
                symbol="SYMBOL_2",
                timestamp_utc=datetime(2026, 1, 1, tzinfo=timezone.utc),
                tick_type=68,
                price=100.0,
                size=1.0,
            ),
        ]
    }
    market_store.ingest(payload=payload)
    print(f"\n{market_store.view()}")
    feature_store.update(market_store.view())
    print(f"\n{feature_store.view()}")

    payload = {
        "SYMBOL_1": [
            RawTick(
                symbol="SYMBOL_1",
                timestamp_utc=datetime(2026, 1, 2, tzinfo=timezone.utc),
                tick_type=68,
                price=125.0,
                size=2.0,
            ),
        ],
    }
    market_store.ingest(payload=payload)
    print(f"\n{market_store.view()}")
    feature_store.update(market_store.view())
    print(f"\n{feature_store.view()}")
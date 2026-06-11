from datetime import datetime, timezone

from investiq.domain.decision_layer.no_op import NoOperationDecisionLayer
from investiq.domain.feature_store import FeatureStore
from investiq.domain.market_store import MarketStore
from investiq.domain.models import RawTick


def test_market_feature_store_one_symbol_valid_update():
    market_store = MarketStore()
    feature_store = FeatureStore()
    decision_layer = NoOperationDecisionLayer()
    payload = {
        "TEST_SYMBOL": [
            RawTick(
                symbol="TEST_SYMBOL",
                timestamp_utc=datetime(2026, 1, 1, tzinfo=timezone.utc),
                tick_type=68,
                price=100.0,
                size=1.0,
            ),
        ]
    }
    market_store.ingest(payload=payload)
    feature_store.update(market_store.view())


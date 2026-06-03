from datetime import datetime, timezone

from investiq.domain.decision_layer import NoOperationDecisionLayer, NoOperation
from investiq.domain.feature_store import FeatureStore
from investiq.domain.market_store import MarketStore
from investiq.domain.models import RawTick


def test_no_op_layer_returns_valid_no_operation():

    market_store = MarketStore()
    feature_store = FeatureStore()
    decision_layer = NoOperationDecisionLayer()

    tick_1 = RawTick(
        symbol="test_symbol",
        timestamp_utc=datetime(2026, 6, 1, 12, tzinfo=timezone.utc),
        tick_type=68,
        price=100.0,
        size=1.0,
    )
    payload = {"test_symbol": [tick_1]}
    market_store.ingest(payload=payload)
    feature_store.update(market_store.view())
    decision_layer.evaluate(market_view=market_store.view(), features_view=feature_store.view())

    tick_2 = RawTick(
        symbol="test_symbol",
        timestamp_utc=datetime(2026, 6, 1, 13, tzinfo=timezone.utc),
        tick_type=68,
        price=101.0,
        size=2.0,
    )
    payload = {"test_symbol": [tick_2]}
    market_store.ingest(payload=payload)
    feature_store.update(market_store.view())
    decision_layer.evaluate(market_view=market_store.view(), features_view=feature_store.view())

    tick_3 = RawTick(
        symbol="test_symbol",
        timestamp_utc=datetime(2026, 6, 1, 14, tzinfo=timezone.utc),
        tick_type=68,
        price=110.0,
        size=3.0,
    )
    payload = {"test_symbol": [tick_3]}
    market_store.ingest(payload=payload)
    feature_store.update(market_store.view())
    result_3 = decision_layer.evaluate(market_view=market_store.view(), features_view=feature_store.view())

    assert isinstance(result_3, NoOperation) 
    assert result_3.context.market_view == {"test_symbol":tick_3}
    assert result_3.context.feature_view == {"test_symbol":{"sma_2": 105.5}}

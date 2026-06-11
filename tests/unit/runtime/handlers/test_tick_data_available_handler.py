from datetime import datetime, timezone

from investiq.domain.decision_layer.no_op import NoOperationDecisionLayer, NoOperation
from investiq.domain.feature_store import FeatureStore
from investiq.domain.market_store import MarketStore
from investiq.domain.models import RawTick
from investiq.events.factory import CanonicalEventFactory
from investiq.runtime.handlers.tick_data_available_handler import TickDataAvailableHandler

def test_nominal_tick_data_available_handler_returns_no_operation():
    # initialization
    market_store = MarketStore()
    feature_store = FeatureStore()
    decision_layer = NoOperationDecisionLayer()
    event_factory = CanonicalEventFactory(run_id="test_run_id")
    handler = TickDataAvailableHandler(
        market_store=market_store,
        feature_store=feature_store,
        decision_layer=decision_layer,
        event_factory=event_factory
    )

    # first tick data available
    tick_1 = RawTick(
        symbol="test_symbol",
        timestamp_utc=datetime(2026, 6, 1, 12, tzinfo=timezone.utc),
        tick_type=68,
        price=100.0,
        size=1.0,
    )
    payload = {"test_symbol": [tick_1]}
    event = event_factory.create_tick_data_available(
        payload=payload
    )
    result = handler.handle(event)
    assert isinstance(result.payload, NoOperation)

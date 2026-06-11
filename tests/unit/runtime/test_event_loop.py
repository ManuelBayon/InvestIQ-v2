from datetime import datetime, timezone

from investiq.domain.decision_layer.no_op import NoOperationDecisionLayer
from investiq.domain.feature_store import FeatureStore
from investiq.domain.market_store import MarketStore
from investiq.domain.models import RawTick
from investiq.events.factory import CanonicalEventFactory
from investiq.runtime.canonical_event_queue import CanonicalEventQueue
from investiq.runtime.event_loop import EventLoop
from investiq.runtime.handlers.tick_data_available_handler import TickDataAvailableHandler
from investiq.runtime.journal import CanonicalJournal
from investiq.runtime.orchestrator import Orchestrator


def test_event_loop_run_until_empty():
    journal = CanonicalJournal()
    queue = CanonicalEventQueue()
    market_store = MarketStore()
    feature_store = FeatureStore()
    decision_layer = NoOperationDecisionLayer()
    event_factory = CanonicalEventFactory("test_run")
    tick_data_available_handler = TickDataAvailableHandler(
        market_store=market_store,
        feature_store=feature_store,
        decision_layer=decision_layer,
        event_factory=event_factory,
    )
    orchestrator = Orchestrator(
        tick_available_handler=tick_data_available_handler,
    )
    loop = EventLoop(
        journal=journal,
        event_queue=queue,
        orchestrator=orchestrator,
    )
    event_1 = event_factory.create_tick_data_available(
        payload={
            "symbol" : [
                RawTick(
                    symbol="symbol",
                    timestamp_utc=datetime(2026,1,1, tzinfo=timezone.utc),
                    tick_type=68,
                    price=100.0,
                    size=1.0,
                )
            ]
        }
    )
    queue.enqueue(event_1)
    event_2 = event_factory.create_tick_data_available(
        payload={
            "symbol": [
                RawTick(
                    symbol="symbol",
                    timestamp_utc=datetime(2026, 1, 1, tzinfo=timezone.utc),
                    tick_type=68,
                    price=100.0,
                    size=1.0,
                )
            ]
        }
    )
    queue.enqueue(event_2)
    loop.run_until_empty()
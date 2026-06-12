from investiq.adapters.ib_live_market_data_feed import IBLiveMarketDataFeed
from investiq.domain.decision_layer.no_op import NoOperationDecisionLayer
from investiq.domain.feature_store import FeatureStore
from investiq.domain.market_store import MarketStore
from investiq.events.factory import CanonicalEventFactory

from investiq.runtime.canonical_event_queue import CanonicalEventQueue
from investiq.runtime.event_loop import EventLoop
from investiq.runtime.handlers.tick_data_available_handler import TickDataAvailableHandler
from investiq.runtime.journal import CanonicalJournal
from investiq.runtime.live_runtime import LiveRuntime
from investiq.runtime.orchestrator import Orchestrator

def bootstrap_live_runtime() -> LiveRuntime:

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
    orchestrator = Orchestrator(tick_available_handler=tick_data_available_handler)
    event_loop = EventLoop(journal=journal, event_queue=queue, orchestrator=orchestrator)
    data_feed = IBLiveMarketDataFeed(event_factory=event_factory, event_queue=queue)
    return LiveRuntime(data_feed=data_feed, event_loop=event_loop)
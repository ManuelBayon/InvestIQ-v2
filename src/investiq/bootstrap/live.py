from investiq.adapters.ibkr_adapter import IBKRGatewayAdapter
from investiq.domain.decision_layer.always_buy_amd_market import AlwaysBuyAMDMarketDecisionLayer
from investiq.domain.feature_store import FeatureStore
from investiq.domain.market_store import MarketStore
from investiq.events.factory import CanonicalEventFactory

from investiq.runtime.canonical_event_queue import CanonicalEventQueue
from investiq.runtime.event_loop import EventLoop
from investiq.runtime.handlers.intent_generated_handler import IntentGeneratedHandler
from investiq.runtime.handlers.tick_data_available_handler import TickDataAvailableHandler
from investiq.runtime.journal import CanonicalJournal
from investiq.runtime.live_runtime import LiveRuntime
from investiq.runtime.orchestrator import Orchestrator

def bootstrap_live_runtime() -> LiveRuntime:

    journal = CanonicalJournal()
    queue = CanonicalEventQueue()
    event_factory = CanonicalEventFactory("test_run")
    gateway_adapter = IBKRGatewayAdapter(event_factory=event_factory, event_queue=queue)
    market_store = MarketStore()
    feature_store = FeatureStore()
    decision_layer = AlwaysBuyAMDMarketDecisionLayer()
    tick_data_available_handler = TickDataAvailableHandler(
        market_store=market_store,
        feature_store=feature_store,
        decision_layer=decision_layer,
        event_factory=event_factory,
    )
    intent_generated_handler = IntentGeneratedHandler(ibkr_adapter=gateway_adapter)

    orchestrator = Orchestrator(
        tick_available_handler=tick_data_available_handler,
        intent_generated_handler=intent_generated_handler,
    )
    event_loop = EventLoop(journal=journal, event_queue=queue, orchestrator=orchestrator)

    return LiveRuntime(data_feed=gateway_adapter, event_loop=event_loop)
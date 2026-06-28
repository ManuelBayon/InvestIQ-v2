from investiq.adapters.ibkr.ib_adapter import IBKRAdapter
from investiq.adapters.ibkr.ib_broker_adapter import IBKRBrokerAdapter
from investiq.adapters.ibkr.ib_client import IBKRClient
from investiq.adapters.ibkr.ib_market_data_adapter import IBKRMarketDataAdapter

from investiq.domain.decision.no_op import NoOperationDecisionLayer
from investiq.domain.features.store import FeatureStore
from investiq.domain.market_data.stores.trade_store import TradeStore

from investiq.events.factory import CanonicalEventFactory

from investiq.runtime.event_queue import CanonicalEventQueue
from investiq.runtime.event_loop import EventLoop
from investiq.runtime.handlers.intent_generated_handler import IntentGeneratedHandler
from investiq.runtime.handlers.trade_received_handler import TradeReceivedHandler
from investiq.runtime.event_journal import CanonicalJournal
from investiq.applications.live_runtime import LiveRuntime
from investiq.runtime.event_dispatcher import Orchestrator

def bootstrap_live_runtime() -> LiveRuntime:

    journal = CanonicalJournal()
    event_queue = CanonicalEventQueue()
    event_factory = CanonicalEventFactory("test_run")

    ibkr_client = IBKRClient()
    ibkr_market_data_adapter = IBKRMarketDataAdapter(
        ibkr_client=ibkr_client,
        event_factory=event_factory,
        event_queue=event_queue
    )
    ibkr_adapter = IBKRAdapter(
        ibkr_client=ibkr_client,
        ibkr_market_data_adapter=ibkr_market_data_adapter,
    )
    ibkr_broker_adapter = IBKRBrokerAdapter(
        ibkr_client=ibkr_client,
        event_queue=event_queue,
        event_factory=event_factory
    )

    trade_store = TradeStore()
    feature_store = FeatureStore()
    decision_layer = NoOperationDecisionLayer()#AlwaysBuyMNQMarket()

    tick_data_available_handler = TradeReceivedHandler(
        market_store=trade_store,
        feature_store=feature_store,
        decision_layer=decision_layer,
        event_factory=event_factory,
    )
    intent_generated_handler = IntentGeneratedHandler(
        ibkr_adapter=ibkr_adapter,
        broker_adapter=ibkr_broker_adapter,
        event_factory=event_factory
    )

    orchestrator = Orchestrator(
        tick_available_handler=tick_data_available_handler,
        intent_generated_handler=intent_generated_handler,
    )
    event_loop = EventLoop(
        journal=journal,
        event_queue=event_queue,
        orchestrator=orchestrator
    )
    return LiveRuntime(
        ibkr_adapter=ibkr_adapter,
        event_loop=event_loop
    )
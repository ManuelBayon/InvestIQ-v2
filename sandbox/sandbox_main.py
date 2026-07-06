
from investiq.core.event_journal import EventTransitionJournal
from investiq.core.event_loop import CanonicalEventLoop
from investiq.core.event_queue import CanonicalEventQueue
from investiq.domain.features.SMA import SMA
from investiq.domain.features.engine import FeatureEngine
from investiq.domain.features.feature_set import FeatureSet
from investiq.domain.trade_store import InMemoryTradeStore
from investiq.events.factory import CanonicalEventFactory
from investiq.handlers.trade_received_handler import TradeReceivedHandler

from investiq.ingress.synthetic import SyntheticIngress
from investiq.process.dispatcher import Dispatcher
from tests.fixtures.market.simple import SIMPLE_TRADES

if __name__ == "__main__":

    run_id = "TEST_RUN"

    trade_store = InMemoryTradeStore()
    features = [
        FeatureSet(symbol="TEST_SYMBOL", features={"sma_2": SMA(2), "sma_3": SMA(3)})
    ]
    feature_engine = FeatureEngine(feature_sets=features)

    trade_received_handler = TradeReceivedHandler(
        trade_store=trade_store,
        feature_engine=feature_engine
    )

    dispatcher = Dispatcher(
        trade_received_handler=trade_received_handler
    )

    event_queue = CanonicalEventQueue()
    event_factory = CanonicalEventFactory(run_id=run_id)

    journal = EventTransitionJournal()

    ingress = SyntheticIngress(
        event_queue=event_queue,
        event_factory=event_factory,
        scenario=SIMPLE_TRADES
    )

    event_loop = CanonicalEventLoop(
        event_queue=event_queue,
        dispatcher=dispatcher,
        journal=journal
    )

    ingress.start()
    event_loop.run_until_empty()

    print()
    print(f"sma_2: {feature_engine.value("TEST_SYMBOL", "sma_2")}")
    print(f"sma_3: {feature_engine.value("TEST_SYMBOL", "sma_3")}")

from investiq.core.event_journal import EventTransitionJournal
from investiq.core.event_loop import CanonicalEventLoop
from investiq.core.event_queue import CanonicalEventQueue

from investiq.features.SMA import SMA
from investiq.features.feature_engine import FeatureEngine, FeatureSet
from investiq.domain.market_store import InMemoryMarketStore

from investiq.events.factory import CanonicalEventFactory

from investiq.handlers.trade_received_handler import TradeReceivedHandler

from investiq.ingress.synthetic import SyntheticIngress
from investiq.process.dispatcher import Dispatcher
from tests.fixtures.market.simple import SIMPLE_TRADES

if __name__ == "__main__":

    run_id = "TEST_RUN"
    symbol = "TEST_SYMBOL"

    trade_store = InMemoryTradeStore()
    feature_sets = [
        FeatureSet(symbol=symbol, features={"sma_2": SMA(2), "sma_3": SMA(3)})
    ]
    feature_engine = FeatureEngine(feature_sets=feature_sets)

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

    print(f"{feature_engine.features(symbol)}")

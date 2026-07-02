from investiq.ingress.synthetic import SyntheticIngress
from investiq.runtime.sequential import SequentialRuntime
from investiq.domain.market_data.stores.in_memory_trade_store import MarketStore, InMemoryTradeStore
from investiq.events.factory import CanonicalEventFactory

from investiq.process.dispatcher import Dispatcher
from investiq.core.event_journal import EventTransitionJournal
from investiq.core.event_loop import CanonicalEventLoop
from investiq.core.event_queue import CanonicalEventQueue
from investiq.handlers.trade_received_handler import TradeReceivedHandler


def bootstrap_synthetical_runtime(run_id: str) -> SequentialRuntime:
    event_queue = CanonicalEventQueue()
    event_factory = CanonicalEventFactory(run_id=run_id)
    ingress = SyntheticIngress(
        symbol="TEST_SYMBOL",
        event_factory=event_factory,
        event_queue=event_queue,
        n=100,
    )
    event_loop = CanonicalEventLoop(
        event_queue=event_queue,
        journal=EventTransitionJournal(),
        dispatcher=Dispatcher(
            trade_received_handler=TradeReceivedHandler(
                trade_store=InMemoryTradeStore(),
                event_factory=event_factory
            )
        )
    )
    return SequentialRuntime(
        run_id=run_id,
        ingress=ingress,
        event_loop=event_loop,
    )
from decimal import Decimal

from investiq.ingress.synthetic import SyntheticIngress, SyntheticStream
from investiq.runtime.sequential import SequentialRuntime
from investiq.domain.market_data.stores.in_memory.trade_store import InMemoryTradeStore
from investiq.events.factory import CanonicalEventFactory

from investiq.process.dispatcher import Dispatcher
from investiq.core.event_journal import EventTransitionJournal
from investiq.core.event_loop import CanonicalEventLoop
from investiq.core.event_queue import CanonicalEventQueue
from investiq.handlers.market_data_handler import TradeReceivedHandler


def bootstrap_synthetical_runtime(run_id: str) -> SequentialRuntime:
    event_queue = CanonicalEventQueue()
    event_factory = CanonicalEventFactory(run_id=run_id)
    stream_1 = SyntheticStream(
        symbol="TEST_SYMBOL_1",
        n=2,
        min_price=Decimal(100),
        max_price=Decimal(110),
        min_size=Decimal(1),
        max_size=Decimal(5),
    )
    ingress = SyntheticIngress(
        event_factory=event_factory,
        event_queue=event_queue,
        streams=[stream_1]
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
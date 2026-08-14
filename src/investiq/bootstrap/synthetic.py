from investiq.ingress.synthetic import SyntheticIngress
from investiq.runtime.sequential import SequentialRuntime
from investiq.domain.market_store import InMemoryMarketStore
from investiq.events.factory import CanonicalEventFactory

from investiq.process.dispatcher import Dispatcher
from investiq.core.event_journal import EventTransitionJournal
from investiq.core.event_loop import CanonicalEventLoop
from investiq.core.event_queue import CanonicalEventQueue
from investiq.handlers.trade_received_handler import TradeReceivedHandler
from tests.fixtures.market.simple import MONO_SYMBOL_SIMPLE_TRADES


def bootstrap_synthetical_runtime(run_id: str, num_trades: int) -> SequentialRuntime:

    event_queue = CanonicalEventQueue()
    event_factory = CanonicalEventFactory(run_id=run_id)

    ingress = SyntheticIngress(
        event_queue=event_queue,
        event_factory=event_factory,
        scenario=[t for t in MONO_SYMBOL_SIMPLE_TRADES[:num_trades]]
    )

    event_loop = CanonicalEventLoop(
        event_queue=event_queue,
        journal=EventTransitionJournal(),
        dispatcher=Dispatcher(
            trade_received_handler=TradeReceivedHandler(
                market_store=InMemoryMarketStore(("SYMBOL_1",)),
            )
        )
    )
    return SequentialRuntime(
        run_id=run_id,
        ingress=ingress,
        event_loop=event_loop,
    )
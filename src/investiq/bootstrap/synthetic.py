from investiq.runtime.sequential import SequentialRuntime
from investiq.domain.market_data.stores.trade_store import TradeStore
from investiq.events.factory import CanonicalEventFactory
from investiq.ingress.synthetic import SyntheticIngress
from investiq.process.event_dispatcher import Orchestrator
from investiq.process.event_journal import CanonicalEventJournal
from investiq.process.event_loop import CanonicalEventLoop
from investiq.process.event_queue import CanonicalEventQueue
from investiq.process.handlers.trade_received_handler import TradeReceivedHandler


def bootstrap_synthetical_runtime(
        run_id: str,
) -> SequentialRuntime:
    event_queue = CanonicalEventQueue()
    event_factory = CanonicalEventFactory(run_id=run_id)
    ingress = SyntheticIngress(
        event_factory=event_factory,
        event_queue=event_queue,
        n=10,
        delay_seconds=None,
    )
    event_loop = CanonicalEventLoop(
        event_queue=event_queue,
        journal=CanonicalEventJournal(),
        orchestrator=Orchestrator(
            trade_received_handler=TradeReceivedHandler(
                trade_store=TradeStore(),
                event_factory=event_factory
            )
        )
    )
    return SequentialRuntime(
        run_id=run_id,
        ingress=ingress,
        event_loop=event_loop,
    )
from investiq.applications.synthetic_runtime import SyntheticRuntime

from investiq.domain.market_data.stores.trade_store import TradeStore
from investiq.events.factory import CanonicalEventFactory
from investiq.ingress.synthetic_ingress import SyntheticIngress

from investiq.runtime.event_queue import CanonicalEventQueue
from investiq.runtime.event_loop import CanonicalEventLoop
from investiq.runtime.handlers.trade_received_handler import TradeReceivedHandler
from investiq.runtime.event_journal import CanonicalEventJournal
from investiq.runtime.event_dispatcher import Orchestrator

def bootstrap_synthetic_runtime() -> SyntheticRuntime:

    event_queue = CanonicalEventQueue()
    event_factory = CanonicalEventFactory("SYNTHETIC_RUN")
    journal = CanonicalEventJournal()

    trade_store = TradeStore()

    trade_received_handler = TradeReceivedHandler(
        trade_store=trade_store,
        event_factory=event_factory
    )

    orchestrator = Orchestrator(
        trade_received_handler=trade_received_handler,
    )
    event_loop = CanonicalEventLoop(
        journal=journal,
        event_queue=event_queue,
        orchestrator=orchestrator
    )

    ingress = SyntheticIngress(
        event_queue=event_queue,
        event_factory=event_factory
    )

    return SyntheticRuntime(
        event_loop=event_loop,
        ingress=ingress
    )
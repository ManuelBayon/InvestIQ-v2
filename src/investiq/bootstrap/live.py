from investiq.adapters.ibkr.ib_client import IBKRClient
from investiq.ingress.ib_live import IBKRLiveIngress
from investiq.runtime.live import LiveRuntime
from investiq.domain.market_data.stores.in_memory_trade_store import MarketStore, InMemoryTradeStore
from investiq.events.factory import CanonicalEventFactory
from investiq.process.dispatcher import Dispatcher
from investiq.core.event_journal import EventTransitionJournal
from investiq.core.event_loop import CanonicalEventLoop
from investiq.core.event_queue import CanonicalEventQueue
from investiq.handlers.trade_received_handler import TradeReceivedHandler


def bootstrap_live_runtime(
        run_id: str,
) -> LiveRuntime:
    ib_client = IBKRClient()
    event_factory = CanonicalEventFactory(run_id=run_id)
    event_queue = CanonicalEventQueue()
    ingress = IBKRLiveIngress(
        event_factory=event_factory,
        event_queue=event_queue,
        ibkr_client=ib_client,
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
    return LiveRuntime(
        run_id=run_id,
        ingress=ingress,
        event_loop=event_loop,
    )
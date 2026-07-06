from datetime import datetime, timezone
from decimal import Decimal

from investiq.ingress.synthetic import SyntheticIngress, TradeFixture
from investiq.runtime.sequential import SequentialRuntime
from investiq.domain.trade_store import InMemoryTradeStore
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
        event_queue=event_queue,
        event_factory=event_factory,
        scenario=[
          TradeFixture(
              symbol="TEST_SYMBOL",
              timestamp_utc=datetime(2026,1,1,12, tzinfo=timezone.utc),
              price=Decimal(100),
              size=Decimal(1)
          )
        ]
    )

    event_loop = CanonicalEventLoop(
        event_queue=event_queue,
        transition_journal=EventTransitionJournal(),
        dispatcher=Dispatcher(
            trade_received_handler=TradeReceivedHandler(
                trade_store=InMemoryTradeStore(),
            )
        )
    )
    return SequentialRuntime(
        run_id=run_id,
        ingress=ingress,
        event_loop=event_loop,
    )
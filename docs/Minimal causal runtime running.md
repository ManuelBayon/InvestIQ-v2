![[Pasted image 20260603145524.png]]

```python
from threading import Thread

from investiq.adapters.ib_live_market_data_feed import IBLiveMarketDataFeed
from investiq.domain.decision_layer import NoOperationDecisionLayer
from investiq.domain.feature_store import FeatureStore
from investiq.domain.market_store import MarketStore
from investiq.events.factory import CanonicalEventFactory
from investiq.runtime.canonical_event_queue import CanonicalEventQueue
from investiq.runtime.event_loop import EventLoop
from investiq.runtime.handlers.tick_data_available_handler import TickDataAvailableHandler
from investiq.runtime.journal import CanonicalJournal
from investiq.runtime.orchestrator import Orchestrator

if __name__ == "__main__":
    journal = CanonicalJournal()
    queue = CanonicalEventQueue()
    market_store = MarketStore()
    feature_store = FeatureStore()
    decision_layer = NoOperationDecisionLayer()
    event_factory = CanonicalEventFactory("test_run")
    tick_data_available_handler = TickDataAvailableHandler(
        market_store=market_store,
        feature_store=feature_store,
        decision_layer=decision_layer,
        event_factory=event_factory,
    )
    orchestrator = Orchestrator(
        tick_available_handler=tick_data_available_handler,
    )
    loop = EventLoop(
        journal=journal,
        event_queue=queue,
        orchestrator=orchestrator,
    )
    data_feed = IBLiveMarketDataFeed(
        event_factory=event_factory,
        event_queue=queue,
    )
    data_feed.connect()
    data_feed.subscribe_to_cont_fut(symbol="MNQ", local_symbol="MNQM6")

    runtime_thread = Thread(target=loop.run, daemon=True)
    runtime_thread.start()
    data_feed.run()
```



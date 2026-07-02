from investiq.bootstrap.live import bootstrap_live_runtime
from investiq.bootstrap.synthetic import bootstrap_synthetical_runtime
from investiq.core.event_queue import CanonicalEventQueue
from investiq.domain.market_data.readers.in_memory_market_data_reader import InMemoryMarketDataReader
from investiq.domain.market_data.stores.in_memory_trade_store import InMemoryTradeStore
from investiq.events.factory import CanonicalEventFactory
from investiq.events.market_data import TradeReceived
from investiq.ingress.synthetic import SyntheticIngress

if __name__ == "__main__":

    synthetical_runtime = bootstrap_synthetical_runtime("TEST_RUN")
    live_runtime = bootstrap_live_runtime("TEST_RUN")

    #synthetical_runtime.run()
    #live_runtime.run()

    #################################################################

    event_queue = CanonicalEventQueue()
    event_factory = CanonicalEventFactory(run_id="TEST_RUN_ID")

    store = InMemoryTradeStore()
    reader = InMemoryMarketDataReader(store=store)

    _symbol = "TEST_SYMBOL"
    _n = 10

    ingress = SyntheticIngress(
        symbol=_symbol,
        event_queue=event_queue,
        event_factory=event_factory,
        n=_n,
    )
    ingress.start()

    while not event_queue.is_empty:
        event = event_queue.dequeue_nowait()
        if isinstance(event, TradeReceived):
            store.append(event)

    trades = reader.window(_symbol, _n)
    for t in trades:
        print(t)
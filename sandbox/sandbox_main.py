from decimal import Decimal

from investiq.bootstrap.live import bootstrap_live_runtime
from investiq.bootstrap.synthetic import bootstrap_synthetical_runtime
from investiq.core.event_queue import CanonicalEventQueue
from investiq.domain.market_data.readers.in_memory_market_data_reader import InMemoryMarketDataReader
from investiq.domain.market_data.stores.in_memory_trade_store import InMemoryTradeStore
from investiq.events.factory import CanonicalEventFactory
from investiq.events.market_data import TradeReceived
from investiq.ingress.synthetic import SyntheticIngress, SyntheticStream

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

    s1 = SyntheticStream(
        symbol="TEST_SYMBOL_1",
        n=20,
        min_price=Decimal(100),
        max_price=Decimal(110),
        min_size=Decimal(1),
        max_size=Decimal(5),
    )
    s2 = SyntheticStream(
        symbol="TEST_SYMBOL_2",
        n=25,
        min_price=Decimal(200),
        max_price=Decimal(220),
        min_size=Decimal(1),
        max_size=Decimal(10),
    )
    ingress = SyntheticIngress(
        event_queue=event_queue,
        event_factory=event_factory,
        streams=[s1, s2],
    )

    ingress.start()

    while not event_queue.is_empty:
        event = event_queue.dequeue_nowait()
        assert isinstance(event, TradeReceived)
        store.append(event)

    trades_1 = reader.window(s1.symbol, s1.n)
    trades_2 = reader.window(s2.symbol, s2.n)

    trades = list(trades_1 + trades_2)
    trades.sort(key=lambda trade: trade.event_id)

    for t in trades:
        print(t)
from decimal import Decimal

from investiq.core.event_journal import EventTransitionJournal
from investiq.core.event_loop import CanonicalEventLoop
from investiq.core.event_queue import CanonicalEventQueue
from investiq.domain.market_data.readers.in_memory_market_data_reader import InMemoryMarketDataReader
from investiq.domain.market_data.stores.in_memory.trade_store import InMemoryTradeStore
from investiq.events.factory import CanonicalEventFactory

from investiq.handlers.market_data_handler import MarketDataHandler
from investiq.ingress.synthetic import SyntheticIngress, SyntheticStream
from investiq.process.dispatcher import Dispatcher

if __name__ == "__main__":

    run_id = "TEST_RUN"

    symbol_1 = "TEST_SYMBOL_1"
    num_trades_1 = 1

    symbol_2 = "TEST_SYMBOL_2"
    num_trades_2 = 1

    trade_store = InMemoryTradeStore()
    reader = InMemoryMarketDataReader(store=trade_store)

    market_data_handler = MarketDataHandler(trade_store=trade_store)

    dispatcher = Dispatcher(market_data_handler=market_data_handler)

    event_queue = CanonicalEventQueue()
    journal = EventTransitionJournal()
    event_factory = CanonicalEventFactory(run_id=run_id)

    event_loop = CanonicalEventLoop(
        event_queue=event_queue,
        dispatcher=dispatcher,
        transition_journal=journal
    )

    ingress = SyntheticIngress(
        event_queue=event_queue,
        event_factory=event_factory,
        streams=[
            SyntheticStream(
                symbol=symbol_1,
                n=num_trades_1,
                min_price=Decimal(100),
                max_price=Decimal(110),
                min_size=Decimal(1),
                max_size=Decimal(5),
            ),
            SyntheticStream(
                symbol=symbol_2,
                n=num_trades_2,
                min_price=Decimal(100),
                max_price=Decimal(110),
                min_size=Decimal(1),
                max_size=Decimal(5),
            )
        ],
    )

    ingress.start()
    event_loop.run_until_empty()


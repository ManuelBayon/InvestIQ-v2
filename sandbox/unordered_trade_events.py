from datetime import datetime, timezone
from decimal import Decimal

from investiq.domain.market_data.readers.in_memory_market_data_reader import InMemoryMarketDataReader
from investiq.domain.market_data.stores.in_memory.trade_store import InMemoryTradeStore
from investiq.events.factory import CanonicalEventFactory

if __name__ == "__main__":
    run_id = "TEST_RUN"

    symbol = "TEST_SYMBOL_1"
    num_trades_1 = 1

    trade_store = InMemoryTradeStore()
    reader = InMemoryMarketDataReader(store=trade_store)

    event_factory=CanonicalEventFactory(run_id=run_id)
    regular_trade = event_factory.create_trade_received(
        symbol=symbol,
        timestamp_utc=datetime(
            2026,1,1,12,00,00,
            tzinfo=timezone.utc
        ),
        price=Decimal(100.0),
        size=Decimal(1.0),
    )
    unordered_trade = event_factory.create_trade_received(
        symbol=symbol,
        timestamp_utc=datetime(
            2026,1,1,11,59,59,
            tzinfo=timezone.utc
        ),
        price=Decimal(100.0),
        size=Decimal(1.0),
    )

    trade_store.ingest(regular_trade)
    print(trade_store.window(symbol=symbol, n=1))
    trade_store.ingest(unordered_trade)
    print(trade_store.window(symbol=symbol, n=2))





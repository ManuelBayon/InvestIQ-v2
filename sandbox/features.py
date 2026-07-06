from dataclasses import dataclass
from datetime import datetime, timezone
from decimal import Decimal

from investiq.domain.features.SMA import SMA
from investiq.domain.features.engine import FeatureEngine
from investiq.domain.features.feature_set import FeatureSet
from investiq.domain.trade_store import InMemoryTradeStore
from investiq.events.market_data import TradeReceived
from investiq.handlers.trade_received_handler import TradeReceivedHandler





if __name__ == "__main__":

    run_id = "TEST_RUN"
    symbol_1 = "TEST_SYMBOL_1"

    event_1 = TradeReceived(
        run_id=run_id,
        event_id="EVT_00001",
        symbol=symbol_1,
        timestamp_utc=datetime(year=2026, month=1, day=1, hour=12, minute=0, tzinfo=timezone.utc),
        price=Decimal(100),
        size=Decimal(1)
    )
    event_2 = TradeReceived(
        run_id=run_id,
        event_id="EVT_00002",
        symbol=symbol_1,
        timestamp_utc=datetime(year=2026, month=1, day=1, hour=12, minute=1, tzinfo=timezone.utc),
        price=Decimal(101),
        size=Decimal(1)
    )
    event_3 = TradeReceived(
        run_id=run_id,
        event_id="EVT_00003",
        symbol=symbol_1,
        timestamp_utc=datetime(year=2026, month=1, day=1, hour=12, minute=2, tzinfo=timezone.utc),
        price=Decimal(103),
        size=Decimal(1)
    )
    event_4 = TradeReceived(
        run_id=run_id,
        event_id="EVT_00004",
        symbol=symbol_1,
        timestamp_utc=datetime(year=2026, month=1, day=1, hour=12, minute=3, tzinfo=timezone.utc),
        price=Decimal(90),
        size=Decimal(1)
    )
    events = [event_1, event_2, event_3, event_4]

    store = InMemoryTradeStore()
    feature_engine = FeatureEngine(
        feature_set = [
            FeatureSet(
                symbol=symbol_1,
                features={"sma_2": SMA(2), "sma_3": SMA(3)}
            )
        ]
    )
    handler = TradeReceivedHandler(trade_store=store, feature_engine=feature_engine)

    for e in events:
        handler.handle(event=e)
        if feature_engine.is_ready(symbol_1, "sma_2"):
            print(feature_engine.value(symbol_1, "sma_2"))
        else:
            print("warming up...")
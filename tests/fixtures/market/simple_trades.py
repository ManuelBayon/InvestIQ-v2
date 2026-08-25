from datetime import datetime, timezone

from investiq.ingress.synthetic import TradeFixture

symbol_1 = "SYMBOL_1"
symbol_2 = "SYMBOL_2"

MONO_SYMBOL_SIMPLE_TRADES = [
    TradeFixture(symbol=symbol_1, timestamp_utc=datetime(2026, 1, 1,12, 0, 0, tzinfo=timezone.utc), price=100.0, size=1.0),
    TradeFixture(symbol=symbol_1, timestamp_utc=datetime(2026, 1, 1,12, 1, 0, tzinfo=timezone.utc), price=110.0, size=2.0),
    TradeFixture(symbol=symbol_1, timestamp_utc=datetime(2026, 1, 1,12, 2, 0, tzinfo=timezone.utc), price=103.0, size=1.0),
    TradeFixture(symbol=symbol_1, timestamp_utc=datetime(2026, 1, 1,12, 3, 0, tzinfo=timezone.utc), price=107.5, size=3.0),
    TradeFixture(symbol=symbol_1, timestamp_utc=datetime(2026, 1, 1,12, 4, 0, tzinfo=timezone.utc), price=101.0, size=1.0),
    TradeFixture(symbol=symbol_1, timestamp_utc=datetime(2026, 1, 1,12, 5, 0, tzinfo=timezone.utc), price=99.5, size=1.0),
    TradeFixture(symbol=symbol_1, timestamp_utc=datetime(2026, 1, 1,12, 6, 0, tzinfo=timezone.utc), price=91.0, size=1.0),
]
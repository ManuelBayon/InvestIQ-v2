from datetime import datetime, timezone
from decimal import Decimal

from investiq.ingress.synthetic import TradeFixture

symbol_1 = "SYMBOL_1"
symbol_2 = "SYMBOL_2"

MONO_SYMBOL_SIMPLE_TRADES = [
    TradeFixture(symbol=symbol_1, timestamp_utc=datetime(2026, 1, 1,12, 0, 0, tzinfo=timezone.utc), price=Decimal(100.0), size=Decimal(1.0)),
    TradeFixture(symbol=symbol_1, timestamp_utc=datetime(2026, 1, 1,12, 1, 0, tzinfo=timezone.utc), price=Decimal(110.0), size=Decimal(2.0)),
    TradeFixture(symbol=symbol_1, timestamp_utc=datetime(2026, 1, 1,12, 2, 0, tzinfo=timezone.utc), price=Decimal(103.0), size=Decimal(1.0)),
    TradeFixture(symbol=symbol_1, timestamp_utc=datetime(2026, 1, 1,12, 3, 0, tzinfo=timezone.utc), price=Decimal(107.5), size=Decimal(3.0)),
    TradeFixture(symbol=symbol_1, timestamp_utc=datetime(2026, 1, 1,12, 3, 0, tzinfo=timezone.utc), price=Decimal(101.0), size=Decimal(1.0)),
    TradeFixture(symbol=symbol_1, timestamp_utc=datetime(2026, 1, 1,12, 3, 0, tzinfo=timezone.utc), price=Decimal(99.5), size=Decimal(1.0)),
    TradeFixture(symbol=symbol_1, timestamp_utc=datetime(2026, 1, 1,12, 3, 0, tzinfo=timezone.utc), price=Decimal(91.0), size=Decimal(1.0)),
]

MULTI_SYMBOLS_SIMPLE_TRADES = [
    TradeFixture(symbol=symbol_1, timestamp_utc=datetime(2026, 1, 1,12, 0, 0, tzinfo=timezone.utc), price=Decimal(100.0), size=Decimal(1.0)),
    TradeFixture(symbol=symbol_2, timestamp_utc=datetime(2026, 1, 1,12, 1, 0, tzinfo=timezone.utc), price=Decimal(110.0), size=Decimal(2.0)),
    TradeFixture(symbol=symbol_1, timestamp_utc=datetime(2026, 1, 1,12, 2, 0, tzinfo=timezone.utc), price=Decimal(103.0), size=Decimal(1.0)),
    TradeFixture(symbol=symbol_2, timestamp_utc=datetime(2026, 1, 1,12, 3, 0, tzinfo=timezone.utc), price=Decimal(107.5), size=Decimal(3.0)),
    TradeFixture(symbol=symbol_1, timestamp_utc=datetime(2026, 1, 1,12, 3, 0, tzinfo=timezone.utc), price=Decimal(101.0), size=Decimal(1.0)),
    TradeFixture(symbol=symbol_2, timestamp_utc=datetime(2026, 1, 1,12, 3, 0, tzinfo=timezone.utc), price=Decimal(99.5), size=Decimal(1.0)),
    TradeFixture(symbol=symbol_1, timestamp_utc=datetime(2026, 1, 1,12, 3, 0, tzinfo=timezone.utc), price=Decimal(91.0), size=Decimal(1.0)),
    TradeFixture(symbol=symbol_2, timestamp_utc=datetime(2026, 1, 1,12, 0, 0, tzinfo=timezone.utc), price=Decimal(100.0), size=Decimal(1.0)),
    TradeFixture(symbol=symbol_1, timestamp_utc=datetime(2026, 1, 1,12, 1, 0, tzinfo=timezone.utc), price=Decimal(110.0), size=Decimal(2.0)),
    TradeFixture(symbol=symbol_2, timestamp_utc=datetime(2026, 1, 1,12, 2, 0, tzinfo=timezone.utc), price=Decimal(103.0), size=Decimal(1.0)),
    TradeFixture(symbol=symbol_1, timestamp_utc=datetime(2026, 1, 1,12, 3, 0, tzinfo=timezone.utc), price=Decimal(107.5), size=Decimal(3.0)),
    TradeFixture(symbol=symbol_2, timestamp_utc=datetime(2026, 1, 1,12, 3, 0, tzinfo=timezone.utc), price=Decimal(101.0), size=Decimal(1.0)),
    TradeFixture(symbol=symbol_1, timestamp_utc=datetime(2026, 1, 1,12, 3, 0, tzinfo=timezone.utc), price=Decimal(99.5), size=Decimal(1.0)),
    TradeFixture(symbol=symbol_2, timestamp_utc=datetime(2026, 1, 1,12, 3, 0, tzinfo=timezone.utc), price=Decimal(91.0), size=Decimal(1.0)),
]
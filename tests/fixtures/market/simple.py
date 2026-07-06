from datetime import datetime, timezone
from decimal import Decimal

from investiq.ingress.synthetic import TradeFixture

symbol = "TEST_SYMBOL"

SIMPLE_TRADES = [
    TradeFixture(symbol=symbol, timestamp_utc=datetime(2026, 1, 1,12, 0, 0, tzinfo=timezone.utc), price=Decimal(100), size=Decimal(1)),
    TradeFixture(symbol=symbol, timestamp_utc=datetime(2026, 1, 1,12, 1, 0, tzinfo=timezone.utc), price=Decimal(101), size=Decimal(1)),
    TradeFixture(symbol=symbol, timestamp_utc=datetime(2026, 1, 1,12, 2, 0, tzinfo=timezone.utc), price=Decimal(102), size=Decimal(1))
]
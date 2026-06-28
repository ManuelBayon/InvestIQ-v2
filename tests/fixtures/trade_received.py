from datetime import datetime, timezone

from investiq.events.factory import CanonicalEventFactory
from investiq.events.market_data import TradeReceived

def make_trade_received(
        event_factory: CanonicalEventFactory,
        symbol: str,
        price: float,
        _day: int = 1,
        _hour: int = 12,
        _min: int = 0,
) -> TradeReceived:
    return event_factory.create_trade_received(
        symbol=symbol,
        timestamp_utc=datetime(
            2026,1,_day,
            _hour, _min,
            tzinfo=timezone.utc
        ),
        price=price,
        size=1.0,
    )


if __name__ == "__main__":
    trade = make_trade_received("AMD", 100.0)
    print(trade)
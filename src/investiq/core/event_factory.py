from datetime import datetime

from investiq.core.events import TradeReceived


class CanonicalEventFactory:

    def __init__(self, run_id: str):
        self._run_id = run_id
        self._next_event_id: int = 1

    def _make_next_event_id(self) -> str:
        event_id =  f"EVT_{self._next_event_id:05d}"
        self._next_event_id += 1
        return event_id

    def create_trade_received(
            self,
            symbol: str,
            timestamp_utc: datetime,
            price: float,
            size: float,
    ) -> TradeReceived:

        event = TradeReceived(
            run_id=self._run_id,
            event_id=self._make_next_event_id(),
            symbol=symbol,
            timestamp_utc=timestamp_utc,
            price=price,
            size=size,
        )
        return event
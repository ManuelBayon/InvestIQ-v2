from datetime import datetime

from investiq.core.events import IntentGenerated, TradeReceived
from investiq.domain.orders import OrderSpec


class EventFactory:
    """Create event identities on the canonical thread only."""

    def __init__(self, run_id: str):
        self._run_id = run_id
        self._next_event_id = 1

    def next_event_id(self) -> str:
        event_id = f"EVT_{self._next_event_id:05d}"
        self._next_event_id += 1
        return event_id

    def create_trade_received(
        self,
        symbol: str,
        timestamp_utc: datetime,
        price: float,
        size: float,
    ) -> TradeReceived:
        return TradeReceived(
            run_id=self._run_id,
            event_id=self.next_event_id(),
            symbol=symbol,
            timestamp_utc=timestamp_utc,
            price=price,
            size=size,
        )

    def create_intent_generated(
        self,
        causation_id: str,
        instrument_id: str,
        order_spec: OrderSpec,
    ) -> IntentGenerated:
        return IntentGenerated(
            run_id=self._run_id,
            event_id=self.next_event_id(),
            causation_id=causation_id,
            instrument_id=instrument_id,
            order_spec=order_spec,
        )

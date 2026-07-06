from datetime import datetime
from dataclasses import dataclass
from decimal import Decimal

from investiq.events.factory import CanonicalEventFactory
from investiq.core.event_queue import CanonicalEventQueue


@dataclass(frozen=True)
class TradeFixture:
    symbol: str
    timestamp_utc: datetime
    price: Decimal
    size: Decimal


class SyntheticIngress:


    def __init__(
            self,
            event_queue: CanonicalEventQueue,
            event_factory: CanonicalEventFactory,
            scenario: list[TradeFixture],
    ):
        self._event_queue = event_queue
        self._event_factory = event_factory
        self._scenario = scenario


    def start(self) -> None:
        for trade in self._scenario:
            event = self._event_factory.create_trade_received(
                symbol=trade.symbol,
                timestamp_utc=trade.timestamp_utc,
                price=trade.price,
                size=trade.size,
            )
            self._event_queue.enqueue(event)
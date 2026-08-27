from datetime import datetime
from dataclasses import dataclass

from investiq.core.event_factory import CanonicalEventFactory
from investiq.core.external_event_queue import ExternalEventQueue


@dataclass(frozen=True)
class TradeFixture:
    symbol: str
    timestamp_utc: datetime
    price: float
    size: float


class SyntheticIngress:


    def __init__(
            self,
            event_queue: ExternalEventQueue,
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
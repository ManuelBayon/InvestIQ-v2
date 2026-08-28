from datetime import datetime
from dataclasses import dataclass

from investiq.adapters.ibkr.ib_client import IBKRClient
from investiq.core.event_factory import CanonicalEventFactory
from investiq.core.event_queue import EventQueue


@dataclass(frozen=True)
class TradeFixture:
    symbol: str
    timestamp_utc: datetime
    price: float
    size: float


class SyntheticIngress:


    def __init__(
            self,
            scenario: list[TradeFixture],
            event_queue: EventQueue,
            event_factory: CanonicalEventFactory,
    ):
        self._scenario = scenario
        self._event_queue = event_queue
        self._event_factory = event_factory


    def start(self) -> None:
        for trade in self._scenario:
            event = self._event_factory.create_trade_received(
                symbol=trade.symbol,
                timestamp_utc=trade.timestamp_utc,
                price=trade.price,
                size=trade.size,
            )
            self._event_queue.enqueue(event)
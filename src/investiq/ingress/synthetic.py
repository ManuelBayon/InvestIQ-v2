from datetime import datetime
from dataclasses import dataclass

from investiq.core.broker_messages import MarketTrade
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
            run_id: str,
    ):
        self._scenario = scenario
        self._event_queue = event_queue
        self._run_id = run_id


    def start(self) -> None:
        for trade in self._scenario:
            event = MarketTrade(
                run_id=self._run_id,
                symbol=trade.symbol,
                timestamp_utc=trade.timestamp_utc,
                price=trade.price,
                size=trade.size,
            )
            self._event_queue.enqueue(event)

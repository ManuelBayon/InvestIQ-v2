import random
from time import sleep

from investiq.events.factory import CanonicalEventFactory
from investiq.process.event_queue import CanonicalEventQueue

from tests.fixtures.trade_received import make_trade_received


class SyntheticIngress:

    def __init__(
            self,
            event_queue: CanonicalEventQueue,
            event_factory: CanonicalEventFactory,
            n: int,
            delay_seconds: int | None = 1,
    ):
        self._event_queue = event_queue
        self._event_factory = event_factory
        self._n = n
        self._delay = delay_seconds

    def start(self) -> None:
        for _ in range(self._n):
            price = float(random.randrange(start=100, stop=110, step=1))
            trade = make_trade_received(
                event_factory=self._event_factory,
                symbol="AMD",
                price=price
            )
            self._event_queue.enqueue(trade)
            if self._delay:
                sleep(self._delay)
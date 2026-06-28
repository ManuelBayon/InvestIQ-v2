import random

from investiq.events.factory import CanonicalEventFactory
from investiq.runtime.event_queue import CanonicalEventQueue

from tests.fixtures.trade_received import make_trade_received


class SyntheticIngress:

    def __init__(
            self,
            event_queue: CanonicalEventQueue,
            event_factory: CanonicalEventFactory,
    ):
        self._event_queue = event_queue
        self._event_factory = event_factory

    def enqueue_one_trade(self) -> None:
        price = float(random.randrange(start=100, stop=110, step=1))
        trade = make_trade_received(
            event_factory=self._event_factory,
            symbol="AMD",
            price=price
        )
        self._event_queue.enqueue(trade)
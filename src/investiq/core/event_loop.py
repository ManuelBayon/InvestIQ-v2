from investiq.core.contracts.events import CanonicalEvent
from investiq.core.event_queue import CanonicalEventQueue

from investiq.core.event_journal import CanonicalEventJournal
from investiq.process.dispatcher import Dispatcher

class CanonicalEventLoop:

    def __init__(
            self,
            journal: CanonicalEventJournal,
            event_queue: CanonicalEventQueue,
            dispatcher: Dispatcher,
    ):
        self._journal = journal
        self._event_queue = event_queue
        self._dispatcher = dispatcher
        self.running = False

    def _process(self, event: CanonicalEvent) -> None:
        self._journal.append(event)
        print(f"[EVENT LOOP] Processed event= {event}")
        result = self._dispatcher.dispatch(event)
        if result is not None:
            self._journal.append(result)
            self._event_queue.enqueue(result)

    def run_until_empty(self) -> None:
        """
        Non-blocking, used for backtest or replay,
        While there are elements returns the elements then ends.
        :return:
        """
        while not self._event_queue.is_empty():
            event = self._event_queue.dequeue_nowait()
            self._process(event)

    def run_forever(self) -> None:
        """
        Blocking method, awaits elements
        To stop the loop, set self._running = False.
        :return:
        """
        self.running = True
        while self.running:
            event = self._event_queue.dequeue_blocking()
            self._process(event)
from investiq.runtime.canonical_event_queue import CanonicalEventQueue
from investiq.events.events import CanonicalEvent, OrderSubmitted, ExecutionSkipped
from investiq.runtime.journal import CanonicalJournal
from investiq.runtime.orchestrator import Orchestrator

class EventLoop:

    def __init__(
            self,
            journal: CanonicalJournal,
            event_queue: CanonicalEventQueue,
            orchestrator: Orchestrator,
    ):
        self._journal = journal
        self._event_queue = event_queue
        self._orchestrator = orchestrator
        self._running = False

    def _process(self, event: CanonicalEvent) -> None:
        print(f"\nProcessed event= {event}")
        self._journal.append(event)
        if isinstance(event, OrderSubmitted) or isinstance(event, ExecutionSkipped):
            return
        result = self._orchestrator.dispatch(event)
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

    def run(self) -> None:
        """
        Blocking method, awaits elements
        To stop the loop, set self._running = False.
        :return:
        """
        self._running = True
        while self._running:
            event = self._event_queue.dequeue_blocking()
            self._process(event)
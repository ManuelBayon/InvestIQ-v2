
from investiq.core.event_queue import CanonicalEventQueue

from investiq.core.event_journal import EventTransitionJournal, EventTransition
from investiq.core.dispatcher import Dispatcher
from investiq.core.events import CanonicalEvent


class CanonicalEventLoop:

    def __init__(
            self,
            journal: EventTransitionJournal,
            event_queue: CanonicalEventQueue,
            dispatcher: Dispatcher,
    ):
        self._journal = journal
        self._event_queue = event_queue
        self._dispatcher = dispatcher
        self.running = False


    def _process(self, event: CanonicalEvent) -> None:
        print(
            f"\n————————————————————————————————————————————————————————————————————————————————————\n"
            f"[EVENT LOOP — PROCESS] : {event}"
        )

        result = self._dispatcher.dispatch(event)

        for evt in result.emitted_events:
            self._event_queue.enqueue(evt)

        self._journal.append(
            EventTransition(
                input_event=event,
                emitted_events=result.emitted_events,
            )
        )


    def run_until_empty(self) -> None:
        """
        Non-blocking, used for backtest or replay,
        While there are elements returns the elements then ends.
        :return:
        """
        while not self._event_queue.is_empty:
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
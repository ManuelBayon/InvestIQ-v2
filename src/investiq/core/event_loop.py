
from investiq.core.event_queue import EventQueue

from investiq.core.event_journal import EventTransitionJournal, EventTransition
from investiq.core.dispatcher import Dispatcher
from investiq.core.events import CanonicalEvent, InternalEvent


class CanonicalEventLoop:

    def __init__(
            self,
            journal: EventTransitionJournal,
            external_event_queue: EventQueue,
            internal_event_queue: EventQueue,
            dispatcher: Dispatcher,
    ):
        self._journal = journal
        self._external_event_queue = external_event_queue
        self._internal_event_queue = internal_event_queue
        self._dispatcher = dispatcher
        self.running = False


    def _process(self, event: CanonicalEvent) -> None:
        print(
            f"\n————————————————————————————————————————————————————————————————————————————————————\n"
            f"[EVENT LOOP — PROCESS] : "
            f"{"InternalEvent" if isinstance(event, InternalEvent) else "ExternalEvent"}"
            f"{event}"

        )

        handler_result = self._dispatcher.dispatch(event)

        for evt in handler_result.emitted_events:
            if isinstance(evt, InternalEvent):
                self._internal_event_queue.enqueue(evt)
            else:
                raise ValueError(
                    f"Unsupported event type for event={evt}, "
                    f"must be either InternalEvent or ExternalEvent"
                )

        self._journal.append(
            EventTransition(
                input_event=event,
                emitted_events=handler_result.emitted_events,
            )
        )


    def run_until_empty(self) -> None:
        """
        Non-blocking, used for backtest or replay,
        While there are elements returns the elements then ends.
        :return:
        """
        while not self._external_event_queue.is_empty:
            external_event = self._external_event_queue.dequeue_nowait()
            self._process(external_event)

            while not self._internal_event_queue.is_empty:
                internal_event = self._internal_event_queue.dequeue_nowait()
                self._process(internal_event)


    def run_forever(self) -> None:
        """
        Blocking method, awaits elements
        To stop the loop, set self._running = False.
        """
        
        self.running = True
        while self.running:

            external_event = self._external_event_queue.dequeue_blocking()
            self._process(external_event)

            while not self._internal_event_queue.is_empty:
                internal_event = self._internal_event_queue.dequeue_nowait()
                self._process(internal_event)
from queue import Empty

from investiq.core.dispatcher import Dispatcher
from investiq.core.event_journal import EventJournal
from investiq.core.event_queue import EventQueue, Message
from investiq.core.events import CanonicalEvent
from investiq.core.order_correlation import OrderCorrelation


class CanonicalEventLoop:
    def __init__(
        self,
        journal: EventJournal,
        inbound_queue: EventQueue,
        internal_event_queue: EventQueue,
        dispatcher: Dispatcher,
        correlation: OrderCorrelation,
    ) -> None:
        self._journal = journal
        self._inbound_queue = inbound_queue
        self._internal_event_queue = internal_event_queue
        self._dispatcher = dispatcher
        self._correlation = correlation
        self.running = False

    def _record(self, event: CanonicalEvent) -> None:
        self._journal.append(event)
        self._correlation.apply(event)

    def _process(self, message: Message, *, already_recorded: bool = False) -> None:
        if isinstance(message, CanonicalEvent) and not already_recorded:
            self._record(message)
        result = self._dispatcher.dispatch(message)

        # All facts are recorded and projected before any command is scheduled.
        for event in result.events:
            self._record(event)
        for event in result.events:
            if self._dispatcher.has_handler(event):
                self._internal_event_queue.enqueue(event)
        for command in result.commands:
            self._internal_event_queue.enqueue(command)

    def _drain_internal(self) -> None:
        while True:
            try:
                message = self._internal_event_queue.dequeue_nowait()
            except Empty:
                return
            # Internal events have already been recorded when their handler returned.
            self._process(message, already_recorded=isinstance(message, CanonicalEvent))

    def run_until_empty(self) -> None:
        """Process available messages; this does not wait for pending IB callbacks."""
        self._drain_internal()
        while True:
            try:
                message = self._inbound_queue.dequeue_nowait()
            except Empty:
                return
            self._process(message)
            self._drain_internal()

    def run_forever(self) -> None:
        self.running = True
        while self.running:
            self._drain_internal()
            message = self._inbound_queue.dequeue_blocking()
            self._process(message)

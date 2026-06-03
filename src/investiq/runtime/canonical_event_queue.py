from queue import Queue

from investiq.events.canonical_events import BaseEvent

class CanonicalEventQueue:

    def __init__(self):
        self._queue: Queue[BaseEvent] = Queue()

    def enqueue(self, event: BaseEvent) -> None:
        self._queue.put(event)

    def dequeue_nowait(self) -> BaseEvent:
        return self._queue.get_nowait()

    def dequeue_blocking(self) -> BaseEvent:
        return self._queue.get()

    def is_empty(self) -> bool:
        return self._queue.empty()
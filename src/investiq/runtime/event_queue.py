from queue import Queue

from investiq.events.base import CanonicalEvent

class CanonicalEventQueue:

    def __init__(self):
        self._queue: Queue[CanonicalEvent] = Queue()

    def enqueue(self, event: CanonicalEvent) -> None:
        self._queue.put(event)

    def dequeue_nowait(self) -> CanonicalEvent:
        return self._queue.get_nowait()

    def dequeue_blocking(self) -> CanonicalEvent:
        return self._queue.get()

    def is_empty(self) -> bool:
        return self._queue.empty()
from queue import Queue

from investiq.core.events import CanonicalEvent


class EventQueue:

    def __init__(self):
        self._queue: Queue[CanonicalEvent] = Queue()

    def enqueue(self, event: CanonicalEvent) -> None:
        self._queue.put(event)

    def dequeue_nowait(self) -> CanonicalEvent:
        """
        Remove and return an item from the queue without blocking.

        Only get an item if one is immediately available.
        Otherwise, raise the Empty exception.
        :return: CanonicalEvent
        """
        return self._queue.get_nowait()

    def dequeue_blocking(self, block: bool = True, timeout=None) -> CanonicalEvent:
        """
        Remove and return an item from the queue.

        - If optional args 'block' is true and 'timeout' is None (the default),
        block if necessary until an item is available.

        - If 'timeout' is a non-negative number, it blocks at most 'timeout'
        seconds and raisesthe Empty exception if no item was available within
        that time.

        - Otherwise ('block' is false), return an item if one is immediately
        available, else raise the Empty exception ('timeout' is ignored
        in that case).

        - Raises ShutDown if the queue has been shut down and is empty,
        or if the queue has been shut down immediately.

        :param block:
        :param timeout:
        :return: CanonicalEvent
        """
        return self._queue.get(block=block, timeout=timeout)

    @property
    def is_empty(self) -> bool:
        return self._queue.empty()

    def __len__(self) -> int:
        return self._queue.qsize()
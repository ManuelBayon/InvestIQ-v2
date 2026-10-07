from queue import Queue

from investiq.core.broker_messages import InboundMessage
from investiq.core.commands import Command
from investiq.core.events import CanonicalEvent


Message = CanonicalEvent | Command | InboundMessage


class EventQueue:
    """Thread-safe FIFO for messages entering or circulating in the canonical loop."""

    def __init__(self) -> None:
        self._queue: Queue[Message] = Queue()

    def enqueue(self, message: Message) -> None:
        self._queue.put(message)

    def dequeue_nowait(self) -> Message:
        return self._queue.get_nowait()

    def dequeue_blocking(self, block: bool = True, timeout: float | None = None) -> Message:
        return self._queue.get(block=block, timeout=timeout)

    @property
    def is_empty(self) -> bool:
        return self._queue.empty()

    def __len__(self) -> int:
        return self._queue.qsize()

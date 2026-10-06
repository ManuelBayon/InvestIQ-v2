from itertools import count


class OrderIdGenerator:
    """Allocate order IDs within one run, from the canonical thread."""

    def __init__(self) -> None:
        self._ids = count(1)

    def next_id(self) -> int:
        return next(self._ids)

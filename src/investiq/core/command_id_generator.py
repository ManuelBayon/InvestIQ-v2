from itertools import count


class CommandIdGenerator:
    """Allocate command IDs within one run, on the canonical thread."""

    def __init__(self) -> None:
        self._ids = count(1)

    def next_id(self) -> str:
        return f"CMD_{next(self._ids):05d}"

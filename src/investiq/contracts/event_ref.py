"""Canonical event identity shared by reception and causality."""
from dataclasses import dataclass
from investiq.contracts._validation import require_text


@dataclass(frozen=True, slots=True)
class EventRef:
    """Identify a reception by run and one-based processing sequence.

    Sequence allocation and uniqueness are enforced by event admission.
    This reference does not identify or deduplicate an external business fact.
    """
    run_id: str
    sequence: int

    def __post_init__(self) -> None:
        require_text(self.run_id, "run_id")
        if isinstance(self.sequence, bool) or not isinstance(self.sequence, int):
            raise TypeError("sequence must be an integer")
        if self.sequence < 1:
            raise ValueError("sequence must be strictly positive")

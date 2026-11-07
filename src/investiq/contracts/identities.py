"""Canonical event and order/request identities."""

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


@dataclass(frozen=True, slots=True)
class OrderId:
    """Opaque identity retained throughout a logical order's lifetime.

    Attributes:
        value: Globally unique identifier allocated before submission.

    Allocation and uniqueness belong to the generator, not this value object.
    No broker identifier or run identifier is encoded by this contract.
    """

    value: str

    def __post_init__(self) -> None:
        require_text(self.value, "value")


@dataclass(frozen=True, slots=True)
class CommandId:
    """Opaque globally unique request identity, allocated by the producer.

    Distinct from the stable order identity. Uniqueness and retry behavior
    are external responsibilities; this type validates the value only.
    """
    value: str

    def __post_init__(self) -> None:
        require_text(self.value, "value")

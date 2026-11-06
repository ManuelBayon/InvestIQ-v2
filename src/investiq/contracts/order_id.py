"""Internal order identity, independent of broker references."""

from dataclasses import dataclass

from investiq.contracts._validation import require_text


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

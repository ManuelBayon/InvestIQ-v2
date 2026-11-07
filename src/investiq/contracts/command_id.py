"""Identity of a single execution request."""
from dataclasses import dataclass
from investiq.contracts._validation import require_text


@dataclass(frozen=True, slots=True)
class CommandId:
    """Opaque globally unique request identity, allocated by the producer.

    Distinct from the stable order identity. Uniqueness and retry behavior
    are external responsibilities; this type validates the value only.
    """
    value: str

    def __post_init__(self) -> None:
        require_text(self.value, "value")

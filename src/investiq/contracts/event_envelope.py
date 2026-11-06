"""Reception metadata kept separate from normalized event payloads."""

from dataclasses import dataclass
from datetime import datetime

from investiq.contracts._validation import require_text, require_utc


@dataclass(frozen=True, slots=True)
class EventEnvelope:
    """Identify and timestamp an event reception within a run.

    Attributes:
        run_id: Identifier of the run admitting the event.
        sequence: One-based sequence reflecting the engine consumption order.
        received_at_utc: Local reception time, expressed as aware UTC;
            distinct from the source timestamp carried by the payload.

    The pair (run_id, sequence) identifies this reception, not the external
    business fact. Repeated source notifications have distinct receptions.
    The admitting component assigns metadata and guarantees sequence uniqueness
    and ordering; this value object only validates intrinsic invariants.

    No identifiers or timestamps are generated during construction, allowing
    explicit clocks and deterministic replay. Broker provenance belongs to the
    run configuration. Payloads are composed with this envelope, not inherited.

    Raises:
        TypeError: A field has an unsupported type.
        ValueError: A field violates an intrinsic contract invariant.
    """

    run_id: str
    sequence: int
    received_at_utc: datetime

    def __post_init__(self) -> None:
        require_text(self.run_id, "run_id")
        # bool is an int subclass but is not a valid sequence number.
        if isinstance(self.sequence, bool) or not isinstance(self.sequence, int):
            raise TypeError("sequence must be an integer")
        if self.sequence < 1:
            raise ValueError("sequence must be strictly positive")
        require_utc(self.received_at_utc, "received_at_utc")

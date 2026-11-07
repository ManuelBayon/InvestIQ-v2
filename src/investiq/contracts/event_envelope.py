"""Admission metadata separate from normalized event payloads."""
from dataclasses import dataclass
from datetime import datetime
from investiq.contracts._validation import require_utc
from investiq.contracts.event_ref import EventRef


@dataclass(frozen=True, slots=True)
class EventEnvelope:
    """Identify and timestamp admission of an event to the engine.

    event_ref identifies this reception. received_at_utc is local admission
    time, distinct from the payload's source time. Admission assigns these
    values explicitly; construction never reads a clock or generates identity.
    """
    event_ref: EventRef
    received_at_utc: datetime

    def __post_init__(self) -> None:
        if not isinstance(self.event_ref, EventRef):
            raise TypeError("event_ref must be an EventRef")
        require_utc(self.received_at_utc, "received_at_utc")

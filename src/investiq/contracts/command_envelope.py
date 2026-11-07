"""Causal context for a produced command."""
from dataclasses import dataclass
from datetime import datetime
from investiq.contracts._validation import require_utc
from investiq.contracts.event_ref import EventRef


@dataclass(frozen=True, slots=True)
class CommandEnvelope:
    """Record the immediate cause and production time of a command.

    The producing run is causation_ref.run_id; no duplicate run ID is stored.
    The engine verifies the cause exists. The clock is supplied externally.
    """
    causation_ref: EventRef
    created_at_utc: datetime

    def __post_init__(self) -> None:
        if not isinstance(self.causation_ref, EventRef):
            raise TypeError("causation_ref must be an EventRef")
        require_utc(self.created_at_utc, "created_at_utc")

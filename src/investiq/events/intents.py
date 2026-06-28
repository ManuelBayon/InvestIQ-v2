from dataclasses import dataclass

from investiq.domain.decision.base import NoOperation, OrderIntent
from investiq.events.base import CanonicalEvent


@dataclass(frozen=True)
class IntentGenerated(CanonicalEvent):
    intent: NoOperation | OrderIntent
    def __repr__(self):
        return (
            f"IntentGenerated(\n"
            f"\trun_id={self.run_id},\n"
            f"\tevent_id={self.event_id},\n"
            f"\tcausation_id={self.causation_id},\n"
            f"\tintent={self.intent}\n"
            f")"
        )
from investiq.domain.decision_layer.base import NoOperation, OrderIntent
from investiq.domain.models import RawTick
from investiq.domain.order_specs import OrderSpecs
from investiq.events.events import TickDataAvailable, IntentGenerated, OrderSubmitted, ExecutionSkipped


class CanonicalEventFactory:

    def __init__(self, run_id: str):
        self._run_id = run_id
        self._next_event_id: int = 1

    def _make_next_event_id(self) -> str:
        event_id =  f"EVT_{self._next_event_id:05d}"
        self._next_event_id += 1
        return event_id

    def create_tick_data_available(
            self,
            payload: dict[str, list[RawTick]],
            meta_data : dict | None = None,
    ) -> TickDataAvailable:

        if meta_data is None:
            meta_data = {}

        return TickDataAvailable(
            run_id=self._run_id,
            event_id=self._make_next_event_id(),
            causation_id=None,
            meta_data=meta_data,
            payload=payload
        )

    def create_intent_generated(
            self,
            causation_id: str,
            payload: NoOperation | OrderIntent,
            meta_data: dict | None = None
    ) -> IntentGenerated:

        if meta_data is None:
            meta_data = {}

        return IntentGenerated(
            run_id=self._run_id,
            event_id=self._make_next_event_id(),
            causation_id=causation_id,
            meta_data=meta_data,
            payload=payload
        )

    def create_order_submitted(
            self,
            causation_id: str,
            payload: OrderSpecs,
            meta_data: dict | None = None
    ) -> OrderSubmitted:

        if meta_data is None:
            meta_data = {}

        return OrderSubmitted(
            run_id=self._run_id,
            event_id=self._make_next_event_id(),
            causation_id=causation_id,
            meta_data=meta_data,
            payload=payload,
        )

    def create_no_order_submitted(
            self,
            causation_id: str,
            payload: dict,
            meta_data: dict | None = None
    ) -> ExecutionSkipped:

        if meta_data is None:
            meta_data = {}

        return ExecutionSkipped(
            run_id=self._run_id,
            event_id=self._make_next_event_id(),
            causation_id=causation_id,
            meta_data=meta_data,
            payload=payload,
        )
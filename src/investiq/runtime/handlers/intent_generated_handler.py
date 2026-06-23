from investiq.adapters.ibkr_adapter import IBKRAdapter
from investiq.domain.decision_layer.base import NoOperation, OrderIntent
from investiq.events.events import IntentGenerated, OrderSubmitted, ExecutionSkipped
from investiq.events.factory import CanonicalEventFactory


class IntentGeneratedHandler:

    def __init__(
            self,
            ibkr_adapter: IBKRAdapter,
            event_factory: CanonicalEventFactory,
    ):
        self._adapter =ibkr_adapter
        self._event_factory = event_factory

    def handle(self, event: IntentGenerated) -> OrderSubmitted | ExecutionSkipped:

        if isinstance(event.payload, NoOperation):
            return self._event_factory.create_no_order_submitted(
                causation_id=event.event_id,
                payload={"reason": "NoOperation"}
            )
        elif isinstance(event.payload, OrderIntent):
            self._adapter.ib_loop.call_soon_threadsafe(
                self._adapter.place_market_order,
                event.payload.order_specs,
            )
            return self._event_factory.create_order_submitted(
                causation_id=event.event_id,
                payload=event.payload.order_specs
            )
        else:
            raise NotImplementedError(
                f"Unsupported event.payload, got:{type(event.payload).__name__}"
            )
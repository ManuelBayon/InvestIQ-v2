from investiq.adapters.ibkr_adapter import IBKRAdapter
from investiq.domain.decision_layer.base import NoOperation
from investiq.domain.order_specs import MarketOrderSpec
from investiq.events.events import IntentGenerated, OrderSubmitted
from investiq.events.factory import CanonicalEventFactory


class IntentGeneratedHandler:

    def __init__(
            self,
            ibkr_adapter: IBKRAdapter,
            event_factory: CanonicalEventFactory,
    ):
        self._adapter =ibkr_adapter
        self._event_factory = event_factory

    def handle(self, event: IntentGenerated) -> OrderSubmitted:

        if isinstance(event.payload, NoOperation):
            return self._event_factory.create_order_submitted(
                causation_id=event.causation_id,
                payload=None
            )

        order_intent = event.payload
        order_specs = order_intent.order_spec

        if isinstance(order_specs, MarketOrderSpec):
            self._adapter.place_market_order(order_specs)
        else:
            raise NotImplementedError(
                f"Unsupported OrderSpec type, got:{type(order_specs).__name__}"
            )

        return self._event_factory.create_order_submitted(
            causation_id=event.causation_id,
            payload=None
        )
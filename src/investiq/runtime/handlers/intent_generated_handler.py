from investiq.adapters.ibkr_adapter import IBKRGatewayAdapter
from investiq.domain.decision_layer.base import NoOperation
from investiq.domain.order_specs import MarketOrderSpec
from investiq.events.events import IntentGenerated


class IntentGeneratedHandler:

    def __init__(self, ibkr_adapter: IBKRGatewayAdapter):
        self._adapter =ibkr_adapter

    def handle(self, event: IntentGenerated) -> None:

        if isinstance(event.payload, NoOperation):
            return None

        order_intent = event.payload
        order_specs = order_intent.order_spec

        if isinstance(order_specs, MarketOrderSpec):
            self._adapter.place_market_order(order_specs)
        else:
            raise NotImplementedError(
                f"Unsupported OrderSpec type, got:{type(order_specs).__name__}"
            )
        return None
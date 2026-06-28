from investiq.adapters.ibkr.ib_adapter import IBKRAdapter
from investiq.adapters.ibkr.ib_broker_adapter import IBKRBrokerAdapter
from investiq.domain.decision.base import NoOperation, OrderIntent
from investiq.events.intents import IntentGenerated
from investiq.events.orders import OrderSubmitted, ExecutionSkipped
from investiq.events.factory import CanonicalEventFactory


class IntentGeneratedHandler:

    def __init__(
            self,
            ibkr_adapter: IBKRAdapter,
            broker_adapter: IBKRBrokerAdapter,
            event_factory: CanonicalEventFactory,
    ):
        self._ibkr_adapter = ibkr_adapter
        self._broker_adapter = broker_adapter
        self._event_factory = event_factory

    def handle(self, event: IntentGenerated) -> OrderSubmitted | ExecutionSkipped:

        if isinstance(event.intent, NoOperation):
            return self._event_factory.create_no_order_submitted(
                causation_id=event.event_id,
                reason= "NoOperation",
            )
        elif isinstance(event.intent, OrderIntent):
            self._ibkr_adapter.ib_loop.call_soon_threadsafe(
                self._broker_adapter.place_market_order,
                event.intent.order_specs,
            )
            return self._event_factory.create_order_submitted(
                causation_id=event.event_id,
                order=event.intent.order_specs
            )
        else:
            raise NotImplementedError(
                f"Unsupported intent type, got:{type(event.intent).__name__}"
                f"Supported intents are NoOperation and OrderIntent"
            )
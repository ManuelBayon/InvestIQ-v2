from investiq.domain.decision.base import NoOperation
from investiq.domain.market_data.stores.trade_store import TradeStore
from investiq.events.factory import CanonicalEventFactory
from investiq.events.intents import IntentGenerated
from investiq.events.market_data import TradeReceived


class TradeReceivedHandler:

    def __init__(
            self,
            trade_store: TradeStore,
            event_factory: CanonicalEventFactory,
    ):
        self._trade_store = trade_store
        self._event_factory = event_factory

    def handle(
            self,
            event: TradeReceived
    ) -> IntentGenerated:

        self._trade_store.ingest(event)

        return self._event_factory.create_intent_generated(
            causation_id=event.event_id,
            intent=NoOperation(),
        )
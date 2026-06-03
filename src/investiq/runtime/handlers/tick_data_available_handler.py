from investiq.domain.decision_layer import DecisionLayer
from investiq.domain.feature_store import FeatureStore
from investiq.domain.market_store import MarketStore
from investiq.events.canonical_event_factory import CanonicalEventFactory
from investiq.events.canonical_events import IntentGenerated,TickDataAvailable

class TickDataAvailableHandler:

    def __init__(
            self,
            market_store: MarketStore,
            feature_store: FeatureStore,
            decision_layer: DecisionLayer,
            event_factory: CanonicalEventFactory,
    ):
        self._market_store = market_store
        self._feature_store = feature_store
        self._decision_layer = decision_layer
        self._event_factory = event_factory

    def handle(
            self,
            event: TickDataAvailable
    ) -> IntentGenerated:
        self._market_store.ingest(event.payload)
        self._feature_store.update(self._market_store.view())
        result = self._decision_layer.evaluate(
            market_view=self._market_store.view(),
            features_view=self._feature_store.view()
        )
        intent = self._event_factory.create_intent_generated(
            causation_id=event.event_id,
            payload=result,
        )
        return intent

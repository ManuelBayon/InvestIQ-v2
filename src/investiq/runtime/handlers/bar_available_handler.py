
from investiq.domain.decision_layer import DecisionLayer, DecisionLayerContext
from investiq.domain.feature_store import FeatureStore
from investiq.domain.market_store import MarketStore
from investiq.events.canonical_events import BarAvailable, IntentGenerated, NoOperation


class BarAvailableHandler:

    def __init__(
            self,
            market_store: MarketStore,
            feature_store: FeatureStore,
            decision_layer: DecisionLayer,
    ):
        self._market_store = market_store
        self._feature_store = feature_store
        self._decision_layer = decision_layer

    def handle(
            self,
            next_id: str,
            bar_available: BarAvailable
    ) -> NoOperation | IntentGenerated:

        # Update market store
        self._market_store.ingest(bar_available.bar)
        market_view = self._market_store.view()

        # Update feature store
        self._feature_store.update(market_view=market_view)
        feature_view = self._feature_store.view()

        # Evaluate
        intent = self._decision_layer.evaluate(
            layer_context=DecisionLayerContext(
                run_id=bar_available.run_id,
                next_event_id=next_id,
                causation_id=bar_available.event_id,
            ),
            market_view=market_view,
            features_view=feature_view,
        )

        # Return intent
        return intent
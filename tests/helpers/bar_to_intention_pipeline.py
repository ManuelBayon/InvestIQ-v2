from sandbox.canonical_events import BarAvailable, IntentGenerated, NoOperation
from investiq.domain.decision_layer import DecisionLayer
from investiq.domain.feature_store import FeatureStore
from investiq.domain.market_store import MarketStore


def run_bar_available_to_intention_causal_pipeline(
        market_store: MarketStore,
        feature_store: FeatureStore,
        decision_layer: DecisionLayer,
        bars: list[BarAvailable],
) -> tuple[IntentGenerated | NoOperation, ...]:
    """
    2026-05-19:
    Parametrized bar to intention pipeline, use it with trivial decision layers to test scenarios :
    - different BarAvailable sequences
    - different OrderIntent,
    It returns immuable intents.
    Decision layers can be found here : sandbox/components/no_op.py
    2026-05-17 : Bar to Intention pipeline
    """

    # Internal state initialization
    decisions: list[IntentGenerated | NoOperation] = []
    next_event_id: int = 0

    # Run pipeline for each `BarAvailable` event
    for b in bars:
        market_store.ingest(b.bar)
        market_view = market_store.view()
        feature_store.update(market_view=market_view)
        feature_view = feature_store.view()
        decision = decision_layer.evaluate(
            run_id=b.run_id,
            next_event_id=f"next_event_id_{next_event_id}",
            bar_event_id=b.event_id,
            market_view=market_view,
            features_view=feature_view,
        )
        decisions.append(decision)
        next_event_id += 1

    # Return immuable intents
    return tuple(decisions)

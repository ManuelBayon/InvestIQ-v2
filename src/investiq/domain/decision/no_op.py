from investiq.domain.decision.base import DecisionLayer, NoOperation, _build_context
from investiq.domain.models import RawTick

class NoOperationDecisionLayer(DecisionLayer):
    """
    2026-06-02 : Trivial NoOperation DecisionLayer build decision context and returns it to the handler
    and adds metadata event_id, causation_id, run_id etc.
    2026-05-19 : Trivial decision pipeline returning NoOperation used to test complete causal pipeline.
    2026-05-17 : Naive pure decision pipeline. Transforms market and feature into trading decision.
    """
    def evaluate(
            self,
            market_view: dict[str, list[RawTick]],
            feature_view: dict[str, dict[str, list[float]]],
    ) -> NoOperation:
        context = _build_context(market_view, feature_view)
        return NoOperation(context=context)
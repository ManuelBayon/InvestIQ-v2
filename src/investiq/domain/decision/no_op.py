from investiq.domain.decision.base import DecisionLayer, NoOperation

class NoOperationDecisionLayer(DecisionLayer):
    """
    2026-06-02 : Trivial NoOperation DecisionLayer build decision context and returns it to the handler
    and adds metadata event_id, causation_id, run_id etc.
    2026-05-19 : Trivial decision pipeline returning NoOperation used to test complete causal pipeline.
    2026-05-17 : Naive pure decision pipeline. Transforms market and feature into trading decision.
    """
    def evaluate(self) -> NoOperation:
        return NoOperation()
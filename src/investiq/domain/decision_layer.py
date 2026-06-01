from typing import Protocol
from dataclasses import dataclass

from investiq.domain.order_intents import(
    MarketOrderIntent,
    Side,
    LimitOrderIntent,
    StopMarketOrderIntent,
    BracketOrderIntent
)
from investiq.domain.models import Bar
from investiq.events.canonical_events import(
    IntentGenerated,
    NoOperation,
    DecisionContext
)

@dataclass(frozen=True)
class DecisionLayerContext:
    run_id: str
    next_event_id: str
    causation_id: str


class DecisionLayer(Protocol):
    def evaluate(
            self,
            layer_context : DecisionLayerContext,
            market_view: tuple[Bar,  ...],
            features_view: tuple[float, ...],
    ) -> IntentGenerated | NoOperation:
        ...

class NoOperationDecisionLayer:
    """
    2026-05-19 : Trivial decision pipeline returning NoOperation used to test complete causal pipeline.
    2026-05-17 : Naive pure decision pipeline. Transforms market and feature into trading decision.
    """
    def evaluate(
            self,
            layer_context : DecisionLayerContext,
            market_view: tuple[Bar,  ...],
            features_view: tuple[float, ...],
    ) -> IntentGenerated | NoOperation:
        decision_context = DecisionContext(
            bar=market_view[-1],
            features={
                "sma_2": features_view[-1] if features_view else None
            },
        )
        return NoOperation(
            run_id=layer_context.run_id,
            event_id=layer_context.next_event_id,
            causation_id=layer_context.causation_id,
            meta_data={},
            context=decision_context,
        )

class MarketOrderIntentDecisionLayer:
    """
    2026-05-19 : Trivial decision pipeline returning MarketOrderIntent used to test complete causal pipeline.
    """
    def evaluate(
            self,
            layer_context: DecisionLayerContext,
            market_view: tuple[Bar,  ...],
            features_view: tuple[float, ...],
    ) -> IntentGenerated | NoOperation:
        context = DecisionContext(
            bar=market_view[-1],
            features={
                "sma_2": features_view[-1] if features_view else None
            },
        )
        order_intent = MarketOrderIntent(
            quantity=1,
            direction=Side.BUY,
        )
        return IntentGenerated(
            run_id=layer_context.run_id,
            event_id=layer_context.next_event_id,
            causation_id=layer_context.causation_id,
            meta_data={},
            context=context,
            intent=order_intent
        )

class LimitOrderIntentDecisionLayer:
    """
    2026-05-19 : Trivial decision pipeline returning LimitOrderIntent used to test complete causal pipeline.
    """
    def evaluate(
            self,
            layer_context: DecisionLayerContext,
            market_view: tuple[Bar,  ...],
            features_view: tuple[float, ...],
    ) -> IntentGenerated | NoOperation:
        context = DecisionContext(
            bar=market_view[-1],
            features={
                "sma_2": features_view[-1] if features_view else None
            },
        )
        order_intent = LimitOrderIntent(
            quantity=1,
            direction=Side.SELL,
            price=90.0
        )
        return IntentGenerated(
            run_id=layer_context.run_id,
            event_id=layer_context.next_event_id,
            causation_id=layer_context.causation_id,
            meta_data={},
            context=context,
            intent=order_intent
        )

class StopMarketOrderIntentDecisionLayer:
    """
    2026-05-19 : Trivial decision pipeline returning StopMarketOrderIntent used to test complete causal pipeline.
    """
    def evaluate(
            self,
            layer_context : DecisionLayerContext,
            market_view: tuple[Bar,  ...],
            features_view: tuple[float, ...],
    ) -> IntentGenerated | NoOperation:
        context = DecisionContext(
            bar=market_view[-1],
            features={
                "sma_2": features_view[-1] if features_view else None
            },
        )
        order_intent = StopMarketOrderIntent(
            trigger_price=100.0,
            triggered_order=MarketOrderIntent(
               quantity=1,
                direction=Side.BUY,
            )
        )
        return IntentGenerated(
            run_id=layer_context.run_id,
            event_id=layer_context.next_event_id,
            causation_id=layer_context.causation_id,
            meta_data={},
            context=context,
            intent=order_intent
        )

class BracketOrderIntentDecisionLayer:
    """
    2026-05-19 : Trivial decision pipeline returning StopMarketOrderIntent used to test complete causal pipeline.
    """
    def evaluate(
            self,
            layer_context: DecisionLayerContext,
            market_view: tuple[Bar,  ...],
            features_view: tuple[float, ...],
    ) -> IntentGenerated | NoOperation:
        context = DecisionContext(
            bar=market_view[-1],
            features={
                "sma_2": features_view[-1] if features_view else None
            },
        )
        order_intent = BracketOrderIntent(
                entry=MarketOrderIntent(
                   quantity=1,
                   direction=Side.BUY,
                ),
                stop_loss=[
                    StopMarketOrderIntent(
                        trigger_price=90.0,
                        triggered_order=MarketOrderIntent(
                            quantity=1,
                            direction=Side.SELL,
                        )
                    )
                ],
                take_profit=[
                    LimitOrderIntent(
                        quantity=1,
                        direction=Side.SELL,
                        price=130.0
                    )
                ]
            )
        return IntentGenerated(
            run_id=layer_context.run_id,
            event_id=layer_context.next_event_id,
            causation_id=layer_context.causation_id,
            meta_data={},
            context=context,
            intent=order_intent
        )
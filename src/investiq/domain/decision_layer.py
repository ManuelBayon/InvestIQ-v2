from dataclasses import dataclass
from typing import Protocol

from investiq.domain.models import RawTick
from investiq.domain.order_intents import OrderSpec


@dataclass(frozen=True)
class IntentContext:
    market_view: dict[str, RawTick]
    feature_view: dict[str, dict[str, float]]

@dataclass(frozen=True)
class OrderIntent:
    context: IntentContext
    order_spec: OrderSpec

@dataclass(frozen=True)
class NoOperation:
    context: IntentContext

class DecisionLayer(Protocol):
    def evaluate(
            self,
            market_view: dict[str, list[RawTick]],
            features_view: dict[str, dict[str, list[float]]],
    ) -> NoOperation | OrderIntent:
        ...

class NoOperationDecisionLayer:
    """
    2026-06-02 : Trivial NoOperation DecisionLayer build decision context and returns it to the handler
    the handler adds meta data event_id, causation_id, run_id etc.
    2026-05-19 : Trivial decision pipeline returning NoOperation used to test complete causal pipeline.
    2026-05-17 : Naive pure decision pipeline. Transforms market and feature into trading decision.
    """
    def evaluate(
            self,
            market_view: dict[str, list[RawTick]],
            features_view: dict[str, dict[str, list[float]]],
    ) -> NoOperation:
        last_tick_view = {}
        for symbol, ticks in market_view.items():
            if not ticks:
                continue
            last_tick_view[symbol] = ticks[-1]

        last_features = {}
        for symbol, features in features_view.items():
            if not features:
                continue
            last_features[symbol] = {}
            for feature_name, values in features.items():
                if not values:
                    continue
                last_features[symbol][feature_name] = values[-1]
        return NoOperation(
            context=IntentContext(
                market_view=last_tick_view,
                feature_view=last_features
            )
        )
from dataclasses import dataclass
from typing import Protocol

from investiq.domain.models import RawTick
from investiq.domain.order_specs import OrderSpec


@dataclass(frozen=True)
class DecisionContext:
    last_tick: dict[str, RawTick]
    last_features: dict[str, dict[str, float]]

@dataclass(frozen=True)
class OrderIntent:
    context: DecisionContext
    order_spec: OrderSpec

@dataclass(frozen=True)
class NoOperation:
    context: DecisionContext

def _build_context(
        market_view: dict[str, list[RawTick]],
        feature_view: dict[str, dict[str, list[float]]],
) -> DecisionContext:

    # Build market context
    last_tick_view = {}
    for symbol, ticks in market_view.items():
        if not ticks:
            continue
        last_tick_view[symbol] = ticks[-1]

    # Build feature context
    last_features = {}
    for symbol, features in feature_view.items():
        if not features:
            continue
        last_features[symbol] = {}
        for feature_name, values in features.items():
            if not values:
                continue
            last_features[symbol][feature_name] = values[-1]
    # Return decision context
    return DecisionContext(
        last_tick=last_tick_view,
        last_features=last_features,
    )

class DecisionLayer(Protocol):
    def evaluate(
            self,
            market_view: dict[str, list[RawTick]],
            feature_view: dict[str, dict[str, list[float]]],
    ) -> NoOperation | OrderIntent:
        ...
from typing import Sequence, ClassVar

from investiq.domain.features.simple_moving_average import SimpleMovingAverage
from investiq.domain.order_types import MarketOrderSpec, Order
from investiq.domain.strategies.base_strategy import TradingIntent, DecisionContext, FeatureRequirement


class MovingAverageCrossStrategy:

    requirements: ClassVar[Sequence[FeatureRequirement]] = (
        FeatureRequirement(
            name="sma_short",
            feature_type=SimpleMovingAverage,
        ),
        FeatureRequirement(
            name="sma_long",
            feature_type=SimpleMovingAverage,
        )
    )

    def decide(self, context: DecisionContext) -> list[Order]:

        sma_short = context.features["sma_short"]
        sma_long = context.features["sma_long"]

        if sma_short > sma_long:
            return [MarketOrderSpec(quantity=1)]

        elif sma_short < sma_long:
            return [MarketOrderSpec(quantity=-1)]

        else:
            return []
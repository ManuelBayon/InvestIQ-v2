from typing import Sequence, ClassVar

from investiq.features.simple_moving_average import SimpleMovingAverage
from investiq.strategies.base_strategy import TradingIntent, DecisionContext, FeatureRequirement


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


    def decide(self, context: DecisionContext) -> list[TradingIntent]:

        sma_short = context.features["sma_short"]
        sma_long = context.features["sma_long"]

        symbol = context.symbol

        if sma_short > sma_long:
            return [TradingIntent(symbol=symbol, target=1.0)]

        elif sma_short < sma_long:
            return [TradingIntent(symbol=symbol, target=-1.0)]

        else:
            return []
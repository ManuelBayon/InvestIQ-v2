from investiq.features.features import FeatureSpecs
from investiq.features.simple_moving_average import SimpleMovingAverage
from investiq.strategies.base_strategy import TradingIntent, DecisionContext

class MovingAverageCrossStrategy:

    requirements : dict[str, FeatureSpecs] = {
        "sma_short" : SimpleMovingAverage,
        "sma_long" : SimpleMovingAverage
    }

    def decide(
            self,
            context: DecisionContext,
    ) -> list[TradingIntent]:

        sma_short = context.features["sma_short"]
        sma_long = context.features["sma_long"]

        if sma_short > sma_long:
            return [
                TradingIntent(
                    symbol = context.symbol,
                    target = 1.0
                )
            ]
        elif sma_short < sma_long:
            return [
                TradingIntent(
                    symbol = context.symbol,
                    target = -1.0
                )
            ]
        else:
            return []
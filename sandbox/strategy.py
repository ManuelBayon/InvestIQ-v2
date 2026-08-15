from investiq.features.examples import SimpleMovingAverage
from investiq.features.features import PriceSource, Feature, Source, FeatureSpecs
from investiq.strategies.base_strategy import TradingIntent


class MovingAverageCrossStrategy:

    requirements = {
        "price" : FeatureSpecs(
            type = PriceSource,
            sources = ["symbol"],
            params = {}
        ),
        "sma_short" : FeatureSpecs(
            type = SimpleMovingAverage,
            sources = ["price"],
            params= {
                "window" : "short_window"
            }
        ),
        "sma_long" : FeatureSpecs(
            type = SimpleMovingAverage,
            sources = ["price"],
            params = {
                "window": "long_window"
            }
        )
    }

    def __init__(
            self,
            symbol: str,
            short_window: int,
            long_window: int
    ):
        self._symbol = symbol
        self._short_window = short_window
        self._long_window = long_window

    def decide(self) -> list[TradingIntent]:
        return []
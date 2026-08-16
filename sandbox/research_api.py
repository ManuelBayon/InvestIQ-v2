from dataclasses import dataclass

from investiq.features.features import PriceSource, FeatureSpecs
from investiq.features.simple_moving_average import SimpleMovingAverage
from investiq.strategies.base_strategy import StrategySpecs
from sandbox.strategy import MovingAverageCrossStrategy

@dataclass
class Experiment:
    symbol: str
    price_source: type[PriceSource]
    features: dict[str, FeatureSpecs]
    strategy_specs: StrategySpecs


price_source = PriceSource

sma_short = FeatureSpecs(
    feature=SimpleMovingAverage,
    sources=[price_source],
    params={
        "window": 2
    }
)

sma_long = FeatureSpecs(
    feature=SimpleMovingAverage,
    sources=[price_source],
    params={
        "window": 5
    }
)

strategy_specs = StrategySpecs(
    type=MovingAverageCrossStrategy,
    params= {}
)

experiment = Experiment(
    symbol="SYMBOL_1",
    price_source=price_source,
    features={
        "sma_short": sma_short,
        "sma_long": sma_long
    },
    strategy_specs=strategy_specs,
)
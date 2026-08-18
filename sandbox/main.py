from dataclasses import dataclass

from investiq.domain.market_store import InMemoryMarketStore
from investiq.features.bootstrap_graph import bootstrap_feature_graph
from investiq.features.feature_runtime import FeatureRuntime
from investiq.features.features import PriceSource, FeatureSpecs
from investiq.features.simple_moving_average import SimpleMovingAverage
from investiq.strategies.base_strategy import StrategySpecs
from sandbox.strategy import MovingAverageCrossStrategy
from tests.fixtures.market.simple_trades import MONO_SYMBOL_SIMPLE_TRADES


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

if __name__ == "__main__":

    # Market data
    universe = (experiment.symbol,)
    store = InMemoryMarketStore(universe)
    price_source = experiment.price_source(source=store, symbol=experiment.symbol)

    # Features
    features = [
        f.feature([price_source], **f.params)
        for f in experiment.features.values()
    ]
    graph = bootstrap_feature_graph(sources=[price_source], features=features)
    runtime = FeatureRuntime(graph=graph)

    # Strategy
    strategy = experiment.strategy_specs.type(**strategy_specs.params)

    for i, trade in enumerate(MONO_SYMBOL_SIMPLE_TRADES):
        store.on_trade_received(trade)
        runtime.on_trade_received()

        print(f"\n  ————————————  STEP n°{i+1} ————————————  \nfeatures={features}")
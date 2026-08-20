from collections.abc import Mapping, Sequence
from dataclasses import dataclass

from investiq.domain.market_store import InMemoryMarketStore
from investiq.errors import MissingFeatureRequirementError, FeatureTypeMismatchError
from investiq.features.bootstrap_graph import bootstrap_feature_runtime
from investiq.features.features import FeatureSpec, build_features, Feature
from investiq.features.simple_moving_average import SimpleMovingAverage
from investiq.features.sources import PriceSource
from investiq.strategies.base_strategy import StrategySpec, FeatureRequirement, DecisionContext
from investiq.strategies.simple_moving_average_cross import MovingAverageCrossStrategy
from tests.fixtures.market.simple_trades import MONO_SYMBOL_SIMPLE_TRADES


@dataclass(frozen=True, slots=True)
class ExperimentSpec:
    """
    2026-08-19: Work hypothesis : Mono symbol experiment
    """
    symbol: str
    features: Mapping[str, FeatureSpec]
    strategy_spec: StrategySpec


sma_short_spec = FeatureSpec(
    feature_type=SimpleMovingAverage,
    params={
        "window": 2
    }
)

sma_long_spec = FeatureSpec(
    feature_type=SimpleMovingAverage,
    params={
        "window": 5,
    }
)

strategy_spec = StrategySpec(
    strategy_type=MovingAverageCrossStrategy,
)

experiment = ExperimentSpec(
    symbol="SYMBOL_1",
    features={
        "sma_short": sma_short_spec,
        "sma_long": sma_long_spec,
    },
    strategy_spec=strategy_spec,
)


def validate_strategy_requirements(
        requirements: Sequence[FeatureRequirement],
        available_feature: Mapping[str, Feature],
) -> None:

    for requirement in requirements:

        name = requirement.name
        expected_type = requirement.feature_type

        if name not in available_feature:
            raise MissingFeatureRequirementError(
                f"Feature {name} is missing."
                f"Available features are: {available_feature.keys()}."
            )

        feature = available_feature[name]

        if not isinstance(feature, expected_type):
            raise FeatureTypeMismatchError(
                f"Invalid feature type for feature {name}."
                f"Expected={expected_type}, "
                f"Actual={type(feature)}."
            )


if __name__ == "__main__":

    universe = (experiment.symbol,)
    store = InMemoryMarketStore(universe)

    source = PriceSource(
        source=store,
        symbol=experiment.symbol
    )

    features_by_name = build_features(
        source=source,
        features=experiment.features
    )

    validate_strategy_requirements(
        requirements=experiment.strategy_spec.strategy_type.requirements,
        available_feature=features_by_name
    )

    feature_runtime = bootstrap_feature_runtime(
        sources=[source],
        features=list(features_by_name.values())
    )

    strategy = experiment.strategy_spec.strategy_type()

    strategy_features = {
        requirement.name : features_by_name[requirement.name]
        for requirement in strategy.requirements
    }

    for name, feature in strategy_features.items(): #debug
        print(f"{name} : {feature}")

    for i, trade in enumerate(MONO_SYMBOL_SIMPLE_TRADES): # debug
        print(f"\n—————————————  NEW TRADE n°{i+1}  ——————————————\n") # debug

        store.on_trade_received(trade)
        emitted = feature_runtime.on_trade_received()
        emitted_feature = [
            node.payload
            for node in emitted
        ]

        for e in emitted: # debug
            print(f"{e.payload}")

        # Check if all features needed by the strategy have emitted
        all_requirements_emitted = all(
            feature in emitted_feature
            for feature in strategy_features.values()
        )

        if all_requirements_emitted:
            trading_intent = strategy.decide(
                context=DecisionContext(
                    symbol=experiment.symbol,
                    price=source.last(),
                    features={
                        name: feature.latest()
                        for name, feature in strategy_features.items()
                    },
                )
            )
            print(f"trading intent: {trading_intent}")
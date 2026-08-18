from investiq.domain.market_store import InMemoryMarketStore
from investiq.features.feature_runtime import FeatureGraph, FeatureNode
from sandbox.research_api import Experiment, experiment

"""
experiment = Experiment(
    symbol="SYMBOL_1",
    price_source=price_source,
    features={
        "sma_short": sma_short,
        "sma_long": sma_long
    },
    strategy_specs=strategy_specs,
)
"""

def bootstrap(exp: Experiment) -> None:
    symbol = exp.symbol
    store = InMemoryMarketStore(symbols=(symbol,))

    # Build independent features
    price_source = exp.price_source(store, symbol)
    features = {}

    for key, feature_specs in exp.features.items():
        feature = feature_specs.feature(
            price_source,
            **feature_specs.params
        )
        features[key] = feature

    # Validate requirements against features
    requirements = exp.strategy_specs.type.requirements

    for name, expected_type in requirements.items():
        if name not in features:
            raise ValueError(
                f"Expected Feature: {name}"
                f"but is not available in Experiment.\n"
                f"Requirements={requirements.keys()}"
                f"Available={features.keys()}."
            )

        feature = features[name]

        if not isinstance(feature, expected_type):
            raise ValueError(
                f"Invalid type for feature : {name}."
                f"Expected={expected_type}, got {type(feature)}."
            )

    # Build graph
    graph = FeatureGraph(
        root=FeatureNode(type=),
    )

    for feature in features.values():
        print(f"Feature: {feature}")

        source = feature.__dict__.get("_source")
        print(f"Sources: {source}")
        source.__dict__.get("_successors").append(feature)
        graph.add_node(feature)

    print(graph)


if __name__ == "__main__":
    bootstrap(experiment)

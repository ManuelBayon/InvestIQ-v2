from investiq.domain.market_store import InMemoryMarketStore
from investiq.features.feature_runtime import FeatureRuntime, FeatureGraph
from investiq.features.features import Feature, PriceSource
from tests.fixtures.features.fake_feature import FakeFeature
from tests.fixtures.market.simple_trades import MONO_SYMBOL_SIMPLE_TRADES


def print_successors(feature: Feature) -> None:
    print(
        f"Feature {feature.name} "
        f"successors are {
            [s.__dict__.get("name") for s in feature.successors]
        }"
    )

def bootstrap_feature_graph(
        root_key: str,
        root_value: Feature,
        features: list[Feature]
) -> FeatureGraph:

    if any(feature is root_value for feature in features):
        raise ValueError("root must not be passed as feature")

    _graph = FeatureGraph(
        root_key=root_key,
        root_value=root_value,
    )

    for feature in features:
        sources = feature.__dict__.get("_sources")
        for s in sources:
            s.__dict__.get("_successors").append(feature)
        _graph.add_node(feature)

    return _graph


if __name__ == "__main__":

    universe = ("SYMBOL_1","SYMBOL_2")
    store = InMemoryMarketStore(universe)

    # Bootstrap symbol 1 feature graph
    price_s1 = PriceSource(source=store, symbol="SYMBOL_1")
    A = FakeFeature(name="A", emissions=[False, True, True, True], sources=[price_s1])
    B = FakeFeature(name="B", emissions=[False, True, True], sources=[A])
    C = FakeFeature(name="C", emissions=[False, True, True], sources=[A])
    D = FakeFeature(name="D", emissions=[False, True], sources=[B])
    E = FakeFeature(name="E", emissions=[False, True], sources=[A, C])
    F = FakeFeature(name="F", emissions=[True], sources=[D, E])

    graph_s1 = bootstrap_feature_graph(
        root_key="SYMBOL_1",
        root_value=A,
        features=[B, C, D, E, F])

    print("Feature graph for SYMBOL_1 :")
    for node in graph_s1.nodes:
        print_successors(node)

    # Bootstrap symbol 2 feature graph
    price_s2 = PriceSource(source=store, symbol="SYMBOL_2")
    A = FakeFeature(name="A", emissions=[False, True, True], sources=[price_s2])
    F = FakeFeature(name="F", emissions=[False, True], sources=[A])
    G = FakeFeature(name="G", emissions=[True], sources=[A])
    C = FakeFeature(name="C", emissions=[True], sources=[F])

    graph_s2 = bootstrap_feature_graph(
        root_key="SYMBOL_2",
        root_value=A,
        features=[F, G, C])

    print("\nFeature graph for SYMBOL_2 :")
    for node in graph_s2.nodes:
        print_successors(node)

    runtime = FeatureRuntime(
        graph={
            graph_s1.root_symbol: graph_s1,
            graph_s2.root_symbol: graph_s2
        }
    )

    runtime.on_trade_received(MONO_SYMBOL_SIMPLE_TRADES[0])
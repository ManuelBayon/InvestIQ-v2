from investiq.domain.market_store import InMemoryMarketStore
from investiq.features.feature_graph import Node, NodeKind
from investiq.features.features import Feature, PriceSource, Source
from tests.fixtures.features.fake_feature import FakeFeature


def bootstrap_feature_graph(
        sources: list[Source],
        features: list[Feature]
) -> None:

    all_nodes: list[Node] = []

    # Initialize sources nodes
    for source in sources:
        node = Node(
            kind=NodeKind.SOURCE,
            payload=source,
            parents=[],
            successors=[]
        )
        all_nodes.append(node)

    # Initialize compute nodes
    for feature in features:
        node = Node(
            kind=NodeKind.COMPUTE,
            payload=feature,
            parents=[],
            successors=[]
        )
        all_nodes.append(node)

    # Add parents to all nodes (except sources)
    for node in all_nodes:
        if node.kind == NodeKind.SOURCE:
            continue

        sources = node.payload.sources
        for source in sources:
            found = [n for n in all_nodes if n.payload is source]

            if len(found)  == 0:
                raise ValueError(f"Did not found node for node={node} and source={source}.")
            if len(found)  > 1:
                raise ValueError(f"Did found multiple corresponding nodes for node={node} and source={source}.")

            node.parents.append(found[0])

    # Add successors to all nodes
    for node in all_nodes:
        if node.kind is NodeKind.SOURCE:
            continue

        for parent in node.parents:
            parent.successors.append(node)

    for n in all_nodes:
        print(n)


if __name__ == "__main__":

    universe = ("SYMBOL_1",)
    store = InMemoryMarketStore(universe)

    # Bootstrap symbol 1 feature graph
    price_source = PriceSource(source=store, symbol="SYMBOL_1", name="PriceSource")
    A = FakeFeature(name="A", emissions=[], sources=[price_source])
    B = FakeFeature(name="B", emissions=[], sources=[A])
    C = FakeFeature(name="C", emissions=[], sources=[A])
    D = FakeFeature(name="D", emissions=[], sources=[B, C])

    bootstrap_feature_graph(
        sources=[price_source],
        features=[A, B, C, D]
    )
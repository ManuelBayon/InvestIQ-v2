from investiq.features.feature_graph import Node, NodeKind, FeatureGraph
from investiq.features.feature_runtime import FeatureRuntime
from investiq.features.features import Feature, Source


def bootstrap_feature_runtime(
        sources: list[Source],
        features: list[Feature]
) -> FeatureRuntime:

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

        source = node.payload.source
        found = [n for n in all_nodes if n.payload is source]
        if len(found)  == 0:
            raise ValueError(
                f"\nDid not found a node which has for source: \n{source}."
                f"\nAvailable nodes={all_nodes}."
            )
        if len(found)  > 1:
            raise ValueError(f"Did found multiple nodes for source={source}.")

        node.parents.append(found[0])

    # Add successors to all nodes
    for node in all_nodes:
        if node.kind is NodeKind.SOURCE:
            continue

        for parent in node.parents:
            parent.successors.append(node)

    input_nodes = [n for n in all_nodes if n.kind == NodeKind.SOURCE]
    compute_nodes = [n for n in all_nodes if n.kind == NodeKind.COMPUTE]

    _graph = FeatureGraph(
        input_nodes=input_nodes,
        compute_nodes=compute_nodes
    )
    return FeatureRuntime(graph=_graph)
from collections.abc import Mapping, Sequence
from dataclasses import dataclass

from investiq.domain.features.features import FeatureSpec, Feature
from investiq.errors import MissingFeatureRequirementError, FeatureTypeMismatchError
from investiq.domain.features.feature_graph import Node, NodeKind, FeatureGraph
from investiq.domain.features.feature_runtime import FeatureRuntime

from investiq.domain.features.sources import Source
from investiq.domain.strategies.base_strategy import StrategySpec, FeatureRequirement


@dataclass(frozen=True, slots=True)
class ExperimentSpec:
    """
    2026-08-19: Work hypothesis : Mono symbol experiment
    """
    symbol: str
    features: Mapping[str, FeatureSpec]
    strategy: StrategySpec


def build_features(source: Source, features: Mapping[str, FeatureSpec]) -> Mapping[str, Feature]:
    _features_by_name: dict[str, Feature] = {}

    for name, feature_spec in features.items():
        feature = feature_spec.feature_type(
            source,
            **feature_spec.params
        )
        _features_by_name[name] = feature

    return _features_by_name


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
from dataclasses import dataclass, field
from enum import StrEnum, auto

from investiq.features.features import Feature, Source


class NodeKind(StrEnum):
    SOURCE = "SOURCE"
    COMPUTE = "COMPUTE"


@dataclass
class Node:
    kind: NodeKind
    payload: Feature | Source
    parents: list["Node"]
    successors: list["Node"]

    def __repr__(self) -> str:
        return (
            f"\n{self.kind} NODE"
            f"\npayload = {self.payload.name}"
            f"\nparents = {[p.payload.name for p in self.parents]}"
            f"\nsuccessors = {[s.payload.name for s in self.successors]}"
        )


class FeatureGraph:

    def __init__(self):
        self._nodes: dict[Feature, Node] = {}


    def add_node(self, feature: Feature, node: Node) -> None:
        self._nodes[feature] = node


    def get_node(self, feature: Feature) -> Node:
        return self._nodes[feature]
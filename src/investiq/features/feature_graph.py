from dataclasses import dataclass, field
from enum import StrEnum, auto

from investiq.features.features import Feature, Source


class NodeKind(StrEnum):
    SOURCE = "SOURCE"
    COMPUTE = "COMPUTE"


@dataclass(eq=False)
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

    def __init__(
            self,
            input_nodes: list[Node],
            compute_nodes: list[Node]
    ):
        self._input_nodes: list[Node] = input_nodes
        self._compute_nodes: list[Node] = compute_nodes

    def input_nodes(self) -> list[Node]:
        return self._input_nodes
from collections.abc import Mapping
from dataclasses import dataclass
from typing import Protocol, Sequence, ClassVar

from investiq.domain.features.features import Feature
from investiq.domain.orders import OrderSpec


@dataclass
class DecisionContext:
    price : float
    features: Mapping[str, float]


@dataclass(frozen=True)
class FeatureRequirement:
    name: str
    feature_type: type[Feature]

class Strategy(Protocol):
    requirements: ClassVar[Sequence[FeatureRequirement]]
    def decide(
            self,
            context: DecisionContext,
    ) -> list[OrderSpec]:
        ...
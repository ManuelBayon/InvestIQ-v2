from collections.abc import Mapping
from dataclasses import dataclass
from typing import Protocol, Sequence, ClassVar

from investiq.domain.features.features import Feature


@dataclass
class DecisionContext:
    symbol: str
    price : float
    features: Mapping[str, float]


@dataclass
class TradingIntent:
    symbol: str
    target: float

@dataclass(frozen=True)
class FeatureRequirement:
    name: str
    feature_type: type[Feature]

class Strategy(Protocol):
    requirements: ClassVar[Sequence[FeatureRequirement]]
    def decide(
            self,
            context: DecisionContext,
    ) -> list[TradingIntent]:
        ...


@dataclass
class StrategySpec:
    strategy_type: type[Strategy]
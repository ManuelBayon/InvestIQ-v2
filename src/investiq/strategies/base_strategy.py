from dataclasses import dataclass
from typing import Protocol, ClassVar

from investiq.features.features import FeatureSpecs


@dataclass
class DecisionContext:
    symbol: str
    price: float
    features: dict[str, float]


@dataclass
class TradingIntent:
    symbol: str
    target: float


class Strategy(Protocol):
    requirements: ClassVar[dict[str, FeatureSpecs]]
    def decide(
            self,
            context: DecisionContext,
    ) -> list[TradingIntent]:
        ...


@dataclass
class StrategySpecs:
    type: type[Strategy]
    params: dict[str, object]
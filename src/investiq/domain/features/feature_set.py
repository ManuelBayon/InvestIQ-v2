from dataclasses import dataclass
from typing import Mapping

from investiq.domain.features.protocol import Feature


@dataclass(frozen=True)
class FeatureSet:
    symbol: str
    features: Mapping[str, Feature]
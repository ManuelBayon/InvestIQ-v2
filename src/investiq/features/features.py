from dataclasses import dataclass
from typing import Protocol, Callable, runtime_checkable
from collections.abc import Sequence, Mapping

from investiq.features.sources import Source

@runtime_checkable
class Feature(Protocol):
    @property
    def source(self) -> Source:...
    def compute(self) -> bool:
        """
        True  : a new observation has been produced.
        False : No new observation.
        """
        ...
    def load(self, window: int) -> Sequence[float]:
        ...
    def latest(self) -> float:...

@dataclass
class SourceSpec:
    source_type: Callable[..., Source]
    dependencies: dict[str, object]
    params: dict[str, object]


@dataclass
class FeatureSpec:
    feature_type: Callable[..., Feature]
    params: Mapping[str, object]


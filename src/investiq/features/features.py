from dataclasses import dataclass
from typing import Protocol, runtime_checkable, Callable
from collections.abc import Sequence

from investiq.domain.market_store import InMemoryMarketStore

@runtime_checkable
class Source(Protocol):
    """
    Source should raise InsufficientHistory error if
    not enough data is available.
    """
    def load(self, window: int) -> Sequence[float]:
        ...


class PriceSource:
    def __init__(
            self,
            source: InMemoryMarketStore,
            symbol: str,
            name: str,
    ):
        self._source = source
        self._symbol = symbol
        self.name = name

    def load(self, window: int) -> Sequence[float]:
        return self._source.price_window(self._symbol, window)

    def __repr__(self) -> str:
        return (
            f"PriceSource(source={self._source}, symbol={self._symbol})"
        )


@runtime_checkable
class Feature(Protocol):
    sources: Sequence[Source]
    def compute(self) -> bool:
        """
        True  : a new observation has been produced.
        False : No new observation.
        """
        ...

    def load(self, window: int) -> Sequence[float]:
        ...

@dataclass
class SourceSpecs:
    source: type[Source]

@dataclass
class FeatureSpecs:
    feature: Callable[..., Feature]
    sources: list["Source | FeatureSpecs"]
    params: dict[str, object]
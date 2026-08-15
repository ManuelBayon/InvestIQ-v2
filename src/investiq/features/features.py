from dataclasses import dataclass
from typing import Protocol, runtime_checkable
from collections.abc import Sequence

from investiq.domain.market_store import InMemoryMarketStore


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
            symbol: str
    ):
        self._source = source
        self._symbol = symbol

    def load(self, window: int) -> Sequence[float]:
        return self._source.price_window(self._symbol, window)


@runtime_checkable
class Feature(Protocol):
    def compute(self) -> bool:
        """
        True  : a new observation has been produced.
        False : No new observation.
        """
        ...

    def load(self, window: int) -> Sequence[float]:
        ...


@dataclass
class FeatureSpecs:
    type: type[Feature]
    sources: list[str]
    params: dict[str, str]

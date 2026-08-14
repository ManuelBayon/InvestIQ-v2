from typing import Protocol, runtime_checkable
from collections.abc import Sequence

from investiq.domain.market_store import InMemoryMarketStore


class Source(Protocol):
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

    @property
    def successors(self) -> list["Feature"]:...
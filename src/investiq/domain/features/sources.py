from typing import runtime_checkable, Protocol, Sequence

from investiq.domain.market_store import InMemoryMarketStore


@runtime_checkable
class Source(Protocol):
    """
    Source should raise InsufficientHistory error if
    not enough data is available.
    """
    def load(self, window: int) -> Sequence[float]:...
    def last(self) -> float:...


class PriceSource:
    def __init__(
            self,
            source: InMemoryMarketStore,
            symbol: str,
    ):
        self._source = source
        self._symbol = symbol

    def last(self) -> float:
        return self._source.price_window(self._symbol, 1)[0]

    def load(self, window: int) -> Sequence[float]:
        return self._source.price_window(self._symbol, window)

    def __repr__(self) -> str:
        return (
            f"PriceSource(source={self._source}, symbol={self._symbol})"
        )
from math import log
from typing import Protocol

from investiq.domain.market_store import InMemoryMarketStore
from tests.fixtures.market.simple import SIMPLE_TRADES


class Source(Protocol):
    _source: object
    def load(self, window: int) -> object:
        ...

class PriceSource:
    def __init__(self, market_store: InMemoryMarketStore):
        self._source = market_store
    def load(self, window: int) -> list[float]:
        if self._source.has_at_least("TEST_SYMBOL", window):
            return self._source.price_window("TEST_SYMBOL", window)
        else:
            return []

class Feature(Protocol):
    _sources: list[Source]
    _history: list[object]
    def compute(self) -> None:
        ...

class Returns1:
    def __init__(self, price_source: PriceSource):
        self._sources = [price_source]
        self._history: list[float] = []

    def compute(self) -> None:
        prices = self._sources[0].load(2)
        if len(prices) == 2:
            result = log(prices[-1] / prices[-2])
            self._history.append(result)

    def get(self) -> list[float]:
        return self._history


if __name__ == "__main__":
    store = InMemoryMarketStore()
    priceSource = PriceSource(store)
    returns1 = Returns1(priceSource)

    trade_0 = SIMPLE_TRADES[0]
    trade_1  =SIMPLE_TRADES[1]

    store.on_trade_received(trade_0)
    returns1.compute()
    print(returns1.get())

    store.on_trade_received(trade_1)
    returns1.compute()
    print(returns1.get())

from math import log
from statistics import stdev
from typing import Protocol

from investiq.domain.market_store import InMemoryMarketStore

from tests.fixtures.market.simple import SIMPLE_TRADES

class Feature(Protocol):
    window_size: int
    def compute(self, window: tuple[float, ...]) -> float:
        ...

class Returns1:
    window_size = 2
    def compute(self, window: tuple[float, ...]) -> float:
        price = window[-1]
        last_price = window[-2]
        return log(price / last_price)

class Vol3:
    window_size = 3
    def compute(self, window: tuple[float, ...]) -> float:
        if len(window) != 3:
            raise ValueError(f"len(window)={len(window)} != 3.")
        return stdev(window)


class FeatureEngine:
    def __init__(
            self,
            pipelines: list[Feature],
            store: InMemoryMarketStore,
    ):
        self._pipelines = pipelines
        self._market_store = store
        self._features: dict[str, float] = {}

    def update(self):
        for p in self._pipelines:
            if self._market_store.has_at_least("TEST_SYMBOL", p.window_size):
                view = self._market_store.window("TEST_SYMBOL", p.window_size)
                r = p.compute(window=view)
                self._features["TEST_SYMBOL"] = r

    def get(self, symbol: str) -> float:
        if symbol not in self._features:
            raise KeyError(f"unknown symbol={symbol}")
        return self._features["TEST_SYMBOL"]

if __name__ == "__main__":
    trade_0 = SIMPLE_TRADES[0]
    trade_1 = SIMPLE_TRADES[1]
    trade_2 = SIMPLE_TRADES[2]

    market_store = InMemoryMarketStore()
    feature_engine = FeatureEngine(
        pipelines=[Returns1(), Vol3()],
        store=market_store
    )

    market_store.on_trade_received(trade_0)
    feature_engine.update()

    market_store.on_trade_received(trade_1)
    feature_engine.update()
    result = feature_engine.get("TEST_SYMBOL")
    print(result)

    market_store.on_trade_received(trade_2)
    feature_engine.update()
    result = feature_engine.get("TEST_SYMBOL")
    print(result)



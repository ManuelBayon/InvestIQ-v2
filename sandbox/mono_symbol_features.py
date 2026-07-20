from math import log
from statistics import stdev
from typing import Protocol

from investiq.domain.market_store import InMemoryMarketStore
from tests.fixtures.market.simple import SIMPLE_TRADES


class Source(Protocol):
    _source: object
    def load(self, window: int) -> object:
        ...


class PriceSource:
    def __init__(self, source: InMemoryMarketStore):
        self._source = source
    def load(self, window: int) -> list[float]:
        if self._source.has_at_least("TEST_SYMBOL", window):
            return self._source.price_window("TEST_SYMBOL", window)
        else:
            return []


class Returns1Source:
    def __init__(self, source: "Returns1"):
        self._source = source
    def load(self, window: int) -> list[float]:
        if len(self._source) >= window:
            return self._source.get(window)
        else:
            return []


class VolatilitySource:
    def __init__(self, source: "Volatility"):
        self._source = source
    def load(self, window: int) -> list[float]:
        if len(self._source) >= window:
            return self._source.get(window)
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

    def get(self, window: int = 1) -> list[float]:
        return self._history[-window:]

    def __len__(self):
        return len(self._history)


class Volatility:
    def __init__(self, source: Returns1Source, n: int):
        self._sources = [source]
        self._n = n
        self._history: list[float] = []

    def compute(self) -> None:
        series = self._sources[0].load(self._n)
        if len(series) == self._n:
            result = stdev(series)
            self._history.append(result)

    def get(self, window: int = 1) -> list[float]:
        return self._history[-window:]

    def __len__(self):
        return len(self._history)


class ZScore:
    def __init__(self, source: VolatilitySource, n: int):
        self._sources = [source]
        self._n = n
        self._history: list[float] = []

    def compute(self) -> None:
        series = self._sources[0].load(self._n)
        if len(series) == self._n:
            result = stdev(series)
            self._history.append(result)

    def get(self, window: int = 1) -> list[float]:
        return self._history[-window:]

    def __len__(self):
        return len(self._history)


if __name__ == "__main__":
    store = InMemoryMarketStore()
    priceSource = PriceSource(source=store)
    returns1 = Returns1(priceSource)
    returns1Source = Returns1Source(source=returns1)
    volatility3 = Volatility(source=returns1Source, n=3)
    volatilitySource = VolatilitySource(volatility3)
    zscore = ZScore(source=volatilitySource, n=3)

    trade_0 = SIMPLE_TRADES[0]
    trade_1 = SIMPLE_TRADES[1]
    trade_2 = SIMPLE_TRADES[2]
    trade_3 = SIMPLE_TRADES[3]
    trade_4 = SIMPLE_TRADES[4]
    trade_5 = SIMPLE_TRADES[5]

    store.on_trade_received(trade_0)
    returns1.compute()
    volatility3.compute()
    zscore.compute()
    print(f"New step :")
    print(f"returns1={returns1.get()}")
    print(f"volatility3={volatility3.get()}")
    print(f"zscore={zscore.get()}")

    store.on_trade_received(trade_1)
    returns1.compute()
    volatility3.compute()
    zscore.compute()
    print(f"\nNew step :")
    print(f"returns1={returns1.get()}")
    print(f"volatility3={volatility3.get()}")
    print(f"zscore={zscore.get()}")

    store.on_trade_received(trade_2)
    returns1.compute()
    volatility3.compute()
    zscore.compute()
    print(f"\nNew step :")
    print(f"returns1={returns1.get()}")
    print(f"volatility3={volatility3.get()}")
    print(f"zscore={zscore.get()}")

    store.on_trade_received(trade_3)
    returns1.compute()
    volatility3.compute()
    zscore.compute()
    print(f"\nNew step :")
    print(f"returns1={returns1.get()}")
    print(f"volatility3={volatility3.get()}")
    print(f"zscore={zscore.get()}")

    store.on_trade_received(trade_4)
    returns1.compute()
    volatility3.compute()
    zscore.compute()
    print(f"\nNew step :")
    print(f"returns1={returns1.get()}")
    print(f"volatility3={volatility3.get()}")
    print(f"zscore={zscore.get()}")

    store.on_trade_received(trade_5)
    returns1.compute()
    volatility3.compute()
    zscore.compute()
    print(f"\nNew step :")
    print(f"returns1={returns1.get()}")
    print(f"volatility3={volatility3.get()}")
    print(f"zscore={zscore.get()}")
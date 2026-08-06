from collections.abc import Sequence
from math import log
from statistics import stdev, mean
from typing import Protocol
from investiq.domain.market_store import InMemoryMarketStore
from investiq.errors import InsufficientHistoryError
from investiq.events.trade_received import TradeReceived
from tests.fixtures.market.simple import SIMPLE_TRADES

class Source(Protocol):
    def load(self, n: int) -> Sequence[float]:...


class PriceSource:
    def __init__(self, source: InMemoryMarketStore, symbol: str):
        self._source = source
        self._symbol = symbol

    def load(self, n: int) -> list[float]:
        return self._source.price_window(self._symbol, n)


class FeatureSource:
    def __init__(self, source: "Feature"):
        self._source = source

    def load(self, n: int) -> Sequence[float]:
        return self._source.window(n)


class Feature(Protocol):
    def compute(self) -> None:...
    def window(self, n: int) -> Sequence[float]:...


class Returns1:
    def __init__(self, source: Source):
        self._price_source = source
        self._history: list[float] = []
        self._is_ready: bool = False

    def compute(self) -> None:
        try:
            series = self._price_source.load(n=2)
        except InsufficientHistoryError:
            return

        result = log(series[-1] / series[-2])
        self._history.append(result)
        self._is_ready = True

    def window(self, n: int) -> list[float]:
        if n < 1:
            raise ValueError(f"n must be positive, got n={n}")

        size = len(self._history)
        if size < n:
            raise InsufficientHistoryError(f"requested={n}, available={size}")

        return self._history[-n:]


class Volatility:
    def __init__(self, source: Source, n: int):
        self._return_source = source
        self._n = n
        self._history: list[float] = []
        self._is_ready : bool = False

    def compute(self) -> None:
        try:
            series = self._return_source.load(self._n)
        except InsufficientHistoryError:
            return

        result = stdev(series)
        self._history.append(result)
        self._is_ready = True

    def window(self, n: int) -> list[float]:
        if n < 1:
            raise ValueError(f"n must be positive, got n={n}")

        size = len(self._history)
        if size < n:
            raise InsufficientHistoryError(f"requested={n}, available={size}")

        return self._history[-n:]


class ZScore:

    def __init__(self, source: Source, n: int):
        self._volatility_source = source
        self._n = n
        self._history: list[float] = []
        self._is_ready: bool = False

    def compute(self) -> None:
        try:
            series = self._volatility_source.load(self._n)
        except InsufficientHistoryError:
            return

        value = series[-1]
        m = mean(series)
        sigma = stdev(series)

        if sigma == 0.0:
            raise ValueError("z_score is undefined when standard deviation is zero.")

        result = (value - m) / sigma
        self._history.append (result)
        self._is_ready = True

    def window(self, n: int) -> list[float]:
        if n < 1:
            raise ValueError(f"n must be positive, got n={n}")

        size = len(self._history)
        if size < n:
            raise InsufficientHistoryError(f"requested={n}, available={size}")

        return self._history[-n:]


def on_trade_received(trade: TradeReceived) -> None:
    store.on_trade_received(trade)
    returns1.compute()
    volatility3.compute()
    zscore3.compute()

def print_state(
        ret: Returns1,
        vol: Volatility,
        zs: ZScore
) -> None:
    print(ret.window(1))
    print(vol.window(1))
    print(zs.window(1))


if __name__ == "__main__":
    store = InMemoryMarketStore()
    priceSource = PriceSource(source=store, symbol="TEST_SYMBOL")
    returns1 = Returns1(priceSource)
    returns1Source = FeatureSource(source=returns1)
    volatility3 = Volatility(source=returns1Source, n=3)
    volatilitySource = FeatureSource(volatility3)
    zscore3 = ZScore(source=volatilitySource, n=3)

    trade_0 = SIMPLE_TRADES[0]
    trade_1 = SIMPLE_TRADES[1]
    trade_2 = SIMPLE_TRADES[2]
    trade_3 = SIMPLE_TRADES[3]
    trade_4 = SIMPLE_TRADES[4]
    trade_5 = SIMPLE_TRADES[5]
    trades = [trade_0, trade_1, trade_2, trade_3, trade_4, trade_5]

    on_trade_received(trade_0)
    on_trade_received(trade_1)
    on_trade_received(trade_2)
    on_trade_received(trade_3)
    on_trade_received(trade_4)
    on_trade_received(trade_5)

    print(f"Prices: {[float(t.price) for t in trades]}")
    print(f"Returns1: {returns1._history}")
    print(f"Volatility 3: {volatility3._history}")
    print(f"ZScore 3: {zscore3._history}")
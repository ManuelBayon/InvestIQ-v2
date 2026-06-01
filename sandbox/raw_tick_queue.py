from sandbox.tick_aggregation import FakeTickData, FakeTicker


class FakeRawMarketDataQueue:

    def __init__(self):
        self._queue: dict[str, list[FakeTickData]] = {}

    def push(self, tickers: list[FakeTicker]) -> None:
        for t in tickers:
            _symbol = t.symbol
            if _symbol not in self._queue.keys():
                self._queue[_symbol] = t.ticks
            else:
                self._queue[_symbol].extend(t.ticks)
        print(self._queue)

    def pull(
            self,
            symbol: str,
            tick_type: int
    ) -> list[FakeTickData]:
        result = [item for item in self._queue[symbol] if item.tickType == tick_type]
        return result
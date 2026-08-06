from investiq.errors import InsufficientHistoryError
from investiq.events.trade_received import TradeReceived
from tests.fixtures.market.simple import SIMPLE_TRADES


class InMemoryMarketStore:
    """
    In memory trade store.

    TradeReceived events are supposed to be ordered by timestamp for each symbol.
    TradeReceived are stored by symbol.
    """

    def __init__(self):
        self._trades: dict[str, list[TradeReceived]] = {}


    def on_trade_received(self, event: TradeReceived) -> None:
        symbol = event.symbol
        if symbol in self._trades:
            last = self._trades[event.symbol][-1]

            if event.timestamp_utc < last.timestamp_utc:
                raise ValueError(
                    f"event.timestamp_utc={event.timestamp_utc} < last.timestamp_utc={last.timestamp_utc}"
                )

        self._trades.setdefault(symbol, []).append(event)


    def price_window(self, symbol: str, n: int) -> list[float]:
        if n < 1:
            raise ValueError(f"n must be positive, got n={n}")

        if symbol not in self._trades:
            raise KeyError(
                f"Unknown symbol={symbol}, registered symbols={[s for s in self._trades]}"
            )

        available_size  = len(self._trades[symbol])
        if available_size < n:
            raise InsufficientHistoryError(f"asked={n}, available={available_size}")

        return [float(trade.price) for trade in self._trades[symbol][-n:]]


    def size(self, symbol) -> int:
        return len(self._trades[symbol])


if __name__ == "__main__":
    store = InMemoryMarketStore()
    trade_0 = SIMPLE_TRADES[0]

    store.on_trade_received(trade_0)
    result = store.price_window("TEST_SYMBOL", 1)
    print(result)

from investiq.core.events import TradeReceived
from investiq.errors import InsufficientHistoryError, UnknownSymbolError
from tests.fixtures.market.simple_trades import MONO_SYMBOL_SIMPLE_TRADES


class InMemoryMarketStore:
    """
    In memory trade store.

    TradeReceived events are supposed to be ordered by timestamp for each symbol.
    TradeReceived are stored by symbol.
    """

    def __init__(self, symbol: str):

        self._trades: dict[str, list[TradeReceived]] = {symbol : []}
        self._universe = symbol

    def on_trade_received(self, trade: TradeReceived) -> None:
        try:
            history = self._trades[trade.symbol]
        except KeyError as exc:
            raise UnknownSymbolError(
                f"symbol={trade.symbol} "
                f"is outside the configured universe={self._universe}."
            ) from exc
        history.append(trade)


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


    def last(self, symbol: str) -> float:
        return self.price_window(symbol=symbol, n=1)[0]


    def size(self, symbol) -> int:
        return len(self._trades[symbol])


if __name__ == "__main__":
    store = InMemoryMarketStore("SYMBOL_1")
    trade_0 = MONO_SYMBOL_SIMPLE_TRADES[0]

    store.on_trade_received(trade_0)
    result = store.price_window("SYMBOL_1", 1)
    print(result)

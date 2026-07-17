from collections.abc import Mapping
from dataclasses import dataclass
from decimal import Decimal

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

    def window(self, symbol: str, size: int) -> tuple[float, ...]:
        window = self._trades[symbol][-size:]
        return tuple(float(p.price) for p in window)

    def has_at_least(self, symbol: str, size: int) -> bool:
        if size <= 0:
            raise ValueError(f"size must be positive, got size={size}.")
        if symbol not in self._trades:
            raise KeyError(f"symbol={symbol} not found in self._trades")
        if len(self._trades[symbol]) >= size:
            return True
        else:
            return False


if __name__ == "__main__":
    store = InMemoryMarketStore()
    trade_0 = SIMPLE_TRADES[0]

    store.on_trade_received(trade_0)
    print(store.has_at_least(symbol="TEST_SYMBOL", size=2))

from collections.abc import Mapping
from dataclasses import dataclass
from decimal import Decimal

from investiq.events.trade_received import TradeReceived

@dataclass(frozen=True)
class LatestTradeSnapshot:
    latest: Mapping[str, Decimal]


class InMemoryMarketStore:
    """
    In memory trade store.

    TradeReceived events are supposed to be ordered by timestamp for each symbol.
    """

    def __init__(self):
        self._trades_by_symbol: dict[str, list[TradeReceived]] = {}


    def on_trade_received(self, event: TradeReceived) -> None:
        symbol = event.symbol

        if symbol in self._trades_by_symbol:
            last = self._trades_by_symbol[event.symbol][-1]

            if event.timestamp_utc < last.timestamp_utc:
                raise ValueError(
                    f"timestamp_utc for symbol={event.symbol}, "
                    f"is decreasing."
                )

        self._trades_by_symbol.setdefault(symbol, []).append(event)

    def has_at_least(self, symbol: str, n: int) -> bool:
        if n <= 0:
            raise ValueError(f"window_size must be > 0, got {n}")
        return len(self._trades_by_symbol.get(symbol, ())) >= n

    def window(self, symbol: str, n: int) -> tuple[TradeReceived, ...]:
        events = self._trades_by_symbol.get(symbol)
        if events is None:
            raise KeyError(
                f"Unknown symbol={symbol}. "
                f"Available symbols={self._trades_by_symbol.keys()}"
            )
        if n <= 0:
            raise ValueError(f"window must be > 0, got window={n}")
        if len(events) < n:
            raise ValueError(
                f"Insufficient data for symbol={symbol}, "
                f"required={n}, available={len(events)}."
            )
        return tuple(events[-n:])


    def latest(self, symbol: str) -> Decimal:
        return self.window(symbol, 1)[0].price


    @property
    def symbols(self) -> tuple[str, ...]:
        return tuple(self._trades_by_symbol)
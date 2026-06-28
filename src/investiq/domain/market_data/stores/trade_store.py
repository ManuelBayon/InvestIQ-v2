from investiq.events.market_data import TradeReceived

class TradeStore:
    """
    """
    def __init__(self):
        self._events: list[TradeReceived] = []

    def ingest(self, trade: TradeReceived) -> None:
        self._events.append(trade)

    def all(self) -> tuple[TradeReceived, ...]:
        return tuple(self._events)

    def available_symbols(self) -> set[str]:
        return set(e.symbol for e in self._events)

    def window_by_symbol(self, symbol: str, n: int) -> tuple[TradeReceived, ...]:
        if n <= 0:
            raise ValueError(f"window_size must be > 0, got {n}")

        _available_symbols = self.available_symbols()
        if symbol not in _available_symbols:
            raise KeyError(
                f"Unrecognized symbol, available symbols: {_available_symbols}"
            )
        events = [e for e in self.all() if e.symbol == symbol]
        return tuple(events[-n:])

    def has_at_least(self, symbol: str, n: int) -> bool:
        if n <= 0:
            raise ValueError(f"window_size must be > 0, got {n}")

        quantity = sum(1 for e in self._events if e.symbol == symbol)
        return quantity >= n
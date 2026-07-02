from investiq.domain.market_data.contracts.store import MarketStore
from investiq.events.market_data import TradeReceived

class InMemoryTradeStore:
    """
    In memory trade store.
    """

    def __init__(self):
        self._events: list[TradeReceived] = []
        self._by_symbol: dict[str, list[TradeReceived]] = {}


    def append(self, event: TradeReceived) -> None:
        if not isinstance(event, TradeReceived):
            raise ValueError(
                f"event must be of type TradeReceived, got type(event)={type(event)}"
            )

        _symbol = event.symbol
        if _symbol not in self._by_symbol:
            self._by_symbol[_symbol] = []

        self._events.append(event)
        self._by_symbol[_symbol].append(event)

    @property
    def symbols(self) -> set[str]:
        return set(e.symbol for e in self._events)


    def _all(self) -> tuple[TradeReceived, ...]:
        return tuple(self._events)


    def window(self, symbol: str, n: int) -> tuple[TradeReceived, ...]:
        if n <= 0:
            raise ValueError(f"window_size must be > 0, got {n}")

        _symbols = self.symbols
        if symbol not in _symbols:
            raise KeyError(
                f"Unrecognized symbol, available symbols: {_symbols}"
            )
        events = [e for e in self._all() if e.symbol == symbol]

        return tuple(events[-n:])


    def has_at_least(self, symbol: str, n: int) -> bool:
        if n <= 0:
            raise ValueError(f"window_size must be > 0, got {n}")

        quantity = sum(1 for e in self._events if e.symbol == symbol)
        return quantity >= n


if __name__ == "__main__":
    store = InMemoryTradeStore()
    print(isinstance(store, MarketStore))
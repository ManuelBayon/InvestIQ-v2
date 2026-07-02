from investiq.events.events import MarketDataEvent
from investiq.events.market_data import TradeReceived

class InMemoryTradeStore:
    """
    In memory trade store.
    """

    def __init__(self):
        self._by_symbol: dict[str, list[TradeReceived]] = {}
        self._symbols: set[str] = set()


    def ingest(self, event: MarketDataEvent) -> None:
        if not isinstance(event, TradeReceived):
            return

        symbol = event.symbol
        if symbol not in self._by_symbol:
            self._by_symbol.setdefault(symbol, [])
            self._symbols.add(symbol)

        self._by_symbol[symbol].append(event)


    @property
    def symbols(self) -> tuple[str, ...]:
        return tuple(self._symbols)

    def has_at_least(self, symbol: str, n: int) -> bool:
        if n <= 0:
            raise ValueError(f"window_size must be > 0, got {n}")
        return len(self._by_symbol.get(symbol, ())) >= n


    def window(self, symbol: str, n: int) -> tuple[MarketDataEvent, ...]:
        events = self._by_symbol.get(symbol)
        if events is None:
            raise KeyError(f"Unknown symbol={symbol}")
        if len(events) < n:
            raise ValueError(
                f"Insufficient data for symbol={symbol}, required={n}, available={len(events)}"
            )
        return tuple(events[-n:])
from typing import Protocol

from investiq.domain.market_data.stores.trade_store import TradeStore
from investiq.events.market_data import TradeReceived


class MarketDataReader(Protocol):
    def trades(self, symbol: str, n: int) -> tuple[TradeReceived, ...]:...
    def available_symbols(self) -> set[str]:...
    def has_at_least(self, symbol: str, n: int) -> bool:...


class InMemoryMarketDataReader:
    """
    In-memory read-only façade over market data projections.

    Current dependencies:
        - TradeStore,

    Future extensions may include:
        - QuoteStore (L1 bid/ask)
        - OrderBookStore (DOM/L2)
        - GreekStore (options greeks)
        - BarStore (OHLCV bars)

    Feature pipelines should depend on this reader rather than on
    individual stores.
    """

    def __init__(
            self,
            *,
            trade_store: TradeStore,
    ):
        self._trade_store = trade_store

    def trades(self, symbol: str, n: int) -> tuple[TradeReceived, ...]:
        return self._trade_store.window_by_symbol(symbol, n)

    def available_trade_symbols(self) -> set[str]:
        return self._trade_store.available_symbols()

    def has_at_least_n_trades(self, symbol: str, n: int) -> bool:
        return self._trade_store.has_at_least(symbol, n)
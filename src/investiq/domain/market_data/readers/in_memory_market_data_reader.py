from investiq.domain.market_data.contracts.reader import MarketStoreReader
from investiq.domain.market_data.contracts.store import MarketStore
from investiq.domain.market_data.stores.in_memory.trade_store import InMemoryTradeStore
from investiq.events.market_data import TradeReceived

class InMemoryMarketDataReader:
    """
    In-memory read-only façade over market market_data projections.

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
            store: MarketStore,
    ):
        self._store = store

    @property
    def symbols(self) -> tuple[str]:
        return self._store.symbols


    def window(self, symbol: str, n: int) -> tuple[TradeReceived, ...]:
        return self._store.window(symbol, n)


    def has_at_least(self, symbol: str, n: int) -> bool:
        return self._store.has_at_least(symbol, n)
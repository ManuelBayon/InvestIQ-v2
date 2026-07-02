from investiq.domain.market_data.contracts.store import MarketStore
from investiq.events.events import MarketDataEvent

from investiq.handlers.base import HandlerResult


class MarketDataHandler:

    def __init__(
            self,
            trade_store: MarketStore,
    ):
        self._trade_store = trade_store


    def handle(self, event: MarketDataEvent) -> HandlerResult:
        self._trade_store.ingest(event)
        return HandlerResult()
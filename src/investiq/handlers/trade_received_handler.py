from investiq.domain.market_data.stores.in_memory_trade_store import MarketStore

from investiq.events.factory import CanonicalEventFactory
from investiq.events.market_data import TradeReceived

from investiq.handlers.base import HandlerResult


class TradeReceivedHandler:

    def __init__(
            self,
            trade_store: MarketStore,
            event_factory: CanonicalEventFactory,
    ):
        self._trade_store = trade_store
        self._event_factory = event_factory

    def handle(
            self,
            event: TradeReceived
    ) -> HandlerResult:
        self._trade_store.append(event)
        return HandlerResult()
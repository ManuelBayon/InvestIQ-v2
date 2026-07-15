from investiq.domain.market_store import InMemoryMarketStore
from investiq.events.trade_received import TradeReceived

from investiq.handlers.base import HandlerResult


class TradeReceivedHandler:

    def __init__(
            self,
            trade_store: InMemoryMarketStore,
    ):
        self._trade_store = trade_store


    def handle(self, event: TradeReceived) -> HandlerResult:
        self._trade_store.on_trade_received(event)
        return HandlerResult()
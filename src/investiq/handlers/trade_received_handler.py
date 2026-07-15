from investiq.features.feature_engine import FeatureEngine
from investiq.domain.market_store import InMemoryMarketStore
from investiq.events.trade_received import TradeReceived

from investiq.handlers.base import HandlerResult


class TradeReceivedHandler:

    def __init__(
            self,
            trade_store: InMemoryMarketStore,
            feature_engine: FeatureEngine,
    ):
        self._trade_store = trade_store
        self._feature_engine = feature_engine


    def handle(self, event: TradeReceived) -> HandlerResult:
        self._trade_store.on_trade_received(event)
        self._feature_engine.update(event)
        return HandlerResult()
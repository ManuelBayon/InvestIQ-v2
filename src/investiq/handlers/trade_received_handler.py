from investiq.features.feature_engine import FeatureEngine
from investiq.domain.market_store import InMemoryTradeStore
from investiq.events.trade_received import TradeReceived

from investiq.handlers.base import HandlerResult


class TradeReceivedHandler:

    def __init__(
            self,
            trade_store: InMemoryTradeStore,
            feature_engine: FeatureEngine,
    ):
        self._trade_store = trade_store
        self._feature_engine = feature_engine


    def handle(self, event: TradeReceived) -> HandlerResult:
        self._trade_store.append(event)
        self._feature_engine.update(event)
        return HandlerResult()
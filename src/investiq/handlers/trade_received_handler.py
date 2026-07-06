from investiq.domain.features.engine import FeatureEngine
from investiq.domain.trade_store import InMemoryTradeStore
from investiq.events.market_data import TradeReceived

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
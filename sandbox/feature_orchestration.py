from collections.abc import Callable

from investiq.domain.market_store import InMemoryMarketStore
from investiq.events.trade_received import TradeReceived
from sandbox.feature_declaration import returns_1, vol_3, z_score_3
from tests.fixtures.market.simple import SIMPLE_TRADES

class FeatureEngine:
    def __init__(self, pipelines: list[Callable[..., object]]):
        self._pipelines = pipelines

    def update(self, event: TradeReceived):
        for p in self._pipelines:
            p(event)

if __name__ == "__main__":
    trade_0 = SIMPLE_TRADES[0]
    trade_1 = SIMPLE_TRADES[1]
    trade_2 = SIMPLE_TRADES[2]

    market_store = InMemoryMarketStore()
    feature_engine = FeatureEngine([returns_1, vol_3, z_score_3])

    market_store.on_trade_received(trade_0)
    feature_engine.update(trade_0)



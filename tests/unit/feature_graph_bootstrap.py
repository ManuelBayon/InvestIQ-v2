from investiq.domain.market_store import InMemoryMarketStore
from investiq.features.bootstrap_graph import bootstrap_feature_graph
from investiq.features.feature_runtime import FeatureRuntime
from investiq.features.features import PriceSource
from tests.fixtures.features.fake_feature import FakeFeature
from tests.fixtures.market.simple_trades import MONO_SYMBOL_SIMPLE_TRADES

if __name__ == "__main__":

    universe = ("SYMBOL_1",)
    store = InMemoryMarketStore(universe)

    # Bootstrap symbol 1 feature graph
    price_source = PriceSource(source=store, symbol="SYMBOL_1", name="PriceSource")
    A = FakeFeature(name="A", emissions=[False, True, True, True, True, True], sources=[price_source])
    B = FakeFeature(name="B", emissions=[False, True, True, True, True], sources=[A])
    C = FakeFeature(name="C", emissions=[False, False, True, True], sources=[A])
    D = FakeFeature(name="D", emissions=[False, True, True], sources=[B, C])

    graph = bootstrap_feature_graph(sources=[price_source], features=[A, B, C, D])
    runtime = FeatureRuntime(graph=graph)

    for trade in MONO_SYMBOL_SIMPLE_TRADES[:5]:
        runtime.on_trade_received(trade=trade)
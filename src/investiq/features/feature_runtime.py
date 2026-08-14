from investiq.domain.market_store import InMemoryMarketStore
from investiq.events.trade_received import TradeReceived
from investiq.features.bootstrap_graph import bootstrap_feature_graph
from investiq.features.features import Feature, PriceSource
from tests.fixtures.features.fake_feature import FakeFeature
from tests.helpers.feature_runtime_trace import print_trace
from tests.fixtures.market.simple_trades import MULTI_SYMBOLS_SIMPLE_TRADES


class FeatureRuntime:

    def __init__(self, roots: dict[str, Feature]):
        self._roots = roots


    def on_trade_received(self, trade: TradeReceived) -> None:

        root = self._roots[trade.symbol]

        eligible: list[Feature] = [root]
        emitted = set()
        step: int = 0

        while len(eligible) > 0:

            eligible_before = eligible.copy()
            current = eligible.pop(0)
            emit = current.compute()

            if not emit:
                print_trace(
                    trade.symbol, trade.timestamp_utc, step, eligible_before,
                    current, emit, emitted, current.successors, eligible)

                step += 1
                continue

            emitted.add(current)

            for successor in current.successors:
                sources = successor.__dict__.get("_sources")

                if set(sources).issubset(emitted):
                    eligible.append(successor)

            print_trace(
                trade.symbol, trade.timestamp_utc, step, eligible_before,
                current, emit, emitted, current.successors, eligible)

            step += 1


if __name__ == "__main__":

    universe = ("SYMBOL_1", "SYMBOL_2")
    store = InMemoryMarketStore(universe)

    roots = {}

    # Bootstrap symbol 1 feature graph
    price_s1 = PriceSource(source=store, symbol=universe[0])
    A = FakeFeature(name="A", emissions=[False, True, True, True], sources=[price_s1])
    B = FakeFeature(name="B", emissions=[False, True, True], sources=[A])
    C = FakeFeature(name="C", emissions=[False, True, True], sources=[A])
    D = FakeFeature(name="D", emissions=[False, True], sources=[B])
    E = FakeFeature(name="E", emissions=[False, True], sources=[A, C])
    F = FakeFeature(name="F", emissions=[True], sources=[D, E])

    roots["SYMBOL_1"] = A
    bootstrap_feature_graph(roots=roots, features=[A, B, C, D, E, F])

    # Bootstrap symbol 2 feature graph
    price_s2 = PriceSource(source=store, symbol=universe[1])
    A = FakeFeature(name="A", emissions=[False, True, True], sources=[price_s2])
    F = FakeFeature(name="F", emissions=[False, True], sources=[A])
    G = FakeFeature(name="G", emissions=[True], sources=[A])
    C = FakeFeature(name="C", emissions=[True], sources=[F])

    roots["SYMBOL_2"] = A
    bootstrap_feature_graph(roots=roots, features=[A, F, G, C])

    # Run
    runtime = FeatureRuntime(roots=roots)
    num_trades = 3
    for i, trade in enumerate(MULTI_SYMBOLS_SIMPLE_TRADES[:num_trades]):
        # on_trade(trade, i)
        runtime.on_trade_received(trade)
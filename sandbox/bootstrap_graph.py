from investiq.domain.market_store import InMemoryMarketStore
from investiq.events.trade_received import TradeReceived
from sandbox.features import ZScore, PriceSource, Returns1, Volatility, Mean, Feature
from tests.fixtures.market.simple import MULTI_SYMBOLS_SIMPLE_TRADES, MONO_SYMBOL_SIMPLE_TRADES

def bootstrap_feature_graph(features: list[Feature]) -> None:
    for feature in features:
        if feature in roots.values():
            continue

        source = feature.__dict__.get("_source")
        source_successors: list[Feature] = source.__dict__.get("successors")
        source_successors.append(feature)


def print_successors() -> None:
    print(f"\nS1 returns successors: {s1_returns.successors}")
    print(f"S1 Vol successors: {s1_volatility.successors}")
    print(f"S1 Mean successors: {s1_mean.successors}")
    print(f"S1 ZScore successors: {s1_zscore.successors}")

    print(f"\nS2 returns successors: {s2_returns.successors}")
    print(f"S2 Vol successors: {s2_volatility.successors}")
    print(f"S2 Mean successors: {s2_mean.successors}")
    print(f"S2 ZScore successors: {s2_zscore.successors}")


def print_features(features: list[Feature]) -> None:
    for f in features:
        print(f._history)

def on_trade(trade: TradeReceived) -> None:
    root = roots[trade.symbol]
    eligible: list[Feature] = [root]

    store.on_trade_received(trade)

    while len(eligible) > 0:
        current = eligible.pop(0)
        if current.compute():
            eligible.extend(current.successor)


def run() -> None:
    for t in MULTI_SYMBOLS_SIMPLE_TRADES:
        on_trade(t)

    print("\nSYMBOL_1 :")
    print_features(s1_features)
    print("\nSYMBOL_2 :")
    print_features(s2_features)


if __name__ == "__main__":
    universe = ("SYMBOL_1", "SYMBOL_2")
    store = InMemoryMarketStore(universe)

    # Symbol 1 features
    s1_price = PriceSource(source=store, symbol="SYMBOL_1")
    s1_returns = Returns1(source=s1_price)
    s1_volatility = Volatility(source=s1_returns, window=3)
    s1_mean = Mean(source=s1_returns, window=3)
    s1_zscore = ZScore(source=s1_volatility, window=3)
    s1_features = [s1_returns, s1_volatility, s1_mean, s1_zscore]

    # Symbol 2 features
    s2_price = PriceSource(source=store, symbol="SYMBOL_2")
    s2_returns = Returns1(source=s2_price)
    s2_volatility = Volatility(source=s2_returns, window=3)
    s2_mean = Mean(source=s2_returns, window=3)
    s2_zscore = ZScore(source=s2_volatility, window=3)
    s2_features = [s2_returns, s2_volatility, s2_mean, s2_zscore]

    roots = {
        "SYMBOL_1": s1_returns,
        "SYMBOL_2": s2_returns,
    }

    bootstrap_feature_graph(s1_features)
    bootstrap_feature_graph(s2_features)
    print_successors()

    run()
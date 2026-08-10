from investiq.domain.market_store import InMemoryMarketStore
from investiq.events.trade_received import TradeReceived
from sandbox.features import ZScore, PriceSource, Returns1, Volatility, Mean, Feature
from tests.fixtures.market.simple import MULTI_SYMBOLS_SIMPLE_TRADES, MONO_SYMBOL_SIMPLE_TRADES

def print_feature_status() -> None:
    print(f"Prices: {[float(trade.price) for trade in MULTI_SYMBOLS_SIMPLE_TRADES]}")

    print("\nSymbol 1: ")
    print(f"Returns1: {s1_returns._history}")
    print(f"Volatility_3: {s1_volatility._history}")
    print(f"Mean_3: {s1_mean._history}")
    print(f"ZScore_3: {s1_zscore._history}")

    print("\nSymbol 2: ")
    print(f"Returns1: {s2_returns._history}")
    print(f"Volatility_3: {s2_volatility._history}")
    print(f"Mean_3: {s2_mean._history}")
    print(f"ZScore_3: {s2_zscore._history}")


def bootstrap_feature_graph() -> dict[str, Feature]:
    s1_returns.successors = [s1_volatility, s1_mean]
    s1_volatility.successors = [s1_zscore]
    s2_returns.successors = [s2_volatility, s2_mean]
    s2_volatility.successors = [s2_zscore]
    return {
        "SYMBOL_1": s1_returns,
        "SYMBOL_2": s2_returns,
    }


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
    print_feature_status()


if __name__ == "__main__":
    universe = ("SYMBOL_1", "SYMBOL_2")
    store = InMemoryMarketStore(universe)

    # Symbol 1 features
    s1_price = PriceSource(source=store, symbol="SYMBOL_1")
    s1_returns = Returns1(source=s1_price)
    s1_volatility = Volatility(source=s1_returns, window=3)
    s1_mean = Mean(source=s1_returns, window=3)
    s1_zscore = ZScore(source=s1_volatility, window=3)

    # Symbol 2 features
    s2_price = PriceSource(source=store, symbol="SYMBOL_2")
    s2_returns = Returns1(source=s2_price)
    s2_volatility = Volatility(source=s2_returns, window=3)
    s2_mean = Mean(source=s2_returns, window=3)
    s2_zscore = ZScore(source=s2_volatility, window=3)

    # Bootstrap and run
    roots = bootstrap_feature_graph()
    run()
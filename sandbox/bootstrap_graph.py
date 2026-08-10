from investiq.domain.market_store import InMemoryMarketStore
from investiq.events.trade_received import TradeReceived
from sandbox.features import ZScore, PriceSource, Returns1, Volatility, Mean, Feature
from tests.fixtures.market.simple import MULTI_SYMBOLS_SIMPLE_TRADES, MONO_SYMBOL_SIMPLE_TRADES

def print_feature_status():
    print(f"\nPrices: {[float(trade.price) for trade in MONO_SYMBOL_SIMPLE_TRADES]}")
    print(f"Returns1: {s1_returns._history}")
    print(f"Volatility_3: {s1_volatility._history}")
    print(f"Mean_3: {s1_mean._history}")
    print(f"ZScore_3: {s1_zscore._history}")

def on_trade(trade: TradeReceived) -> None:
    root = roots[trade.symbol]
    eligible: list[Feature] = [root]

    store.on_trade_received(trade)

    while len(eligible) > 0:
        current = eligible.pop(0)
        if current.compute():
            eligible.extend(current.successor)


def run() -> None:
    for t in MONO_SYMBOL_SIMPLE_TRADES:
        on_trade(t)


if __name__ == "__main__":
    universe = ("SYMBOL_1",)
    store = InMemoryMarketStore(universe)

    # Symbol 1 features
    s1_price = PriceSource(source=store, symbol="SYMBOL_1")
    s1_returns = Returns1(source=s1_price)
    s1_volatility = Volatility(source=s1_returns, window=3)
    s1_mean = Mean(source=s1_returns, window=3)
    s1_zscore = ZScore(source=s1_volatility, window=3)


    # ignore source of root

    print(f"Volatility source: {s1_volatility.__dict__.get("_source")}")
    source = s1_volatility.__dict__.get("_source")
    source_successors : list[Feature] = source.__dict__.get("successors")
    source_successors.append(s1_volatility)

    print(f"Mean source: {s1_mean.__dict__.get("_source")}")
    source = s1_mean.__dict__.get("_source")
    source_successors: list[Feature] = source.__dict__.get("successors")
    source_successors.append(s1_mean)

    print(f"Zscore source: {s1_zscore.__dict__.get("_source")}")
    source = s1_zscore.__dict__.get("_source")
    source_successors: list[Feature] = source.__dict__.get("successors")
    source_successors.append(s1_zscore)

    print(f"Returns1 successors: {s1_returns.successors}")
    print(f"Vol successors: {s1_volatility.successors}")
    print(f"Mean successors: {s1_mean.successors}")
    print(f"ZScore successors: {s1_zscore.successors}")

    roots = {"SYMBOL_1": s1_returns}

    run()
    print_feature_status()
from investiq.domain.market_store import InMemoryMarketStore
from investiq.events.trade_received import TradeReceived
from sandbox.features import ZScore, PriceSource, Returns1, Volatility, Mean, Feature
from tests.fixtures.market.simple import MULTI_SYMBOLS_SIMPLE_TRADES, MONO_SYMBOL_SIMPLE_TRADES

def print_feature_status():
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


def on_trade(trade: TradeReceived) -> None:
    root = roots[trade.symbol]
    eligible: list[Feature] = [root]

    store.on_trade_received(trade)

    while len(eligible) > 0:
        current = eligible.pop(0)
        if current.compute():
            eligible.extend(current.successor)


if __name__ == "__main__":

    universe = ("SYMBOL_1", "SYMBOL_2")
    store = InMemoryMarketStore(universe)
    s1_price = PriceSource(source=store, symbol="SYMBOL_1")
    s2_price = PriceSource(source=store, symbol="SYMBOL_2")

    # Symbol 1 features
    s1_returns = Returns1(source=s1_price)
    s1_volatility = Volatility(source=s1_returns, window=3)
    s1_mean = Mean(source=s1_returns, window=3)
    s1_zscore = ZScore(source=s1_volatility, window=3)

    s1_returns.successors = [s1_volatility, s1_mean]
    s1_volatility.successors = [s1_zscore]

    # Symbol 2 features
    s2_returns = Returns1(source=s2_price)
    s2_volatility = Volatility(source=s2_returns, window=3)
    s2_mean = Mean(source=s2_returns, window=3)
    s2_zscore = ZScore(source=s2_volatility, window=3)

    s2_returns.successors = [s2_volatility, s2_mean]
    s2_volatility.successors = [s2_zscore]

    trade_1 = MULTI_SYMBOLS_SIMPLE_TRADES[0]
    trade_2 = MULTI_SYMBOLS_SIMPLE_TRADES[1]
    trade_3 = MULTI_SYMBOLS_SIMPLE_TRADES[2]
    trade_4 = MULTI_SYMBOLS_SIMPLE_TRADES[3]
    trade_5 = MULTI_SYMBOLS_SIMPLE_TRADES[4]
    trade_6 = MULTI_SYMBOLS_SIMPLE_TRADES[5]
    trade_7 = MULTI_SYMBOLS_SIMPLE_TRADES[6]
    trade_8 = MULTI_SYMBOLS_SIMPLE_TRADES[7]
    trade_9 = MULTI_SYMBOLS_SIMPLE_TRADES[8]
    trade_10 = MULTI_SYMBOLS_SIMPLE_TRADES[9]
    trade_11 = MULTI_SYMBOLS_SIMPLE_TRADES[10]
    trade_12 = MULTI_SYMBOLS_SIMPLE_TRADES[11]

    roots = {
        "SYMBOL_1" : s1_returns,
        "SYMBOL_2": s2_returns,
    }

    on_trade(trade_1)
    on_trade(trade_2)
    on_trade(trade_3)
    on_trade(trade_4)
    on_trade(trade_5)
    on_trade(trade_6)
    on_trade(trade_7)
    on_trade(trade_8)
    on_trade(trade_9)
    on_trade(trade_10)
    on_trade(trade_11)
    on_trade(trade_12)

    print_feature_status()
from investiq.domain.market_store import InMemoryMarketStore
from investiq.events.trade_received import TradeReceived
from sandbox.features import ZScore, PriceSource, Returns1, Volatility, Mean, Feature
from tests.fixtures.market.simple import MULTI_SYMBOLS_SIMPLE_TRADES, MONO_SYMBOL_SIMPLE_TRADES

def print_feature_status():
    print(f"Prices: {[float(trade.price) for trade in MONO_SYMBOL_SIMPLE_TRADES]}")
    print(f"Returns1: {returns._history}")
    print(f"Volatility_3: {volatility._history}")
    print(f"Mean_3: {mean._history}")
    print(f"ZScore_3: {zscore._history}")


def on_trade(trade: TradeReceived) -> None:
    print("\nNew step: ")
    eligible: list[Feature] = [returns]

    store.on_trade_received(trade)

    while len(eligible) > 0:
        current = eligible.pop(0)
        print(f"current={current}")

        if current.compute():
            eligible.extend(current.successor)

        print(f"eligible={eligible}")


if __name__ == "__main__":

    universe = ("SYMBOL_1",)
    store = InMemoryMarketStore(universe)
    price = PriceSource(source=store, symbol="SYMBOL_1")

    returns = Returns1(source=price)
    volatility = Volatility(source=returns, window=3)
    mean = Mean(source=returns, window=3)
    zscore = ZScore(source=volatility, window=3)

    returns.successors = [volatility, mean]
    volatility.successors = [zscore]


    trade_1 = MONO_SYMBOL_SIMPLE_TRADES[0]
    trade_2 = MONO_SYMBOL_SIMPLE_TRADES[1]
    trade_3 = MONO_SYMBOL_SIMPLE_TRADES[2]
    trade_4 = MONO_SYMBOL_SIMPLE_TRADES[3]
    trade_5 = MONO_SYMBOL_SIMPLE_TRADES[4]
    trade_6 = MONO_SYMBOL_SIMPLE_TRADES[5]

    on_trade(trade_1)
    on_trade(trade_2)
    on_trade(trade_3)
    on_trade(trade_4)
    on_trade(trade_5)
    on_trade(trade_6)
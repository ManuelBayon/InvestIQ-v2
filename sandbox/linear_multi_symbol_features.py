from investiq.domain.market_store import InMemoryMarketStore
from investiq.events.trade_received import TradeReceived
from sandbox.features import ZScore, PriceSource, Returns1, Volatility
from tests.fixtures.market.simple import MULTI_SYMBOLS_SIMPLE_TRADES

def on_trade(trade: TradeReceived) -> None:
    store.on_trade_received(trade)

    pipelines = pipelines_by_symbol[trade.symbol]

    for pipeline in pipelines:
        for feature in pipeline:
            emitted  = feature.compute()
            if not emitted:
                break


if __name__ == "__main__":
    universe = ("SYMBOL_1", "SYMBOL_2")
    store = InMemoryMarketStore(universe)

    s1_price = PriceSource(source=store, symbol="SYMBOL_1")
    s1_returns = Returns1(source=s1_price)
    s1_vol = Volatility(source=s1_returns, window=3)
    s1_z_score = ZScore(source=s1_vol, window=3)

    s2_price = PriceSource(source=store, symbol="SYMBOL_2")
    s2_returns = Returns1(source=s2_price)
    s2_vol = Volatility(s2_returns, 3)
    s2_z_score = ZScore(source=s2_vol, window=3)

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

    pipelines_by_symbol = {
        "SYMBOL_1" : [(s1_returns, s1_vol, s1_z_score)],
        "SYMBOL_2": [(s2_returns, s2_vol, s2_z_score)],
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

    print(f"Prices: {[float(t.price) for t in MULTI_SYMBOLS_SIMPLE_TRADES]}")

    print("\nSYMBOL_1 :")
    print(f"Returns1: {s1_returns._history}")
    print(f"Volatility 3: {s1_vol._history}")
    print(f"ZScore 3: {s1_z_score._history}")

    print("\nSYMBOL_2 :")
    print(f"Returns1: {s2_returns._history}")
    print(f"Volatility 3: {s2_vol._history}")
    print(f"ZScore 3: {s2_z_score._history}")

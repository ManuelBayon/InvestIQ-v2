from investiq.domain.market_store import InMemoryMarketStore
from investiq.events.trade_received import TradeReceived
from sandbox.features import Returns1, Volatility, ZScore, PriceSource

from tests.fixtures.market.simple import MONO_SYMBOL_SIMPLE_TRADES


def on_trade_received(trade: TradeReceived) -> None:
    store.on_trade_received(trade)
    returns.compute()
    volatility.compute()
    zscore.compute()

def print_state(
        ret: Returns1,
        vol: Volatility,
        zs: ZScore
) -> None:
    print(ret.load(1))
    print(vol.load(1))
    print(zs.load(1))

if __name__ == "__main__":

    universe = ("SYMBOL_1",)
    store = InMemoryMarketStore(symbols=universe)
    price = PriceSource(source=store, symbol="SYMBOL_1")

    returns = Returns1(source=price)
    volatility = Volatility(source=returns, window=3)
    zscore = ZScore(source=volatility, window=3)

    trade_0 = MONO_SYMBOL_SIMPLE_TRADES[0]
    trade_1 = MONO_SYMBOL_SIMPLE_TRADES[1]
    trade_2 = MONO_SYMBOL_SIMPLE_TRADES[2]
    trade_3 = MONO_SYMBOL_SIMPLE_TRADES[3]
    trade_4 = MONO_SYMBOL_SIMPLE_TRADES[4]
    trade_5 = MONO_SYMBOL_SIMPLE_TRADES[5]
    trades = [trade_0, trade_1, trade_2, trade_3, trade_4, trade_5]

    on_trade_received(trade_0)
    on_trade_received(trade_1)
    on_trade_received(trade_2)
    on_trade_received(trade_3)
    on_trade_received(trade_4)
    on_trade_received(trade_5)

    print(f"Prices: {[float(t.price) for t in trades]}")
    print(f"Returns1: {returns._history}")
    print(f"Volatility 3: {volatility._history}")
    print(f"ZScore 3: {zscore._history}")
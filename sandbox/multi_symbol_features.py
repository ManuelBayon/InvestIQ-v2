from investiq.domain.market_store import InMemoryMarketStore
from sandbox.mono_symbol_features import PriceSource, Returns1
from tests.fixtures.market.simple import MULTI_SYMBOLS_SIMPLE_TRADES


if __name__ == "__main__":
    store = InMemoryMarketStore()
    symbol_1_source = PriceSource(source=store, symbol="SYMBOL_1")
    symbol_2_source = PriceSource(source=store, symbol="SYMBOL_2")
    symbol_1_returns1 = Returns1(source=symbol_1_source)
    symbol_2_returns1 = Returns1(source=symbol_2_source)

    trade_1 = MULTI_SYMBOLS_SIMPLE_TRADES[0]
    trade_2 = MULTI_SYMBOLS_SIMPLE_TRADES[1]
    trade_3 = MULTI_SYMBOLS_SIMPLE_TRADES[2]

    store.on_trade_received(trade_1)
    symbol_1_returns1.compute()
    symbol_2_returns1.compute()
    print(symbol_1_returns1._history)

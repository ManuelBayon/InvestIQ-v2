import random

from investiq.domain.features.caculators.SMA import SMA
from investiq.domain.market_data.reader import InMemoryMarketDataReader
from investiq.domain.market_data.stores.trade_store import TradeStore

from tests.fixtures.trade_received import make_trade_stream

if __name__ == "__main__":



    store = TradeStore()
    store_reader = InMemoryMarketDataReader(trade_store=store)
    sma_3 = SMA(window=3)

    for trade in trades:
        store.ingest(trade=trade)

        if store_reader.has_at_least_n_trades(symbol="AMD", n=sma_3.window):
            result = sma_3.calculate(events=store_reader.trades(symbol="AMD", n=3))
            print(result)
        else:
            print("warmup")
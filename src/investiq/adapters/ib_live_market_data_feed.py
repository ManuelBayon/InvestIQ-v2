from ib_insync import IB, Ticker, Stock, Future

from investiq.domain.models import RawTick
from investiq._archive.raw_tick_buffer import RawTickBuffer

class IBLiveMarketDataFeed:
    """
    2026-05-21 :
        MVP limitation:
            IB reqMktData delayed ticks are used as proxy ticks.
            TickData.time is treated as tick timestamp for aggregation,
            but this is not guaranteed to be exchange trade-time.
    """
    def __init__(
            self,
            queue: RawTickBuffer,
    ):
        self._ib = IB()
        self._ib.pendingTickersEvent += self.on_pending_ticker
        self._tickers: dict[str, Ticker] = {}

        self._history: dict[str, list[Ticker]]
        self._queue = queue


    def connect(
            self,
            host: str = "127.0.0.1",
            port: int = 7497,
            client_id: int = 1,
            data_type: int = 3,  # 1 = Live / 3 = Delayed
    ) -> None:
        self._ib.connect(host, port, clientId=client_id)
        self._ib.reqMarketDataType(data_type)

    def disconnect(self):
        self._ib.disconnect()

    def subscribe_to_stock(
            self,
            symbol: str,
            exchange: str = "SMART",
            currency: str = "USD",
    ) -> None:
        """
        Example : reqMktData(symbol="AMD", exchange= "SMART", currency= "USD")
        """
        self._tickers[symbol] = self._ib.reqMktData(Stock(symbol, exchange, currency))

    def subscribe_to_cont_fut(
            self,
            symbol: str,
            local_symbol: str,
            exchange: str = "CME",
            currency: str = "USD",
    ) -> None:
        """
        Example : reqMktData(Future(symbol="NQ", localSymbol="NQM6",exchange="CME", currency="USD"))
        """
        self._tickers[symbol] = self._ib.reqMktData(
            contract=Future(
                symbol=symbol,
                localSymbol=local_symbol,
                exchange=exchange,
                currency=currency
            ),
        )

    def run(self) -> None:
        self._ib.run()

    def on_pending_ticker(
            self,
            tickers: set[Ticker]
    ) -> None:
        """
        2026-05-28 — Adapter boundary:
        - ib_insync.Ticker and ib_insync.TickData do not cross this method.
        - This method converts IB ticks into internal RawTick objects.
        - Current prototype forwards all observed ticks.
        - No deduplication is guaranteed here yet.
        - Ordering is the iteration order received from ib_insync.
        """
        raw_ticks: dict[str, list[RawTick]] = {}
        for t in tickers:
            _symbol = t.contract.symbol
            if _symbol not in raw_ticks.keys():
                raw_ticks[_symbol] = []
            for tick in t.ticks:
                raw_tick = RawTick(
                    symbol=_symbol,
                    tick_type=tick.tickType,
                    timestamp_utc=tick.time,
                    price=tick.price,
                    size=tick.size,
                )
                raw_ticks[_symbol].append(raw_tick)
        self._queue.enqueue(raw_ticks)

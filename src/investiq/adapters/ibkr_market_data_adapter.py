from ib_insync import Ticker, Future, Stock

from investiq.adapters.ibkr_client import IBKRClient
from investiq.domain.models import RawTick
from investiq.events.factory import CanonicalEventFactory
from investiq.runtime.canonical_event_queue import CanonicalEventQueue


class IBKRMarketDataAdapter:

    def __init__(
            self,
            ibkr_client: IBKRClient,
            event_factory: CanonicalEventFactory,
            event_queue: CanonicalEventQueue,
    ):
        self._ibkr_client = ibkr_client
        self._event_factory = event_factory
        self._event_queue = event_queue

        self._tickers: dict[str, Ticker] = {}

        self._ibkr_client.subscribe_pending_tickers(
            handler=self.on_pending_ticker
        )

    def subscribe_to_stock(
            self,
            symbol: str,
            exchange: str = "SMART",
            currency: str = "USD",
    ) -> None:
        """
        Example : reqMktData(symbol="AMD", exchange= "SMART", currency= "USD")
        """
        self._tickers[symbol] = self._ibkr_client.request_market_data(
            contract=Stock(
                symbol=symbol,
                exchange=exchange,
                currency=currency
            )
        )

    def subscribe_to_future(
            self,
            symbol: str,
            local_symbol: str,
            exchange: str = "CME",
            currency: str = "USD",
    ) -> None:
        """
        Example : reqMktData(Future(symbol="NQ", local_symbol="NQU6", exchange"CME"))
        """
        self._tickers[symbol] = self._ibkr_client.request_market_data(
            contract=Future(
                symbol=symbol,
                localSymbol=local_symbol,
                exchange=exchange,
                currency=currency
            ),
        )

    def on_pending_ticker(self, tickers: set[Ticker]) -> None:
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
            for tick in t.ticks:

                if tick.tickType != 68:
                    continue

                if _symbol not in raw_ticks:
                    raw_ticks[_symbol] = []

                raw_tick = RawTick(
                    symbol=_symbol,
                    tick_type=tick.tickType,
                    timestamp_utc=tick.time,
                    price=tick.price,
                    size=tick.size,
                )
                raw_ticks[_symbol].append(raw_tick)

        if not raw_ticks:
            return

        event = self._event_factory.create_tick_data_available(
            payload=raw_ticks
        )
        self._event_queue.enqueue(event)
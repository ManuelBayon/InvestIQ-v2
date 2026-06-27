import asyncio

from ib_insync import Stock, Future, MarketOrder, Trade, Fill, CommissionReport

from investiq.adapters.ibkr_client import IBKRClient
from investiq.adapters.ibkr_market_data_adapter import IBKRMarketDataAdapter
from investiq.adapters.mappers import map_ibkr_order_status_to_canonical_event

from investiq.domain.instruments import StockSpecs, FutureSpecs
from investiq.domain.order_specs import MarketOrderSpecs
from investiq.events.factory import CanonicalEventFactory
from investiq.runtime.canonical_event_queue import CanonicalEventQueue


class IBKRAdapter:
    """
    2026-05-21 :
        MVP limitation:
            IB reqMktData delayed ticks are used as proxy ticks.
            TickData.time is treated as tick timestamp for aggregation,
            but this is not guaranteed to be exchange trade-time.
    """
    def __init__(
            self,
            ibkr_client: IBKRClient,
            ibkr_market_data_adapter: IBKRMarketDataAdapter,
    ):
        self._ibkr_client = ibkr_client
        self._ibkr_market_data_adapter = ibkr_market_data_adapter

    def run(self) -> None:
        self._ib_loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self._ib_loop)

        self._ibkr_client.connect()
        self._ibkr_client.set_market_data_type()
        self._ibkr_market_data_adapter.subscribe_to_future(
            symbol="MNQ",
            local_symbol="MNQU6"
        )
        self._ibkr_client.run()

    @property
    def ib_loop(self):
        return self._ib_loop
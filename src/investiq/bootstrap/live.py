from investiq.adapters.ib_live_market_data_feed import IBLiveMarketDataFeed
from investiq._archive.raw_tick_buffer import RawTickBuffer
from investiq._archive.tick_aggregator import TickAggregator

class LiveRuntime:

    def __init__(self):
        self._tick_buffer = RawTickBuffer()
        self._live_data_feed = IBLiveMarketDataFeed(queue=self._tick_buffer)
        self._tick_aggregator = TickAggregator(bar_size="1 min", )


    def live_market_data_feed(self) -> None:
        self._live_data_feed.connect()
        self._live_data_feed.subscribe_to_cont_fut(
            symbol="MNQ",
            local_symbol="MNQM6",
        )
        self._live_data_feed.subscribe_to_stock("AMD")
        self._live_data_feed.run()


    def run_tick_aggregation(self) -> None:
        ...





"""
market_store = MarketStore()
feature_store = FeatureStore()
decision_layer = NoOperationDecisionLayer()
bar_available_handler = BarAvailableHandler(
    market_store=market_store,
    feature_store=feature_store,
    decision_layer=decision_layer
)

orchestrator = Orchestrator(
    bar_available_handler=bar_available_handler
)

5. créer event_loop / ingress
6. créer aggregator
7. créer feed
8. connect / subscribe
9. run"""





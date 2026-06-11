from threading import Thread

from investiq.adapters.ib_live_market_data_feed import IBLiveMarketDataFeed
from investiq.runtime.event_loop import EventLoop


class LiveRuntime:

    def __init__(
            self,
            data_feed: IBLiveMarketDataFeed,
            event_loop: EventLoop,
    ):
        self._data_feed = data_feed
        self._event_loop = event_loop

    def run(self) -> None:

        self._data_feed.connect()
        self._data_feed.subscribe_to_cont_fut(symbol="MNQ", local_symbol="MNQM6")

        runtime_thread = Thread(target=self._event_loop.run, daemon=True)

        runtime_thread.start()
        self._data_feed.run()
from threading import Thread

from investiq.adapters.ibkr_adapter import IBKRGatewayAdapter
from investiq.runtime.event_loop import EventLoop


class LiveRuntime:

    def __init__(
            self,
            data_feed: IBKRGatewayAdapter,
            event_loop: EventLoop,
    ):
        self._data_feed = data_feed
        self._event_loop = event_loop

    def run(self) -> None:

        self._data_feed.connect()
        self._data_feed.subscribe_to_future(symbol="MNQ", local_symbol="MNQM6")
        self._data_feed.subscribe_to_stock("AMD")

        runtime_thread = Thread(target=self._event_loop.run, daemon=True)

        runtime_thread.start()
        self._data_feed.run()
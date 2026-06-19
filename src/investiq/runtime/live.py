from threading import Thread

from investiq.adapters.ibkr_adapter import IBKRAdapter
from investiq.runtime.event_loop import EventLoop


class LiveRuntime:

    def __init__(
            self,
            ibkr_adapter: IBKRAdapter,
            event_loop: EventLoop,
    ):
        self._ibkr_adapter = ibkr_adapter
        self._event_loop = event_loop

    def run(self) -> None:

        event_loop_thread = Thread(
            target=self._event_loop.run,
            name="event_loop_thread",
        )
        ibkr_thread = Thread(
            target=self._ibkr_adapter.run,
            name="ibkr_thread",
        )

        self._ibkr_adapter.connect()
        self._ibkr_adapter.subscribe_to_future(symbol="MNQ", local_symbol="MNQU6")

        event_loop_thread.start()
        ibkr_thread.start()
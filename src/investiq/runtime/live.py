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

    def run_process_thread(self) -> None:
        event_loop_thread = Thread(target=self._event_loop.run, name="process_thread")
        event_loop_thread.start()

    def run_ibkr_thread(self) -> None:
        ibkr_thread = Thread(target=self._ibkr_adapter.run, name="ibkr_thread")
        ibkr_thread.start()
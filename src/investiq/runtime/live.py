from threading import Thread

from investiq.ingress.base import Ingress
from investiq.process.event_loop import CanonicalEventLoop


class LiveRuntime:

    def __init__(
            self,
            run_id: str,
            ingress: Ingress,
            event_loop: CanonicalEventLoop,
    ):
        self._run_id = run_id
        self._ingress = ingress
        self._event_loop = event_loop


    def run(self) -> None:
        thread = Thread(target=self._event_loop.run_forever)
        thread.start()

        self._ingress.start()

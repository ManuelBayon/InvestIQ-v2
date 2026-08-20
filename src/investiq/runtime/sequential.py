from investiq.core.event_loop import CanonicalEventLoop
from investiq.ingress.protocol import Ingress


class SequentialRuntime:

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
        self._ingress.start()
        self._event_loop.run_until_empty()
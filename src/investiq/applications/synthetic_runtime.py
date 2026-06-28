from threading import Thread
from time import sleep

from investiq.ingress.synthetic_ingress import SyntheticIngress
from investiq.runtime.event_loop import CanonicalEventLoop


class SyntheticRuntime:

    def __init__(
            self,
            event_loop: CanonicalEventLoop,
            ingress: SyntheticIngress
    ):
        self._event_loop = event_loop
        self._ingress = ingress

    def run(
            self,
            n: int,
    ) -> None:
        for _ in range(n):
            self._ingress.enqueue_one_trade()
            self._event_loop.run_until_empty()

    def run_slow(
            self,
            n: int,
            delay_seconds: float = 1.0
    ) -> None:
        for _ in range(n):
            self._ingress.enqueue_one_trade()
            self._event_loop.run_until_empty()
            sleep(delay_seconds)
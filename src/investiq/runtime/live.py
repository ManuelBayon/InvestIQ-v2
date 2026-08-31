import asyncio
from dataclasses import dataclass
from threading import Thread

from investiq.adapters.ibkr.ib_client import IBKRClient
from investiq.core.event_loop import CanonicalEventLoop

from investiq.ingress.protocol import Ingress
from investiq.runtime.base import Runtime, RuntimeConfig


@dataclass(frozen=True)
class LiveRuntimeConfig(RuntimeConfig):
    ...

class LiveRuntime:

    def __init__(
            self,
            ingress: Ingress,
            event_loop: CanonicalEventLoop,
            ib_client: IBKRClient,
    ):
        self._ingress = ingress
        self._event_loop = event_loop
        self._ib_client = ib_client

    def run(self) -> None:
        self._ib_client.connect()

        thread = Thread(target=self._event_loop.run_forever, name="canonical_thread")
        thread.start()

        self._ingress.start()
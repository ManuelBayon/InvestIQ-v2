import asyncio
import threading
from dataclasses import dataclass
from threading import Thread

from investiq.adapters.ibkr.ib_client import IBClient
from investiq.core.event_loop import CanonicalEventLoop

from investiq.ingress.protocol import Ingress
from investiq.runtime.base import RuntimeConfig


@dataclass(frozen=True)
class LiveRuntimeConfig(RuntimeConfig):
    ...

class LiveRuntime:

    def __init__(
            self,
            ingress: Ingress,
            event_loop: CanonicalEventLoop,
            ib_client: IBClient,
    ):
        self._ingress = ingress
        self._event_loop = event_loop
        self._ib_client = ib_client

    def run(self) -> None:

        self._ib_client.connect()

        canonical_thread = Thread(
            target=self._event_loop.run_forever,
            name="canonical_thread"
        )

        canonical_thread.start()
        self._ingress.start()

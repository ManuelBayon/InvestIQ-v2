from dataclasses import dataclass

from investiq.adapters.ibkr.ib_client import IBKRClient
from investiq.core.event_loop import CanonicalEventLoop

from investiq.ingress.protocol import Ingress
from investiq.ingress.synthetic import TradeFixture
from investiq.runtime.base import RuntimeConfig, Runtime


@dataclass(frozen=True)
class SequentialRuntimeConfig(RuntimeConfig):
    trades: list[TradeFixture]
    num_trades: int

class SequentialRuntime(Runtime):

    def __init__(
            self,
            ingress: Ingress,
            event_loop: CanonicalEventLoop,
            ib_client: IBKRClient
    ):
        self._ingress = ingress
        self._event_loop = event_loop
        self._ib_client = ib_client

    def run(self) -> None:
        self._ib_client.connect()
        self._ingress.start()
        self._event_loop.run_until_empty()
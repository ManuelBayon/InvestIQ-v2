from collections.abc import Callable

from investiq.events.base import CanonicalEvent
from investiq.events.intents import IntentGenerated
from investiq.events.market_data import TradeReceived
from investiq.runtime.handlers.trade_received_handler import TradeReceivedHandler


class Orchestrator:

    def __init__(
            self,
            trade_received_handler: TradeReceivedHandler,
    ):
        self._trade_received_handler = trade_received_handler

        self._dispatch_table: dict[type[CanonicalEvent], Callable] = {
            TradeReceived: self._on_trade_received,
        }

    def _on_trade_received(self, event: TradeReceived) -> IntentGenerated:
        return self._trade_received_handler.handle(event=event)


    def dispatch(self, event: CanonicalEvent) -> CanonicalEvent:
        print(f"[DISPATCH] event:{type(event).__name__}")
        handler = self._dispatch_table[type(event)]
        print(f"[DISPATCH] handler:{handler}")
        return handler(event)
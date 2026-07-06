from collections.abc import Callable

from investiq.events.trade_received import TradeReceived
from investiq.core.contracts.events import CanonicalEvent
from investiq.handlers.base import HandlerResult
from investiq.handlers.trade_received_handler import TradeReceivedHandler



class Dispatcher:


    def __init__(
            self,
            trade_received_handler: TradeReceivedHandler,
    ):
        self._trade_received_handler = trade_received_handler

        self._dispatch_table: dict[type[CanonicalEvent], Callable] = {
            TradeReceived: self._on_trade_received,
        }


    def _on_trade_received(self, event: TradeReceived) -> HandlerResult:
        return self._trade_received_handler.handle(event)


    def dispatch(self, event: CanonicalEvent) -> HandlerResult:
        event_type = type(event)
        handler = self._dispatch_table[event_type]
        return handler(event)
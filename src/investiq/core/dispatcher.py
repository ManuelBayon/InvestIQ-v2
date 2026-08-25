from collections.abc import Callable

from investiq.core.events import CanonicalEvent, TradeReceived, OrderGenerated
from investiq.core.handlers.base import HandlerResult
from investiq.core.handlers.trade_received_handler import TradeReceivedHandler



class Dispatcher:

    def __init__(
            self,
            trade_received_handler: TradeReceivedHandler,
    ):
        self._trade_received_handler = trade_received_handler

        self._dispatch_table: dict[type[CanonicalEvent], Callable] = {
            TradeReceived: self._on_trade_received,
            OrderGenerated: self._on_orders_generated
        }


    def _on_trade_received(self, event: TradeReceived) -> HandlerResult:
        return self._trade_received_handler.handle(event)


    def _on_orders_generated(self, event: OrderGenerated) -> HandlerResult:
        return HandlerResult()


    def dispatch(self, event: CanonicalEvent) -> HandlerResult:
        event_type = type(event)
        handler = self._dispatch_table[event_type]
        return handler(event)
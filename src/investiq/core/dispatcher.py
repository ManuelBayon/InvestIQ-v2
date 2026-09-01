from collections.abc import Callable

from investiq.core.events import CanonicalEvent, TradeReceived, OrderGenerated, OrderStatusUpdated, FillReceived, \
    CommissionReportReceived
from investiq.core.handlers.base import HandlerResult
from investiq.core.handlers.order_generated_handler import OrderGeneratedHandler
from investiq.core.handlers.trade_received_handler import TradeReceivedHandler



class Dispatcher:

    def __init__(
            self,
            trade_received_handler: TradeReceivedHandler,
            order_generated_handler: OrderGeneratedHandler,
    ):
        self._trade_received_handler = trade_received_handler
        self._order_generated_handler = order_generated_handler

        self._dispatch_table: dict[type[CanonicalEvent], Callable] = {
            TradeReceived: self._on_trade_received,
            OrderGenerated: self._on_order_generated,
            OrderStatusUpdated: self._on_order_status_updated,
            FillReceived: self._on_fill_received,
            CommissionReportReceived: self._on_commission_report_received,
        }


    def _on_trade_received(self, event: TradeReceived) -> HandlerResult:
        return self._trade_received_handler.handle(event)


    def _on_order_generated(self, event: OrderGenerated) -> HandlerResult:
        return self._order_generated_handler.handle(event)

    def _on_order_status_updated(self, event: OrderStatusUpdated) -> HandlerResult:
        return HandlerResult()

    def _on_fill_received(self, event: FillReceived) -> HandlerResult:
        return HandlerResult()

    def _on_commission_report_received(self, event: CommissionReportReceived) -> HandlerResult:
        return HandlerResult()

    def dispatch(self, event: CanonicalEvent) -> HandlerResult:
        event_type = type(event)
        handler = self._dispatch_table[event_type]
        return handler(event)
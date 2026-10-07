import logging

from investiq.core.broker_messages import (
    BrokerFill, BrokerMessage, BrokerOperationFailed, BrokerOrderStatus, MarketTrade,
)
from investiq.core.event_factory import EventFactory
from investiq.core.events import (
    BrokerReturnUnmatched, CommissionReportReceived, FillReceived, IBOperationFailed, OrderStatusUpdated,
)
from investiq.core.handlers.base import HandlerResult
from investiq.core.order_correlation import OrderCorrelation


class BrokerReturnHandler:
    def __init__(self, correlation: OrderCorrelation, event_factory: EventFactory) -> None:
        self._correlation = correlation
        self._event_factory = event_factory

    def handle(self, message: BrokerMessage | MarketTrade | BrokerOperationFailed) -> HandlerResult:
        if isinstance(message, MarketTrade):
            return HandlerResult(events=(self._event_factory.create_trade_received(
                symbol=message.symbol, timestamp_utc=message.timestamp_utc,
                price=message.price, size=message.size,
            ),))
        event_id = self._event_factory.next_event_id()
        if isinstance(message, BrokerOperationFailed):
            logging.getLogger(__name__).error("IB %s failed: %s", message.operation, message.error)
            return HandlerResult(events=(IBOperationFailed(
                run_id=message.run_id, event_id=event_id,
                command_id=message.command_id, operation=message.operation, error=message.error,
            ),))
        try:
            association = self._correlation.by_broker(message.run_id, message.broker_order_id)
        except KeyError:
            logging.getLogger(__name__).error(
                "Unknown broker order ID %s in run %s", message.broker_order_id, message.run_id
            )
            return HandlerResult(events=(
                BrokerReturnUnmatched(message.run_id, event_id, message),
            ))

        if isinstance(message, BrokerOrderStatus):
            event = OrderStatusUpdated(
                run_id=message.run_id, event_id=event_id,
                order_id=association.order_id, parent_id=association.parent_id,
                status=message.status,
            )
        elif isinstance(message, BrokerFill):
            event = FillReceived(
                run_id=message.run_id, event_id=event_id,
                order_id=association.order_id, parent_id=association.parent_id,
                exec_id=message.exec_id, timestamp_utc=message.timestamp_utc,
                qty_executed=message.qty_executed, side=message.side,
                price=message.price, cumul_qty=message.cumul_qty,
            )
        else:
            event = CommissionReportReceived(
                run_id=message.run_id, event_id=event_id,
                order_id=association.order_id, parent_id=association.parent_id,
                exec_id=message.exec_id, commission=message.commission,
                currency=message.currency, realized_pnl=message.realized_pnl,
            )
        return HandlerResult(events=(event,))

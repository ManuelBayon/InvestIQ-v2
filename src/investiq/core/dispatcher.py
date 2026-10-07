from collections.abc import Callable
from typing import Any

from investiq.core.broker_messages import (
    BracketPrepared, BrokerCommission, BrokerFill, BrokerOperationFailed, BrokerOrderStatus, MarketTrade,
)
from investiq.core.commands import IBSubmitOrder, PrepareBracket
from investiq.core.event_queue import Message
from investiq.core.events import (
    BrokerReturnUnmatched, CommissionReportReceived, FillReceived,
    IBOperationFailed, IntentGenerated, OrderCreated, OrderStatusUpdated, TradeReceived,
)
from investiq.core.handlers.base import HandlerResult
from investiq.core.handlers.bracket_prepared_handler import BracketPreparedHandler
from investiq.core.handlers.broker_return_handler import BrokerReturnHandler
from investiq.core.handlers.ib_command_handlers import IBSubmitOrderHandler, PrepareBracketHandler
from investiq.core.handlers.intent_generated_handler import IntentGeneratedHandler
from investiq.core.handlers.trade_received_handler import TradeReceivedHandler


class Dispatcher:
    def __init__(
        self,
        trade_received_handler: TradeReceivedHandler,
        intent_generated_handler: IntentGeneratedHandler,
        prepare_bracket_handler: PrepareBracketHandler,
        bracket_prepared_handler: BracketPreparedHandler,
        submit_order_handler: IBSubmitOrderHandler,
        broker_return_handler: BrokerReturnHandler,
    ) -> None:
        self._dispatch_table: dict[type, Callable[[Any], HandlerResult]] = {
            TradeReceived: trade_received_handler.handle,
            IntentGenerated: intent_generated_handler.handle,
            PrepareBracket: prepare_bracket_handler.handle,
            BracketPrepared: bracket_prepared_handler.handle,
            IBSubmitOrder: submit_order_handler.handle,
            BrokerOrderStatus: broker_return_handler.handle,
            BrokerFill: broker_return_handler.handle,
            BrokerCommission: broker_return_handler.handle,
            MarketTrade: broker_return_handler.handle,
            BrokerOperationFailed: broker_return_handler.handle,
        }
        self._record_only = {
            OrderCreated, OrderStatusUpdated, FillReceived, CommissionReportReceived,
            IBOperationFailed, BrokerReturnUnmatched,
        }

    def dispatch(self, message: Message) -> HandlerResult:
        if type(message) in self._record_only:
            return HandlerResult()
        return self._dispatch_table[type(message)](message)

    def has_handler(self, message: Message) -> bool:
        return type(message) in self._dispatch_table

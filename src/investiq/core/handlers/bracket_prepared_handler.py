from investiq.core.command_id_generator import CommandIdGenerator
from investiq.core.broker_messages import BracketPrepared
from investiq.core.commands import IBSubmitOrder
from investiq.core.event_factory import EventFactory
from investiq.core.events import OrderCreated
from investiq.core.handlers.base import HandlerResult


class BracketPreparedHandler:
    def __init__(self, event_factory: EventFactory, command_id_generator: CommandIdGenerator) -> None:
        self._event_factory = event_factory
        self._command_id_generator = command_id_generator

    def handle(self, event: BracketPrepared) -> HandlerResult:
        events: list[OrderCreated] = []
        commands: list[IBSubmitOrder] = []
        for order in (event.entry, event.stop_loss, event.take_profit):
            if order is None:
                continue
            events.append(OrderCreated(
                run_id=event.run_id,
                event_id=self._event_factory.next_event_id(),
                intention_id=event.intention_id,
                instrument_id=event.instrument_id,
                order_id=order.order_id,
                parent_id=order.parent_id,
                broker_order_id=order.broker_order_id,
                broker_parent_id=order.broker_parent_id,
                spec=order.spec,
            ))
            commands.append(IBSubmitOrder(
                run_id=event.run_id,
                command_id=self._command_id_generator.next_id(),
                instrument_id=event.instrument_id,
                order_spec=order.spec,
                broker_order_id=order.broker_order_id,
                broker_parent_id=order.broker_parent_id,
                transmit=order.transmit,
            ))
        return HandlerResult(events=tuple(events), commands=tuple(commands))

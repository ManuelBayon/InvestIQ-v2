from investiq.core.command_id_generator import CommandIdGenerator
from investiq.core.commands import OrderToPrepare, PrepareBracket
from investiq.core.events import IntentGenerated
from investiq.core.handlers.base import HandlerResult
from investiq.core.order_id_generator import OrderIdGenerator
from investiq.domain.orders import BracketOrderSpec, LimitOrderSpec, MarketOrderSpec
from investiq.errors import InvalidOrderType


class IntentGeneratedHandler:
    def __init__(
        self,
        order_id_generator: OrderIdGenerator,
        command_id_generator: CommandIdGenerator,
    ) -> None:
        self._order_id_generator = order_id_generator
        self._command_id_generator = command_id_generator

    def handle(self, event: IntentGenerated) -> HandlerResult:
        spec = event.order_spec
        if isinstance(spec, (MarketOrderSpec, LimitOrderSpec)):
            spec = BracketOrderSpec(entry=spec)
        if not isinstance(spec, BracketOrderSpec):
            raise InvalidOrderType(f"Unsupported intent specification: {type(spec).__name__}")

        entry = OrderToPrepare(self._order_id_generator.next_id(), None, spec.entry)
        stop_loss = (
            OrderToPrepare(self._order_id_generator.next_id(), entry.order_id, spec.stop_loss)
            if spec.stop_loss is not None else None
        )
        take_profit = (
            OrderToPrepare(self._order_id_generator.next_id(), entry.order_id, spec.take_profit)
            if spec.take_profit is not None else None
        )
        return HandlerResult(commands=(
            PrepareBracket(
                run_id=event.run_id,
                command_id=self._command_id_generator.next_id(),
                intention_id=event.event_id,
                instrument_id=event.instrument_id,
                entry=entry,
                stop_loss=stop_loss,
                take_profit=take_profit,
            ),
        ))

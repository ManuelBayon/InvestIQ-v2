from investiq.core.command_id_generator import CommandIdGenerator
from investiq.core.commands import PrepareBracket
from investiq.core.event_factory import EventFactory
from investiq.core.handlers.intent_generated_handler import IntentGeneratedHandler
from investiq.core.order_id_generator import OrderIdGenerator
from investiq.domain.orders import BracketOrderSpec, LimitOrderSpec, MarketOrderSpec, StopOrderSpec


def test_handle_bracket_returns_preparation_without_creating_or_submitting_orders():
    handler = IntentGeneratedHandler(OrderIdGenerator(), CommandIdGenerator())
    factory = EventFactory("TEST_RUN")
    intent = factory.create_intent_generated(
        causation_id="EVT_00000",
        instrument_id="MNQZ6",
        order_spec=BracketOrderSpec(
            entry=MarketOrderSpec(side="BUY", quantity=1, tif="DAY"),
            stop_loss=StopOrderSpec(side="SELL", quantity=1, tif="DAY", stop_price=29800),
            take_profit=LimitOrderSpec(side="SELL", quantity=1, tif="DAY", limit_price=30200),
        ),
    )

    result = handler.handle(intent)

    assert result.events == ()
    assert len(result.commands) == 1
    command = result.commands[0]
    assert isinstance(command, PrepareBracket)
    assert command.intention_id == intent.event_id
    assert command.instrument_id == "MNQZ6"
    assert (command.entry.order_id, command.stop_loss.order_id, command.take_profit.order_id) == (1, 2, 3)
    assert command.entry.parent_id is None
    assert command.stop_loss.parent_id == command.take_profit.parent_id == 1

    second = handler.handle(intent).commands[0]
    assert second.entry.order_id == 4
    assert second.command_id != command.command_id

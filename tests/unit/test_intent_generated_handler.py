from unittest.mock import create_autospec

from investiq.adapters.ibkr.ib_broker_adapter import IBAdapter
from investiq.core.event_factory import EventFactory
from investiq.core.events import OrderCreated, OrderRole
from investiq.core.handlers.intent_generated_handler import IntentGeneratedHandler
from investiq.domain.instrument_spec import FutureSpec
from investiq.domain.orders import BracketOrderSpec, MarketOrderSpec, StopLoss, TakeProfit

def test_handle_bracket_order_returns_3_order_created():
    ib_adapter = create_autospec(
        IBAdapter,
        instance=True,
        spec_set=True
    )
    event_factory = EventFactory("TEST_RUN")

    handler = IntentGeneratedHandler(
        ib_adapter=ib_adapter,
        instrument=FutureSpec("MNQ", "MNQZ6", "CME"),
        event_factory=event_factory
    )

    intent = event_factory.create_intent_generated(
        causation_id="EVT_00000",
        order_spec=BracketOrderSpec(
            entry=MarketOrderSpec(1),
            stop_loss=StopLoss(29800),
            take_profit=TakeProfit(30200),
        )
    )

    result = handler.handle(intent)
    assert len(result.events) == 3

    entry = result.events[0]
    assert isinstance(entry, OrderCreated)

    stop_loss = result.events[1]
    assert isinstance(stop_loss, OrderCreated)

    take_profit = result.events[2]
    assert isinstance(take_profit, OrderCreated)

    assert entry.intention_id == intent.event_id
    assert entry.parent_id is None
    assert entry.role == OrderRole.ENTRY

    assert stop_loss.intention_id == intent.event_id
    assert stop_loss.parent_id == entry.order_id
    assert stop_loss.role == OrderRole.STOP_LOSS

    assert take_profit.intention_id == intent.event_id
    assert take_profit.parent_id == entry.order_id
    assert take_profit.role == OrderRole.TAKE_PROFIT


from investiq.domain.decision_layer.base import OrderIntent, DecisionContext
from investiq.domain.order_specs import MarketOrderSpec, Side
from investiq.events.events import IntentGenerated
from tests.helpers.raw_ticks import make_raw_tick


def make_market_order_intent_generated(
        decision_context = DecisionContext(
            last_tick={"symbol": make_raw_tick()},
            last_features={"symbol": {"feature": 100.0}}
        ),
        market_order = MarketOrderSpec(
            direction= Side.BUY,
            quantity=1
        ),
        run_id = "test_run_id",
        event_id = "EVT_00002",
        causation_id = "EVT_0001",
) -> IntentGenerated:
    return IntentGenerated(
        run_id=run_id,
        event_id=event_id,
        causation_id=causation_id,
        meta_data={},
        payload= OrderIntent(
            context=decision_context,
            order_spec= market_order,
        ),
    )


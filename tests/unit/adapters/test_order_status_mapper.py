from ib_insync import OrderStatus

from sandbox.market_order_lifecycle.canonical_execution_events import map_ibkr_order_status
from tests.fixtures.ibkr_status_events import make_presubmitted_order_status


def test_map_presubmitted_order_to_canonical_event():
    order_status = make_presubmitted_order_status()
    event = map_ibkr_order_status(order_status)

    assert event.run_id == "test"
    assert event.event_id == "EVT_00002"
    assert event.causation_id == "EVT_00001"
    assert event.meta_data == {}
    assert event.payload == {}
    assert event.order_id == 277
    assert event.parent_id == 0
    assert event.status == OrderStatus.PreSubmitted
    assert event.broker_perm_id == 2005721994


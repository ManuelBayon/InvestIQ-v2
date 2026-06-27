from ib_insync import OrderStatus

from investiq.events.factory import CanonicalEventFactory
from tests.fixtures.ibkr_status_events import make_presubmitted_order_status


def test_create_order_status_updated_from_ibkr_order_status_fixture():
    factory = CanonicalEventFactory("TEST_RUN")
    order_status = make_presubmitted_order_status()
    event = factory.create_order_status_updated(
        order_id=order_status.orderId,
        parent_id=order_status.parentId,
        status=order_status.status,
        client_id=order_status.clientId,
        broker_perm_id=order_status.permId,
    )

    assert event.run_id == "TEST_RUN"
    assert event.event_id == "EVT_00001"
    assert event.causation_id is None
    assert event.meta_data == {}
    assert event.order_id == 277
    assert event.parent_id == 0
    assert event.client_id == 1
    assert event.status == OrderStatus.PreSubmitted
    assert event.broker_perm_id == 2005721994


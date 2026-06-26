from ib_insync import OrderStatus

from investiq.events.events import OrderStatusUpdated
from investiq.events.factory import CanonicalEventFactory


def map_ibkr_order_status_to_canonical_event(
        status: OrderStatus,
        event_factory: CanonicalEventFactory
) -> OrderStatusUpdated:
    return event_factory.create_order_status_updated(
        order_id=status.orderId,
        parent_id=status.parentId,
        status=status.status,
        client_id=status.clientId,
        broker_perm_id=status.permId,
    )
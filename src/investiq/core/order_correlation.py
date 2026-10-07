from collections.abc import Iterable
from dataclasses import dataclass

from investiq.core.events import CanonicalEvent, OrderCreated


@dataclass(frozen=True)
class OrderAssociation:
    order_id: int
    parent_id: int | None
    broker_order_id: int


class OrderCorrelation:
    """Projection owned exclusively by the canonical thread; one client per run."""

    def __init__(self) -> None:
        self._by_broker: dict[tuple[str, int], OrderAssociation] = {}
        self._by_internal: dict[tuple[str, int], OrderAssociation] = {}

    def apply(self, event: CanonicalEvent) -> None:
        if not isinstance(event, OrderCreated):
            return
        association = OrderAssociation(event.order_id, event.parent_id, event.broker_order_id)
        broker_key = (event.run_id, event.broker_order_id)
        internal_key = (event.run_id, event.order_id)
        for existing in (self._by_broker.get(broker_key), self._by_internal.get(internal_key)):
            if existing is not None and existing != association:
                raise ValueError(f"Conflicting order association: {association}")
        self._by_broker[broker_key] = association
        self._by_internal[internal_key] = association

    def by_broker(self, run_id: str, broker_order_id: int) -> OrderAssociation:
        return self._by_broker[(run_id, broker_order_id)]

    def by_internal(self, run_id: str, order_id: int) -> OrderAssociation:
        return self._by_internal[(run_id, order_id)]

    @classmethod
    def from_events(cls, events: Iterable[CanonicalEvent]) -> "OrderCorrelation":
        projection = cls()
        for event in events:
            projection.apply(event)
        return projection

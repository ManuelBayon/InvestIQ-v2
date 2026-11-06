"""Order status observation after external-to-internal correlation."""

from dataclasses import dataclass
from decimal import Decimal

from investiq.contracts._validation import require_decimal
from investiq.contracts.order_id import OrderId
from investiq.contracts.order_status import OrderStatus


@dataclass(frozen=True, slots=True)
class OrderStatusReceived:
    """Broker-reported order state; repeated observations are permitted.

    Attributes:
        order_id: Internal identity resolved before publication.
        status: Canonical order state resolved by the source adapter.
        filled_quantity: Broker-reported cumulative executed quantity.
        remaining_quantity: Broker-reported open quantity of this order,
            not the remaining portfolio position.

    Quantities must be finite and non-negative. This observation neither
    creates executions nor enforces lifecycle transitions or monotonicity.
    Invalid values raise TypeError or ValueError without implicit coercion.
    """

    order_id: OrderId
    status: OrderStatus
    filled_quantity: Decimal
    remaining_quantity: Decimal

    def __post_init__(self) -> None:
        if not isinstance(self.order_id, OrderId):
            raise TypeError("order_id must be an OrderId")
        if not isinstance(self.status, OrderStatus):
            raise TypeError("status must be an OrderStatus")
        for name in ("filled_quantity", "remaining_quantity"):
            value = getattr(self, name)
            require_decimal(value, name)
            if value < 0:
                raise ValueError(f"{name} must be non-negative")

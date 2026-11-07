"""Normalized broker observations after correlation."""

from dataclasses import dataclass
from decimal import Decimal
from investiq.contracts._validation import require_decimal
from investiq.contracts.identities import OrderId
from investiq.contracts.orders.types import OrderStatus
from datetime import datetime
from investiq.contracts._validation import require_decimal, require_text, require_utc
from investiq.contracts.orders.types import Side
from investiq.contracts._validation import require_decimal, require_text


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


@dataclass(frozen=True, slots=True)
class ExecutionReceived:
    """An individual execution, excluding commissions.

    Attributes:
        order_id: Internal order identity resolved before publication.
        execution_id: Unmodified external execution reference, scoped to
            the broker source configured for the run.
        symbol: Normalized instrument reference, shared with market data.
            Its cross-asset naming convention is defined separately;
            this field is not a raw broker display symbol.
        timestamp_utc: Source execution time normalized to aware UTC.
        side: Reported execution direction normalized to BUY or SELL.
        quantity: Quantity of this execution only, in instrument units.
        price: Execution price excluding commissions, in quotation units.

    Quantity must be finite and positive; price must be finite. Instrument
    matching and tick/lot rules require configuration outside this contract.
    Invalid values raise TypeError or ValueError without implicit coercion.
    """

    order_id: OrderId
    execution_id: str
    symbol: str
    timestamp_utc: datetime
    side: Side
    quantity: Decimal
    price: Decimal

    def __post_init__(self) -> None:
        if not isinstance(self.order_id, OrderId):
            raise TypeError("order_id must be an OrderId")
        require_text(self.execution_id, "execution_id")
        require_text(self.symbol, "symbol")
        require_utc(self.timestamp_utc, "timestamp_utc")
        if not isinstance(self.side, Side):
            raise TypeError("side must be a Side")
        require_decimal(self.quantity, "quantity")
        if self.quantity <= 0:
            raise ValueError("quantity must be strictly positive")
        require_decimal(self.price, "price")


@dataclass(frozen=True, slots=True)
class ExecutionCommissionReceived:
    """Reported commission; may precede its corresponding execution event.

    Attributes:
        execution_id: External execution reference, using the same source
            scope as ExecutionReceived.execution_id.
        commission: Reported finite monetary amount; credits are permitted.
        currency: Normalized reporting currency code.

    No order lookup, accumulation, revision handling or PnL calculation is
    performed here. Source sentinels must be rejected before construction.
    Invalid values raise TypeError or ValueError without implicit coercion.
    """

    execution_id: str
    commission: Decimal
    currency: str

    def __post_init__(self) -> None:
        require_text(self.execution_id, "execution_id")
        require_decimal(self.commission, "commission")
        require_text(self.currency, "currency")

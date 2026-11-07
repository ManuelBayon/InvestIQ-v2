"""Immutable requested characteristics of an individual order."""

from dataclasses import dataclass
from decimal import Decimal

from investiq.contracts._validation import require_decimal, require_text
from investiq.contracts.execution_spec import ExecutionSpec, Limit, Market, StopMarket
from investiq.contracts.side import Side
from investiq.contracts.time_in_force import TimeInForce


@dataclass(frozen=True, slots=True)
class OrderSpec:
    """Describe an order without its identity, lifecycle state or broker IDs.

    Attributes:
        symbol: Normalized instrument reference shared with input events.
        side: Explicit buy or sell direction; quantity is always positive.
        quantity: Total quantity requested for this individual order,
            expressed in instrument units.
        execution: Market, limit or stop-market execution instructions.
        time_in_force: Explicit requested validity policy.

    Construction validates intrinsic invariants without coercion. Instrument
    increments, minimums, broker capabilities and state-dependent constraints
    require separate validation.
    Invalid types raise TypeError; Invalid values raise ValueError.
    This object does not allocate an OrderId.
    """

    symbol: str
    side: Side
    quantity: Decimal
    execution: ExecutionSpec
    time_in_force: TimeInForce

    def __post_init__(self) -> None:
        require_text(self.symbol, "symbol")
        if not isinstance(self.side, Side):
            raise TypeError("side must be a Side")
        require_decimal(self.quantity, "quantity")
        if self.quantity <= 0:
            raise ValueError("quantity must be strictly positive")
        if not isinstance(self.execution, (Market, Limit, StopMarket)):
            raise TypeError("execution must be Market, Limit or StopMarket")
        if not isinstance(self.time_in_force, TimeInForce):
            raise TypeError("time_in_force must be a TimeInForce")

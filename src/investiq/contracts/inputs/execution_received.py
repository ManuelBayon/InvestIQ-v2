"""Normalized individual execution after order correlation."""

from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal

from investiq.contracts._validation import require_decimal, require_text, require_utc
from investiq.contracts.order_id import OrderId
from investiq.contracts.side import Side


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

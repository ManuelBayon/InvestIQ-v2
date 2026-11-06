"""Normalized commission report associated with an execution."""

from dataclasses import dataclass
from decimal import Decimal

from investiq.contracts._validation import require_decimal, require_text


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

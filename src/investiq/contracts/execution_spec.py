"""Requested execution modalities, independent of broker representations."""

from dataclasses import dataclass
from decimal import Decimal
from typing import TypeAlias

from investiq.contracts._validation import require_decimal


@dataclass(frozen=True, slots=True)
class Market:
    """Request execution at available market prices; no price is guaranteed."""


@dataclass(frozen=True, slots=True)
class Limit:
    """Request execution subject to a finite limit_price in quotation units.

    Buy executions must not exceed the limit; sell executions must not be
    below it. Instrument-specific price constraints are validated separately.
    """

    limit_price: Decimal

    def __post_init__(self) -> None:
        require_decimal(self.limit_price, "limit_price")


@dataclass(frozen=True, slots=True)
class StopMarket:
    """Request a market order activated by a stop condition.

    stop_price is a finite threshold in instrument quotation units, not a
    guaranteed execution price. Trigger observation rules are configured and
    validated separately for the execution integration.
    """

    stop_price: Decimal

    def __post_init__(self) -> None:
        require_decimal(self.stop_price, "stop_price")


ExecutionSpec: TypeAlias = Market | Limit | StopMarket

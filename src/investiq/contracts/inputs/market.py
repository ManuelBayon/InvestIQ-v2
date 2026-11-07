"""Normalized market-data inputs."""

from dataclasses import dataclass
from datetime import datetime, timedelta
from decimal import Decimal


@dataclass(frozen=True, slots=True)
class MarketTradeReceived:
    """An individual market transaction, distinct from our order executions.

    Attributes:
        symbol: Normalized instrument reference shared with execution events.
            The cross-asset naming convention is defined separately.
        timestamp_utc: Source transaction time, normalized to aware UTC.
        price: Traded price in the instrument's quotation convention.
        size: Traded quantity in the instrument's unit.

    Reception metadata belongs to a separate envelope. Values must already
    be normalized: construction performs validation, never implicit conversion.
    Instrument-specific constraints are checked by the configured consumer.

    Raises:
        TypeError: A field has an unsupported type.
        ValueError: A field violates an intrinsic contract invariant.
    """

    symbol: str
    timestamp_utc: datetime
    price: Decimal
    size: Decimal

    def __post_init__(self) -> None:
        if not isinstance(self.symbol, str):
            raise TypeError("symbol must be a string")
        if not self.symbol or self.symbol != self.symbol.strip():
            raise ValueError(
                "symbol must be non-empty and contain no surrounding whitespace"
            )

        if not isinstance(self.timestamp_utc, datetime):
            raise TypeError("timestamp_utc must be a datetime")
        if self.timestamp_utc.utcoffset() != timedelta(0):
            raise ValueError("timestamp_utc must be timezone-aware and UTC")

        if not isinstance(self.price, Decimal):
            raise TypeError("price must be a Decimal")
        if not self.price.is_finite():
            raise ValueError("price must be finite")

        if not isinstance(self.size, Decimal):
            raise TypeError("size must be a Decimal")
        if not self.size.is_finite() or self.size <= 0:
            raise ValueError("size must be finite and strictly positive")

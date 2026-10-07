from abc import ABC
from dataclasses import dataclass
from math import isfinite
from typing import Literal


Side = Literal["BUY", "SELL"]


@dataclass(frozen=True)
class OrderSpec(ABC):
    """Canonical specification, independent of the broker API."""


@dataclass(frozen=True)
class SingleOrderSpec(OrderSpec):
    side: Side
    quantity: float
    tif: str

    def __post_init__(self) -> None:
        if self.side not in ("BUY", "SELL"):
            raise ValueError("side must be BUY or SELL")
        if not isfinite(self.quantity) or self.quantity <= 0:
            raise ValueError("quantity must be finite and positive")
        if not self.tif:
            raise ValueError("tif must be explicit")


@dataclass(frozen=True)
class MarketOrderSpec(SingleOrderSpec):
    pass


@dataclass(frozen=True)
class LimitOrderSpec(SingleOrderSpec):
    limit_price: float

    def __post_init__(self) -> None:
        super().__post_init__()
        if not isfinite(self.limit_price):
            raise ValueError("limit_price must be finite")


@dataclass(frozen=True)
class StopOrderSpec(SingleOrderSpec):
    stop_price: float

    def __post_init__(self) -> None:
        super().__post_init__()
        if not isfinite(self.stop_price):
            raise ValueError("stop_price must be finite")


@dataclass(frozen=True)
class BracketOrderSpec(OrderSpec):
    entry: MarketOrderSpec | LimitOrderSpec
    stop_loss: StopOrderSpec | None = None
    take_profit: LimitOrderSpec | None = None

    def __post_init__(self) -> None:
        # Validate runtime construction as well as statically typed callers.
        if not isinstance(self.entry, (MarketOrderSpec, LimitOrderSpec)):  # pyright: ignore[reportUnnecessaryIsInstance]
            raise ValueError("entry must be a MarketOrderSpec or LimitOrderSpec")
        if self.stop_loss is not None and not isinstance(self.stop_loss, StopOrderSpec):  # pyright: ignore[reportUnnecessaryIsInstance]
            raise ValueError("stop_loss must be a StopOrderSpec")
        if self.take_profit is not None and not isinstance(self.take_profit, LimitOrderSpec):  # pyright: ignore[reportUnnecessaryIsInstance]
            raise ValueError("take_profit must be a LimitOrderSpec")
        for exit_spec in (self.stop_loss, self.take_profit):
            if exit_spec is None:
                continue
            if exit_spec.side == self.entry.side:
                raise ValueError("V1 exits must have the opposite side to the entry")
            if exit_spec.quantity != self.entry.quantity:
                raise ValueError("V1 exits must cover the full entry quantity")

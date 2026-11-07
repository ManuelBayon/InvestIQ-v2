"""Entry with optional full-coverage take-profit and stop-loss orders."""

from dataclasses import dataclass

from investiq.contracts.execution_spec import Limit, Market, StopMarket
from investiq.contracts.order_spec import OrderSpec


@dataclass(frozen=True, slots=True)
class BracketSpec:
    """Specify a market/limit entry and at least one opposite-side exit.

    Attributes:
        entry: Market or limit entry order.
        take_profit: Optional limit exit covering the full entry quantity.
        stop_loss: Optional stop-market exit covering the full entry quantity.

    All members refer to the same normalized instrument. Each initial exit
    quantity equals the entry quantity; partial coverage is not supported.

    Execution policy: protect the actual open position from the first entry
    fill. After any exit fill, each active exit's executable remainder must
    follow the remaining position. Keep the entry remainder working after a
    partial exit; subsequent entry fills must also be covered. The two exits
    share the same position and must not intentionally create a reverse one.
    Once a previously opened position is flat, request cancellation of residual
    orders; fills racing cancellation still require position/protection updates.

    This specification validates initial structure only. Dynamic coverage and
    cancellation are obligations of the execution implementation, not guarantees
    enforced by this dataclass. Per-order total quantities may diverge later as
    executions accumulate. Broker support must be verified separately.
    """

    entry: OrderSpec
    take_profit: OrderSpec | None = None
    stop_loss: OrderSpec | None = None

    def __post_init__(self) -> None:
        if not isinstance(self.entry, OrderSpec):
            raise TypeError("entry must be an OrderSpec")
        if not isinstance(self.entry.execution, (Market, Limit)):
            raise ValueError("entry must use Market or Limit execution")
        if self.take_profit is None and self.stop_loss is None:
            raise ValueError("a bracket requires at least one exit")

        for name, order, modality in (
            ("take_profit", self.take_profit, Limit),
            ("stop_loss", self.stop_loss, StopMarket),
        ):
            if order is None:
                continue
            if not isinstance(order, OrderSpec):
                raise TypeError(f"{name} must be an OrderSpec")
            if order.symbol != self.entry.symbol:
                raise ValueError(f"{name} must use the entry instrument")
            if order.side == self.entry.side:
                raise ValueError(f"{name} must oppose the entry side")
            if order.quantity != self.entry.quantity:
                raise ValueError(f"{name} quantity must equal the entry quantity")
            if not isinstance(order.execution, modality):
                raise ValueError(f"{name} must use {modality.__name__} execution")

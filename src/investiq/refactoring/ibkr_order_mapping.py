"""Translate canonical single-order specifications into IBKR orders."""

from decimal import Decimal
from math import isfinite

from ib_insync import LimitOrder, MarketOrder, Order
from ib_insync.util import UNSET_DOUBLE

from investiq.contracts.orders.execution import Limit, Market
from investiq.contracts.orders.specifications import OrderSpec


def _to_ib_number(value: Decimal) -> float:
    """Convert to the client format without changing the decimal value sent."""
    number = float(value)
    if not isfinite(number) or number == UNSET_DOUBLE or Decimal(str(number)) != value:
        raise ValueError(f"Value cannot be represented in an IBKR order: {value}")
    return number


def build_order(
        spec: OrderSpec,
        *,
        broker_id: int,
        client_id: int,
        account: str,
) -> Order:
    """Build a new market or limit order with its preallocated IBKR identity."""

    if broker_id <= 0:
        raise ValueError("An explicit positive IBKR order ID is required")
    if not account.strip():
        raise ValueError("An explicit IBKR account is required")

    action = str(spec.side)
    quantity = _to_ib_number(spec.quantity)
    execution = spec.execution

    if isinstance(execution, Market):
        order = MarketOrder(action, quantity)
    elif isinstance(execution, Limit):
        order = LimitOrder(action, quantity, _to_ib_number(execution.limit_price))
    else:
        raise NotImplementedError(f"Unsupported IBKR execution: {type(execution).__name__}")

    order.orderId = broker_id
    order.clientId = client_id
    order.account = account
    order.tif = str(spec.time_in_force)
    return order

"""Translate canonical single-order specifications into IBKR orders."""

from decimal import Decimal
from math import isfinite

from ib_insync import LimitOrder, MarketOrder, Order, StopOrder
from ib_insync.util import UNSET_DOUBLE

from investiq.contracts.identities import OrderId
from investiq.contracts.orders.execution import Limit, Market, StopMarket
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
    elif isinstance(execution, StopMarket):
        order = StopOrder(action, quantity, _to_ib_number(execution.stop_price))
    else:
        raise NotImplementedError(f"Unsupported IBKR execution: {type(execution).__name__}")

    order.orderId = broker_id
    order.clientId = client_id
    order.account = account
    order.tif = str(spec.time_in_force)
    return order


def build_bracket_orders(
    members: tuple[tuple[OrderId, OrderSpec], ...],
    *,
    broker_ids: dict[OrderId, int],
    client_id: int,
    account: str,
) -> list[tuple[OrderId, Order]]:
    """Build IBKR orders from validated members, with the entry first."""
    entry_id, _ = members[0]
    parent_id = broker_ids[entry_id]
    last_index = len(members) - 1
    prepared: list[tuple[OrderId, Order]] = []

    for index, (order_id, spec) in enumerate(members):
        order = build_order(
            spec,
            broker_id=broker_ids[order_id],
            client_id=client_id,
            account=account,
        )

        if index > 0:
            order.parentId = parent_id

        order.transmit = index == last_index
        prepared.append((order_id, order))

    return prepared
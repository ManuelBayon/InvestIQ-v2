from dataclasses import replace
from decimal import Decimal

import pytest

from investiq.contracts.identities import OrderId
from investiq.contracts.orders.execution import Limit, Market, StopMarket
from investiq.contracts.orders.specifications import OrderSpec
from investiq.contracts.orders.types import Side, TimeInForce
from investiq.refactoring.ibkr_order_mapping import build_bracket_orders


ENTRY_ID = OrderId("entry")
TP_ID = OrderId("take-profit")
SL_ID = OrderId("stop-loss")
BROKER_IDS = {ENTRY_ID: 142, TP_ID: 153, SL_ID: 167}

ENTRY = OrderSpec("AAPL", Side.BUY, Decimal("2"), Market(), TimeInForce.DAY)
LIMIT_ENTRY = replace(ENTRY, execution=Limit(Decimal("100")))
TAKE_PROFIT = replace(ENTRY, side=Side.SELL, execution=Limit(Decimal("105")))
STOP_LOSS = replace(ENTRY, side=Side.SELL, execution=StopMarket(Decimal("95")))


@pytest.mark.parametrize("members,order_types,transmit_flags", [
    pytest.param(
        ((ENTRY_ID, ENTRY), (TP_ID, TAKE_PROFIT)),
        ["MKT", "LMT"], [False, True], id="take-profit-only",
    ),
    pytest.param(
        ((ENTRY_ID, LIMIT_ENTRY), (SL_ID, STOP_LOSS)),
        ["LMT", "STP"], [False, True], id="stop-loss-only",
    ),
    pytest.param(
        ((ENTRY_ID, ENTRY), (TP_ID, TAKE_PROFIT), (SL_ID, STOP_LOSS)),
        ["MKT", "LMT", "STP"], [False, False, True], id="both-exits",
    ),
])
def test_build_bracket_orders(members, order_types, transmit_flags):
    prepared = build_bracket_orders(
        members, broker_ids=BROKER_IDS, client_id=7, account="paper-test",
    )

    assert [(order_id, order.orderId) for order_id, order in prepared] == [
        (order_id, BROKER_IDS[order_id]) for order_id, _ in members
    ]
    assert [order.orderType for _, order in prepared] == order_types
    assert [order.transmit for _, order in prepared] == transmit_flags
    assert [order.parentId for _, order in prepared] == [0] + [BROKER_IDS[ENTRY_ID]] * (
        len(members) - 1
    )

    orders = dict(prepared)
    if TP_ID in orders:
        assert orders[TP_ID].lmtPrice == 105.0
    if SL_ID in orders:
        assert orders[SL_ID].auxPrice == 95.0
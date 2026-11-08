from dataclasses import replace
from decimal import Decimal

import pytest
from ib_insync.util import UNSET_DOUBLE

from investiq.contracts.orders.execution import Limit, Market, StopMarket
from investiq.contracts.orders.specifications import OrderSpec
from investiq.contracts.orders.types import Side, TimeInForce
from investiq.refactoring.ibkr_order_mapping import build_order


MARKET_SPEC = OrderSpec("US:AAPL", Side.BUY, Decimal("1.25"), Market(), TimeInForce.DAY)
ACCOUNT = "paper-test"
CLIENT_ID = 7
BROKER_ID = 142


def test_build_market_order() -> None:
    order = build_order(MARKET_SPEC, broker_id=BROKER_ID, client_id=CLIENT_ID, account=ACCOUNT)

    assert order.orderType == "MKT"
    assert order.action == "BUY"
    assert order.totalQuantity == 1.25
    assert order.tif == "DAY"
    assert (order.orderId, order.clientId, order.account) == (BROKER_ID, CLIENT_ID, ACCOUNT)


def test_build_limit_order() -> None:
    spec = replace(
        MARKET_SPEC,
        side=Side.SELL,
        execution=Limit(Decimal("123.45")),
        time_in_force=TimeInForce.GTC,
    )

    order = build_order(spec, broker_id=BROKER_ID, client_id=CLIENT_ID, account=ACCOUNT)

    assert order.orderType == "LMT"
    assert order.action == "SELL"
    assert order.totalQuantity == 1.25
    assert order.lmtPrice == 123.45
    assert order.tif == "GTC"
    assert (order.orderId, order.clientId, order.account) == (BROKER_ID, CLIENT_ID, ACCOUNT)


@pytest.mark.parametrize("broker_id", [0, -1])
def test_build_order_requires_positive_broker_id(broker_id: int) -> None:
    with pytest.raises(ValueError, match="positive IBKR order ID"):
        build_order(MARKET_SPEC, broker_id=broker_id, client_id=CLIENT_ID, account=ACCOUNT)


@pytest.mark.parametrize("account", ["", "  "])
def test_build_order_requires_explicit_account(account: str) -> None:
    with pytest.raises(ValueError, match="explicit IBKR account"):
        build_order(MARKET_SPEC, broker_id=BROKER_ID, client_id=CLIENT_ID, account=account)


def test_build_order_rejects_stop_market() -> None:
    spec = replace(MARKET_SPEC, execution=StopMarket(Decimal("123.45")))

    with pytest.raises(NotImplementedError, match="StopMarket"):
        build_order(spec, broker_id=BROKER_ID, client_id=CLIENT_ID, account=ACCOUNT)


@pytest.mark.parametrize("value", [
    pytest.param(Decimal("0.1234567890123456789"), id="precision-loss"),
    pytest.param(Decimal("1e309"), id="float-overflow"),
    pytest.param(Decimal(str(UNSET_DOUBLE)), id="ibkr-sentinel"),
])
@pytest.mark.parametrize("field", ["quantity", "limit_price"])
def test_build_order_rejects_numbers_that_cannot_be_sent(field: str, value: Decimal) -> None:
    if field == "quantity":
        spec = replace(MARKET_SPEC, quantity=value)
    else:
        spec = replace(MARKET_SPEC, execution=Limit(value))

    with pytest.raises(ValueError, match="cannot be represented in an IBKR order"):
        build_order(spec, broker_id=BROKER_ID, client_id=CLIENT_ID, account=ACCOUNT)

import pytest
from ib_insync import Order, Trade

from investiq.contracts.identities import OrderId
from investiq.refactoring.ibkr_order_registry import IBKROrderRegistry


ORDER_ID = OrderId("order-1")
CLIENT_ID = 1
BROKER_ORDER_ID = 142


@pytest.fixture
def registry() -> IBKROrderRegistry:
    registry = IBKROrderRegistry()
    registry.reserve(order_id=ORDER_ID, client_id=CLIENT_ID, broker_order_id=BROKER_ORDER_ID)
    return registry


def make_trade(client_id: int = CLIENT_ID, broker_order_id: int = BROKER_ORDER_ID) -> Trade:
    return Trade(order=Order(clientId=client_id, orderId=broker_order_id))


def test_reserved_order_accepts_matching_trade(registry: IBKROrderRegistry) -> None:
    registry.attach_trade(ORDER_ID, make_trade())


@pytest.mark.parametrize("broker_order_id", [0, -1])
def test_reserve_rejects_nonpositive_broker_order_id(broker_order_id: int) -> None:
    registry = IBKROrderRegistry()

    with pytest.raises(ValueError, match="positive IBKR order ID"):
        registry.reserve(order_id=ORDER_ID, client_id=CLIENT_ID, broker_order_id=broker_order_id)


def test_reserve_rejects_duplicate_canonical_order_id(registry: IBKROrderRegistry) -> None:
    with pytest.raises(ValueError, match="Canonical order ID already reserved"):
        registry.reserve(order_id=ORDER_ID, client_id=CLIENT_ID, broker_order_id=BROKER_ORDER_ID + 1)


def test_reserve_rejects_duplicate_broker_identity(registry: IBKROrderRegistry) -> None:
    with pytest.raises(ValueError, match="IBKR order identity already reserved"):
        registry.reserve(
            order_id=OrderId("order-2"), client_id=CLIENT_ID, broker_order_id=BROKER_ORDER_ID,
        )


def test_attach_trade_requires_a_reservation() -> None:
    registry = IBKROrderRegistry()

    with pytest.raises(KeyError):
        registry.attach_trade(ORDER_ID, make_trade())


@pytest.mark.parametrize("client_id,broker_order_id", [
    (CLIENT_ID + 1, BROKER_ORDER_ID),
    (CLIENT_ID, BROKER_ORDER_ID + 1),
])
def test_attach_trade_rejects_mismatched_identity(
    registry: IBKROrderRegistry, client_id: int, broker_order_id: int,
) -> None:
    with pytest.raises(ValueError, match="does not match reserved identity"):
        registry.attach_trade(ORDER_ID, make_trade(client_id, broker_order_id))

    registry.attach_trade(ORDER_ID, make_trade())


def test_attach_trade_accepts_the_same_object_twice(registry: IBKROrderRegistry) -> None:
    trade = make_trade()

    registry.attach_trade(ORDER_ID, trade)
    registry.attach_trade(ORDER_ID, trade)


def test_attach_trade_rejects_replacement_even_with_matching_ids(registry: IBKROrderRegistry) -> None:
    registry.attach_trade(ORDER_ID, make_trade())

    with pytest.raises(ValueError, match="A different Trade is already attached"):
        registry.attach_trade(ORDER_ID, make_trade())

"""Track order identities and local Trade handles on the IBKR loop."""

from dataclasses import dataclass

from ib_insync import Trade

from investiq.contracts.identities import OrderId


@dataclass(slots=True)
class _OrderBinding:
    client_id: int
    broker_order_id: int
    trade: Trade | None = None


class IBKROrderRegistry:
    """Own identity bindings for one session, accessed on its IBKR loop."""

    def __init__(self) -> None:
        self._by_order_id: dict[OrderId, _OrderBinding] = {}
        self._broker_keys: set[tuple[int, int]] = set()

    def reserve(
        self, *, order_id: OrderId, client_id: int, broker_order_id: int,
    ) -> None:
        """Record both identities before attempting submission."""
        if broker_order_id <= 0:
            raise ValueError("An explicit positive IBKR order ID is required")
        broker_key = (client_id, broker_order_id)
        if order_id in self._by_order_id:
            raise ValueError(f"Canonical order ID already reserved: {order_id}")
        if broker_key in self._broker_keys:
            raise ValueError(f"IBKR order identity already reserved: {broker_key}")
        self._by_order_id[order_id] = _OrderBinding(client_id, broker_order_id)
        self._broker_keys.add(broker_key)

    def attach_trade(self, order_id: OrderId, trade: Trade) -> None:
        """Attach the live local handle returned by placeOrder."""
        binding = self._by_order_id[order_id]
        if (trade.order.clientId, trade.order.orderId) != (
            binding.client_id, binding.broker_order_id,
        ):
            raise ValueError(f"Trade does not match reserved identity for {order_id}")
        if binding.trade is not None and binding.trade is not trade:
            raise ValueError(f"A different Trade is already attached to {order_id}")
        binding.trade = trade
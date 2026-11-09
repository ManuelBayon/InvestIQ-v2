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
            self,
            *,
            order_id: OrderId,
            client_id: int,
            broker_order_id: int,
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

    def reserve_many(
            self,
            *,
            client_id: int,
            orders: list[tuple[OrderId, int]],
    ) -> None:
        """Validate all order identities before registering any of them."""
        bindings: dict[OrderId, _OrderBinding] = {}
        broker_keys: set[tuple[int, int]] = set()

        for order_id, broker_id in orders:
            if broker_id <= 0:
                raise ValueError("An explicit positive IBKR order ID is required")
            if order_id in self._by_order_id or order_id in bindings:
                raise ValueError(f"Canonical order ID already reserved: {order_id}")

            key = (client_id, broker_id)
            if key in self._broker_keys or key in broker_keys:
                raise ValueError(f"IBKR order identity already reserved: {key}")

            bindings[order_id] = _OrderBinding(client_id, broker_id)
            broker_keys.add(key)

        self._by_order_id.update(bindings)
        self._broker_keys.update(broker_keys)


    def attach_trade(
            self,
            order_id: OrderId,
            trade: Trade
    ) -> None:
        """Attach the live local handle returned by placeOrder."""
        binding = self._by_order_id[order_id]
        if (trade.order.clientId, trade.order.orderId) != (
            binding.client_id, binding.broker_order_id,
        ):
            raise ValueError(f"Trade does not match reserved identity for {order_id}")
        if binding.trade is not None and binding.trade is not trade:
            raise ValueError(f"A different Trade is already attached to {order_id}")
        binding.trade = trade

    def get_trade(self, order_id: OrderId) -> Trade:
        """Return the Trade attached to a reserved order."""
        trade = self._by_order_id[order_id].trade
        if trade is None:
            raise RuntimeError(f"No IBKR Trade attached to {order_id.value}")
        return trade
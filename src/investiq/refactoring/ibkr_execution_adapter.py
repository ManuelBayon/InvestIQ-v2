"""Dispatch canonical order submissions on the IBKR event loop."""

import asyncio
from collections.abc import Callable

from ib_insync import IB, CommissionReport, Fill, Trade

from investiq.contracts.commands.orders import (
    CancelOrder,
    ModifyOrder,
    SubmitBracket,
    SubmitOrder,
)
from investiq.refactoring.execution_port import ExecutionPort, OrderCommand
from investiq.refactoring.ibkr_instruments import IBKRInstruments
from investiq.refactoring.ibkr_order_mapping import build_order, build_bracket_orders
from investiq.refactoring.ibkr_order_registry import IBKROrderRegistry


class IBKRExecutionAdapter(ExecutionPort):
    """Receive canonical commands and schedule processing on the IBKR loop.

    Construct on the running asyncio loop used to establish the IB connection.
    The bootstrap owns that association and the connection lifecycle. Capturing
    the current loop does not independently establish ownership of the client.

    Only dispatch() may be called from another thread. This increment submits
    individual market and limit orders. The supplied Trade callbacks run on
    the owning IBKR loop and must return promptly.
    """

    def __init__(
        self,
        ib: IB,
        *,
        instruments: IBKRInstruments,
        registry: IBKROrderRegistry,
        account: str,
        on_order_status: Callable[[Trade], None],
        on_fill: Callable[[Trade, Fill], None],
        on_commission_report: Callable[[Trade, Fill, CommissionReport], None],
    ) -> None:
        self._loop = asyncio.get_running_loop()

        if not ib.client.isReady():
            raise ConnectionError("IBKR must be ready before adapter initialization")

        self._ib = ib
        self._client_id = ib.client.clientId
        self._instruments = instruments
        self._registry = registry
        self._account = account
        self._on_order_status = on_order_status
        self._on_fill = on_fill
        self._on_commission_report = on_commission_report

    def dispatch(self, command: OrderCommand) -> None:
        """Schedule a recognized command without waiting for broker acceptance.

        Immediate handoff failures propagate to the caller. Exceptions raised
        later by the scheduled callback reach asyncio's exception handler;
        they cannot propagate to this already completed call.
        """
        if not isinstance(command, (SubmitOrder, SubmitBracket, ModifyOrder, CancelOrder)):
            raise TypeError(f"Unsupported command type: {type(command).__name__}")

        if self._loop.is_closed():
            raise RuntimeError("The IBKR event loop is closed")

        if not self._loop.is_running():
            raise RuntimeError("The IBKR event loop is not running")

        self._loop.call_soon_threadsafe(self._process_command, command)

    def _process_command(self, command: OrderCommand) -> None:
        """Check technical readiness on the owning loop before execution."""
        if asyncio.get_running_loop() is not self._loop:
            raise RuntimeError("Commands must be processed on the owning IBKR loop")

        if not self._ib.client.isReady():
            raise ConnectionError("The IBKR connection is not ready")

        if self._ib.client.clientId != self._client_id:
            raise RuntimeError("The IBKR client identity has changed")

        if isinstance(command, SubmitOrder):
            self._submit_order(command)
            return

        if isinstance(command, SubmitBracket):
            self._submit_bracket(command)
            return

        raise NotImplementedError(
            f"IBKR command execution is not implemented yet: {type(command).__name__}"
        )

    def _subscribe_to_trade(self, trade: Trade) -> None:
        trade.statusEvent += self._on_order_status
        trade.fillEvent += self._on_fill
        trade.commissionReportEvent += self._on_commission_report

    def _submit_order(self, command: SubmitOrder) -> None:
        """Submit an order and subscribe to its Trade on the IBKR loop."""
        contract = self._instruments.resolve(command.spec.symbol)
        broker_order_id = self._allocate_broker_order_id()
        order = build_order(
            command.spec,
            broker_id=broker_order_id,
            client_id=self._client_id,
            account=self._account,
        )

        self._registry.reserve(
            order_id=command.order_id,
            client_id=self._client_id,
            broker_order_id=broker_order_id,
        )

        trade = self._ib.placeOrder(contract, order)
        self._registry.attach_trade(command.order_id, trade)
        self._subscribe_to_trade(trade)


    def _submit_bracket(self, command: SubmitBracket) -> None:
        """Submit a native IBKR bracket on the owning event loop."""
        contract = self._instruments.resolve(command.spec.entry.symbol)
        members = tuple(command.iter_members())

        broker_ids = {
            order_id: self._allocate_broker_order_id()
            for order_id, _ in members
        }

        prepared = build_bracket_orders(
            members,
            broker_ids=broker_ids,
            client_id=self._client_id,
            account=self._account,
        )

        self._registry.reserve_many(
            client_id=self._client_id,
            orders=[(order_id, order.orderId) for order_id, order in prepared],
        )

        for order_id, order in prepared:
            trade = self._ib.placeOrder(contract, order)
            self._registry.attach_trade(order_id, trade)
            self._subscribe_to_trade(trade)


    def _allocate_broker_order_id(self) -> int:
        """Allocate an explicit order ID on the owning IBKR loop."""
        broker_order_id = self._ib.client.getReqId()
        if broker_order_id == 0:
            # placeOrder would replace zero with a newly allocated ID.
            broker_order_id = self._ib.client.getReqId()
        if broker_order_id <= 0:
            raise RuntimeError(f"Invalid IBKR order ID: {broker_order_id}")
        return broker_order_id

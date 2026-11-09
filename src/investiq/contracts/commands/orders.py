"""Canonical order execution requests."""
from collections.abc import Iterator
from dataclasses import dataclass
from investiq.contracts.identities import CommandId
from investiq.contracts.identities import OrderId
from investiq.contracts.orders.specifications import OrderSpec
from investiq.contracts.orders.specifications import BracketSpec
from decimal import Decimal
from investiq.contracts._validation import require_decimal
from investiq.contracts.orders.execution import Limit, StopMarket


@dataclass(frozen=True, slots=True)
class SubmitOrder:
    """Submit spec under a preallocated order_id; command_id identifies the request.

    Construction does not imply broker acceptance or generate identifiers.
    """
    command_id: CommandId
    order_id: OrderId
    spec: OrderSpec

    def __post_init__(self) -> None:
        if not isinstance(self.command_id, CommandId):
            raise TypeError("command_id must be a CommandId")
        if not isinstance(self.order_id, OrderId):
            raise TypeError("order_id must be an OrderId")
        if not isinstance(self.spec, OrderSpec):
            raise TypeError("spec must be an OrderSpec")


@dataclass(frozen=True, slots=True)
class SubmitBracket:
    """Submit a bracket with distinct identities for every present member.

    Exit IDs must exist exactly when their specifications exist. entry_id
    anchors the bracket relationship. Submission is not an atomic acceptance
    guarantee; the adapter must support the requested bracket behavior.
    """
    command_id: CommandId
    entry_id: OrderId
    take_profit_id: OrderId | None
    stop_loss_id: OrderId | None
    spec: BracketSpec

    def __post_init__(self) -> None:
        if not isinstance(self.command_id, CommandId):
            raise TypeError("command_id must be a CommandId")
        if not isinstance(self.entry_id, OrderId):
            raise TypeError("entry_id must be an OrderId")
        if not isinstance(self.spec, BracketSpec):
            raise TypeError("spec must be a BracketSpec")
        ids = [self.entry_id]
        for name, identity, order in (
            ("take_profit_id", self.take_profit_id, self.spec.take_profit),
            ("stop_loss_id", self.stop_loss_id, self.spec.stop_loss),
        ):
            if identity is not None and not isinstance(identity, OrderId):
                raise TypeError(f"{name} must be an OrderId or None")
            if (identity is None) != (order is None):
                raise ValueError(f"{name} must match the presence of its exit")
            if identity is not None:
                ids.append(identity)
        if len(set(ids)) != len(ids):
            raise ValueError("bracket member IDs must be distinct")

    def iter_members(self) -> Iterator[tuple[OrderId, OrderSpec]]:
        """Yield the entry and each configured exit with its canonical ID."""
        yield self.entry_id, self.spec.entry

        for order_id, spec in (
                (self.take_profit_id, self.spec.take_profit),
                (self.stop_loss_id, self.spec.stop_loss),
        ):
            if order_id is not None:
                assert spec is not None  # Guaranteed by __post_init__.
                yield order_id, spec


@dataclass(frozen=True, slots=True)
class ModifyOrder:
    """Modify one existing order, including an individual bracket member.

    total_quantity is the new total target, including prior fills on this
    order. new_execution supplies a new limit or stop price. None means
    unchanged; at least one field must be supplied. Use CancelOrder to cancel.

    The engine must verify the execution modality is unchanged and quantities
    agree with fills, pending requests and bracket coverage. These checks
    require the operational projection and are not performed here.
    """
    command_id: CommandId
    order_id: OrderId
    total_quantity: Decimal | None = None
    new_execution: Limit | StopMarket | None = None

    def __post_init__(self) -> None:
        if not isinstance(self.command_id, CommandId):
            raise TypeError("command_id must be a CommandId")
        if not isinstance(self.order_id, OrderId):
            raise TypeError("order_id must be an OrderId")
        if self.total_quantity is None and self.new_execution is None:
            raise ValueError("at least one modification must be specified")
        if self.total_quantity is not None:
            require_decimal(self.total_quantity, "total_quantity")
            if self.total_quantity <= 0:
                raise ValueError("total_quantity must be strictly positive")
        if self.new_execution is not None and not isinstance(self.new_execution, (Limit, StopMarket)):
            raise TypeError("new_execution must be Limit, StopMarket or None")


@dataclass(frozen=True, slots=True)
class CancelOrder:
    """Request cancellation, without implying broker confirmation.

    order_id targets one order or bracket leg; command_id identifies this
    request. Prior executions remain valid and further fills may race it.
    """
    command_id: CommandId
    order_id: OrderId

    def __post_init__(self) -> None:
        if not isinstance(self.command_id, CommandId):
            raise TypeError("command_id must be a CommandId")
        if not isinstance(self.order_id, OrderId):
            raise TypeError("order_id must be an OrderId")

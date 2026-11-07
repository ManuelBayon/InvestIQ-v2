"""Request an absolute quantity and/or price change for one order."""
from dataclasses import dataclass
from decimal import Decimal
from investiq.contracts._validation import require_decimal
from investiq.contracts.command_id import CommandId
from investiq.contracts.execution_spec import Limit, StopMarket
from investiq.contracts.order_id import OrderId


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

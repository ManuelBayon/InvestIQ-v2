"""Request cancellation of an individual order's unexecuted remainder."""
from dataclasses import dataclass
from investiq.contracts.command_id import CommandId
from investiq.contracts.order_id import OrderId


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

"""Request submission of one identified order."""
from dataclasses import dataclass
from investiq.contracts.command_id import CommandId
from investiq.contracts.order_id import OrderId
from investiq.contracts.order_spec import OrderSpec


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

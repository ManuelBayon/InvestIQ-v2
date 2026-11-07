"""Request submission of identified, linked bracket members."""
from dataclasses import dataclass
from investiq.contracts.bracket_spec import BracketSpec
from investiq.contracts.command_id import CommandId
from investiq.contracts.order_id import OrderId


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

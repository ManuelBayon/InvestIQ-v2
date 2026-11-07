"""Journal representation of an execution command and its causal context."""
from dataclasses import dataclass
from typing import Generic, TypeVar
from investiq.contracts.command_envelope import CommandEnvelope
from investiq.contracts.commands.submit_order import SubmitOrder
from investiq.contracts.commands.submit_bracket import SubmitBracket
from investiq.contracts.commands.modify_order import ModifyOrder
from investiq.contracts.commands.cancel_order import CancelOrder

CommandT = TypeVar("CommandT", SubmitOrder, SubmitBracket, ModifyOrder, CancelOrder)


@dataclass(frozen=True, slots=True)
class RecordedCommand(Generic[CommandT]):
    """Record context with a command; pass only command to the adapter.

    Identity is command.command_id. Journal ordering and persistence are
    external responsibilities; construction performs no side effects.
    """
    envelope: CommandEnvelope
    command: CommandT

    def __post_init__(self) -> None:
        if not isinstance(self.envelope, CommandEnvelope):
            raise TypeError("envelope must be a CommandEnvelope")
        if not isinstance(self.command, (SubmitOrder, SubmitBracket, ModifyOrder, CancelOrder)):
            raise TypeError("command must be a supported execution command")

"""Typed composition of canonical payloads and envelopes."""

from dataclasses import dataclass
from typing import Generic, TypeVar
from investiq.contracts.envelopes import EventEnvelope
from investiq.contracts.inputs.market import MarketTradeReceived
from investiq.contracts.inputs.broker import OrderStatusReceived
from investiq.contracts.inputs.broker import ExecutionReceived
from investiq.contracts.inputs.broker import ExecutionCommissionReceived
from investiq.contracts.envelopes import CommandEnvelope
from investiq.contracts.commands.orders import SubmitOrder
from investiq.contracts.commands.orders import SubmitBracket
from investiq.contracts.commands.orders import ModifyOrder
from investiq.contracts.commands.orders import CancelOrder


PayloadT = TypeVar("PayloadT", MarketTradeReceived, OrderStatusReceived,
                   ExecutionReceived, ExecutionCommissionReceived)


@dataclass(frozen=True, slots=True)
class Event(Generic[PayloadT]):
    """Associate a supported immutable input payload with its envelope.

    Construction validates membership, without normalization or correlation.
    Internal-event transport is outside this input contract.
    """
    envelope: EventEnvelope
    payload: PayloadT

    def __post_init__(self) -> None:
        if not isinstance(self.envelope, EventEnvelope):
            raise TypeError("envelope must be an EventEnvelope")
        if not isinstance(self.payload, (MarketTradeReceived, OrderStatusReceived,
                                         ExecutionReceived, ExecutionCommissionReceived)):
            raise TypeError("payload must be a supported canonical input")


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

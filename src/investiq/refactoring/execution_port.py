"""Broker-independent command handoff boundary."""

from typing import Protocol, TypeAlias

from investiq.contracts.commands.orders import (
    CancelOrder,
    ModifyOrder,
    SubmitBracket,
    SubmitOrder,
)


OrderCommand: TypeAlias = SubmitOrder | SubmitBracket | ModifyOrder | CancelOrder


class ExecutionPort(Protocol):
    """Accept canonical execution requests from the engine.

    The engine validates and journals each command before dispatch. The
    implementation owns broker translation and scheduling on its transport
    thread or event loop. It must not mutate engine projections.
    """

    def dispatch(self, command: OrderCommand) -> None:
        """Hand off a command without waiting for a broker response.

        A normal return means local handoff only, not broker acceptance,
        execution, or confirmation of a modification or cancellation.
        Immediate handoff failures raise an exception. Failures occurring
        after handoff must be surfaced separately by the implementation.
        Broker observations return through the engine's event ingress.
        """
        ...

"""Typed composition of an input payload and its admission metadata."""
from dataclasses import dataclass
from typing import Generic, TypeVar
from investiq.contracts.event_envelope import EventEnvelope
from investiq.contracts.inputs.market_trade_received import MarketTradeReceived
from investiq.contracts.inputs.order_status_received import OrderStatusReceived
from investiq.contracts.inputs.execution_received import ExecutionReceived
from investiq.contracts.inputs.execution_commission_received import ExecutionCommissionReceived

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

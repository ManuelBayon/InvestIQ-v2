from abc import ABC
from dataclasses import dataclass
from datetime import datetime, timezone
from math import isfinite

from investiq.core.broker_messages import BrokerMessage
from investiq.domain.orders import OrderSpec, Side, SingleOrderSpec
from investiq.errors import InvalidTrade


@dataclass(frozen=True)
class CanonicalEvent(ABC):
    run_id: str
    event_id: str


@dataclass(frozen=True)
class ExternalEvent(CanonicalEvent):
    pass


@dataclass(frozen=True)
class InternalEvent(CanonicalEvent):
    pass


@dataclass(frozen=True)
class MarketDataEvent(ExternalEvent):
    pass


@dataclass(frozen=True)
class TradeReceived(MarketDataEvent):
    symbol: str
    timestamp_utc: datetime
    price: float
    size: float

    def __post_init__(self):
        if self.timestamp_utc.tzinfo is not timezone.utc:
            raise InvalidTrade("timestamp must be in UTC use datetime.timezone.utc")
        if self.price < 0 or not isfinite(self.price):
            raise InvalidTrade(f"price must be a finite non-negative float: price={self.price}")
        if self.size < 0:
            raise InvalidTrade(f"size must be non-negative: size={self.size}")


@dataclass(frozen=True)
class IntentGenerated(InternalEvent):
    causation_id: str
    instrument_id: str
    order_spec: OrderSpec


@dataclass(frozen=True)
class OrderCreated(InternalEvent):
    intention_id: str
    instrument_id: str
    order_id: int
    parent_id: int | None
    broker_order_id: int
    broker_parent_id: int
    spec: SingleOrderSpec


@dataclass(frozen=True)
class OrderStatusUpdated(ExternalEvent):
    order_id: int
    parent_id: int | None
    status: str


@dataclass(frozen=True)
class FillReceived(ExternalEvent):
    order_id: int
    parent_id: int | None
    exec_id: str
    timestamp_utc: datetime
    qty_executed: float
    side: Side
    price: float
    cumul_qty: float


@dataclass(frozen=True)
class CommissionReportReceived(ExternalEvent):
    order_id: int
    parent_id: int | None
    exec_id: str
    commission: float
    currency: str
    realized_pnl: float


@dataclass(frozen=True)
class IBOperationFailed(InternalEvent):
    command_id: str
    operation: str
    error: str


@dataclass(frozen=True)
class BrokerReturnUnmatched(InternalEvent):
    message: BrokerMessage

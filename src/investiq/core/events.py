from abc import ABC
from dataclasses import dataclass
from datetime import datetime, timezone
from math import isfinite

from investiq.domain.orders import OrderSpec
from investiq.errors import InvalidTrade


@dataclass(frozen=True)
class CanonicalEvent(ABC):
    run_id: str
    event_id: str


@dataclass(frozen=True)
class ExternalEvent(CanonicalEvent):
    ...

@dataclass(frozen=True)
class InternalEvent(CanonicalEvent):
    ...


@dataclass(frozen=True)
class MarketDataEvent(ExternalEvent):
    ...


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
    def __repr__(self) -> str:
        return (
            f"{self.event_id} "
            f"TradeReceived : "
            f"symbol={self.symbol}, "
            f"timestamp_utc={self.timestamp_utc}, "
            f"price={self.price}, "
            f"size={self.size}"
        )


@dataclass(frozen=True)
class OrderStatusUpdated(ExternalEvent):
    broker_id: int
    broker_parent_id: int
    status: str

    def __repr__(self) -> str:
        return (
            f"{self.event_id} "
            f"OrderStatusUpdated : "
            f"broker_id={self.broker_id}, "
            f"broker_parent_id={self.broker_parent_id}, "
            f"status={self.status}, "
        )


@dataclass(frozen=True)
class FillReceived(ExternalEvent):
    order_id: int
    parent_id: int
    exec_id:str
    timestamp_utc: datetime
    qty_executed: float
    side: str
    price: float
    cumul_qty: float


    def __repr__(self) -> str:
        return (
            f"{self.event_id} "
            f"FillReceived : "
            f"order_id={self.order_id}, "
            f"parent_id={self.parent_id}, "
            f"exec_id={self.exec_id}, "
            f"timestamp={self.timestamp_utc}, "
            f"qty_executed={self.qty_executed}, "
            f"side={self.side}, "
            f"price={self.price}, "
            f"cumul_qty={self.cumul_qty}"
        )


@dataclass(frozen=True)
class CommissionReportReceived(ExternalEvent):
    order_id: int
    parent_id: int
    exec_id: str
    commission: float
    currency: str
    realized_pnl: float

    def __repr__(self) -> str:
        return (
            f"{self.event_id} "
            f"CommissionReport : "
            f"order_id={self.order_id}, "
            f"parent_id={self.parent_id}, "
            f"exec_id={self.exec_id}, "
            f"commission={self.commission}, "
            f"currency={self.currency}, "
            f"realized_pnl={self.realized_pnl}"
        )


@dataclass(frozen=True)
class IntentGenerated(InternalEvent):
    causation_id: str
    spec: OrderSpec
    def __repr__(self) -> str:
        return (
            f"{self.event_id} "
            f"IntentGenerated : "
            f"causation_id={self.causation_id}, "
            f"spec={self.spec}"
        )
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
    order_id: int
    parent_id: int
    status: str
    client_id: int
    perm_id: int

    def __repr__(self) -> str:
        return (
            f"{self.event_id} "
            f"OrderStatusUpdated : "
            f"order_id={self.order_id}, "
            f"parent_id={self.parent_id}, "
            f"status={self.status}, "
            f"client_id={self.client_id}, "
            f"perm_id={self.perm_id}"
        )


@dataclass(frozen=True)
class FillReceived(ExternalEvent):
    order_id: int
    parent_id: int
    client_id: int
    perm_id: int
    exec_id: str
    timestamp_utc: datetime
    account_num: str
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
            f"client_id={self.client_id}, "
            f"perm_id={self.perm_id}, "
            f"exec_id={self.exec_id}, "
            f"timestamp={self.timestamp_utc}, "
            f"account_num={self.account_num}, "
            f"qty_executed={self.qty_executed}, "
            f"side={self.side}, "
            f"price={self.price}, "
            f"cumul_qty={self.cumul_qty}"
        )


@dataclass(frozen=True)
class CommissionReportReceived(ExternalEvent):
    order_id: int
    parent_id: int
    client_id: int
    perm_id: int
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
            f"perm_id={self.perm_id}, "
            f"exec_id={self.exec_id}, "
            f"commission={self.commission}, "
            f"currency={self.currency}, "
            f"realized_pnl={self.realized_pnl}"
        )


@dataclass(frozen=True)
class IntentGenerated(InternalEvent):
    causation_id: str
    order_spec: OrderSpec
    def __repr__(self) -> str:
        return (
            f"{self.event_id} "
            f"IntentGenerated : "
            f"causation_id={self.causation_id}, "
            f"order={self.order_spec}"
        )
from abc import ABC
from dataclasses import dataclass
from datetime import datetime, timezone
from enum import StrEnum, auto
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

class OrderRole(StrEnum):
    ENTRY = auto()
    STOP_LOSS = auto()
    TAKE_PROFIT = auto()


@dataclass(frozen=True, slots=True)
class OrderCreated(InternalEvent):
    intention_id: str
    order_id: int
    parent_id: int | None
    role: OrderRole
from abc import ABC
from dataclasses import dataclass
from datetime import datetime, timezone
from math import isfinite

from investiq.domain.order_types import Order
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
            f"\nTradeReceived(\n"
            f"\trun_id={self.run_id},\n"
            f"\tevent_id={self.event_id},\n"
            f"\tsymbol={self.symbol},\n"
            f"\ttimestamp_utc={self.timestamp_utc:%Y-%m-%dT%H:%M:%S.%f}Z,\n"
            f"\tprice={self.price},\n"
            f"\tsize={self.size}\n"
            f")"
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
            f"\nOrderStatusUpdated(\n"
            f"\torder_id={self.order_id}\n"
            f"\tparent_id={self.parent_id}\n"
            f"\tstatus={self.status}\n"
            f"\tclient_id={self.client_id}\n"
            f"\tperm_id={self.perm_id}\n"
            f")"
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
            f"\nFillReceived(\n"
            f"\torder_id={self.order_id}\n"
            f"\tparent_id={self.parent_id}\n"
            f"\tclient_id={self.client_id}\n"
            f"\tperm_id={self.perm_id}\n"
            f"\texec_id={self.exec_id}\n"
            f"\taccount_num={self.account_num}\n"
            f"\ttimestamp_utc={self.timestamp_utc}\n"
            f"\tqty_executed={self.qty_executed}\n"
            f"\tside={self.side}\n"
            f"\tprice={self.price}\n"
            f"\tcumul_qty={self.cumul_qty}\n"
            f")"
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
            f"\nCommissionReportReceived(\n"
            f"\torder_id={self.order_id}\n"
            f"\tparent_id={self.parent_id}\n"
            f"\tclient_id={self.client_id}\n"
            f"\tperm_id={self.perm_id}\n"
            f"\texec_id={self.exec_id}\n"
            f"\tcommission={self.commission}\n"
            f"\tcurrency={self.currency}\n"
            f"\trealized_pnl={self.realized_pnl}\n"
            f")"
        )


@dataclass(frozen=True)
class OrderGenerated(InternalEvent):
    order: Order
    def __repr__(self) -> str:
        return (
            f"\nOrderGenerated(\n"
            f"\trun_id={self.run_id}\n"
            f"\tevent_id={self.event_id}\n"
            f"\torder={self.order}\n"
            f")"
        )
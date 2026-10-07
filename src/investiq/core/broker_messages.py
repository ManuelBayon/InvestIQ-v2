"""Immutable copies of IB callbacks; correlation belongs to the canonical thread."""
from dataclasses import dataclass
from datetime import datetime

from investiq.core.commands import PreparedOrder
from investiq.domain.orders import Side


@dataclass(frozen=True)
class BrokerOrderStatus:
    run_id: str
    broker_order_id: int
    status: str


@dataclass(frozen=True)
class BrokerFill:
    run_id: str
    broker_order_id: int
    exec_id: str
    timestamp_utc: datetime
    qty_executed: float
    side: Side
    price: float
    cumul_qty: float


@dataclass(frozen=True)
class BrokerCommission:
    run_id: str
    broker_order_id: int
    exec_id: str
    commission: float
    currency: str
    realized_pnl: float


@dataclass(frozen=True)
class MarketTrade:
    run_id: str
    symbol: str
    timestamp_utc: datetime
    price: float
    size: float


@dataclass(frozen=True)
class BracketPrepared:
    run_id: str
    preparation_id: str
    intention_id: str
    instrument_id: str
    entry: PreparedOrder
    stop_loss: PreparedOrder | None = None
    take_profit: PreparedOrder | None = None


@dataclass(frozen=True)
class BrokerOperationFailed:
    run_id: str
    command_id: str
    operation: str
    error: str


BrokerMessage = BrokerOrderStatus | BrokerFill | BrokerCommission
InboundMessage = BrokerMessage | MarketTrade | BracketPrepared | BrokerOperationFailed

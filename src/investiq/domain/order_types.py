from abc import ABC
from dataclasses import dataclass


@dataclass(frozen=True)
class Order(ABC):
    ...


@dataclass(frozen=True, slots=True)
class MarketOrder(Order):
    symbol: str
    quantity: float


@dataclass(frozen=True, slots=True)
class LimitOrder(Order):
    symbol: str
    quantity: float
    price: float


@dataclass(frozen=True, slots=True)
class StopLoss:
    price: float


@dataclass(frozen=True, slots=True)
class TakeProfit:
    price: float


@dataclass(frozen=True, slots=True)
class BracketOrder(Order):
    entry: MarketOrder | LimitOrder
    stop_loss: StopLoss
    take_profit: TakeProfit
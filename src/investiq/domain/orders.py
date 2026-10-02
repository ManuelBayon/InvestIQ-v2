from abc import ABC
from dataclasses import dataclass

@dataclass(frozen=True, slots=True)
class StopLoss:
    price: float
    def __repr__(self) -> str:
        return f"StopLoss(price={self.price})"


@dataclass(frozen=True, slots=True)
class TakeProfit:
    price: float
    def __repr__(self) -> str:
        return f"TakeProfit(price={self.price})"


@dataclass(frozen=True)
class OrderSpec(ABC):
    ...


@dataclass(frozen=True, slots=True)
class MarketOrderSpec(OrderSpec):
    quantity: float
    def __repr__(self) -> str:
        return f"MarketOrder(quantity={self.quantity})"


@dataclass(frozen=True, slots=True)
class LimitOrderSpec(OrderSpec):
    quantity: float
    price: float
    def __repr__(self) -> str:
        return f"LimitOrder(quantity={self.quantity}, price={self.price})"


@dataclass(frozen=True, slots=True)
class BracketOrderSpec(OrderSpec):
    entry: MarketOrderSpec | LimitOrderSpec
    stop_loss: StopLoss | None = None
    take_profit: TakeProfit | None = None
    def __repr__(self) -> str:
        return f"Bracket({self.entry}, SL={self.stop_loss}, TP={self.take_profit})"
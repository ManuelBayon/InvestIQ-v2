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
class Order(ABC):
    ...


@dataclass(frozen=True, slots=True)
class MarketOrderSpec(Order):
    quantity: float
    def __repr__(self) -> str:
        return f"MarketOrder(quantity={self.quantity})"


@dataclass(frozen=True, slots=True)
class LimitOrderSpec(Order):
    quantity: float
    price: float
    def __repr__(self) -> str:
        return f"LimitOrder(quantity={self.quantity}, price={self.price})"


@dataclass(frozen=True, slots=True)
class BracketOrderSpec(Order):
    entry: MarketOrderSpec | LimitOrderSpec
    stop_loss: StopLoss | None = None
    take_profit: TakeProfit | None = None
    def __repr__(self) -> str:
        return f"BracketOrder(entry={self.entry}, stop_loss={self.stop_loss}, take_profit={self.take_profit})"
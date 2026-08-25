from abc import ABC
from dataclasses import dataclass


@dataclass(frozen=True)
class Order(ABC):
    ...


@dataclass(frozen=True, slots=True)
class MarketOrder(Order):
    symbol: str
    quantity: float
    def __repr__(self) -> str:
        return f"MarketOrder(symbol={self.symbol}, quantity={self.quantity})"


@dataclass(frozen=True, slots=True)
class LimitOrder(Order):
    symbol: str
    quantity: float
    price: float
    def __repr__(self) -> str:
        return f"LimitOrder(symbol={self.symbol}, quantity={self.quantity}, price={self.price})"



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


@dataclass(frozen=True, slots=True)
class BracketOrder(Order):
    entry: MarketOrder | LimitOrder
    stop_loss: StopLoss
    take_profit: TakeProfit
    def __repr__(self) -> str:
        return f"BracketOrder(entry={self.entry}, stop_loss={self.stop_loss}, take_profit={self.take_profit})"
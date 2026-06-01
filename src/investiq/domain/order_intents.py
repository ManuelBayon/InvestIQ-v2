from abc import ABC
from dataclasses import dataclass
from enum import Enum, auto
from math import isfinite

class Side(Enum):
    BUY = auto()
    SELL = auto()

@dataclass(frozen=True)
class Intent(ABC):
    ...

@dataclass(frozen=True)
class MarketOrderIntent(Intent):
    quantity: float
    direction : Side
    def __post_init__(self):
        if not isfinite(self.quantity):
            raise ValueError(f"quantity must be finite, got quantity={self.quantity}")
        if not self.quantity > 0:
            raise ValueError(f"quantity must be positive, got quantity={self.quantity}")

@dataclass(frozen=True)
class LimitOrderIntent(Intent):
    quantity: float
    direction: Side
    price: float
    def __post_init__(self):
        if not isfinite(self.quantity):
            raise ValueError(f"quantity must be finite, got quantity={self.quantity}")
        if not self.quantity > 0:
            raise ValueError(f"quantity must be positive, got quantity={self.quantity}")
        if not isfinite(self.price):
            raise ValueError(f"price must be finite, got price={self.quantity}")
        if not self.price > 0:
            raise ValueError(f"price must be positive, got price={self.quantity}")


@dataclass(frozen=True)
class StopMarketOrderIntent(Intent):
    trigger_price: float
    triggered_order : MarketOrderIntent
    def __post_init__(self):
        if not isfinite(self.trigger_price):
            raise ValueError(f"trigger_price must be finite, got trigger_price={self.trigger_price}")
        if not self.trigger_price > 0:
            raise ValueError(f"trigger_price must be positive, got trigger_price={self.trigger_price}")

@dataclass(frozen=True)
class BracketOrderIntent(Intent):
    entry: MarketOrderIntent | LimitOrderIntent
    stop_loss: list[StopMarketOrderIntent] | None
    take_profit: list[LimitOrderIntent] | None
    def __post_init__(self):

        if not self.take_profit and not self.stop_loss:
            raise ValueError("Must have at leat one stop_loss or one take_profit otherwise don't use brackets.")

        for i, sl in enumerate(self.stop_loss or []):
            if sl.triggered_order.direction == self.entry.direction:
                raise ValueError(f"stop_loss(i={i}) direction must be opposite to entry, got direction={sl.triggered_order.direction}")

        for i, tp in enumerate(self.take_profit or []):
            if tp.direction == self.entry.direction:
                raise ValueError(f"take_profit(i={i}) direction must be opposite to entry, got direction={tp.direction}")

        sl_quantity = sum(sl.triggered_order.quantity for sl in self.stop_loss or [])
        if sl_quantity > self.entry.quantity:
            raise ValueError(
                f"stop_loss total quantity can't be greater than entry quantity: "
                f"entry.quantity={self.entry.quantity}"
                f"stop_loss total quantity={sl_quantity}")

        tp_quantity = sum(tp.quantity for tp in self.take_profit or [])
        if tp_quantity > self.entry.quantity:
            raise ValueError(
                f"take_profit total quantity can't be greater than entry quantity: "
                f"entry.quantity={self.entry.quantity}"
                f"take_profit total quantity={tp_quantity}")
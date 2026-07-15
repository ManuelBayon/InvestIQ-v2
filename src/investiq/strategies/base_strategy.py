from dataclasses import dataclass
from decimal import Decimal
from typing import Protocol, TypeVar


@dataclass
class TradingIntent:
    strategy_id: str
    symbol: str
    target: Decimal


class Strategy(Protocol):
    def decide(self, *args, **kwargs) -> list[TradingIntent]:
        ...
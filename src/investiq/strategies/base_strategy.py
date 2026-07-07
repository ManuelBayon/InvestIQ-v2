from dataclasses import dataclass
from decimal import Decimal
from typing import Protocol, TypeVar


@dataclass
class TradingIntent:
    strategy_id: str
    symbol: str
    target: Decimal


SnapshotT = TypeVar("SnapshotT")
class Strategy[SnapshotT](Protocol):
    def decide(self, snapshot: SnapshotT) -> list[TradingIntent]:
        ...
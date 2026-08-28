from abc import ABC
from dataclasses import dataclass


@dataclass(frozen=True)
class InstrumentSpec(ABC):
    symbol: str

@dataclass(frozen=True)
class StockSpec(InstrumentSpec):
    exchange: str = "SMART"
    currency: str = "USD"

@dataclass(frozen=True)
class FutureSpec(InstrumentSpec):
    local_symbol: str
    exchange: str = "CME"
    currency: str = "USD"
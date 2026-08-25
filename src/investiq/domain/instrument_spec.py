from abc import ABC
from dataclasses import dataclass


@dataclass(frozen=True)
class InstrumentSpec(ABC):
    ...

@dataclass(frozen=True)
class StockSpec(InstrumentSpec):
    symbol: str
    exchange: str = "SMART"
    currency: str = "USD"

@dataclass(frozen=True)
class FutureSpec(InstrumentSpec):
    symbol: str
    local_symbol: str
    exchange: str = "CME"
    currency: str = "USD"
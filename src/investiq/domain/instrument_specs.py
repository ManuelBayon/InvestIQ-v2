from abc import ABC
from dataclasses import dataclass


@dataclass(frozen=True)
class InstrumentSpec(ABC):
    ...

@dataclass(frozen=True)
class StockSpecs(InstrumentSpec):
    symbol: str
    exchange: str = "SMART"
    currency: str = "USD"

@dataclass(frozen=True)
class FutureSpecs(InstrumentSpec):
    symbol: str
    local_symbol: str
    exchange: str = "CME"
    currency: str = "USD"
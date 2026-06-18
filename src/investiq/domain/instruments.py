from abc import ABC
from dataclasses import dataclass


@dataclass(frozen=True)
class InstrumentSpecs(ABC):
    ...

@dataclass(frozen=True)
class StockSpecs(InstrumentSpecs):
    symbol: str
    exchange: str = "SMART"
    currency: str = "USD"

@dataclass(frozen=True)
class FutureSpecs(InstrumentSpecs):
    symbol: str
    local_symbol: str
    exchange: str = "CME"
    currency: str = "USD"
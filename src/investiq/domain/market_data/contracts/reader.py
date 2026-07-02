from typing import runtime_checkable, Protocol

from investiq.events.events import MarketDataEvent


@runtime_checkable
class MarketStoreReader(Protocol):

    def window(self, symbol: str, n: int) -> tuple[MarketDataEvent, ...]:
        ...

    def symbols(self) -> set[str]:
        ...

    def has_at_least(self, symbol: str, n: int) -> bool:
        ...
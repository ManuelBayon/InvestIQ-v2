from typing import Protocol, TypeVar, runtime_checkable

from investiq.events.events import MarketDataEvent

@runtime_checkable
class MarketStore(Protocol):

    def ingest(self, event: MarketDataEvent) -> None:
        ...

    @property
    def symbols(self) -> tuple[str, ...]:
        ...

    def has_at_least(self, symbol: str, n: int) -> bool:
        ...

    def window(self, symbol: str, n: int) -> tuple[MarketDataEvent, ...]:
        ...
from typing import Protocol, TypeVar, runtime_checkable

from investiq.events.events import MarketDataEvent

TMarketEvent = TypeVar("TMarketEvent", bound=MarketDataEvent)

@runtime_checkable
class MarketStore(Protocol):

    def append(self, event: TMarketEvent) -> None:
        ...

    @property
    def symbols(self) -> set[str]:
        ...

    def window(self, symbol: str, n: int) -> tuple[TMarketEvent, ...]:
        ...

    def has_at_least(self, symbol: str, n: int) -> bool:
        ...
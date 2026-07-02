from typing import TypeVar, Protocol, runtime_checkable

from investiq.events.events import MarketDataEvent

E = TypeVar("E", bound=MarketDataEvent)
V = TypeVar("V")

@runtime_checkable
class Calculator(Protocol[E, V]):
    name: str
    window: int
    def calculate(self, events: tuple[E, ...]) -> V:
        ...
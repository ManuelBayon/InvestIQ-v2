from typing import TypeVar, Protocol, runtime_checkable

E = TypeVar("E")
V = TypeVar("V")

@runtime_checkable
class Calculator(Protocol[E, V]):
    def calculate(self, events: tuple[E, ...]) -> V:
        ...
from typing import runtime_checkable, Protocol, TypeVar

E = TypeVar("E")
V = TypeVar("V")

@runtime_checkable
class Feature(Protocol[E, V]):
    def compute(self, value: E) -> None:...
    @property
    def is_ready(self) -> bool:...
    @property
    def value(self) -> V:...
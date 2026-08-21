from typing import Protocol

class Ingress(Protocol):

    def start(self) -> None:
        ...
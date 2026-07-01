from abc import ABC
from dataclasses import dataclass


@dataclass(frozen=True)
class Command(ABC):
    ...

@dataclass(frozen=True)
class BrokerCommand(Command):
    run_id: str
    command_id: str
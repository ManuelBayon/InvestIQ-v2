from dataclasses import dataclass
from typing import Protocol

from investiq.domain.experiment import ExperimentSpec


class Runtime(Protocol):
    def run(self) -> None:
        ...

@dataclass(frozen=True)
class RuntimeConfig:
    experiment: ExperimentSpec

from abc import ABC
from dataclasses import dataclass

from investiq.domain.instrument_specs import InstrumentSpecs


@dataclass(frozen=True, slots=True)
class Order(ABC):
    instrument: InstrumentSpecs
    tif: str
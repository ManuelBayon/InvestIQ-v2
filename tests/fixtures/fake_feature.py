from collections.abc import Sequence

from investiq.domain.features.features import Feature
from investiq.domain.features.sources import Source


class FakeFeature:
    def __init__(
            self,
            name: str,
            sources: list[Source],
            emissions: list[bool],
    ):
        self.sources = sources
        self._emissions = emissions
        self._successors: list[Feature] = []
        self._index = 0
        self.name = name

    def compute(self) -> bool:
        result = self._emissions[self._index % len(self._emissions)]
        self._index += 1
        return result

    def load(self, window: int) -> Sequence[float]:
        return []

    @property
    def successors(self) -> list["Feature"]:
        return self._successors
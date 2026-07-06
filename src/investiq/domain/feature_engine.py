from collections.abc import Mapping
from dataclasses import dataclass
from types import MappingProxyType
from typing import Protocol, runtime_checkable, TypeVar

from investiq.events.trade_received import TradeReceived

E = TypeVar("E")
V = TypeVar("V")

@runtime_checkable
class Feature(Protocol[E, V]):
    def compute(self, event: E) -> None:...
    @property
    def is_ready(self) -> bool:...
    @property
    def value(self) -> V:...


@dataclass(frozen=True)
class FeatureSet:
    """
    Declare a set of features for a given symbol.
    """
    symbol: str
    features: dict[str, Feature]


@dataclass(frozen=True)
class FeatureSnapshot:
    """

    """
    data: Mapping[str, Mapping[str, object]]


class FeatureEngine:
    """
    Multi-symbol, multi-features Feature engine.
    """
    def __init__(self, feature_sets: list[FeatureSet]):
        _registry: dict[str, FeatureSet] = {}
        for fs in feature_sets:
            if fs.symbol in _registry:
                raise ValueError(
                    f"Duplicate FeatureSet for symbol={fs.symbol}."
                )
            _registry[fs.symbol] = fs
        self._registry: MappingProxyType[str, FeatureSet] = MappingProxyType(_registry)


    def update(self, event: TradeReceived) -> None:
        fs = self._registry.get(event.symbol)
        if fs is None:
            raise KeyError(
                f"symbol={event.symbol} is not recognized. "
                f"Available symbols={self._registry}"
            )
        for feature in fs.features.values():
            feature.compute(event)


    def _get_feature(self, symbol: str, feature_name: str) -> Feature:
        fs = self._registry.get(symbol)
        if fs is None:
            raise KeyError(
                f"symbol={symbol} is not recognized. "
                f"Available symbols={self._registry.keys()}"
            )
        feature = fs.features.get(feature_name)
        if feature is None:
            raise KeyError(
                f"feature={feature_name} is not recognized in FeatureSet for symbol={symbol}. "
                f"Available features={[f for f in fs.features]}"
            )
        return feature


    @property
    def snapshot(self) -> FeatureSnapshot:
        data = {}

        for symbol, feature_set in self._registry.items():
            values = {
                name: feature.value
                for name, feature in feature_set.features.items()
            }
            data[symbol] = MappingProxyType(values)

        return FeatureSnapshot(
            data=MappingProxyType(data)
        )
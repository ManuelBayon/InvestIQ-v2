from types import MappingProxyType

from investiq.domain.features.feature_set import FeatureSet
from investiq.domain.features.protocol import Feature

from investiq.events.market_data import TradeReceived


class FeatureEngine:

    def __init__(self, feature_sets: list[FeatureSet]):
        _registry = {}
        for fs in feature_sets:
            if fs.symbol in _registry:
                raise ValueError(
                    f"Duplicate FeatureSet for symbol={fs.symbol}."
                )
            _registry[fs.symbol] = fs
        self._registry = MappingProxyType(_registry)


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


    def is_ready(self, symbol: str, feature_name: str) -> bool:
        return self._get_feature(symbol, feature_name).is_ready


    def value(self, symbol: str, feature_name: str) -> object:
        return self._get_feature(symbol, feature_name).value

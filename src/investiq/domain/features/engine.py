from types import MappingProxyType

from investiq.domain.features.feature_set import FeatureSet
from investiq.domain.features.protocol import Feature

from investiq.events.market_data import TradeReceived


class FeatureEngine:

    def __init__(self, feature_set: list[FeatureSet]):
        self._registry = MappingProxyType({
            f.symbol: f for f in feature_set
        })


    def update(self, event: TradeReceived) -> None:
        symbol = event.symbol
        if symbol not in self._registry:
            raise KeyError(
                f"symbol={symbol} is not recognized. "
                f"Available symbols={self._registry}"
            )

        for feature in self._registry[symbol].features.values():
            feature.compute(event)


    def _get_feature(self, symbol: str, feature_name: str) -> Feature:
        feature_set = self._registry.get(symbol)
        if feature_set is None:
            raise KeyError(
                f"symbol={symbol} is not recognized. "
                f"Available symbols={self._registry}"
            )

        feature = feature_set.features.get(feature_name)
        if feature is None:
            raise KeyError(
                f"feature={feature_name} is not recognized in FeatureSet for symbol={symbol}. "
                f"Available features={[f for f in feature_set.features]}"
            )
        return feature


    def is_ready(self, symbol: str, feature_name: str) -> bool:
        return self._get_feature(symbol, feature_name).is_ready


    def value(self, symbol: str, feature_name: str) -> object:
        return self._get_feature(symbol, feature_name).value

from investiq.domain.features.caculators.base import Calculator
from investiq.domain.features.point import FeaturePoint
from investiq.domain.features.store import FeatureStore
from investiq.domain.market_data.readers.in_memory_market_data_reader import InMemoryMarketDataReader


class FeaturePipeline:

    def __init__(
            self,
            calculators: list[Calculator],
            market_data_reader: InMemoryMarketDataReader,
            feature_store: FeatureStore,
    ):
        self._calculators = calculators
        self._market_data_reader = market_data_reader
        self._feature_store = feature_store


    def update(self) -> list[FeaturePoint]:
        points_updated = []
        for symbol in self._market_data_reader.symbols:
            for calc in self._calculators:
                if not self._market_data_reader.has_at_least(symbol, calc.window):
                    continue
                events = self._market_data_reader.window(symbol, calc.window)
                value = calc.calculate(events=events)
                point = FeaturePoint(
                    symbol=symbol,
                    timestamp_utc=events[-1].timestamp_utc,
                    causation_id=events[-1].event_id,
                    feature_name=calc.name,
                    value=value
                )
                self._feature_store.update(point=point)
                points_updated.append(point)
        return points_updated
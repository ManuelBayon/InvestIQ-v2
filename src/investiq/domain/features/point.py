from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class FeaturePoint[V]:
    causation_id: str
    timestamp_utc: datetime
    symbol: str
    feature_name: str
    value: V
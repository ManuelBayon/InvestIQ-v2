from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class FeaturePoint[V]:
    causation_id: str
    symbol: str
    timestamp_utc: datetime
    feature_name: str
    value: V
    def __repr__(self) -> str:
        return (
            f"FeaturePoint(\n"
            f"\tcausation_id={self.causation_id}\n"
            f"\tsymbol={self.symbol}\n"
            f"\ttimestamp_utc={self.timestamp_utc}\n"
            f"\tfeature_name={self.feature_name}\n"
            f"\tvalue={self.value}\n"
            f")"
        )
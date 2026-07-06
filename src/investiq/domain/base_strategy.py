from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from typing import Protocol

from investiq.domain.feature_engine import FeatureSnapshot
from investiq.domain.trade_store import LatestTradeSnapshot

@dataclass(frozen=True)
class DecisionSnapshot:
    market: LatestTradeSnapshot
    features: FeatureSnapshot


@dataclass
class TradingIntent:
    strategy_id: str
    decision_ts_utc: datetime
    symbol: str
    target: Decimal


class Strategy(Protocol):

    def decide(
            self,
            snapshot: DecisionSnapshot
    ) -> list[TradingIntent]:
        ...
from dataclasses import dataclass

from investiq.core.contracts.events import ExternalEvent, InternalEvent


@dataclass(frozen=True)
class MarketDataEvent(ExternalEvent):...


@dataclass(frozen=True)
class BrokerEvent(ExternalEvent):
    order_id: str


@dataclass(frozen=True)
class DecisionEvent(InternalEvent):
    instrument_id: str
    target_exposure: float


@dataclass(frozen=True)
class RiskEvent(InternalEvent):
    decision_id: str
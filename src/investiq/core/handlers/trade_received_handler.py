from collections.abc import Mapping

from investiq.core.event_factory import EventFactory
from investiq.core.events import IntentGenerated, TradeReceived
from investiq.domain.features.features import Feature
from investiq.domain.market_store import InMemoryMarketStore
from investiq.domain.features.feature_runtime import FeatureRuntime
from investiq.domain.features.sources import PriceSource

from investiq.core.handlers.base import HandlerResult
from investiq.domain.strategies.base_strategy import DecisionContext, Strategy


class TradeReceivedHandler:

    def __init__(
            self,
            market_store: InMemoryMarketStore,
            price_source: PriceSource,
            symbol: str,
            feature_runtime: FeatureRuntime,
            strategy_features: Mapping[str, Feature],
            strategy: Strategy,
            event_factory: EventFactory,
            instrument_id: str,
    ):
        self._market_store = market_store
        self._price_source = price_source
        self._symbol = symbol
        self._feature_runtime = feature_runtime
        self._strategy_features = strategy_features
        self._strategy = strategy
        self._event_factory= event_factory
        self._instrument_id = instrument_id


    def handle(self, event: TradeReceived) -> HandlerResult:

        self._market_store.on_trade_received(event)

        emitted = self._feature_runtime.on_trade_received()
        emitted_features = [
            node.payload
            for node in emitted
        ]

        all_requirements_emitted = all(
            feature in emitted_features
            for feature in self._strategy_features.values()
        )

        intents_generated: list[IntentGenerated] = []

        if all_requirements_emitted:
            order_specs = self._strategy.decide(
                context=DecisionContext(
                    price=self._price_source.last(),
                    features={
                        name: feature.latest()
                        for name, feature in self._strategy_features.items()
                    },
                )
            )

            for spec in order_specs:
                intent_generated = self._event_factory.create_intent_generated(
                    causation_id=event.event_id,
                    instrument_id=self._instrument_id,
                    order_spec=spec
                )
                intents_generated.append(intent_generated)

        return HandlerResult(
            events=tuple(intents_generated)
        )

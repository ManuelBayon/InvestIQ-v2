from collections.abc import Mapping

from investiq.core.event_factory import CanonicalEventFactory
from investiq.core.events import TradeReceived
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
            event_factory: CanonicalEventFactory
    ):
        self._market_store = market_store
        self._price_source = price_source
        self._symbol = symbol
        self._feature_runtime = feature_runtime
        self._strategy_features = strategy_features
        self._strategy = strategy
        self._event_factory= event_factory


    def handle(self, event: TradeReceived) -> HandlerResult:

        self._market_store.on_trade_received(event)

        emitted = self._feature_runtime.on_trade_received()
        emitted_features = [
            node.payload
            for node in emitted
        ]

        if emitted_features:
            print("\n[TRADE_RECEIVED_HANDLER — EMITTED FEATURES] :") # debug
            for feature in emitted_features: # debug
                print(f"{feature.name}: {feature.latest()}")

        all_requirements_emitted = all(
            feature in emitted_features
            for feature in self._strategy_features.values()
        )

        orders_generated = []

        if all_requirements_emitted:
            orders = self._strategy.decide(
                context=DecisionContext(
                    price=self._price_source.last(),
                    features={
                        name: feature.latest()
                        for name, feature in self._strategy_features.items()
                    },
                )
            )

            for order in orders:
                order_generated = self._event_factory.create_order_generated(
                    causation_id=event.event_id,
                    order=order
                )
                orders_generated.append(order_generated)

        return HandlerResult(
            emitted_events=tuple(orders_generated)
        )
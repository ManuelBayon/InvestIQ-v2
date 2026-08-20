from collections.abc import Mapping

from investiq.domain.market_store import InMemoryMarketStore
from investiq.events.trade_received import TradeReceived
from investiq.features.feature_runtime import FeatureRuntime
from investiq.features.features import Feature
from investiq.features.sources import PriceSource

from investiq.handlers.base import HandlerResult
from investiq.strategies.base_strategy import DecisionContext, Strategy


class TradeReceivedHandler:

    def __init__(
            self,
            market_store: InMemoryMarketStore,
            price_source: PriceSource,
            symbol: str,
            feature_runtime: FeatureRuntime,
            strategy_features: Mapping[str, Feature],
            strategy: Strategy,
    ):
        self._market_store = market_store
        self._price_source = price_source
        self._symbol = symbol
        self._feature_runtime = feature_runtime
        self._strategy_features = strategy_features
        self._strategy = strategy


    def handle(self, event: TradeReceived) -> HandlerResult:

        self._market_store.on_trade_received(event)

        emitted = self._feature_runtime.on_trade_received()
        emitted_features = [
            node.payload
            for node in emitted
        ]

        print("\nEmitted features values :") # debug
        for feature in emitted_features: # debug
            print(f"{feature}: {feature.latest()}")
        print("")

        all_requirements_emitted = all(
            feature in emitted_features
            for feature in self._strategy_features.values()
        )

        if all_requirements_emitted:
            trading_intent = self._strategy.decide(
                context=DecisionContext(
                    symbol=self._symbol,
                    price=self._price_source.last(),
                    features={
                        name: feature.latest()
                        for name, feature in self._strategy_features.items()
                    },
                )
            )
            print(f"{trading_intent}\n") # debug
        return HandlerResult()
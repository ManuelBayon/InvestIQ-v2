from collections.abc import Sequence
from typing import ClassVar

from investiq.domain.order_types import Order, MarketOrder, LimitOrder, BracketOrder, StopLoss, TakeProfit
from investiq.domain.strategies.base_strategy import FeatureRequirement, DecisionContext


class Return1MarketOrderStrategy:
    requirements: ClassVar[Sequence[FeatureRequirement]] = []
    def decide(
            self,
            context: DecisionContext,
    ) -> list[Order]:
        return [
            MarketOrder(
                symbol=context.symbol,
                quantity=1
            )
        ]

class Return1LimitOrderStrategy:
    requirements: ClassVar[Sequence[FeatureRequirement]] = []
    def decide(
            self,
            context: DecisionContext,
    ) -> list[Order]:
        return [
            LimitOrder(
                symbol=context.symbol,
                quantity=1,
                price=5000
            )
        ]

class Return1BracketOrderStrategy:
    requirements: ClassVar[Sequence[FeatureRequirement]] = []
    def decide(
            self,
            context: DecisionContext,
    ) -> list[Order]:

        return [
            BracketOrder(
                entry=LimitOrder(
                    symbol=context.symbol,
                    quantity=1,
                    price=5000
                ),
                stop_loss=StopLoss(price=4980),
                take_profit=TakeProfit(price=5050),
            )
        ]



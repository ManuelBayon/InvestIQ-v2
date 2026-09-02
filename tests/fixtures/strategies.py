from typing import Sequence, ClassVar

from investiq.domain.order_types import MarketOrderSpec, Order, BracketOrderSpec, StopLoss, LimitOrderSpec, TakeProfit
from investiq.domain.strategies.base_strategy import TradingIntent, DecisionContext, FeatureRequirement


class MarketOrderStrategy:

    requirements: ClassVar[Sequence[FeatureRequirement]] = ()

    def __init__(self):
        self._num_trade = 0

    def decide(self, context: DecisionContext) -> list[Order]:
        order_list = []
        if self._num_trade % 5 == 0:
            order_list.append(
                BracketOrderSpec(
                    entry=MarketOrderSpec(1),
                    stop_loss=StopLoss(context.price - 5),
                    take_profit=None,
                )
            )
        self._num_trade += 1
        return order_list


class LimitOrderStrategy:

    requirements: ClassVar[Sequence[FeatureRequirement]] = ()

    def __init__(self):
        self._num_trade = 0

    def decide(
            self,
            context: DecisionContext
    ) -> list[Order]:
        order_list = []
        if self._num_trade % 5 == 0:
            order_list.append(
                LimitOrderSpec(
                    quantity=1,
                    price=context.price - 5
                )
            )
        self._num_trade += 1
        return order_list


class BracketOrderStrategy:

    requirements: ClassVar[Sequence[FeatureRequirement]] = ()

    def __init__(self):
        self._num_trade = 0

    def decide(
            self,
            context: DecisionContext
    ) -> list[Order]:
        order_list = []
        if self._num_trade % 5 == 0:
            order_list.append(
                BracketOrderSpec(
                    entry=MarketOrderSpec(1),
                    stop_loss=StopLoss(context.price - 5),
                    take_profit=TakeProfit(context.price + 5),
                )
            )
        self._num_trade += 1
        return order_list
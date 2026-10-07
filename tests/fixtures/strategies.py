from typing import Sequence, ClassVar

from investiq.domain.orders import MarketOrderSpec, OrderSpec, BracketOrderSpec, StopOrderSpec, LimitOrderSpec
from investiq.domain.strategies.base_strategy import DecisionContext, FeatureRequirement


class MarketOrderStrategy:

    requirements: ClassVar[Sequence[FeatureRequirement]] = ()

    def __init__(self):
        self._num_trade = 0

    def decide(self, context: DecisionContext) -> list[OrderSpec]:
        order_list = []
        if self._num_trade % 5 == 0:
            order_list.append(
                BracketOrderSpec(
                    entry=MarketOrderSpec(side="BUY", quantity=1, tif="DAY"),
                    stop_loss=StopOrderSpec(side="SELL", quantity=1, tif="DAY", stop_price=context.price - 5),
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
    ) -> list[OrderSpec]:
        order_list = []
        if self._num_trade % 5 == 0:
            order_list.append(
                LimitOrderSpec(
                    side="BUY",
                    quantity=1,
                    tif="DAY",
                    limit_price=context.price - 5
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
    ) -> list[OrderSpec]:
        order_list = []
        if self._num_trade % 5 == 0:
            order_list.append(
                BracketOrderSpec(
                    entry=MarketOrderSpec(side="BUY", quantity=1, tif="DAY"),
                    stop_loss=StopOrderSpec(side="SELL", quantity=1, tif="DAY", stop_price=context.price - 5),
                    take_profit=LimitOrderSpec(side="SELL", quantity=1, tif="DAY", limit_price=context.price + 5),
                )
            )
        self._num_trade += 1
        return order_list

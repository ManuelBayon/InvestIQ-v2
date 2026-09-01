from typing import Sequence, ClassVar

from investiq.domain.order_types import MarketOrderSpec, Order
from investiq.domain.strategies.base_strategy import TradingIntent, DecisionContext, FeatureRequirement


class MarketOrderStrategy:

    requirements: ClassVar[Sequence[FeatureRequirement]] = ()

    def __init__(self, n: int = 3):
        self._n = n
        self._num_trade = 0

    def decide(self, context: DecisionContext) -> list[Order]:
        order_list = []

        if self._num_trade % self._n == 0:
            order_list.append(MarketOrderSpec(quantity=1))

        self._num_trade += 1

        return order_list
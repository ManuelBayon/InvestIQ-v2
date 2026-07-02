from investiq.domain.decision.base import DecisionLayer, _build_context, OrderIntent
from investiq.domain.instruments import FutureSpecs
from investiq.domain.models import RawTick
from investiq.domain.orders.orders import MarketOrderSpecs, Side


class AlwaysBuyMNQMarket(DecisionLayer):
    """
    """
    def evaluate(
            self,
            market_view: dict[str, list[RawTick]],
            feature_view: dict[str, dict[str, list[float]]],
    ) -> OrderIntent:
        context = _build_context(market_view, feature_view)
        return OrderIntent(
            context=context,
            order_specs=MarketOrderSpecs(
                instrument=FutureSpecs("MNQ", "MNQU6"),
                quantity=1,
                direction=Side.BUY,
                tif="GTC"
            )
        )
from investiq.domain.decision_layer.base import DecisionLayer, _build_context, OrderIntent
from investiq.domain.instruments import StockSpecs
from investiq.domain.models import RawTick
from investiq.domain.order_specs import MarketOrderSpec, Side


class AlwaysBuyAMDMarketDecisionLayer(DecisionLayer):
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
            order_spec=MarketOrderSpec(
                instrument=StockSpecs(symbol="AMD"),
                quantity=1,
                direction=Side.BUY,
                tif="DAY"
            )
        )
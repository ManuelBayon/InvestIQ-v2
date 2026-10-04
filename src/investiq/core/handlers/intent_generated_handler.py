from investiq.adapters.ibkr.ib_broker_adapter import IBKRAdapter
from investiq.core.events import IntentGenerated
from investiq.core.handlers.base import HandlerResult
from investiq.domain.instrument_spec import InstrumentSpec
from investiq.domain.orders import MarketOrderSpec, LimitOrderSpec, BracketOrderSpec
from investiq.errors import InvalidOrderType


class IntentGeneratedHandler:

    def __init__(
            self,
            ib_adapter: IBKRAdapter,
            instrument: InstrumentSpec
    ):
        self._ib_adapter = ib_adapter
        self._instrument_spec = instrument

    def handle(self, intent: IntentGenerated) -> HandlerResult:

        if isinstance(intent.spec, MarketOrderSpec):
            self._ib_adapter.place_market_order(
                contract_spec=self._instrument_spec,
                order_spec=intent.spec
            )
        elif isinstance(intent.spec, LimitOrderSpec):
            self._ib_adapter.place_limit_order(
                contract_spec=self._instrument_spec,
                order_spec=intent.spec
            )
        elif isinstance(intent.spec, BracketOrderSpec):
            self._ib_adapter.place_bracket_order(
                contract_spec=self._instrument_spec,
                order_spec=intent.spec
            )
        else:
            raise InvalidOrderType(
                f"Order type not recognize, "
                f"order.__class__={intent.spec.__class__}"
            )

        return HandlerResult(events=())
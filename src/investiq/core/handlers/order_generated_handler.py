from investiq.adapters.ibkr.ib_broker_adapter import IBKRAdapter
from investiq.core.events import OrderGenerated
from investiq.core.handlers.base import HandlerResult
from investiq.domain.instrument_spec import InstrumentSpec
from investiq.domain.order_types import MarketOrderSpec, LimitOrderSpec
from investiq.errors import InvalidOrderType


class OrderGeneratedHandler:

    def __init__(
            self,
            ib_adapter: IBKRAdapter,
            instrument: InstrumentSpec
    ):
        self._ib_adapter = ib_adapter
        self._instrument_spec = instrument

    def handle(self, event: OrderGenerated) -> HandlerResult:

        if isinstance(event.order, MarketOrderSpec):
            self._ib_adapter.place_market_order(
                contract_spec=self._instrument_spec,
                order_spec=event.order
            )
        else:
            raise InvalidOrderType(
                f"Order type not recognize, "
                f"order.__class__={event.order.__class__}"
            )
        self._ib_adapter._ib_client._ib.sleep(5)
        return HandlerResult(emitted_events=())
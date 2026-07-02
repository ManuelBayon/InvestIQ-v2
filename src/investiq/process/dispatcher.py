from collections.abc import Callable
from investiq.events.events import MarketDataEvent

from investiq.events.market_data import TradeReceived
from investiq.core.contracts.events import CanonicalEvent
from investiq.handlers.base import HandlerResult
from investiq.handlers.market_data_handler import MarketDataHandler



class Dispatcher:


    def __init__(
            self,
            market_data_handler: MarketDataHandler,
    ):
        self._market_data_handler = market_data_handler

        self._dispatch_table: dict[type[CanonicalEvent], Callable] = {
            TradeReceived: self._on_market_data,
        }


    def _on_market_data(self, event: MarketDataEvent) -> HandlerResult:
        return self._market_data_handler.handle(event)


    def dispatch(self, event: CanonicalEvent) -> HandlerResult:
        event_type = type(event)
        handler = self._dispatch_table[event_type]
        return handler(event)
from collections.abc import Callable

from investiq.events.canonical_events import BaseEvent, IntentGenerated, TickDataAvailable
from investiq.runtime.handlers.tick_data_available_handler import TickDataAvailableHandler


class Orchestrator:

    def __init__(
            self,
            tick_available_handler: TickDataAvailableHandler,
    ):
        self._tick_data_available_handler = tick_available_handler
        self._dispatch_table: dict[type[BaseEvent], Callable] = {
            TickDataAvailable: self.on_tick_data_available,
        }

    def on_tick_data_available(
            self,
            event: TickDataAvailable
    ) -> IntentGenerated:
        return self._tick_data_available_handler.handle(event=event)

    def dispatch(
            self,
            event: BaseEvent,
    ) -> BaseEvent:
        handler = self._dispatch_table[type(event)]
        return handler(event)
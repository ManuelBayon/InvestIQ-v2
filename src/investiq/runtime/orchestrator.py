from collections.abc import Callable

from investiq.events.canonical_events import BarAvailable, BaseEvent, IntentGenerated, NoOperation
from investiq.runtime.handlers.bar_available_handler import BarAvailableHandler

class Orchestrator:

    def __init__(
            self,
            bar_available_handler: BarAvailableHandler,
    ):
        self._next_id: int = 1
        self._bar_available_handler = bar_available_handler
        self._dispatch_table: dict[type[BaseEvent], Callable] = {
            BarAvailable: self.on_bar_available,
        }

    def on_bar_available(
            self,
            bar_available: BarAvailable
    ) -> NoOperation | IntentGenerated:
        intent = self._bar_available_handler.handle(
            next_id=f"EVT_{self._next_id:05}",
            bar_available=bar_available
        )
        self._next_id +=1
        return intent

    def dispatch(
            self,
            event: BaseEvent,
    ) -> BaseEvent:
        handler = self._dispatch_table[type(event)]
        result = handler(event)
        return result
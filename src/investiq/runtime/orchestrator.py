from collections.abc import Callable

from investiq.events.events import CanonicalEvent, IntentGenerated, TickDataAvailable
from investiq.runtime.handlers.intent_generated_handler import IntentGeneratedHandler
from investiq.runtime.handlers.tick_data_available_handler import TickDataAvailableHandler


class Orchestrator:

    def __init__(
            self,
            tick_available_handler: TickDataAvailableHandler,
            intent_generated_handler: IntentGeneratedHandler,
    ):
        self._tick_data_available_handler = tick_available_handler
        self._intent_generated_handler = intent_generated_handler

        self._dispatch_table: dict[type[CanonicalEvent], Callable] = {
            TickDataAvailable: self._on_tick_data_available,
            IntentGenerated: self._on_intent_generated,
        }

    def _on_tick_data_available(self, event: TickDataAvailable) -> IntentGenerated:
        return self._tick_data_available_handler.handle(event=event)

    def _on_intent_generated(self, event: IntentGenerated) -> None:
        return self._intent_generated_handler.handle(event=event)

    def dispatch(self, event: CanonicalEvent) -> CanonicalEvent:
        print(f"received event:{type(event).__name__}")
        handler = self._dispatch_table[type(event)]
        print(f"handler:{handler}")
        return handler(event)
from investiq.adapters.ibkr.ib_broker_adapter import IBAdapter
from investiq.adapters.ibkr.ib_client import IBClient
from investiq.core.commands import IBSubmitOrder, PrepareBracket
from investiq.core.event_factory import EventFactory
from investiq.core.events import IBOperationFailed
from investiq.core.handlers.base import HandlerResult


class PrepareBracketHandler:
    def __init__(self, client: IBClient, adapter: IBAdapter, factory: EventFactory) -> None:
        self._client = client
        self._adapter = adapter
        self._factory = factory

    def handle(self, command: PrepareBracket) -> HandlerResult:
        try:
            self._client.ib_loop.call_soon_threadsafe(self._adapter.prepare_on_ib_thread, command)
        except (RuntimeError, AttributeError) as exc:
            return HandlerResult(events=(IBOperationFailed(
                run_id=command.run_id, event_id=self._factory.next_event_id(),
                command_id=command.command_id, operation="prepare", error=str(exc),
            ),))
        return HandlerResult()


class IBSubmitOrderHandler:
    def __init__(self, client: IBClient, adapter: IBAdapter, factory: EventFactory) -> None:
        self._client = client
        self._adapter = adapter
        self._factory = factory

    def handle(self, command: IBSubmitOrder) -> HandlerResult:
        try:
            self._client.ib_loop.call_soon_threadsafe(self._adapter.submit_on_ib_thread, command)
        except (RuntimeError, AttributeError) as exc:
            return HandlerResult(events=(IBOperationFailed(
                run_id=command.run_id, event_id=self._factory.next_event_id(),
                command_id=command.command_id, operation="submit", error=str(exc),
            ),))
        return HandlerResult()

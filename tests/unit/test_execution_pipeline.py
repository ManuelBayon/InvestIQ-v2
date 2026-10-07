import asyncio
from collections import deque
from datetime import datetime, timezone
from threading import Event, Thread, get_ident
from types import SimpleNamespace
from unittest.mock import Mock

import pytest

from investiq.adapters.ibkr.ib_broker_adapter import IBAdapter
from investiq.core.broker_messages import BrokerFill, BrokerOrderStatus, MarketTrade
from investiq.core.command_id_generator import CommandIdGenerator
from investiq.core.dispatcher import Dispatcher
from investiq.core.event_factory import EventFactory
from investiq.core.event_journal import EventJournal
from investiq.core.event_loop import CanonicalEventLoop
from investiq.core.event_queue import EventQueue
from investiq.core.events import (
    BrokerReturnUnmatched, CommissionReportReceived, FillReceived, IBOperationFailed,
    IntentGenerated, OrderCreated, OrderStatusUpdated,
)
from investiq.core.handlers.base import HandlerResult
from investiq.core.handlers.bracket_prepared_handler import BracketPreparedHandler
from investiq.core.handlers.broker_return_handler import BrokerReturnHandler
from investiq.core.handlers.ib_command_handlers import IBSubmitOrderHandler, PrepareBracketHandler
from investiq.core.handlers.intent_generated_handler import IntentGeneratedHandler
from investiq.core.order_correlation import OrderCorrelation
from investiq.core.order_id_generator import OrderIdGenerator
from investiq.domain.instrument_spec import FutureSpec
from investiq.domain.orders import BracketOrderSpec, LimitOrderSpec, MarketOrderSpec, StopOrderSpec


class ScheduledLoop:
    def __init__(self):
        self.pending = deque()

    def call_soon_threadsafe(self, callback, *args):
        self.pending.append((callback, args))

    def drain(self):
        while self.pending:
            callback, args = self.pending.popleft()
            callback(*args)


class FakeClient:
    def __init__(self):
        self.ib_loop = ScheduledLoop()
        self._next_id = 278
        self.placements = []
        self.allocation_threads = []
        self.placement_threads = []
        self.subscriptions = 0
        self.before_place = lambda order: None

    @property
    def next_id(self):
        self.allocation_threads.append(get_ident())
        order_id = self._next_id
        self._next_id += 1
        return order_id

    def subscribe_order_events(self, on_status, on_fill, on_commission):
        self.subscriptions += 1
        self.on_status, self.on_fill, self.on_commission = on_status, on_fill, on_commission

    def place_order(self, contract, order):
        self.before_place(order)
        self.placements.append((contract, order))
        self.placement_threads.append(get_ident())
        # Deliberately invoke callbacks before place_order returns.
        trade = SimpleNamespace(order=order, orderStatus=SimpleNamespace(status="Submitted"))
        self.on_status(trade)
        return trade


class RecordingFactory(EventFactory):
    def __init__(self):
        super().__init__("TEST_RUN")
        self.id_threads = []

    def next_event_id(self):
        self.id_threads.append(get_ident())
        return super().next_event_id()


def build_harness():
    inbound = EventQueue()
    internal = EventQueue()
    factory = RecordingFactory()
    commands = CommandIdGenerator()
    client = FakeClient()
    correlation = OrderCorrelation()
    journal = EventJournal()
    adapter = IBAdapter(client, inbound, "TEST_RUN", {
        "MNQZ6": FutureSpec("MNQ", "MNQZ6", "CME"),
    })
    market_handler = Mock()
    market_handler.handle.return_value = HandlerResult()
    dispatcher = Dispatcher(
        market_handler,
        IntentGeneratedHandler(OrderIdGenerator(), commands),
        PrepareBracketHandler(client, adapter, factory),
        BracketPreparedHandler(factory, commands),
        IBSubmitOrderHandler(client, adapter, factory),
        BrokerReturnHandler(correlation, factory),
    )
    loop = CanonicalEventLoop(journal, inbound, internal, dispatcher, correlation)
    return SimpleNamespace(
        inbound=inbound, internal=internal, factory=factory, client=client,
        correlation=correlation, journal=journal, adapter=adapter, loop=loop,
        market_handler=market_handler,
    )


def enqueue_intent(h, side="BUY", entry_type="market", sl=True, tp=True):
    exit_side = "SELL" if side == "BUY" else "BUY"
    entry = (
        MarketOrderSpec(side=side, quantity=1, tif="DAY")
        if entry_type == "market" else
        LimitOrderSpec(side=side, quantity=1, tif="DAY", limit_price=100)
    )
    intent = h.factory.create_intent_generated(
        causation_id="market-trigger", instrument_id="MNQZ6",
        order_spec=BracketOrderSpec(
            entry=entry,
            stop_loss=StopOrderSpec(side=exit_side, quantity=1, tif="GTC", stop_price=95) if sl else None,
            take_profit=LimitOrderSpec(side=exit_side, quantity=1, tif="DAY", limit_price=105) if tp else None,
        ),
    )
    h.inbound.enqueue(intent)
    return intent


@pytest.mark.parametrize("side", ["BUY", "SELL"])
@pytest.mark.parametrize("entry_type", ["market", "limit"])
@pytest.mark.parametrize("sl,tp", [(True, True), (True, False), (False, True), (False, False)])
def test_nominal_submission_records_all_orders_before_first_place(side, entry_type, sl, tp):
    h = build_harness()
    enqueue_intent(h, side, entry_type, sl, tp)
    count = 1 + int(sl) + int(tp)
    h.loop.run_until_empty()
    assert h.client.placements == []
    assert h.client.allocation_threads == []

    h.client.ib_loop.drain()  # preparation only
    assert h.client.placements == []
    h.loop.run_until_empty()  # no new market tick
    created = [event for event in h.journal if isinstance(event, OrderCreated)]
    assert len(created) == count

    def check_before_place(order):
        assert len([event for event in h.journal if isinstance(event, OrderCreated)]) == count
        for event in created:
            assert h.correlation.by_broker(event.run_id, event.broker_order_id).order_id == event.order_id
    h.client.before_place = check_before_place
    h.client.ib_loop.drain()
    h.loop.run_until_empty()

    orders = [order for _, order in h.client.placements]
    assert [order.orderId for order in orders] == list(range(278, 278 + count))
    assert [order.parentId for order in orders] == [0] + [278] * (count - 1)
    assert [order.transmit for order in orders] == [False] * (count - 1) + [True]
    assert orders[0].action == side
    assert orders[0].orderType == ("MKT" if entry_type == "market" else "LMT")
    assert orders[0].tif == "DAY"
    if entry_type == "limit":
        assert orders[0].lmtPrice == 100
    if sl:
        assert orders[1].orderType == "STP"
        assert orders[1].auxPrice == 95
        assert orders[1].tif == "GTC"
    if tp:
        assert orders[-1].orderType == "LMT"
        assert orders[-1].lmtPrice == 105
    assert all(order.action != side and order.totalQuantity == 1 for order in orders[1:])
    assert all(contract.localSymbol == "MNQZ6" for contract, _ in h.client.placements)
    statuses = [event for event in h.journal if isinstance(event, OrderStatusUpdated)]
    assert [event.order_id for event in statuses] == list(range(1, count + 1))
    assert statuses[0].parent_id is None
    assert h.client.subscriptions == 1
    events = list(h.journal)
    assert len({event.event_id for event in events}) == len(events)

    rebuilt = OrderCorrelation.from_events(h.journal)
    assert rebuilt.by_internal("TEST_RUN", 1).broker_order_id == 278
    assert len(h.client.placements) == count  # replay performs no effects


def test_raw_market_message_gets_event_id_only_when_canonical_loop_processes_it():
    h = build_harness()
    h.inbound.enqueue(MarketTrade(
        "TEST_RUN", "MNQ", datetime.now(timezone.utc), 100, 1,
    ))
    assert h.factory.id_threads == []
    h.loop.run_until_empty()
    h.market_handler.handle.assert_called_once()
    assert h.factory.id_threads == [get_ident()]
    assert len(h.journal) == 1


def test_fill_and_commission_are_correlated_on_canonical_thread():
    h = build_harness()
    enqueue_intent(h)
    h.loop.run_until_empty()
    h.client.ib_loop.drain()
    h.loop.run_until_empty()
    h.client.ib_loop.drain()
    h.loop.run_until_empty()
    execution = SimpleNamespace(
        orderId=278, execId="fill-1", time=datetime.now(timezone.utc),
        shares=1.0, side="BOT", price=100, cumQty=1.0,
    )
    fill = SimpleNamespace(execution=execution)
    h.client.on_fill(None, fill)
    h.client.on_commission(None, fill, SimpleNamespace(
        commission=0.61, currency="USD", realizedPNL=0.0,
    ))
    h.loop.run_until_empty()
    events = list(h.journal)
    assert isinstance(events[-2], FillReceived)
    assert events[-2].order_id == 1 and events[-2].side == "BUY"
    assert events[-2].parent_id is None
    assert isinstance(events[-1], CommissionReportReceived)
    assert events[-1].order_id == 1 and events[-1].exec_id == "fill-1"


def test_unknown_return_is_preserved_and_reported(caplog):
    h = build_harness()
    message = BrokerOrderStatus("TEST_RUN", 999, "Filled")
    h.inbound.enqueue(message)
    h.loop.run_until_empty()
    event = list(h.journal)[0]
    assert isinstance(event, BrokerReturnUnmatched)
    assert event.message == message
    assert "Unknown broker order ID" in caplog.text


def test_preparation_failure_is_journaled_without_submission():
    h = build_harness()
    h.adapter._instruments.clear()
    enqueue_intent(h)
    h.loop.run_until_empty()
    h.client.ib_loop.drain()
    h.loop.run_until_empty()
    failure = list(h.journal)[-1]
    assert isinstance(failure, IBOperationFailed)
    assert failure.operation == "prepare"
    assert "Unknown instrument_id" in failure.error
    assert h.client.placements == []
    assert not h.client.ib_loop.pending


def test_journal_failure_prevents_commands_from_being_scheduled():
    h = build_harness()
    enqueue_intent(h)
    h.loop.run_until_empty()
    h.client.ib_loop.drain()
    original_append = h.journal.append

    def fail_on_created(event):
        if isinstance(event, OrderCreated):
            raise OSError("journal unavailable")
        original_append(event)
    h.journal.append = fail_on_created

    with pytest.raises(OSError, match="journal unavailable"):
        h.loop.run_until_empty()
    assert h.client.placements == []
    assert not h.client.ib_loop.pending


def test_correlation_rejects_conflicting_associations():
    h = build_harness()
    enqueue_intent(h)
    h.loop.run_until_empty()
    h.client.ib_loop.drain()
    h.loop.run_until_empty()
    created = next(event for event in h.journal if isinstance(event, OrderCreated))
    from dataclasses import replace
    with pytest.raises(ValueError, match="Conflicting"):
        h.correlation.apply(replace(created, order_id=999))


def test_ib_work_runs_on_other_thread_and_ids_remain_canonical():
    h = build_harness()
    ib_loop = asyncio.new_event_loop()
    ready = Event()
    begin = Event()
    def run_ib():
        asyncio.set_event_loop(ib_loop)
        ready.set()
        begin.wait(2)
        ib_loop.run_forever()
        ib_loop.close()
    worker = Thread(target=run_ib, name="FakeIB")
    worker.start()
    assert ready.wait(2)
    h.client.ib_loop = ib_loop
    canonical_id = get_ident()
    try:
        enqueue_intent(h)
        h.loop.run_until_empty()
        begin.set()
        # Wait for preparation alone, with no further market input.
        prepared = h.inbound.dequeue_blocking(timeout=2)
        h.inbound.enqueue(prepared)
        h.loop.run_until_empty()
        finished = Event()
        ib_loop.call_soon_threadsafe(finished.set)
        assert finished.wait(2)
        h.loop.run_until_empty()
        assert h.client.allocation_threads == [worker.ident] * 3
        assert h.client.placement_threads == [worker.ident] * 3
        assert set(h.factory.id_threads) == {canonical_id}
        assert len(h.client.placements) == 3
    finally:
        begin.set()
        ib_loop.call_soon_threadsafe(ib_loop.stop)
        worker.join(timeout=2)
        assert not worker.is_alive()


def test_builder_runs_market_to_submission_with_synthetic_data(monkeypatch):
    from investiq.domain.experiment import ExperimentSpec
    from investiq.ingress.synthetic import TradeFixture
    from investiq.runtime import builder
    from investiq.runtime.sequential import SequentialRuntimeConfig

    class OneIntentStrategy:
        requirements = ()
        def decide(self, context):
            return [BracketOrderSpec(
                entry=MarketOrderSpec(side="BUY", quantity=1, tif="DAY"),
                stop_loss=StopOrderSpec(side="SELL", quantity=1, tif="DAY", stop_price=context.price - 5),
                take_profit=LimitOrderSpec(side="SELL", quantity=1, tif="DAY", limit_price=context.price + 5),
            )]

    client = FakeClient()
    monkeypatch.setattr(builder, "IBClient", lambda: client)
    runtime = builder.build_runtime(SequentialRuntimeConfig(
        experiment=ExperimentSpec(
            run_id="TEST_RUN", instrument=FutureSpec("MNQ", "MNQZ6", "CME"),
            features={}, strategy=OneIntentStrategy,
        ),
        trades=[TradeFixture("MNQ", datetime.now(timezone.utc), 100, 1)],
        num_trades=1,
    ))
    # Do not run the live connection; drive the two queues explicitly.
    runtime._ingress.start()
    runtime._event_loop.run_until_empty()
    client.ib_loop.drain()
    runtime._event_loop.run_until_empty()
    client.ib_loop.drain()
    runtime._event_loop.run_until_empty()
    assert len(client.placements) == 3
    facts = list(runtime._event_loop._journal)
    intent = next(event for event in facts if isinstance(event, IntentGenerated))
    assert intent.instrument_id == "MNQZ6"
    assert [event.order_id for event in facts if isinstance(event, OrderStatusUpdated)] == [1, 2, 3]


def test_submission_exception_is_reported_on_canonical_thread():
    h = build_harness()
    enqueue_intent(h, sl=False, tp=False)
    h.loop.run_until_empty()
    h.client.ib_loop.drain()
    h.loop.run_until_empty()
    def fail_place(contract, order):
        raise RuntimeError("fake placement failure")
    h.client.place_order = fail_place
    h.client.ib_loop.drain()
    h.loop.run_until_empty()
    failure = list(h.journal)[-1]
    assert isinstance(failure, IBOperationFailed)
    assert failure.operation == "submit"
    assert "fake placement failure" in failure.error


def test_live_loop_wakes_on_preparation_result_without_new_market_tick():
    h = build_harness()
    allocated = Event()
    journaled = Event()
    original_prepare = h.adapter.prepare_on_ib_thread
    original_append = h.journal.append
    def append(event):
        original_append(event)
        if isinstance(event, OrderCreated) and event.order_id == 3:
            journaled.set()
    h.journal.append = append
    # A synchronization event exposes the moment preparation is scheduled.
    original_schedule = h.client.ib_loop.call_soon_threadsafe
    def schedule(callback, *args):
        original_schedule(callback, *args)
        allocated.set()
    h.client.ib_loop.call_soon_threadsafe = schedule
    worker = Thread(target=h.loop.run_forever, name="CanonicalTest", daemon=True)
    enqueue_intent(h)
    worker.start()
    try:
        assert allocated.wait(2)
        # Only execute preparation here. Submission remains scheduled for IB.
        callback, args = h.client.ib_loop.pending.popleft()
        assert callback == original_prepare
        callback(*args)
        assert journaled.wait(2)
    finally:
        h.loop.running = False
        # Wake the existing blocking loop so the test can join it.
        h.inbound.enqueue(BrokerOrderStatus("TEST_RUN", 278, "Submitted"))
        worker.join(timeout=2)
        assert not worker.is_alive()

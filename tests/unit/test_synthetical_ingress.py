from datetime import datetime, timezone
from decimal import Decimal

from investiq.core.event_queue import CanonicalEventQueue

from investiq.events.factory import CanonicalEventFactory
from investiq.events.trade_received import TradeReceived

from investiq.ingress.synthetic import SyntheticIngress, TradeFixture

from tests.fixtures.market.simple import SIMPLE_TRADES

EVENT_QUEUE = CanonicalEventQueue()
EVENT_FACTORY = CanonicalEventFactory("TEST_RUN_ID")

def _start_ingress(trades: list[TradeFixture]) -> None:
    ingress = SyntheticIngress(
        event_queue=EVENT_QUEUE,
        event_factory=EVENT_FACTORY,
        scenario=trades,
    )
    ingress.start()



def test_ingress_single_trade_into_queue():
    queue = EVENT_QUEUE
    ts = datetime(2026,1,1,12, tzinfo=timezone.utc)
    _start_ingress(
        trades=[
            TradeFixture(symbol="TEST_SYMBOL", timestamp_utc=ts, price=Decimal(100.0), size=Decimal(1.0))
        ]
    )

    assert queue.__len__() == 1
    event = queue.dequeue_nowait()

    assert isinstance(event, TradeReceived)
    assert event.run_id == "TEST_RUN_ID"
    assert event.event_id == "EVT_00001"
    assert event.symbol == "TEST_SYMBOL"
    assert event.timestamp_utc == ts
    assert event.price == Decimal(100.0)
    assert event.size == Decimal(1.0)

def test_ingress_two_trades_into_queue():
    queue = EVENT_QUEUE
    ts_1 = datetime(2026, 1, 1, 12, 0,tzinfo=timezone.utc)
    ts_2 = datetime(2026, 1, 1, 12, 1,tzinfo=timezone.utc)
    _start_ingress(
        trades= [
            TradeFixture(symbol="TEST_SYMBOL", timestamp_utc=ts_1, price=Decimal(100.0), size=Decimal(1.0)),
            TradeFixture(symbol="TEST_SYMBOL", timestamp_utc=ts_2, price=Decimal(101.0), size=Decimal(2.0))
        ]
    )

    assert queue.__len__() == 2
    event_1 = queue.dequeue_nowait()

    assert isinstance(event_1, TradeReceived)
    assert event_1.run_id == "TEST_RUN_ID"
    assert event_1.event_id == "EVT_00001"
    assert event_1.symbol == "TEST_SYMBOL"
    assert event_1.timestamp_utc == ts_1
    assert event_1.price == Decimal(100.0)
    assert event_1.size == Decimal(1.0)

    assert queue.__len__() == 1
    event_2 = queue.dequeue_nowait()

    assert isinstance(event_2, TradeReceived)
    assert event_2.run_id == "TEST_RUN_ID"
    assert event_2.event_id == "EVT_00002"
    assert event_2.symbol == "TEST_SYMBOL"
    assert event_2.timestamp_utc == ts_2
    assert event_2.price == Decimal(101.0)
    assert event_2.size == Decimal(2.0)
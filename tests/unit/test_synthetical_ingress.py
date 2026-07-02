from datetime import datetime, timezone
from decimal import Decimal


from investiq.core.event_queue import CanonicalEventQueue
from investiq.events.factory import CanonicalEventFactory
from investiq.events.market_data import TradeReceived
from investiq.ingress.synthetic import SyntheticIngress, SyntheticStream


def _start_ingress(
        run_id: str,
        streams: list[SyntheticStream],
        event_queue: CanonicalEventQueue,
) -> None:
    event_factory = CanonicalEventFactory(run_id=run_id)
    ingress = SyntheticIngress(
        event_queue=event_queue,
        event_factory=event_factory,
        streams=streams,
    )
    ingress.start()


def test_start_ingress_single_stream_single_trade():
    queue = CanonicalEventQueue()

    run_id = "TEST_RUN_ID"
    symbol = "TEST_SYMBOL"
    n = 1

    _start_ingress(
        run_id=run_id,
        streams=[
            SyntheticStream(
                symbol=symbol,
                n=n,
                min_price=Decimal(100),
                max_price=Decimal(100),
                min_size=Decimal(1),
                max_size=Decimal(1),
            )
        ],
        event_queue=queue,
    )

    assert len(queue) == 1
    trade = queue.dequeue_nowait()
    assert isinstance(trade, TradeReceived)
    assert queue.is_empty

    assert trade.run_id == run_id
    assert trade.event_id == "EVT_00001"
    assert trade.symbol == symbol
    assert trade.timestamp_utc == datetime(2026, 1, 1, 0, 0, 0, tzinfo=timezone.utc)
    assert trade.price == Decimal(100)
    assert trade.size == Decimal(1)


def test_start_ingress_single_stream_multiple_trades():
    queue = CanonicalEventQueue()

    run_id = "TEST_RUN_ID"
    symbol = "TEST_SYMBOL"
    n = 10

    _start_ingress(
        run_id=run_id,
        streams=[
            SyntheticStream(
                symbol=symbol,
                n=n,
                min_price=Decimal(100),
                max_price=Decimal(109),
                min_size=Decimal(1),
                max_size=Decimal(5),
            )
        ],
        event_queue=queue,
    )

    assert len(queue) == 10
    trades = []
    while not queue.is_empty:
        trades.append(queue.dequeue_nowait())
    assert queue.is_empty

    first_trade = trades[0]
    assert isinstance(first_trade, TradeReceived)
    assert first_trade.run_id == run_id
    assert first_trade.event_id == "EVT_00001"
    assert first_trade.symbol == symbol
    assert first_trade.timestamp_utc == datetime(
        2026, 1, 1, 0, 0, 0, tzinfo=timezone.utc
    )
    assert first_trade.price == Decimal(100)
    assert first_trade.size == Decimal(1)

    last_trade = trades[-1] # trades[-1] <=> trades[9]
    assert isinstance(last_trade, TradeReceived)
    assert last_trade.run_id == run_id
    assert last_trade.event_id == "EVT_00010"
    assert last_trade.symbol == symbol
    assert last_trade.timestamp_utc == datetime(
        2026, 1, 1, 0, 0, 9, tzinfo=timezone.utc
    )
    assert last_trade.price == Decimal(109)
    assert last_trade.size == Decimal(5)

def test_two_streams_single_trade_for_each():
    queue = CanonicalEventQueue()

    run_id = "TEST_RUN_ID"

    symbol_1 = "TEST_SYMBOL_1"
    n_1 = 1

    symbol_2 = "TEST_SYMBOL_2"
    n_2 = 1

    _start_ingress(
        run_id=run_id,
        streams=[
            SyntheticStream(
                symbol=symbol_1,
                n=n_1,
                min_price=Decimal(100),
                max_price=Decimal(100),
                min_size=Decimal(1),
                max_size=Decimal(1),
            ),
            SyntheticStream(
                symbol=symbol_2,
                n=n_2,
                min_price=Decimal(110),
                max_price=Decimal(110),
                min_size=Decimal(2),
                max_size=Decimal(2),
            )
        ],
        event_queue=queue,
    )

    assert len(queue) == 2
    trades = []
    while not queue.is_empty:
        trades.append(queue.dequeue_nowait())
    assert queue.is_empty

    first_trade = trades[0]
    assert isinstance(first_trade, TradeReceived)
    assert first_trade.run_id == run_id
    assert first_trade.event_id == "EVT_00001"
    assert first_trade.symbol == symbol_1
    assert first_trade.timestamp_utc == datetime(
        2026, 1, 1, 0, 0, 0, tzinfo=timezone.utc
    )
    assert first_trade.price == Decimal(100)
    assert first_trade.size == Decimal(1)

    second_trade = trades[1]
    assert isinstance(second_trade, TradeReceived)
    assert second_trade.run_id == run_id
    assert second_trade.event_id == "EVT_00002"
    assert second_trade.symbol == symbol_2
    assert second_trade.timestamp_utc == datetime(
        2026, 1, 1, 0, 0, 0, tzinfo=timezone.utc
    )
    assert second_trade.price == Decimal(110)
    assert second_trade.size == Decimal(2)
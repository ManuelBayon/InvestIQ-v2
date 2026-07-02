from datetime import datetime, timezone

import pytest

from investiq.core.event_queue import CanonicalEventQueue
from investiq.events.factory import CanonicalEventFactory
from investiq.events.market_data import TradeReceived
from investiq.ingress.synthetic import SyntheticIngress

def _start_ingress(run_id: str, symbol: str, n: int) -> tuple[TradeReceived, ...]:

    event_queue = CanonicalEventQueue()
    event_factory = CanonicalEventFactory(run_id=run_id)

    ingress = SyntheticIngress(
        event_queue=event_queue,
        event_factory=event_factory,
        symbol=symbol,
        n=n,
    )
    ingress.start()

    trades = []
    while not event_queue.is_empty:
        trade = event_queue.dequeue_nowait()
        trades.append(trade)

    return tuple(trades)


def test_start_ingress_single_trade():
    run_id = "TEST_RUN_ID"
    symbol = "TEST_SYMBOL"
    n = 1

    trades = _start_ingress(run_id=run_id, symbol= symbol, n=n)

    trade = trades[0]
    assert isinstance(trade, TradeReceived)
    assert trade.run_id == run_id
    assert trade.event_id == "EVT_00001"
    assert trade.symbol == symbol
    assert trade.timestamp_utc == datetime(2026, 1, 1, 0, 0, 0, tzinfo=timezone.utc)
    assert trade.price == 90
    assert trade.size == 1


def test_start_ingress_multiple_trades():
    run_id = "TEST_RUN_ID"
    symbol = "TEST_SYMBOL"
    n = 10

    trades = _start_ingress(run_id=run_id, symbol= symbol, n=n)

    assert len(trades) == 10

    trade_1 = trades[0]
    assert isinstance(trade_1, TradeReceived)
    assert trade_1.run_id == run_id
    assert trade_1.event_id == "EVT_00001"
    assert trade_1.symbol == symbol
    assert trade_1.timestamp_utc == datetime(2026, 1, 1, 0, 0, 0, tzinfo=timezone.utc)
    assert trade_1.price == 90
    assert trade_1.size == 1

    trade_2 = trades[9]
    assert isinstance(trade_2, TradeReceived)
    assert trade_2.run_id == run_id
    assert trade_2.event_id == "EVT_00010"
    assert trade_2.symbol == symbol
    assert trade_2.timestamp_utc == datetime(2026, 1, 1, 0, 0, 9, tzinfo=timezone.utc)
    assert trade_2.price == 99
    assert trade_2.size == 10

def test_ingress_rejects_invalid_n():
    run_id = "TEST_RUN_ID"
    symbol = "TEST_SYMBOL"

    n = 0
    with pytest.raises(ValueError):
        _start_ingress(run_id, symbol, n)

    n = 86401
    with pytest.raises(ValueError):
        _start_ingress(run_id, symbol, n)
import pytest
from datetime import datetime, timezone
from decimal import Decimal

from investiq.domain.trade_store import InMemoryTradeStore
from investiq.events.market_data import TradeReceived


def test_ingest_first_trade_received_event():
    store = InMemoryTradeStore()
    symbol = "TEST_SYMBOL"
    event = TradeReceived(
        run_id="TEST_RUN",
        event_id="EVT_00001",
        symbol=symbol,
        timestamp_utc=datetime(2026,1,1,12, tzinfo=timezone.utc),
        price=Decimal(100),
        size=Decimal(1),
    )
    store.append(event)

    assert symbol in store.symbols
    assert store.has_at_least(symbol, 1)
    assert store.window(symbol, 1) == (event,)


def test_ingest_two_trade_received_events():
    store = InMemoryTradeStore()
    symbol = "TEST_SYMBOL"
    event_1 = TradeReceived(
        run_id="TEST_RUN",
        event_id="EVT_00001",
        symbol=symbol,
        timestamp_utc=datetime(
            2026,1,1,
            12, 0,
            tzinfo=timezone.utc
        ),
        price=Decimal(100),
        size=Decimal(1),
    )
    store.append(event_1)
    event_2 = TradeReceived(
        run_id="TEST_RUN",
        event_id="EVT_00002",
        symbol=symbol,
        timestamp_utc=datetime(
            2026, 1, 1,
            12, 1,
            tzinfo=timezone.utc
        ),
        price=Decimal(102),
        size=Decimal(1),
    )
    store.append(event_2)

    assert symbol in store.symbols
    assert store.has_at_least(symbol, 2)
    assert store.window(symbol, 2) == (event_1, event_2)


def test_ingest_two_trade_received_events_with_different_symbols():
    store = InMemoryTradeStore()
    symbol_1 = "TEST_SYMBOL_1"
    symbol_2 = "TEST_SYMBOL_2"
    event_1 = TradeReceived(
        run_id="TEST_RUN",
        event_id="EVT_00001",
        symbol=symbol_1,
        timestamp_utc=datetime(
            2026,1,1,
            12, 0,
            tzinfo=timezone.utc
        ),
        price=Decimal(100),
        size=Decimal(1),
    )
    store.append(event_1)
    event_2 = TradeReceived(
        run_id="TEST_RUN",
        event_id="EVT_00002",
        symbol=symbol_2,
        timestamp_utc=datetime(
            2026, 1, 1,
            12, 0,
            tzinfo=timezone.utc
        ),
        price=Decimal(102),
        size=Decimal(1),
    )
    store.append(event_2)

    assert symbol_1 in store.symbols
    assert symbol_2 in store.symbols
    assert store.has_at_least(symbol_1, 1)
    assert store.has_at_least(symbol_2, 1)
    assert store.window(symbol_1, 1) == (event_1, )
    assert store.window(symbol_2, 1) == (event_2, )


def test_ingest_rejects_decreasing_timestamps_utc():
    store = InMemoryTradeStore()
    symbol = "TEST_SYMBOL"
    event_1 = TradeReceived(
        run_id="TEST_RUN",
        event_id="EVT_00001",
        symbol=symbol,
        timestamp_utc=datetime(
            2026, 1, 1,
            12, 0,
            tzinfo=timezone.utc
        ),
        price=Decimal(100),
        size=Decimal(1),
    )
    store.append(event_1)
    event_2 = TradeReceived(
        run_id="TEST_RUN",
        event_id="EVT_00002",
        symbol=symbol,
        timestamp_utc=datetime(
            2026, 1, 1,
            11, 59,
            tzinfo=timezone.utc
        ),
        price=Decimal(102),
        size=Decimal(1),
    )

    with pytest.raises(ValueError):
        store.append(event_2)


def test_has_at_least_zero_raises():
    store = InMemoryTradeStore()
    symbol = "TEST_SYMBOL"
    event_1 = TradeReceived(
        run_id="TEST_RUN",
        event_id="EVT_00001",
        symbol=symbol,
        timestamp_utc=datetime(
            2026, 1, 1,
            12, 0,
            tzinfo=timezone.utc
        ),
        price=Decimal(100),
        size=Decimal(1),
    )
    store.append(event_1)

    with pytest.raises(ValueError):
        store.has_at_least(symbol, 0)


def test_window_zero_raises():
    store = InMemoryTradeStore()
    symbol = "TEST_SYMBOL"
    event_1 = TradeReceived(
        run_id="TEST_RUN",
        event_id="EVT_00001",
        symbol=symbol,
        timestamp_utc=datetime(
            2026, 1, 1,
            12, 0,
            tzinfo=timezone.utc
        ),
        price=Decimal(100),
        size=Decimal(1),
    )
    store.append(event_1)

    with pytest.raises(ValueError):
        store.window(symbol, 0)


def test_window_unknown_symbol_raises():
    store = InMemoryTradeStore()
    symbol = "TEST_SYMBOL"
    event_1 = TradeReceived(
        run_id="TEST_RUN",
        event_id="EVT_00001",
        symbol=symbol,
        timestamp_utc=datetime(
            2026, 1, 1,
            12, 0,
            tzinfo=timezone.utc
        ),
        price=Decimal(100),
        size=Decimal(1),
    )
    store.append(event_1)

    with pytest.raises(KeyError):
        store.window("unknown", 1)


def test_window_insufficient_data_raises():
    store = InMemoryTradeStore()
    symbol = "TEST_SYMBOL"
    event_1 = TradeReceived(
        run_id="TEST_RUN",
        event_id="EVT_00001",
        symbol=symbol,
        timestamp_utc=datetime(
            2026, 1, 1,
            12, 0,
            tzinfo=timezone.utc
        ),
        price=Decimal(100),
        size=Decimal(1),
    )
    store.append(event_1)

    with pytest.raises(ValueError):
        store.window(symbol, 2)
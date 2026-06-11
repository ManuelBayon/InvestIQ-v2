from datetime import datetime, timezone

from investiq.domain.market_store import MarketStore
from investiq.domain.models import RawTick

class TestMarketStoreSingleSymbol:
    def test_ingest_first_tick(self):
        store = MarketStore()
        tick_1 = RawTick(
            symbol="test_symbol",
            timestamp_utc=datetime(2026,6,1, 12, tzinfo=timezone.utc),
            tick_type=68,
            price=100.0,
            size=1.0,
        )
        payload = {"test_symbol": [tick_1]}
        store.ingest(payload=payload)
        assert store.view()["test_symbol"] == [tick_1]

    def test_ingest_two_ticks(self):
        store = MarketStore()
        tick_1 = RawTick(
            symbol="test_symbol",
            timestamp_utc=datetime(2026, 6, 1, 12, tzinfo=timezone.utc),
            tick_type=68,
            price=100.0,
            size=1.0,
        )
        payload = {"test_symbol": [tick_1]}
        store.ingest(payload=payload)
        tick_2 = RawTick(
            symbol="test_symbol",
            timestamp_utc=datetime(2026, 6, 1, 13, tzinfo=timezone.utc),
            tick_type=68,
            price=101.0,
            size=2.0,
        )
        payload = {"test_symbol": [tick_2]}
        store.ingest(payload=payload)
        assert store.view()["test_symbol"] == [tick_1, tick_2]

class TestMarketStoreTwoSymbols:
    def test_ingest_first_tick_for_both(self):
        store = MarketStore()
        tick_amd = RawTick(
            symbol="AMD",
            timestamp_utc=datetime(2026,6,1, 12, tzinfo=timezone.utc),
            tick_type=68,
            price=250.0,
            size=1.0,
        )
        tick_nvda = RawTick(
            symbol="NVDA",
            timestamp_utc=datetime(2026, 6, 1, 12, tzinfo=timezone.utc),
            tick_type=68,
            price=500.0,
            size=2.0,
        )
        payload = {"AMD": [tick_amd], "NVDA": [tick_nvda]}
        store.ingest(payload=payload)
        assert store.view()["AMD"] == [tick_amd]
        assert store.view()["NVDA"] == [tick_nvda]
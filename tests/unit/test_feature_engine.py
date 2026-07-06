from datetime import datetime, timezone
from decimal import Decimal

import pytest

from investiq.domain.SMA import SMA
from investiq.domain.feature_engine import FeatureEngine
from investiq.domain.features.feature_set import FeatureSet
from investiq.events.trade_received import TradeReceived


class TestFeatureEngine:

    def test_init_register_valid_feature_sets(self):

        fs1 = FeatureSet(symbol="A", features={})
        fs2 = FeatureSet(symbol="B", features={})

        engine = FeatureEngine([fs1, fs2])

        assert engine._registry[fs1.symbol] == fs1
        assert engine._registry[fs2.symbol] == fs2


    def test_init_raises_on_duplicate_feature_sets(self):

        fs1 = FeatureSet(symbol="A", features={})
        fs2 = FeatureSet(symbol="A", features={})

        with pytest.raises(ValueError):
            FeatureEngine([fs1, fs2])


    def test_update_compute_features(self):
        fs1 = FeatureSet(symbol="A", features={"sma_2": SMA(2)})
        engine = FeatureEngine([fs1])
        event_1 = TradeReceived(
            run_id= "TEST_RUN_ID",
            symbol="A",
            event_id="EVT_00001",
            timestamp_utc=datetime(
                2026,1,1,12, 1,
                tzinfo=timezone.utc
            ),
            price=Decimal(100.0),
            size=Decimal(1.0)
        )
        event_2 = TradeReceived(
            run_id="TEST_RUN_ID",
            symbol="A",
            event_id="EVT_00002",
            timestamp_utc=datetime(
                2026, 1, 1, 12, 2,
                tzinfo=timezone.utc
            ),
            price=Decimal(110.0),
            size=Decimal(1.0)
        )
        engine.update(event_1)
        assert not engine.is_ready("A", "sma_2")

        engine.update(event_2)
        assert engine.is_ready("A", "sma_2")
        assert engine.value("A", "sma_2") == Decimal(105.0)


    def test_update_raises_for_unknown_symbol(self):
        fs1 = FeatureSet(symbol="A", features={"sma_2": SMA(2)})
        engine = FeatureEngine([fs1])
        event_1 = TradeReceived(
            run_id="TEST_RUN_ID",
            symbol="unknown",
            event_id="EVT_00001",
            timestamp_utc=datetime(
                2026, 1, 1, 12, 1,
                tzinfo=timezone.utc
            ),
            price=Decimal(100.0),
            size=Decimal(1.0)
        )
        with pytest.raises(KeyError):
            engine.update(event_1)
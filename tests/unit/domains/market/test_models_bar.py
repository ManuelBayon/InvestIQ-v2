import pytest
import datetime
import math
from investiq.errors import InvalidBar
from investiq.domain.models import Bar

def make_timestamp(
        timezone: datetime.timezone | None = datetime.timezone.utc
) -> datetime.datetime:
    return datetime.datetime(
            2026,
            4,
            1,
            tzinfo=timezone
    )


class TestBarPostInitTimestamp:
    def test_init_rejects_not_utc_timezone(self):
        ts = make_timestamp(timezone=None)
        with pytest.raises(InvalidBar):
            Bar(
                timestamp_utc=ts,
                open=100,
                high=100,
                low=100,
                close=100,
                volume=0
            )
    def test_init_rejects_non_utc_timezone(self):
        ts = make_timestamp(timezone=datetime.timezone(datetime.timedelta(hours=-1)))
        with pytest.raises(InvalidBar):
            Bar(
                timestamp_utc=ts,
                open=100,
                high=100,
                low=100,
                close=100,
                volume=0
            )
    def test_init_accepts_utc_timezone(self):
        ts = make_timestamp()
        Bar(
            timestamp_utc=ts,
            open=100,
            high=100,
            low=100,
            close=100,
            volume=0
        )


class TestBarPostInitValues:
    def test_init_rejects_infinite_values(self):
        ts = make_timestamp()
        with pytest.raises(InvalidBar):
            Bar(
                timestamp_utc=ts,
                open=math.inf,
                high=100,
                low=100,
                close=100,
                volume=0
            )
    def test_init_rejects_nan_values(self):
        ts = make_timestamp()
        with pytest.raises(InvalidBar):
            Bar(
                timestamp_utc=ts,
                open=math.nan,
                high=100,
                low=100,
                close=100,
                volume=0
            )
    def test_init_rejects_negative_values(self):
        ts = make_timestamp()
        with pytest.raises(InvalidBar):
            Bar(
                timestamp_utc=ts,
                open=-1.0,
                high=100,
                low=100,
                close=100,
                volume=0
            )
    def test_init_rejects_high_below_ohlc_max(self):
        ts = make_timestamp()
        with pytest.raises(InvalidBar):
            Bar(
                timestamp_utc=ts,
                open=100,
                high=99,
                low=100,
                close=100,
                volume=0
            )
    def test_init_rejects_low_above_ohlc_min(self):
        ts = make_timestamp()
        with pytest.raises(InvalidBar):
            Bar(
                timestamp_utc=ts,
                open=100,
                high=100,
                low=101,
                close=100,
                volume=0
            )
    def test_init_rejects_negative_volume(self):
        ts = make_timestamp()
        with pytest.raises(InvalidBar):
            Bar(
                timestamp_utc=ts,
                open=100,
                high=100,
                low=100,
                close=100,
                volume=-1
            )
    def test_init_accept_valid_case(self):
        ts = make_timestamp()
        bar = Bar(
            timestamp_utc=ts,
            open=100.01,
            high=110.02,
            low=90.03,
            close=105.04,
            volume=1000,
        )
        assert bar.timestamp_utc == datetime.datetime(
            2026,
            4,
            1,
            tzinfo=datetime.timezone.utc
        )
        assert bar.open == 100.01
        assert bar.high == 110.02
        assert bar.low == 90.03
        assert bar.close == 105.04
        assert bar.volume == 1000
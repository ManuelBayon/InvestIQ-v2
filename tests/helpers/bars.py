from datetime import datetime, timezone

from investiq.domain.models import Bar
from sandbox.canonical_events import BarAvailable

def make_valid_bar_available(
        run_id: str = "test_run_id",
        event_id: str = f"EVT_00001",
        bar: Bar = Bar(
            timestamp_utc = datetime(2026,1, 1, tzinfo=timezone.utc),
            open = 100.0,
            high = 100.0,
            low = 100.0,
            close = 100.0,
        ),
) -> BarAvailable:
    return BarAvailable(
        run_id=run_id,
        causation_id= None,
        event_id=event_id,
        meta_data={},
        bar=bar
    )

def make_multiple_valid_available_bars(
        n: int,
        run_id: str = "test_run_id",
        open: float = 100.0,
        high: float = 100.0,
        low: float = 100.0,
        close: float = 100.0,
) -> list[BarAvailable]:
    if not 1 <= n <= 28:
        raise ValueError("param `n` is used for the day as an integer, please provide a value between 1 and 28")

    bars: list[BarAvailable] = []
    for i in range(1, n+1):
        b = make_valid_bar_available(
            run_id = run_id,
            event_id = f"event_id_{i}",
            bar = Bar(
                timestamp_utc = datetime(2026,1, i, tzinfo=timezone.utc),
                open = open,
                high = high,
                low = low,
                close = close,
            )
        )
        bars.append(b)

    return bars


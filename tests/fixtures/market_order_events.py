from datetime import timezone, datetime

from investiq.core.events import OrderStatusUpdated, FillReceived, CommissionReportReceived

nominal_market_order = [
    OrderStatusUpdated(run_id="TEST_RUN_ID", event_id="EVT_SU0001", order_id=1, parent_id=None, status="PreSubmitted"),
    FillReceived(run_id="TEST_RUN_ID", event_id="EVT_FR001", order_id=1, parent_id=None,exec_id="0000e1a7.6a96adc5.01.01",timestamp_utc=datetime(year=2026,month=8, day=30, hour=20, minute=47, second=19, tzinfo=timezone.utc), qty_executed=1.0, side="SELL", price=29442.75, cumul_qty=1.0),
    OrderStatusUpdated(run_id="TEST_RUN_ID", event_id="EVT_SU0002", order_id=1, parent_id=None, status="Filled"),
    CommissionReportReceived(run_id="TEST_RUN_ID", event_id="EVT_CR0001", order_id=1, parent_id=None, exec_id="0000e1a7.6a96aef9.01.01", commission=0.61, currency="USD", realized_pnl=0.0)
]
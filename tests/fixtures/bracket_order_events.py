from datetime import datetime, timezone, tzinfo
from investiq.core.events import TradeReceived, IntentGenerated, OrderStatusUpdated, FillReceived, CommissionReportReceived
from investiq.domain.orders import BracketOrderSpec, MarketOrderSpec, StopOrderSpec, LimitOrderSpec

TradeReceived(run_id="TEST_RUN_ID", event_id="EVT_00001", symbol="MNQ", timestamp_utc=datetime(2026,1,1,12, tzinfo=timezone.utc), price=100.0, size=1.0)
IntentGenerated(run_id="TEST_RUN_ID", event_id="EVT_00002", causation_id="EVT_00001", instrument_id="MNQZ6", order_spec=BracketOrderSpec(MarketOrderSpec(side="BUY", quantity=1, tif="DAY"), stop_loss=StopOrderSpec(side="SELL", quantity=1, tif="DAY", stop_price=95.0), take_profit=LimitOrderSpec(side="SELL", quantity=1, tif="DAY", limit_price=105.0)))
OrderStatusUpdated(run_id="TEST_RUN_ID", event_id="EVT_00003", order_id=2, parent_id=1, status="PreSubmitted")
OrderStatusUpdated(run_id="TEST_RUN_ID", event_id="EVT_00004", order_id=3, parent_id=1, status="PreSubmitted")
OrderStatusUpdated(run_id="TEST_RUN_ID", event_id="EVT_00005", order_id=1, parent_id=None, status="PreSubmitted")
FillReceived(run_id="TEST_RUN_ID", event_id="EVT_00006", order_id=1, parent_id=None, exec_id="0000e1a7.6aa503e1.01.01", timestamp_utc=datetime(2026,9,11,18,7,21, tzinfo=timezone.utc), qty_executed=1.0, side="BUY", price=29389.75, cumul_qty=1.0)
OrderStatusUpdated(run_id="TEST_RUN_ID", event_id="EVT_00007", order_id=1, parent_id=None, status="Filled")
CommissionReportReceived(run_id="TEST_RUN_ID", event_id="EVT_00008", order_id=1, parent_id=None, exec_id="0000e1a7.6aa503e1.01.01", commission=0.61, currency="USD", realized_pnl=0.0)
OrderStatusUpdated(run_id="TEST_RUN_ID", event_id="EVT_00009", order_id=2, parent_id=1, status="PreSubmitted")
OrderStatusUpdated(run_id="TEST_RUN_ID", event_id="EVT_00010", order_id=3, parent_id=1, status="PreSubmitted")
OrderStatusUpdated(run_id="TEST_RUN_ID", event_id="EVT_00011", order_id=2, parent_id=1, status="Cancelled")
FillReceived(run_id="TEST_RUN_ID", event_id="EVT_00012", order_id=3, parent_id=1, exec_id="0000e1a7.6aa503e2.01.01", timestamp_utc=datetime(2026,9,11,18,7,21,tzinfo=timezone.utc), qty_executed=1.0, side="SELL", price=29388.75, cumul_qty=1.0)
OrderStatusUpdated(run_id="TEST_RUN_ID", event_id="EVT_00013", order_id=3, parent_id=1, status="Filled")
CommissionReportReceived(run_id="TEST_RUN_ID", event_id="EVT_00014", order_id=3, parent_id=1, exec_id="0000e1a7.6aa503e2.01.01", commission=0.61, currency="USD", realized_pnl=-3.22)
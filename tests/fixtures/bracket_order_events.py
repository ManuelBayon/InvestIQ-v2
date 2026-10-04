from datetime import datetime, timezone, tzinfo
from investiq.core.events import TradeReceived, IntentGenerated, OrderStatusUpdated, FillReceived, CommissionReportReceived
from investiq.domain.orders import BracketOrderSpec, MarketOrderSpec, StopLoss, TakeProfit

TradeReceived(run_id="TEST_RUN_ID", event_id="EVT_00001", symbol="MNQ", timestamp_utc=datetime(2026,1,1,12, tzinfo=timezone.utc), price=100.0, size=1.0)
IntentGenerated(run_id="TEST_RUN_ID", event_id="EVT_00002", causation_id="EVT_00001", spec=BracketOrderSpec(MarketOrderSpec(quantity=1), stop_loss=StopLoss(price=95.0), take_profit=TakeProfit(price=105.0)))
OrderStatusUpdated(run_id="TEST_RUN_ID", event_id="EVT_00003", broker_id=279, broker_parent_id=278, status="PreSubmitted")
OrderStatusUpdated(run_id="TEST_RUN_ID", event_id="EVT_00004", broker_id=280, broker_parent_id=278, status="PreSubmitted")
OrderStatusUpdated(run_id="TEST_RUN_ID", event_id="EVT_00005", broker_id=278, broker_parent_id=0, status="PreSubmitted")
FillReceived(run_id="TEST_RUN_ID", event_id="EVT_00006", order_id=278, parent_id=0, exec_id="0000e1a7.6aa503e1.01.01", timestamp_utc=datetime(2026,9,11,18,7,21, tzinfo=timezone.utc), qty_executed=1.0, side="BOT", price=29389.75, cumul_qty=1.0)
OrderStatusUpdated(run_id="TEST_RUN_ID", event_id="EVT_00007", broker_id=278, broker_parent_id=0, status="Filled")
CommissionReportReceived(run_id="TEST_RUN_ID", event_id="EVT_00008", order_id=278, parent_id=0, exec_id="0000e1a7.6aa503e1.01.01", commission=0.61, currency="USD", realized_pnl=0.0)
OrderStatusUpdated(run_id="TEST_RUN_ID", event_id="EVT_00009", broker_id=279, broker_parent_id=278, status="PreSubmitted")
OrderStatusUpdated(run_id="TEST_RUN_ID", event_id="EVT_00010", broker_id=280, broker_parent_id=278, status="PreSubmitted")
OrderStatusUpdated(run_id="TEST_RUN_ID", event_id="EVT_00011", broker_id=279, broker_parent_id=278, status="Cancelled")
FillReceived(run_id="TEST_RUN_ID", event_id="EVT_00012", order_id=280, parent_id=278, exec_id="0000e1a7.6aa503e2.01.01", timestamp_utc=datetime(2026,9,11,18,7,21,tzinfo=timezone.utc), qty_executed=1.0, side="SLD", price=29388.75, cumul_qty=1.0)
OrderStatusUpdated(run_id="TEST_RUN_ID", event_id="EVT_00013", broker_id=280, broker_parent_id=278, status="Filled")
CommissionReportReceived(run_id="TEST_RUN_ID", event_id="EVT_00014", order_id=280, parent_id=278, exec_id="0000e1a7.6aa503e2.01.01", commission=0.61, currency="USD", realized_pnl=-3.22)
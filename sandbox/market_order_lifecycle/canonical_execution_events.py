from ib_insync import Trade

from investiq.domain.instruments import FutureSpecs
from investiq.domain.order_specs import MarketOrderSpecs, Side
from investiq.events.events import OrderStatusUpdated
from sandbox.market_order_lifecycle.market_order_lifecycle import FakeIBKRAdapter

def _map_ibkr_order_status(trade: Trade) -> OrderStatusUpdated:
    status = trade.orderStatus
    return OrderStatusUpdated(
        run_id="test",
        event_id="EVT_00002",
        causation_id="EVT_00001",
        meta_data={},
        payload={},
        order_id =status.orderId,
        parent_id =status.parentId,
        status= status.status,
        client_id= status.clientId,
        broker_perm_id= status.permId,
    )

def on_status_update(trade: Trade) -> None:
    event = _map_ibkr_order_status(trade=trade)
    print(event)


if __name__ =="__main__":

    adapter = FakeIBKRAdapter()
    adapter.connect()

    _order_specs = MarketOrderSpecs(
        instrument=FutureSpecs(symbol="MNQ", local_symbol="MNQU6"),
        quantity=1, direction=Side.BUY, tif="DAY",
    )
    _trade = adapter.place_market_order(order_specs=_order_specs)

    _trade.statusEvent += on_status_update

    adapter.ib.sleep(2)


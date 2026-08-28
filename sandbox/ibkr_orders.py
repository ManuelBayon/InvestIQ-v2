from threading import Thread

from investiq.adapters.ibkr.ib_broker_adapter import IBKRBrokerAdapter
from investiq.adapters.ibkr.ib_client import IBKRClient
from investiq.core.event_factory import CanonicalEventFactory
from investiq.core.event_queue import EventQueue
from investiq.domain.instrument_spec import FutureSpec
from investiq.domain.order_types import MarketOrderSpec

if __name__ == "__main__":

    ib_client = IBKRClient()

    other = Thread(target=ib_client.run, name="ib_thread")
    other.start()
    ib_client.connected.wait()
    print("connected")

    event_factory = CanonicalEventFactory(
        run_id="TEST_RUN_ID"
    )
    event_queue = EventQueue()

    ib_adapter = IBKRBrokerAdapter(
        ib_client=ib_client,
        event_factory=event_factory,
        external_event_queue=event_queue
    )

    contract_spec = FutureSpec(symbol="MNQ", local_symbol="MNQU6")
    order_spec = MarketOrderSpec(quantity=1)



    ib_adapter.place_market_order(contract_spec=contract_spec, order_spec=order_spec)

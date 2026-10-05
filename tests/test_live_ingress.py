import unittest
from unittest.mock import Mock

from investiq.adapters.ibkr.ib_broker_adapter import IBAdapter
from investiq.core.event_factory import EventFactory
from investiq.core.event_queue import EventQueue
from investiq.domain.instrument_spec import FutureSpec, StockSpec
from investiq.ingress.ib_live import IBLiveIngress


class LiveIngressInstrumentTests(unittest.TestCase):
    def test_market_data_and_orders_use_the_same_configured_contract(self):
        instruments = (
            FutureSpec(symbol="MNQ", local_symbol="MNQZ6", exchange="CME"),
            FutureSpec(symbol="OTHER", local_symbol="OTHERH7", exchange="TEST", currency="EUR"),
            StockSpec(symbol="ABC", exchange="SMART", currency="EUR"),
        )
        for instrument in instruments:
            with self.subTest(instrument=instrument):
                client = Mock()
                factory = EventFactory(run_id="TEST")
                queue = EventQueue()
                ingress = IBLiveIngress(client, factory, queue, instrument)
                adapter = IBAdapter(client, factory, queue)

                ingress.start()

                client.request_market_data.assert_called_once_with(
                    contract=adapter.build_contract(instrument)
                )
                client.subscribe_pending_tickers.assert_called_once_with(
                    handler=ingress.on_pending_ticker
                )
                client.run.assert_called_once_with()


if __name__ == "__main__":
    unittest.main()

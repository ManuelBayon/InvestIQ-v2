import asyncio
from collections.abc import Callable

from ib_insync import IB, Ticker, Contract, Order, Trade


class IBClient:

    def __init__(self):
        self._ib = IB()

    def connect(
            self,
            host: str = "127.0.0.1",
            port: int = 7497,
            client_id: int = 1,
    ) -> None:
        self._ib.connect(host=host, port=port, clientId=client_id)

    def disconnect(self):
        self._ib.disconnect()

    def set_market_data_type(self, data_type: int = 3) -> None:
        """
        data_type = 1 for real-time
        data_type = 3 for delayed market_data (by default)
        """
        self._ib.reqMarketDataType(marketDataType=data_type)

    def run(self) -> None:
        loop = asyncio.get_event_loop_policy().get_event_loop()
        self.ib_loop = loop
        self._ib.run()

    def subscribe_pending_tickers(
            self,
            handler: Callable[[set[Ticker]], None]
    ) -> None:
        self._ib.pendingTickersEvent += handler


    def request_market_data(self, contract: Contract) -> Ticker:
        return self._ib.reqMktData(contract=contract)


    def place_order(self, contract: Contract, order: Order) -> Trade:
        return self._ib.placeOrder(contract=contract, order=order)

    @property
    def is_connected(self) -> bool:
        return self._ib.isConnected()

    @property
    def next_id(self) -> int:
        return self._ib.client.getReqId()
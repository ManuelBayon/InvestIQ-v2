from collections.abc import Callable

from ib_insync import IB, Ticker


class IBKRClient:

    def __init__(self):
        self._ib = IB()

    def connect(
            self,
            host: str = "127.0.0.1",
            port: int = 7497,
            client_id: int = 1,

    ) -> None:
        self._ib.connect(host, port, clientId=client_id)

    def set_market_data_type(
            self, data_type: int = 3
    ) -> None:
        """
        data_type = 1 for live data
        data_type = 3 for delayed data (default)
        """
        self._ib.reqMarketDataType(data_type)

    def disconnect(self):
        self._ib.disconnect()

    @property
    def ib_client(self) -> IB:
        return self._ib

    def subscribe_pending_tickers(
            self,
            handler: Callable[[set[Ticker]],None]
    ) -> None:
        self._ib.pendingTickersEvent += handler
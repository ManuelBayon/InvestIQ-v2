from ib_insync import IB


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

    def disconnect(self):
        self._ib.disconnect()

    @property
    def ib_client(self) -> IB:
        return self._ib
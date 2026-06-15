from ib_insync import IB,Future, MarketOrder, Trade

def format_trade(trade: Trade) -> str:
    return \
    f"""
    contrat={trade.contract}
    order={trade.order}
    order_status={trade.orderStatus}
    fills={trade.fills}
    log={trade.log} 
    """


class IBLiveMarketDataFeed:
    """
    2026-05-21 :
        MVP limitation:
            IB reqMktData delayed ticks are used as proxy ticks.
            TickData.time is treated as tick timestamp for aggregation,
            but this is not guaranteed to be exchange trade-time.
    """
    def __init__(self):
        self.ib = IB()

    def connect(
            self,
            host: str = "127.0.0.1",
            port: int = 7497,
            client_id: int = 1,
            data_type: int = 3,  # 1 = Live / 3 = Delayed
    ) -> None:
        self.ib.connect(host, port, clientId=client_id)
        self.ib.reqMarketDataType(data_type)

    def disconnect(self):
        self.ib.disconnect()

if __name__ == "__main__":
    ib_connexion = IBLiveMarketDataFeed()
    ib_connexion.connect()
    order = MarketOrder(
        action="BUY",
        totalQuantity=1,
    )
    order.tif = "DAY"
    trade = ib_connexion.ib.placeOrder(
        contract=Future(symbol="MNQ", localSymbol="MNQU6", exchange="CME"),
        order=order
    )
    while True:
        print(format_trade(trade))
        ib_connexion.ib.sleep(2)
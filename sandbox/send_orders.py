from ib_insync import IB, Future, MarketOrder, Trade, LimitOrder, Contract, StopOrder, BracketOrder


def format_trade(trade: Trade) -> str:
    return \
    f"""
    contrat:{trade.contract}
    order:{trade.order}
    status:{trade.orderStatus.status}
    filled:{trade.orderStatus.filled}
    remaining:{trade.orderStatus.remaining}
    avgFillPrice:{trade.orderStatus.avgFillPrice}
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
            port: int = 4002,
            client_id: int = 1,
            data_type: int = 3,  # 1 = Live / 3 = Delayed
    ) -> None:
        self.ib.connect(host, port, clientId=client_id)
        self.ib.reqMarketDataType(data_type)

    def disconnect(self):
        self.ib.disconnect()

def place_market_order(
        connexion: IBLiveMarketDataFeed,
        local_contract: Contract,
) -> Trade:
    order = MarketOrder(action="BUY", totalQuantity=1)
    order.tif = "DAY"
    return connexion.ib.placeOrder(
        contract=local_contract,
        order=order
    )

def place_limit_order(
        connexion: IBLiveMarketDataFeed,
        local_contract: Contract,
) -> Trade:
    order = LimitOrder(action="BUY", totalQuantity=1, lmtPrice=29500)
    order.tif = "DAY"
    return connexion.ib.placeOrder(
        contract=local_contract,
        order=order
    )

def place_stop_order(
        connexion: IBLiveMarketDataFeed,
        local_contract: Contract,
) -> Trade:
    order = StopOrder(action="BUY", totalQuantity=1, stopPrice=29500)
    order.tif = "DAY"
    return connexion.ib.placeOrder(
        contract=local_contract,
        order=order
    )

def place_market_and_stop_loss(
        connexion: IBLiveMarketDataFeed,
        local_contract: Contract,
) -> list[Trade]:
    parent = MarketOrder(action="BUY", totalQuantity=1)
    parent.orderId = connexion.ib.client.getReqId()
    parent.tif = "DAY"
    parent.transmit = False

    stop_loss = StopOrder(action="SELL", totalQuantity=1, stopPrice=29500)
    stop_loss.parentId = parent.orderId
    stop_loss.orderId = parent.orderId + 1
    stop_loss.tif = "DAY"
    stop_loss.transmit = True

    attached_orders: list[Trade] = []

    result = connexion.ib.placeOrder(contract=local_contract, order=parent)
    attached_orders.append(result)

    result = connexion.ib.placeOrder(contract=local_contract, order=stop_loss)
    attached_orders.append(result)

    return attached_orders

def place_bracket_order(
        connexion: IBLiveMarketDataFeed,
        local_contract: Contract,
) -> list[Trade]:
    parent = MarketOrder(action="BUY", totalQuantity=1)
    parent.orderId = connexion.ib.client.getReqId()
    parent.tif = "DAY"
    parent.transmit = False

    take_profit = LimitOrder(action="SELL", totalQuantity=1, lmtPrice=31000)
    take_profit.parentId = parent.orderId
    take_profit.orderId = parent.orderId +1
    take_profit.tif = "DAY"
    take_profit.transmit = False

    stop_loss = StopOrder(action="SELL", totalQuantity=1, stopPrice=29500)
    stop_loss.parentId = parent.orderId
    stop_loss.orderId = parent.orderId + 2
    stop_loss.tif = "DAY"
    stop_loss.transmit = True

    bracket_order = BracketOrder(parent=parent, takeProfit=take_profit, stopLoss=stop_loss)
    bracket_trade: list[Trade] = []
    for order in bracket_order:
        result = connexion.ib.placeOrder(
            contract=local_contract,
            order=order
        )
        bracket_trade.append(result)
    return bracket_trade

if __name__ == "__main__":
    """
    
    """
    ib_connexion = IBLiveMarketDataFeed()
    ib_connexion.connect()
    contract = Future(symbol="MNQ", localSymbol="MNQU6", exchange="CME")
    trade = place_market_and_stop_loss(connexion=ib_connexion, local_contract=contract)
    for _ in range(3):
        for t in trade:
            formated = format_trade(t)
            print(formated)
        ib_connexion.ib.sleep(2)
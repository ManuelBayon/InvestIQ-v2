import asyncio

from ib_insync import IB, Stock, Future, MarketOrder, Trade, Fill, CommissionReport, OrderStatus

from investiq.domain.instruments import StockSpecs, FutureSpecs
from investiq.domain.order_specs import MarketOrderSpecs, Side
from investiq.events.events import OrderStatusUpdated


class FakeIBKRAdapter:
    """
    2026-05-21 :
        MVP limitation:
            IB reqMktData delayed ticks are used as proxy ticks.
            TickData.time is treated as tick timestamp for aggregation,
            but this is not guaranteed to be exchange trade-time.
    """
    def __init__(
            self,
    ):
        self._ib = IB()
        self._ib_loop = None

    def connect(
            self,
            host: str = "127.0.0.1",
            port: int = 4002,
            client_id: int = 1,
    ) -> None:
        self._ib.connect(host, port, clientId=client_id)

    def disconnect(self):
        self._ib.disconnect()

    def run(self) -> None:
        self._ib_loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self._ib_loop)

        self.connect()
        self._ib.run()

    def map_ibkr_order_status(self, status: OrderStatus) -> OrderStatusUpdated:
        return OrderStatusUpdated(
            run_id="test",
            event_id="EVT_00002",
            causation_id="EVT_00001",
            meta_data={},
            order_id=status.orderId,
            parent_id=status.parentId,
            status=status.status,
            broker_perm_id=status.permId,
        )

    def _on_status_update(self, trade: Trade) -> None:
        event = self.map_ibkr_order_status(status=trade.orderStatus)
        print(event)

    def place_market_order(
            self,
            order_specs: MarketOrderSpecs
    ) -> Trade:

        instrument = order_specs.instrument

        if isinstance(instrument, StockSpecs):
            contract = Stock(
                symbol=instrument.symbol,
                exchange=instrument.exchange,
                currency=instrument.currency
            )
        elif isinstance(instrument, FutureSpecs):
            contract = Future(
                symbol=instrument.symbol,
                localSymbol=instrument.local_symbol,
                exchange=instrument.exchange,
                currency=instrument.currency,
            )
        else:
            raise NotImplementedError(
                f"Unsupported instrument for market order:{type(instrument).__name__}"
            )

        order = MarketOrder(
            action=order_specs.direction.name,
            totalQuantity=order_specs.quantity
        )
        order.tif = order_specs.tif
        trade = self._ib.placeOrder(contract, order)
        trade.statusEvent += self._on_status_update
        return trade

    @property
    def ib_loop(self):
        return self._ib_loop

    @property
    def ib(self):
        return self._ib

def _format_trade(trade: Trade) -> str:
    return \
    f"""contrat: {trade.contract}
    order: {trade.order}
    status: {trade.orderStatus}
    fills: {trade.fills}
    log: {trade.log}
    """

def _format_fill(fill: Fill) -> str:
    return \
        f"""contract: {fill.contract}
        execution: {fill.execution}
        commission report: {fill.commissionReport}
        time: {fill.time}
        """

def on_fill(trade: Trade, fill: Fill):
    print("On Fill: ")
    print(f"trade: {_format_trade(trade)}")
    print(f"fill: {_format_fill(fill)}")

def on_filled(trade: Trade):
    print("On Filled")
    print(_format_trade(trade))

def on_status_update(trade: Trade):
    print("On status update: ")
    print(_format_trade(trade))

def on_commission_report(
        trade: Trade,
        fill: Fill,
        report: CommissionReport
) -> None:
    print("On commission report: ")
    print(_format_trade(trade))
    print(_format_fill(fill))
    print(f"{report}")

if __name__ == "__main__":

    adapter = FakeIBKRAdapter()
    adapter.connect()

    _order_specs = MarketOrderSpecs(
        instrument=FutureSpecs(symbol="MNQ", local_symbol="MNQU6"),
        quantity=1, direction=Side.BUY, tif="DAY",
    )

    _trade = adapter.place_market_order(order_specs=_order_specs)

    _trade.fillEvent += on_fill
    _trade.commissionReportEvent += on_commission_report

    adapter.ib.sleep(2)



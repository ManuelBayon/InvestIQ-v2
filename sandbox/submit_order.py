import asyncio
from decimal import Decimal
from os import environ
from uuid import uuid4

from ib_insync import IB, Stock, Trade

from investiq.contracts.commands.orders import SubmitOrder
from investiq.contracts.identities import CommandId, OrderId
from investiq.contracts.orders.execution import Limit, Market
from investiq.contracts.orders.specifications import OrderSpec
from investiq.contracts.orders.types import Side, TimeInForce
from investiq.refactoring.ibkr_execution_adapter import IBKRExecutionAdapter
from investiq.refactoring.ibkr_instruments import IBKRInstruments
from investiq.refactoring.ibkr_order_registry import IBKROrderRegistry


PAPER_ACCOUNT = environ["INVESTIQ_IBKR_PAPER_ACCOUNT"]
PORT = 7497
CLIENT_ID = 1
SYMBOL = "AAPL"
LIMIT_PRICE = 25000


def on_status(trade: Trade) -> None:
    print(f"orderId={trade.order.orderId} status={trade.orderStatus.status}")


async def main() -> None:
    command = SubmitOrder(
        command_id=CommandId(uuid4().hex),
        order_id=OrderId(uuid4().hex),
        spec=OrderSpec(
            symbol=SYMBOL,
            side=Side.BUY,
            quantity=Decimal("1"),
            execution=Market(),
            time_in_force=TimeInForce.DAY,
        ),
    )

    ib = IB()
    ib.errorEvent += print

    try:
        await ib.connectAsync("127.0.0.1", PORT, clientId=CLIENT_ID)

        if PAPER_ACCOUNT not in ib.managedAccounts():
            raise RuntimeError("Le compte Paper attendu est absent de la session TWS")

        adapter = IBKRExecutionAdapter(
            ib,
            instruments=IBKRInstruments(
                {SYMBOL: Stock(SYMBOL, "SMART", "USD")}
            ),
            registry=IBKROrderRegistry(),
            account=PAPER_ACCOUNT,
            on_order_status=on_status,
            on_fill=print,
            on_commission_report=print,
        )

        await asyncio.to_thread(adapter.dispatch, command)
        await asyncio.sleep(60)

    finally:
        ib.disconnect()


if __name__ == "__main__":
    asyncio.run(main())
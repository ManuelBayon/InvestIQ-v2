from ib_insync import Trade, Fill, CommissionReport, MarketOrder, Contract, LimitOrder, BracketOrder, StopOrder, Order

from investiq.domain.instrument_spec import StockSpec, FutureSpec, InstrumentSpec
from investiq.domain.order_types import MarketOrderSpec, LimitOrderSpec, BracketOrderSpec
from investiq.adapters.ibkr.ib_client import IBClient
from investiq.adapters.ibkr.ib_contract_mappers import map_stock_specs_to_ib_contract, map_future_specs_to_ib_contract
from investiq.core.event_factory import CanonicalEventFactory
from investiq.core.event_queue import EventQueue


class IBKRAdapter:

    def __init__(
            self,
            ib_client: IBClient,
            event_factory: CanonicalEventFactory,
            external_event_queue: EventQueue,
    ):

        self._ib_client = ib_client
        self._event_factory = event_factory
        self._external_event_queue = external_event_queue


    def _on_status_update(self, trade: Trade) -> None:
        status = trade.orderStatus
        event = self._event_factory.create_order_status_updated(
            order_id=status.orderId,
            parent_id=status.parentId,
            status=status.status,
            client_id=status.clientId,
            perm_id=status.permId,
        )
        self._external_event_queue.enqueue(event)


    def _on_fill(self, trade: Trade, fill: Fill) -> None:
        status = trade.orderStatus
        execution = fill.execution
        event = self._event_factory.create_fill_received(
            order_id=status.orderId,
            parent_id=status.parentId,
            client_id=status.clientId,
            perm_id=status.permId,
            exec_id=execution.execId,
            timestamp_utc=execution.time,
            account_num=execution.acctNumber,
            qty_executed=execution.shares,
            side=execution.side,
            price=execution.price,
            cumul_qty=execution.cumQty,
        )
        self._external_event_queue.enqueue(event)


    def _on_commission_report(
            self,
            trade: Trade,
            fill: Fill,
            report: CommissionReport
    ) -> None:
        status = trade.orderStatus
        execution = fill.execution
        event = self._event_factory.create_commission_report_received(
            order_id=status.orderId,
            parent_id=status.parentId,
            client_id=status.clientId,
            perm_id=status.permId,
            exec_id=execution.execId,
            commission=report.commission,
            currency=report.currency,
            realized_pnl=report.realizedPNL,
        )
        self._external_event_queue.enqueue(event)


    def build_contract(self, spec: InstrumentSpec) -> Contract:
        if isinstance(spec, StockSpec):
            contract = map_stock_specs_to_ib_contract(spec)
        elif isinstance(spec, FutureSpec):
            contract = map_future_specs_to_ib_contract(spec)
        else:
            raise NotImplementedError(
                f"Unsupported instrument type: "
                f"{type(spec).__name__}, "
                f"available are Stock and Future."
            )
        return contract


    def _place_order_on_ib_thread(
            self,
            contract: Contract,
            order: Order
    ) -> None:
        trade = self._ib_client.place_order(contract=contract, order=order)

        trade.statusEvent += self._on_status_update
        trade.fillEvent += self._on_fill
        trade.commissionReportEvent += self._on_commission_report


    def _place_bracket_on_ib_thread(
            self,
            contract: Contract,
            bracket: list[Order]
    ) -> None:
        for order in bracket:
            trade =self._ib_client.place_order(contract=contract, order=order)

            trade.statusEvent += self._on_status_update
            trade.fillEvent += self._on_fill
            trade.commissionReportEvent += self._on_commission_report


    def place_market_order(
            self,
            contract_spec: InstrumentSpec,
            order_spec: MarketOrderSpec
    ) -> None:
        # Build contract
        contract = self.build_contract(contract_spec)

        # Build Market Order
        action = "BUY" if order_spec.quantity > 0 else "SELL"
        order = MarketOrder(
            action=action,
            totalQuantity=abs(order_spec.quantity)
        )
        order.tif = "DAY"

        # Place order and subscribe to trade events
        self._ib_client.ib_loop.call_soon_threadsafe(
            self._place_order_on_ib_thread,
            contract,
            order
        )


    def place_limit_order(
            self,
            contract_spec: InstrumentSpec,
            order_spec: LimitOrderSpec
    ) -> None:
        # Build contract
        contract = self.build_contract(contract_spec)

        # Build order
        action = "BUY" if order_spec.quantity > 0 else "SELL"
        order = LimitOrder(
            action=action,
            totalQuantity=abs(order_spec.quantity),
            lmtPrice=order_spec.price
        )
        order.tif = "DAY"

        # Place order and subscribe to trade events
        self._ib_client.ib_loop.call_soon_threadsafe(
            self._place_order_on_ib_thread,
            contract,
            order
        )

    def place_bracket_order(
            self,
            contract_spec: InstrumentSpec,
            order_spec: BracketOrderSpec,
    ) -> None:

        bracket = []

        # Build contract
        contract = self.build_contract(contract_spec)

        # Build parent order
        entry = order_spec.entry
        parent = None
        if isinstance(entry, MarketOrderSpec):
            parent_action = "BUY" if entry.quantity > 0 else "SELL"
            parent = MarketOrder(
                action=parent_action,
                totalQuantity=abs(entry.quantity)
            )
            parent.orderId = self._ib_client.next_id
            parent.tif = "DAY"
            parent.transmit = False

            bracket.append(parent)

        elif isinstance(entry, LimitOrderSpec):
            parent_action = "BUY" if entry.quantity > 0 else "SELL"
            parent = LimitOrder(
                action=parent_action,
                totalQuantity=abs(entry.quantity),
                lmtPrice=entry.price
            )
            parent.orderId = self._ib_client.next_id
            parent.tif = "DAY"
            parent.transmit = False

            bracket.append(parent)

        # Build stop-loss
        if order_spec.stop_loss:
            stop_loss = StopOrder(
                action= "SELL" if entry.quantity > 0 else "BUY" ,
                totalQuantity= abs(entry.quantity),
                stopPrice=order_spec.stop_loss.price,
            )
            stop_loss.parentId = parent.orderId
            stop_loss.orderId = self._ib_client.next_id
            stop_loss.tif = "DAY"
            stop_loss.transmit = False if order_spec.take_profit else True

            bracket.append(stop_loss)

        # Build take-profit
        if order_spec.take_profit:
            take_profit = LimitOrder(
                action="SELL" if entry.quantity > 0 else "BUY",
                totalQuantity=abs(entry.quantity),
                lmtPrice=order_spec.take_profit.price
            )
            take_profit.parentId = parent.orderId
            take_profit.orderId = self._ib_client.next_id
            take_profit.tif = "DAY"
            take_profit.transmit = True

            bracket.append(take_profit)

        # Place orders
        self._ib_client.ib_loop.call_soon_threadsafe(
            self._place_bracket_on_ib_thread,
            contract,
            bracket
        )
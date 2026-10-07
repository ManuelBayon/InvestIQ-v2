from collections.abc import Mapping

from ib_insync import CommissionReport, Contract, Fill, LimitOrder, MarketOrder, Order, StopOrder, Trade

from investiq.adapters.ibkr.ib_client import IBClient
from investiq.adapters.ibkr.ib_contract_mappers import map_future_specs_to_ib_contract, map_stock_specs_to_ib_contract
from investiq.core.broker_messages import (
    BracketPrepared, BrokerCommission, BrokerFill, BrokerOperationFailed, BrokerOrderStatus,
)
from investiq.core.commands import IBSubmitOrder, OrderToPrepare, PrepareBracket, PreparedOrder
from investiq.core.event_queue import EventQueue
from investiq.domain.instrument_spec import FutureSpec, InstrumentSpec, StockSpec
from investiq.domain.orders import LimitOrderSpec, MarketOrderSpec, Side, SingleOrderSpec, StopOrderSpec


class IBAdapter:
    def __init__(
        self,
        ib_client: IBClient,
        inbound_queue: EventQueue,
        run_id: str,
        instruments: Mapping[str, InstrumentSpec],
    ) -> None:
        self._ib_client = ib_client
        self._inbound_queue = inbound_queue
        self._run_id = run_id
        self._instruments = dict(instruments)
        self._contracts: dict[str, Contract] = {}
        self._subscribed = False

    def _on_status_update(self, trade: Trade) -> None:
        self._inbound_queue.enqueue(BrokerOrderStatus(
            run_id=self._run_id,
            broker_order_id=trade.order.orderId,
            status=trade.orderStatus.status,
        ))

    def _on_fill(self, trade: Trade, fill: Fill) -> None:
        execution = fill.execution
        sides: dict[str, Side] = {"BOT": "BUY", "SLD": "SELL", "BUY": "BUY", "SELL": "SELL"}
        side = sides[execution.side]
        self._inbound_queue.enqueue(BrokerFill(
            run_id=self._run_id,
            broker_order_id=execution.orderId,
            exec_id=execution.execId,
            timestamp_utc=execution.time,
            qty_executed=execution.shares,
            side=side,
            price=execution.price,
            cumul_qty=execution.cumQty,
        ))

    def _on_commission_report(self, trade: Trade, fill: Fill, report: CommissionReport) -> None:
        self._inbound_queue.enqueue(BrokerCommission(
            run_id=self._run_id,
            broker_order_id=fill.execution.orderId,
            exec_id=fill.execution.execId,
            commission=report.commission,
            currency=report.currency,
            realized_pnl=report.realizedPNL,
        ))

    def build_contract(self, spec: InstrumentSpec) -> Contract:
        if isinstance(spec, StockSpec):
            return map_stock_specs_to_ib_contract(spec)
        if isinstance(spec, FutureSpec):
            return map_future_specs_to_ib_contract(spec)
        raise NotImplementedError(f"Unsupported instrument type: {type(spec).__name__}")

    def resolve_contract(self, instrument_id: str) -> Contract:
        if instrument_id not in self._contracts:
            try:
                spec = self._instruments[instrument_id]
            except KeyError:
                raise ValueError(f"Unknown instrument_id: {instrument_id}") from None
            self._contracts[instrument_id] = self.build_contract(spec)
        return self._contracts[instrument_id]

    def prepare_on_ib_thread(self, command: PrepareBracket) -> None:
        try:
            self.resolve_contract(command.instrument_id)
            orders = tuple(order for order in (
                command.entry, command.stop_loss, command.take_profit,
            ) if order is not None)
            broker_ids = {order.order_id: self._ib_client.next_id for order in orders}

            def prepare(order: OrderToPrepare | None) -> PreparedOrder | None:
                if order is None:
                    return None
                return PreparedOrder(
                    order_id=order.order_id,
                    parent_id=order.parent_id,
                    spec=order.spec,
                    broker_order_id=broker_ids[order.order_id],
                    broker_parent_id=0 if order.parent_id is None else broker_ids[order.parent_id],
                    transmit=order.order_id == orders[-1].order_id,
                )

            entry = prepare(command.entry)
            assert entry is not None
            prepared = BracketPrepared(
                run_id=command.run_id,
                preparation_id=command.command_id,
                intention_id=command.intention_id,
                instrument_id=command.instrument_id,
                entry=entry,
                stop_loss=prepare(command.stop_loss),
                take_profit=prepare(command.take_profit),
            )
        except Exception as exc:
            self._report_failure(command, "prepare", exc)
            return
        self._inbound_queue.enqueue(prepared)

    def convert_order(
        self, spec: SingleOrderSpec, *, order_id: int, parent_id: int, transmit: bool,
    ) -> Order:
        if isinstance(spec, MarketOrderSpec):
            order = MarketOrder(action=spec.side, totalQuantity=spec.quantity)
        elif isinstance(spec, LimitOrderSpec):
            order = LimitOrder(action=spec.side, totalQuantity=spec.quantity, lmtPrice=spec.limit_price)
        elif isinstance(spec, StopOrderSpec):
            order = StopOrder(action=spec.side, totalQuantity=spec.quantity, stopPrice=spec.stop_price)
        else:
            raise TypeError(f"Unsupported order specification: {type(spec).__name__}")
        order.tif = spec.tif
        order.orderId = order_id
        order.parentId = parent_id
        order.transmit = transmit
        return order

    def submit_on_ib_thread(self, command: IBSubmitOrder) -> None:
        try:
            contract = self.resolve_contract(command.instrument_id)
            order = self.convert_order(
                command.order_spec,
                order_id=command.broker_order_id,
                parent_id=command.broker_parent_id,
                transmit=command.transmit,
            )
            if not self._subscribed:
                # Subscribe before placement, including callbacks emitted synchronously.
                self._ib_client.subscribe_order_events(
                    self._on_status_update, self._on_fill, self._on_commission_report,
                )
                self._subscribed = True
            self._ib_client.place_order(contract, order)
        except Exception as exc:
            self._report_failure(command, "submit", exc)

    def _report_failure(self, command: PrepareBracket | IBSubmitOrder, operation: str, exc: Exception) -> None:
        self._inbound_queue.enqueue(BrokerOperationFailed(
            run_id=command.run_id,
            command_id=command.command_id,
            operation=operation,
            error=f"{type(exc).__name__}: {exc}",
        ))

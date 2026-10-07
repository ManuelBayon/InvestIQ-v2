from dataclasses import dataclass

from investiq.domain.orders import SingleOrderSpec


@dataclass(frozen=True)
class Command:
    run_id: str
    command_id: str


@dataclass(frozen=True)
class OrderToPrepare:
    order_id: int
    parent_id: int | None
    spec: SingleOrderSpec


@dataclass(frozen=True)
class PreparedOrder:
    order_id: int
    parent_id: int | None
    spec: SingleOrderSpec
    broker_order_id: int
    broker_parent_id: int
    transmit: bool


@dataclass(frozen=True)
class PrepareBracket(Command):
    intention_id: str
    instrument_id: str
    entry: OrderToPrepare
    stop_loss: OrderToPrepare | None = None
    take_profit: OrderToPrepare | None = None


@dataclass(frozen=True)
class IBSubmitOrder(Command):
    instrument_id: str
    order_spec: SingleOrderSpec
    broker_order_id: int
    broker_parent_id: int
    transmit: bool

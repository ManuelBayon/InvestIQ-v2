from investiq.adapters.ibkr.ib_broker_adapter import IBAdapter
from investiq.core.event_factory import EventFactory
from investiq.core.events import IntentGenerated, OrderCreated, OrderRole
from investiq.core.handlers.base import HandlerResult
from investiq.core.order_id_generator import OrderIdGenerator
from investiq.domain.instrument_spec import InstrumentSpec
from investiq.domain.orders import MarketOrderSpec, LimitOrderSpec, BracketOrderSpec
from investiq.errors import InvalidOrderType


class IntentGeneratedHandler:

    def __init__(
            self,
            ib_adapter: IBAdapter,
            instrument: InstrumentSpec,
            event_factory: EventFactory,
            order_id_generator: OrderIdGenerator,
    ):
        self._ib_adapter = ib_adapter
        self._instrument_spec = instrument
        self._event_factory = event_factory
        self._order_id_generator = order_id_generator

    def handle(self, intent: IntentGenerated) -> HandlerResult:

        orders_created = []

        if isinstance(intent.spec, MarketOrderSpec):
            self._ib_adapter.place_market_order(
                contract_spec=self._instrument_spec,
                order_spec=intent.spec
            )
        elif isinstance(intent.spec, LimitOrderSpec):
            self._ib_adapter.place_limit_order(
                contract_spec=self._instrument_spec,
                order_spec=intent.spec
            )
        elif isinstance(intent.spec, BracketOrderSpec):

            # Create entry
            entry_created = self._event_factory.create_order_created(
                intention_id=intent.event_id,
                order_id=self._order_id_generator.next_id(),
                parent_id=None,
                role=OrderRole.ENTRY
            )
            orders_created.append(entry_created)

            if intent.spec.stop_loss:
                # Create stop loss
                stop_loss_created = self._event_factory.create_order_created(
                    intention_id=intent.event_id,
                    order_id=self._order_id_generator.next_id(),
                    parent_id=entry_created.order_id,
                    role=OrderRole.STOP_LOSS
                )
                orders_created.append(stop_loss_created)

            if intent.spec.take_profit:
                # Create take profit
                take_profit_created = self._event_factory.create_order_created(
                    intention_id=intent.event_id,
                    order_id=self._order_id_generator.next_id(),
                    parent_id=entry_created.order_id,
                    role=OrderRole.TAKE_PROFIT
                )
                orders_created.append(take_profit_created)

            self._ib_adapter.place_bracket_order(
                contract_spec=self._instrument_spec,
                order_spec=intent.spec
            )
        else:
            raise InvalidOrderType(
                f"Order type not recognize, "
                f"order.__class__={intent.spec.__class__}"
            )

        return HandlerResult(
            events=tuple(orders_created)
        )

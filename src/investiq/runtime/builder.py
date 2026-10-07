from collections.abc import Mapping

from investiq.adapters.ibkr.ib_broker_adapter import IBAdapter
from investiq.adapters.ibkr.ib_client import IBClient

from investiq.core.dispatcher import Dispatcher
from investiq.core.event_factory import EventFactory
from investiq.core.event_journal import EventJournal
from investiq.core.event_loop import CanonicalEventLoop
from investiq.core.event_queue import EventQueue
from investiq.core.order_id_generator import OrderIdGenerator
from investiq.core.command_id_generator import CommandIdGenerator
from investiq.core.order_correlation import OrderCorrelation
from investiq.core.handlers.bracket_prepared_handler import BracketPreparedHandler
from investiq.core.handlers.broker_return_handler import BrokerReturnHandler
from investiq.core.handlers.ib_command_handlers import IBSubmitOrderHandler, PrepareBracketHandler
from investiq.core.handlers.intent_generated_handler import IntentGeneratedHandler
from investiq.core.handlers.trade_received_handler import TradeReceivedHandler

from investiq.domain.experiment import build_features, validate_strategy_requirements, bootstrap_feature_runtime
from investiq.domain.features.features import Feature
from investiq.domain.features.sources import PriceSource
from investiq.domain.market_store import InMemoryMarketStore
from investiq.domain.instrument_spec import FutureSpec

from investiq.ingress.ib_live import IBLiveIngress
from investiq.ingress.synthetic import SyntheticIngress

from investiq.runtime.base import RuntimeConfig
from investiq.runtime.live import LiveRuntime, LiveRuntimeConfig
from investiq.runtime.sequential import SequentialRuntime, Runtime, SequentialRuntimeConfig


def build_runtime(config: RuntimeConfig) -> Runtime:

    experiment = config.experiment

    symbol = experiment.instrument.symbol
    store = InMemoryMarketStore(symbol)
    price_source = PriceSource(source=store, symbol=symbol)

    features_by_name: Mapping[str, Feature] = build_features(
        source=price_source,
        features=experiment.features
    )

    validate_strategy_requirements(
        requirements=experiment.strategy.requirements,
        available_feature=features_by_name
    )

    feature_runtime = bootstrap_feature_runtime(
        sources=[price_source],
        features=list(features_by_name.values())
    )

    strategy = experiment.strategy()
    strategy_features = {
        requirement.name: features_by_name[requirement.name]
        for requirement in strategy.requirements
    }

    ib_client = IBClient()

    inbound_queue = EventQueue()
    internal_event_queue = EventQueue()
    event_factory = EventFactory(run_id=config.experiment.run_id)
    order_id_generator = OrderIdGenerator()
    command_id_generator = CommandIdGenerator()
    correlation = OrderCorrelation()
    instrument_id = (
        experiment.instrument.local_symbol
        if isinstance(experiment.instrument, FutureSpec) else experiment.instrument.symbol
    )

    ib_adapter = IBAdapter(
        ib_client=ib_client,
        inbound_queue=inbound_queue,
        run_id=experiment.run_id,
        instruments={instrument_id: experiment.instrument},
    )

    trade_received_handler = TradeReceivedHandler(
        market_store=store,
        price_source=price_source,
        symbol=symbol,
        feature_runtime=feature_runtime,
        strategy_features=strategy_features,
        strategy=strategy,
        event_factory=event_factory,
        instrument_id=instrument_id,
    )

    intent_generated_handler = IntentGeneratedHandler(
        order_id_generator=order_id_generator,
        command_id_generator=command_id_generator,
    )

    event_loop = CanonicalEventLoop(
        inbound_queue=inbound_queue,
        internal_event_queue=internal_event_queue,
        journal=EventJournal(),
        correlation=correlation,
        dispatcher=Dispatcher(
            trade_received_handler=trade_received_handler,
            intent_generated_handler=intent_generated_handler,
            prepare_bracket_handler=PrepareBracketHandler(ib_client, ib_adapter, event_factory),
            bracket_prepared_handler=BracketPreparedHandler(event_factory, command_id_generator),
            submit_order_handler=IBSubmitOrderHandler(ib_client, ib_adapter, event_factory),
            broker_return_handler=BrokerReturnHandler(correlation, event_factory),
        )
    )

    if isinstance(config, SequentialRuntimeConfig):
        ingress = SyntheticIngress(
            scenario=config.trades[:config.num_trades],
            event_queue=inbound_queue,
            run_id=experiment.run_id,
        )
        return SequentialRuntime(
            ingress=ingress,
            event_loop=event_loop,
            ib_client=ib_client,
        )
    elif isinstance(config, LiveRuntimeConfig):
        ingress = IBLiveIngress(
            instrument=experiment.instrument,
            inbound_queue=inbound_queue,
            run_id=experiment.run_id,
            ib_client=ib_client
        )
        return LiveRuntime(
            ingress=ingress,
            event_loop=event_loop,
            ib_client=ib_client,
        )
    else:
        raise ValueError("Invalid RuntimeConfig type.")

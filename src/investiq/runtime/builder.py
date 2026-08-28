from investiq.adapters.ibkr.ib_broker_adapter import IBKRAdapter
from investiq.adapters.ibkr.ib_client import IBKRClient

from investiq.core.dispatcher import Dispatcher
from investiq.core.event_factory import CanonicalEventFactory
from investiq.core.event_journal import EventTransitionJournal
from investiq.core.event_loop import CanonicalEventLoop
from investiq.core.event_queue import EventQueue
from investiq.core.handlers.order_generated_handler import OrderGeneratedHandler
from investiq.core.handlers.trade_received_handler import TradeReceivedHandler

from investiq.domain.experiment import build_features, validate_strategy_requirements, bootstrap_feature_runtime
from investiq.domain.features.sources import PriceSource
from investiq.domain.market_store import InMemoryMarketStore

from investiq.ingress.ib_live import IBKRLiveIngress
from investiq.ingress.synthetic import SyntheticIngress

from investiq.runtime.base import RuntimeConfig
from investiq.runtime.live import LiveRuntime, LiveRuntimeConfig
from investiq.runtime.sequential import SequentialRuntime, Runtime, SequentialRuntimeConfig


def build_runtime(config: RuntimeConfig) -> Runtime:

    experiment = config.experiment

    symbol = experiment.instrument.symbol
    store = InMemoryMarketStore(symbol)
    price_source = PriceSource(source=store, symbol=symbol)

    features_by_name = build_features(
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

    ib_client = IBKRClient()

    external_event_queue = EventQueue()
    internal_event_queue = EventQueue()
    event_factory = CanonicalEventFactory(run_id=config.experiment.run_id)

    ib_adapter = IBKRAdapter(
        ib_client=ib_client,
        event_factory=event_factory,
        external_event_queue=external_event_queue,
    )

    trade_received_handler = TradeReceivedHandler(
        market_store=store,
        price_source=price_source,
        symbol=symbol,
        feature_runtime=feature_runtime,
        strategy_features=strategy_features,
        strategy=strategy,
        event_factory=event_factory,
    )

    order_generated_handler = OrderGeneratedHandler(
        ib_adapter=ib_adapter,
        instrument=experiment.instrument
    )

    event_loop = CanonicalEventLoop(
        external_event_queue=external_event_queue,
        internal_event_queue=internal_event_queue,
        journal=EventTransitionJournal(),
        dispatcher=Dispatcher(
            trade_received_handler=trade_received_handler,
            order_generated_handler=order_generated_handler,
        )
    )

    if isinstance(config, SequentialRuntimeConfig):
        ingress = SyntheticIngress(
            scenario=config.trades[:config.num_trades],
            event_queue=external_event_queue,
            event_factory=event_factory,
        )
        return SequentialRuntime(
            ingress=ingress,
            event_loop=event_loop,
            ib_client=ib_client,
        )
    elif isinstance(config, LiveRuntimeConfig):
        ingress = IBKRLiveIngress(
            external_event_queue=external_event_queue,
            event_factory=event_factory,
            ib_client=ib_client
        )
        return LiveRuntime(
            ingress=ingress,
            event_loop=event_loop,
            ib_client=ib_client,
        )
    else:
        raise ValueError("Invalid RuntimeConfig type.")
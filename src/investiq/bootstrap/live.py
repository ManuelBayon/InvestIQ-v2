from investiq.adapters.ibkr.ib_client import IBKRClient
from investiq.bootstrap.experiment import ExperimentSpec, build_features, validate_strategy_requirements, \
    bootstrap_feature_runtime
from investiq.domain.market_store import InMemoryMarketStore
from investiq.features.sources import PriceSource
from investiq.ingress.ib_live import IBKRLiveIngress
from investiq.runtime.live import LiveRuntime
from investiq.events.factory import CanonicalEventFactory
from investiq.process.dispatcher import Dispatcher
from investiq.core.event_journal import EventTransitionJournal
from investiq.core.event_loop import CanonicalEventLoop
from investiq.core.event_queue import CanonicalEventQueue
from investiq.handlers.trade_received_handler import TradeReceivedHandler


def bootstrap_live_runtime(
        run_id: str,
        experiment: ExperimentSpec,
) -> LiveRuntime:

    universe = (experiment.symbol,)
    store = InMemoryMarketStore(universe)

    price_source = PriceSource(
        source=store,
        symbol=experiment.symbol
    )

    features_by_name = build_features(
        source=price_source,
        features=experiment.features
    )

    validate_strategy_requirements(
        requirements=experiment.strategy_spec.strategy_type.requirements,
        available_feature=features_by_name
    )

    feature_runtime = bootstrap_feature_runtime(
        sources=[price_source],
        features=list(features_by_name.values())
    )

    strategy = experiment.strategy_spec.strategy_type()

    strategy_features = {
        requirement.name: features_by_name[requirement.name]
        for requirement in strategy.requirements
    }

    ib_client = IBKRClient()

    event_factory = CanonicalEventFactory(run_id=run_id)
    event_queue = CanonicalEventQueue()

    ingress = IBKRLiveIngress(
        event_factory=event_factory,
        event_queue=event_queue,
        ibkr_client=ib_client,
    )

    trade_received_handler = TradeReceivedHandler(
        market_store=store,
        price_source=price_source,
        symbol=experiment.symbol,
        feature_runtime=feature_runtime,
        strategy_features=strategy_features,
        strategy=strategy,
    )

    event_loop = CanonicalEventLoop(
        event_queue=event_queue,
        journal=EventTransitionJournal(),
        dispatcher=Dispatcher(
            trade_received_handler=trade_received_handler
        )
    )
    return LiveRuntime(
        run_id=run_id,
        ingress=ingress,
        event_loop=event_loop,
    )
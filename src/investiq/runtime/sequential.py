from investiq.domain.experiment import ExperimentSpec, build_features, validate_strategy_requirements, \
    bootstrap_feature_runtime
from investiq.core.dispatcher import Dispatcher
from investiq.core.event_factory import CanonicalEventFactory
from investiq.core.event_journal import EventTransitionJournal
from investiq.core.event_loop import CanonicalEventLoop
from investiq.core.event_queue import CanonicalEventQueue
from investiq.core.handlers.trade_received_handler import TradeReceivedHandler
from investiq.domain.features.sources import PriceSource
from investiq.domain.market_store import InMemoryMarketStore
from investiq.ingress.protocol import Ingress
from investiq.ingress.synthetic import SyntheticIngress
from tests.fixtures.market.simple_trades import MONO_SYMBOL_SIMPLE_TRADES


class SequentialRuntime:

    def __init__(
            self,
            run_id: str,
            ingress: Ingress,
            event_loop: CanonicalEventLoop,
    ):
        self._run_id = run_id
        self._ingress = ingress
        self._event_loop = event_loop


    def run(self) -> None:
        self._ingress.start()
        self._event_loop.run_until_empty()

def bootstrap_synthetical_runtime(
        run_id: str,
        num_trades: int,
        experiment: ExperimentSpec,
) -> SequentialRuntime:

    store = InMemoryMarketStore(experiment.symbol)

    price_source = PriceSource(
        source=store,
        symbol=experiment.symbol
    )

    features_by_name = build_features(
        source=price_source,
        features=experiment.features
    )

    validate_strategy_requirements(
        requirements=experiment.strategy.strategy_type.requirements,
        available_feature=features_by_name
    )

    feature_runtime = bootstrap_feature_runtime(
        sources=[price_source],
        features=list(features_by_name.values())
    )

    strategy = experiment.strategy.strategy_type()

    strategy_features = {
        requirement.name: features_by_name[requirement.name]
        for requirement in strategy.requirements
    }

    event_queue = CanonicalEventQueue()

    event_factory = CanonicalEventFactory(
        run_id=run_id
    )

    ingress = SyntheticIngress(
        event_queue=event_queue,
        event_factory=event_factory,
        scenario=[t for t in MONO_SYMBOL_SIMPLE_TRADES[:num_trades]]
    )

    trade_received_handler = TradeReceivedHandler(
        market_store=store,
        price_source=price_source,
        symbol=experiment.symbol,
        feature_runtime=feature_runtime,
        strategy_features=strategy_features,
        strategy=strategy,
        event_factory=event_factory,
    )

    event_loop = CanonicalEventLoop(
        event_queue=event_queue,
        journal=EventTransitionJournal(),
        dispatcher=Dispatcher(
            trade_received_handler=trade_received_handler,
        )
    )

    return SequentialRuntime(
        run_id=run_id,
        ingress=ingress,
        event_loop=event_loop,
    )
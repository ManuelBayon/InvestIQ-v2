from threading import Thread

from investiq.adapters.ibkr.ib_client import IBKRClient
from investiq.domain.experiment import ExperimentSpec, build_features, validate_strategy_requirements, \
    bootstrap_feature_runtime
from investiq.core.dispatcher import Dispatcher
from investiq.core.event_factory import CanonicalEventFactory
from investiq.core.event_journal import EventTransitionJournal
from investiq.core.event_loop import CanonicalEventLoop
from investiq.core.external_event_queue import ExternalEventQueue
from investiq.core.handlers.trade_received_handler import TradeReceivedHandler
from investiq.domain.features.sources import PriceSource
from investiq.domain.market_store import InMemoryMarketStore
from investiq.ingress.ib_live import IBKRLiveIngress
from investiq.ingress.protocol import Ingress


class LiveRuntime:


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
        thread = Thread(target=self._event_loop.run_forever)
        thread.start()
        self._ingress.start()


def bootstrap_live_runtime(
        run_id: str,
        experiment: ExperimentSpec,
) -> LiveRuntime:
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

    ib_client = IBKRClient()

    event_factory = CanonicalEventFactory(run_id=run_id)
    event_queue = ExternalEventQueue()

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
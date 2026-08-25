from investiq.domain.experiment import ExperimentSpec
from investiq.domain.features.features import FeatureSpec

from investiq.domain.features.simple_moving_average import SimpleMovingAverage

from investiq.domain.strategies.base_strategy import StrategySpec
from investiq.domain.strategies.simple_moving_average_cross import MovingAverageCrossStrategy
from investiq.domain.strategies.trivial_strategy import Return1BracketOrderStrategy
from investiq.runtime.live import bootstrap_live_runtime
from investiq.runtime.sequential import bootstrap_synthetical_runtime

if __name__ == "__main__":

    strategy_spec = StrategySpec(
        strategy_type=Return1BracketOrderStrategy,
    )

    experiment = ExperimentSpec(
        symbol="SYMBOL_1",
        features={},
        strategy=strategy_spec,
    )

    """"""
    bootstrap_synthetical_runtime(
        run_id="TEST_RUN",
        num_trades=5,
        experiment=experiment
    ).run()


    """
    bootstrap_live_runtime(
        run_id="TEST_LIVE_RUN",
        experiment=experiment
    ).run()
    """


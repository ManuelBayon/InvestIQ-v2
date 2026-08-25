from investiq.domain.experiment import ExperimentSpec
from investiq.domain.features.features import FeatureSpec

from investiq.domain.features.simple_moving_average import SimpleMovingAverage

from investiq.domain.strategies.base_strategy import StrategySpec
from investiq.domain.strategies.simple_moving_average_cross import MovingAverageCrossStrategy
from investiq.runtime.live import bootstrap_live_runtime
from investiq.runtime.sequential import bootstrap_synthetical_runtime

if __name__ == "__main__":

    sma_short_spec = FeatureSpec(
        feature_type=SimpleMovingAverage,
        params={
            "window": 2
        }
    )

    sma_long_spec = FeatureSpec(
        feature_type=SimpleMovingAverage,
        params={
            "window": 5,
        }
    )

    strategy_spec = StrategySpec(
        strategy_type=MovingAverageCrossStrategy,
    )

    experiment = ExperimentSpec(
        symbol="MNQ",
        features={
            "sma_short": sma_short_spec,
            "sma_long": sma_long_spec,
        },
        strategy=strategy_spec,
    )

    """
    bootstrap_synthetical_runtime(
        run_id="TEST_RUN",
        num_trades=6,
        experiment=experiment
    ).run()
    """

    """"""
    bootstrap_live_runtime(
        run_id="TEST_LIVE_RUN",
        experiment=experiment
    ).run()


from investiq.bootstrap.experiment import ExperimentSpec
from investiq.bootstrap.live import bootstrap_live_runtime

from investiq.features.features import FeatureSpec

from investiq.features.simple_moving_average import SimpleMovingAverage

from investiq.strategies.base_strategy import StrategySpec
from investiq.strategies.simple_moving_average_cross import MovingAverageCrossStrategy


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

    exp = ExperimentSpec(
        symbol="MNQ",
        features={
            "sma_short": sma_short_spec,
            "sma_long": sma_long_spec,
        },
        strategy_spec=strategy_spec,
    )

    """
    synthetic_runtime = bootstrap_synthetical_runtime(
        run_id="TEST_RUN",
        num_trades=6,
        experiment=exp
    )
    synthetic_runtime.run()
    """
    live_runtime = bootstrap_live_runtime("TEST_LIVE_RUN", exp)
    live_runtime.run()


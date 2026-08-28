from investiq.domain.experiment import ExperimentSpec
from investiq.domain.features.features import FeatureSpec

from investiq.domain.features.simple_moving_average import SimpleMovingAverage
from investiq.domain.instrument_spec import FutureSpec

from investiq.domain.strategies.moving_average_cross import MovingAverageCrossStrategy
from investiq.runtime.builder import build_runtime
from investiq.runtime.sequential import SequentialRuntimeConfig
from tests.fixtures.market.simple_trades import MONO_SYMBOL_SIMPLE_TRADES

if __name__ == "__main__":

    sma_short = FeatureSpec(
        feature=SimpleMovingAverage,
        params={
            "window": 2
        }
    )

    sma_long = FeatureSpec(
        feature=SimpleMovingAverage,
        params={
            "window": 5
        }
    )

    experiment = ExperimentSpec(
        run_id="TEST_SYNTHETIC_RUN",
        instrument=FutureSpec(
            symbol="MNQ",
            local_symbol="MNQU6"
        ),
        features={
            "sma_short": sma_short,
            "sma_long": sma_long,
        },
        strategy=MovingAverageCrossStrategy,
    )

    runtime = build_runtime(
        config=SequentialRuntimeConfig(
            experiment=experiment,
            trades=MONO_SYMBOL_SIMPLE_TRADES,
            num_trades=5
        )
    )
    runtime.run()
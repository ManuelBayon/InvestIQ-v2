from collections.abc import Sequence

from investiq.domain.market_store import InMemoryMarketStore
from investiq.events.trade_received import TradeReceived
from sandbox.features import PriceSource, Feature, Source
from tests.fixtures.market.simple import MONO_SYMBOL_SIMPLE_TRADES

class FakeFeature:
    def __init__(
            self,
            name: str,
            sources: list[Source],
            emissions: list[bool],
    ):
        self._sources = sources
        self._emissions = emissions
        self._successors: list[Feature] = []
        self._index = 0
        self.name = name

    def compute(self) -> bool:
        result = self._emissions[self._index]
        self._index += 1
        return result

    def load(self, window: int) -> Sequence[float]:
        return []

    @property
    def successors(self) -> list["Feature"]:
        return self._successors

def bootstrap_feature_graph(features: list[Feature]) -> None:
    print("Bootstrap running...\n")

    for feature in features:
        feature_name = feature.__dict__.get("name")

        if feature in roots.values():
            continue

        sources = feature.__dict__.get("_sources")
        print(f"Feature {feature_name} source {[s.__dict__.get("name") for s in sources]}")

        for s in sources:
            s.__dict__.get("_successors").append(feature)

    print(f"\nFeature A successors {[s.__dict__.get("name") for s in A.successors]}")
    print(f"Feature B successors {[s.__dict__.get("name") for s in B.successors]}")
    print(f"Feature C successors {[s.__dict__.get("name") for s in C.successors]}")
    print(f"Feature D successors {[s.__dict__.get("name") for s in D.successors]}")
    print(f"Feature E successors {[s.__dict__.get("name") for s in E.successors]}")
    print(f"Feature F successors {[s.__dict__.get("name") for s in F.successors]}")

def print_trace(
        eligible_before: list[Feature],
        current: Feature,
        emit: bool,
        emitted: set[Feature],
        successors: list[Feature],
        eligible_after: list[Feature]
) -> None:
    print(
        f"\neligible before: {[e.name for e in eligible_before]}"
        f"\ncurrent: {current.name}"
        f"\nemit: {emit}"
        f"\nemitted: {[e.name for e in emitted]}"
        f"\nsuccessors: {[s.name for s in successors]}"
        f"\neligible after : {[e.name for e in eligible_after]}"
    )


def on_trade(trade: TradeReceived, i: int) -> None:
    print(f"\nTrade {i}")

    eligible: list[Feature] = [A]
    emitted = set()

    store.on_trade_received(trade)

    while len(eligible) > 0:

        eligible_before = eligible.copy()
        current = eligible.pop(0)
        emit = current.compute()

        if not emit:
            print_trace(
                eligible_before,
                current,
                emit,
                emitted,
                current.successors,
                eligible
            )
            continue

        emitted.add(current)

        for successor in current.successors:
            sources = successor.__dict__.get("_sources")

            if set(sources).issubset(emitted):
                eligible.append(successor)

        print_trace(
            eligible_before,
            current,
            emit,
            emitted,
            current.successors,
            eligible
        )


if __name__ == "__main__":

    universe = ("SYMBOL_1",)
    store = InMemoryMarketStore(universe)
    price = PriceSource(source=store, symbol=universe[0])

    A = FakeFeature(
        name="A",
        emissions=[False, True, True, True],
        sources=[price],
    )

    B = FakeFeature(
        name="B",
        emissions=[False, True, True],
        sources=[A],
    )

    C = FakeFeature(
        name="C",
        emissions=[False, True, True],
        sources=[A],
    )

    D = FakeFeature(
        name="D",
        emissions=[False, True],
        sources=[B],
    )

    E = FakeFeature(
        name="E",
        emissions=[False, True],
        sources=[A, C],
    )

    F = FakeFeature(
        name="F",
        emissions=[True],
        sources=[D, E],
    )

    roots = {"SYMBOL_1": A}
    bootstrap_feature_graph([A, B, C, D, E, F])

    # Run
    for i in range(4):
        trade = MONO_SYMBOL_SIMPLE_TRADES[i]
        on_trade(trade, i)
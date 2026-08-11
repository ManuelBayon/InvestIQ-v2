from collections.abc import Sequence

from investiq.domain.market_store import InMemoryMarketStore
from investiq.events.trade_received import TradeReceived
from sandbox.features import PriceSource, Feature, Source
from tests.fixtures.market.simple import MULTI_SYMBOLS_SIMPLE_TRADES, MONO_SYMBOL_SIMPLE_TRADES

class FakeFeature:
    def __init__(
            self,
            sources: list[Source],
            emissions: list[bool],
            name: str,
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


def on_trade(trade: TradeReceived) -> None:

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

    A = FakeFeature(sources=[price], emissions=[False, True, True, True], name="A")
    B = FakeFeature(sources=[A], emissions=[False, True, True], name="B")
    C = FakeFeature(sources=[A, B], emissions=[False, True], name="C")

    roots = {"SYMBOL_1": A}

    bootstrap_feature_graph([A, B, C])

    trade_0 = MONO_SYMBOL_SIMPLE_TRADES[0]
    trade_1 = MONO_SYMBOL_SIMPLE_TRADES[1]
    trade_2 = MONO_SYMBOL_SIMPLE_TRADES[2]
    trade_3 = MONO_SYMBOL_SIMPLE_TRADES[3]

    # Run
    print("\nTrade 0")
    on_trade(trade_0)

    print("\nTrade 1")
    on_trade(trade_1)

    print("\nTrade 2")
    on_trade(trade_2)

    print("\nTrade 3")
    on_trade(trade_3)


What is currently supported:

- The indicator graph currently supports multiple parents and multiple children.
- It reconstructs the graph based on dependencies (sources) and the root.
- The current policy is as follows: a node becomes eligible when **all of its parents have emitted during the current trade**.
  
What is not yet supported:

- It does not yet support cross-asset features or the related issues.
- Integration into the runtime: currently, the prototype exists in the sandbox; I was planning to create a validated, initialized, and fixed runtime at bootstrap.
- Incomplete validation (duplicates, cycles, etc.)

---
## Example of bootstrap in sandbox before integration in the trading engine

![[Feature Model and Semantics-MultiParents.drawio.png]]

---

```python
from collections.abc import Sequence

from investiq.domain.market_store import InMemoryMarketStore
from investiq.events.trade_received import TradeReceived
from sandbox.features import PriceSource, Feature, Source
from tests.fixtures.market.simple_trades import MULTI_SYMBOLS_SIMPLE_TRADES


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
        result = self._emissions[self._index % len(self._emissions)]
        self._index += 1
        return result

    def load(self, window: int) -> Sequence[float]:
        return []

    @property
    def successors(self) -> list["Feature"]:
        return self._successors


def bootstrap_feature_graph(features: list[Feature]) -> None:
    print("\nBootstrap running...\n")

    for feature in features:
        feature_name = feature.__dict__.get("name")

        if feature in roots.values():
            continue

        sources = feature.__dict__.get("_sources")
        print(f"Feature {feature_name} source {[s.__dict__.get("name") for s in sources]}")

        for s in sources:
            s.__dict__.get("_successors").append(feature)

    print("\nSuccessors : ")
    for f in features:
        print(f"Feature {f.name} successors {[s.__dict__.get("name") for s in f.successors]}")


def print_trace(
        symbol: str,
        num_trade: int,
        step: int,
        eligible_before: list[Feature],
        current: Feature,
        emit: bool,
        emitted: set[Feature],
        successors: list[Feature],
        eligible_after: list[Feature]
) -> None:
    print(
        f"\n{symbol}, trade n°{num_trade}, step n°{step}"
        f"\neligible before: {[e.name for e in eligible_before]}"
        f"\ncurrent: {current.name}"
        f"\nemit: {emit}"
        f"\nemitted: {[e.name for e in emitted]}"
        f"\nsuccessors: {[s.name for s in successors]}"
        f"\neligible after : {[e.name for e in eligible_after]}"
    )


def on_trade(trade: TradeReceived, i: int) -> None:
    root = roots[trade.symbol]

    eligible: list[Feature] = [root]
    emitted = set()

    step: int = 0

    store.on_trade_received(trade)

    while len(eligible) > 0:
        eligible_before = eligible.copy()
        current = eligible.pop(0)
        emit = current.compute()

        if not emit:
            print_trace(
                trade.symbol, i, step, eligible_before, current,
                emit, emitted, current.successors, eligible)

            step += 1
            continue

        emitted.add(current)

        for successor in current.successors:
            sources = successor.__dict__.get("_sources")

            if set(sources).issubset(emitted):
                eligible.append(successor)

        print_trace(
            trade.symbol, i, step, eligible_before, current,
            emit, emitted, current.successors, eligible)

        step += 1


if __name__ == "__main__":

    universe = ("SYMBOL_1", "SYMBOL_2")
    store = InMemoryMarketStore(universe)

    roots = {}

    # Bootstrap symbol 1 feature graph  
    price_s1 = PriceSource(source=store, symbol=universe[0])
    A = FakeFeature(name="A", emissions=[False, True, True, True], sources=[price_s1])
    B = FakeFeature(name="B", emissions=[False, True, True], sources=[A])
    C = FakeFeature(name="C", emissions=[False, True, True], sources=[A])
    D = FakeFeature(name="D", emissions=[False, True], sources=[B])
    E = FakeFeature(name="E", emissions=[False, True], sources=[A, C])
    F = FakeFeature(name="F", emissions=[True], sources=[D, E])

    roots["SYMBOL_1"] = A
    bootstrap_feature_graph([A, B, C, D, E, F])

    # Bootstrap symbol 2 feature graph  
    price_s2 = PriceSource(source=store, symbol=universe[1])
    A = FakeFeature(name="A", emissions=[False, True, True], sources=[price_s2])
    F = FakeFeature(name="F", emissions=[False, True], sources=[A])
    G = FakeFeature(name="G", emissions=[True], sources=[A])
    C = FakeFeature(name="C", emissions=[True], sources=[F])

    roots["SYMBOL_2"] = A
    bootstrap_feature_graph([A, F, G, C])

    # Run  
    for i, trade in enumerate(MULTI_SYMBOLS_SIMPLE_TRADES):
        on_trade(trade, i)
```


---

```terminal
C:\Users\Manuel\Desktop\InvestIQ\.venv\Scripts\python.exe C:\Users\Manuel\Desktop\InvestIQ\sandbox\multiple_parents_feature_graph.py 

Bootstrap running...

Feature B source ['A']
Feature C source ['A']
Feature D source ['B']
Feature E source ['A', 'C']
Feature F source ['D', 'E']

Successors : 
Feature A successors ['B', 'C', 'E']
Feature B successors ['D']
Feature C successors ['E']
Feature D successors ['F']
Feature E successors ['F']
Feature F successors []

Bootstrap running...

Feature F source ['A']
Feature G source ['A']
Feature C source ['F']

Successors : 
Feature A successors ['F', 'G']
Feature F successors ['C']
Feature G successors []
Feature C successors []

SYMBOL_1, trade n°0, step n°0
eligible before: ['A']
current: A
emit: False
emitted: []
successors: ['B', 'C', 'E']
eligible after : []

SYMBOL_2, trade n°1, step n°0
eligible before: ['A']
current: A
emit: False
emitted: []
successors: ['F', 'G']
eligible after : []

SYMBOL_1, trade n°2, step n°0
eligible before: ['A']
current: A
emit: True
emitted: ['A']
successors: ['B', 'C', 'E']
eligible after : ['B', 'C']

SYMBOL_1, trade n°2, step n°1
eligible before: ['B', 'C']
current: B
emit: False
emitted: ['A']
successors: ['D']
eligible after : ['C']

SYMBOL_1, trade n°2, step n°2
eligible before: ['C']
current: C
emit: False
emitted: ['A']
successors: ['E']
eligible after : []

SYMBOL_2, trade n°3, step n°0
eligible before: ['A']
current: A
emit: True
emitted: ['A']
successors: ['F', 'G']
eligible after : ['F', 'G']

SYMBOL_2, trade n°3, step n°1
eligible before: ['F', 'G']
current: F
emit: False
emitted: ['A']
successors: ['C']
eligible after : ['G']

SYMBOL_2, trade n°3, step n°2
eligible before: ['G']
current: G
emit: True
emitted: ['G', 'A']
successors: []
eligible after : []

SYMBOL_1, trade n°4, step n°0
eligible before: ['A']
current: A
emit: True
emitted: ['A']
successors: ['B', 'C', 'E']
eligible after : ['B', 'C']

SYMBOL_1, trade n°4, step n°1
eligible before: ['B', 'C']
current: B
emit: True
emitted: ['B', 'A']
successors: ['D']
eligible after : ['C', 'D']

SYMBOL_1, trade n°4, step n°2
eligible before: ['C', 'D']
current: C
emit: True
emitted: ['C', 'B', 'A']
successors: ['E']
eligible after : ['D', 'E']

SYMBOL_1, trade n°4, step n°3
eligible before: ['D', 'E']
current: D
emit: False
emitted: ['C', 'B', 'A']
successors: ['F']
eligible after : ['E']

SYMBOL_1, trade n°4, step n°4
eligible before: ['E']
current: E
emit: False
emitted: ['C', 'B', 'A']
successors: ['F']
eligible after : []

SYMBOL_2, trade n°5, step n°0
eligible before: ['A']
current: A
emit: True
emitted: ['A']
successors: ['F', 'G']
eligible after : ['F', 'G']

SYMBOL_2, trade n°5, step n°1
eligible before: ['F', 'G']
current: F
emit: True
emitted: ['F', 'A']
successors: ['C']
eligible after : ['G', 'C']

SYMBOL_2, trade n°5, step n°2
eligible before: ['G', 'C']
current: G
emit: True
emitted: ['F', 'G', 'A']
successors: []
eligible after : ['C']

SYMBOL_2, trade n°5, step n°3
eligible before: ['C']
current: C
emit: True
emitted: ['C', 'F', 'G', 'A']
successors: []
eligible after : []

SYMBOL_1, trade n°6, step n°0
eligible before: ['A']
current: A
emit: True
emitted: ['A']
successors: ['B', 'C', 'E']
eligible after : ['B', 'C']

SYMBOL_1, trade n°6, step n°1
eligible before: ['B', 'C']
current: B
emit: True
emitted: ['B', 'A']
successors: ['D']
eligible after : ['C', 'D']

SYMBOL_1, trade n°6, step n°2
eligible before: ['C', 'D']
current: C
emit: True
emitted: ['C', 'B', 'A']
successors: ['E']
eligible after : ['D', 'E']

SYMBOL_1, trade n°6, step n°3
eligible before: ['D', 'E']
current: D
emit: True
emitted: ['C', 'D', 'B', 'A']
successors: ['F']
eligible after : ['E']

SYMBOL_1, trade n°6, step n°4
eligible before: ['E']
current: E
emit: True
emitted: ['C', 'B', 'E', 'A', 'D']
successors: ['F']
eligible after : ['F']

SYMBOL_1, trade n°6, step n°5
eligible before: ['F']
current: F
emit: True
emitted: ['C', 'B', 'E', 'A', 'F', 'D']
successors: []
eligible after : []

SYMBOL_2, trade n°7, step n°0
eligible before: ['A']
current: A
emit: False
emitted: []
successors: ['F', 'G']
eligible after : []

SYMBOL_1, trade n°8, step n°0
eligible before: ['A']
current: A
emit: False
emitted: []
successors: ['B', 'C', 'E']
eligible after : []

SYMBOL_2, trade n°9, step n°0
eligible before: ['A']
current: A
emit: True
emitted: ['A']
successors: ['F', 'G']
eligible after : ['F', 'G']

SYMBOL_2, trade n°9, step n°1
eligible before: ['F', 'G']
current: F
emit: False
emitted: ['A']
successors: ['C']
eligible after : ['G']

SYMBOL_2, trade n°9, step n°2
eligible before: ['G']
current: G
emit: True
emitted: ['G', 'A']
successors: []
eligible after : []

SYMBOL_1, trade n°10, step n°0
eligible before: ['A']
current: A
emit: True
emitted: ['A']
successors: ['B', 'C', 'E']
eligible after : ['B', 'C']

SYMBOL_1, trade n°10, step n°1
eligible before: ['B', 'C']
current: B
emit: False
emitted: ['A']
successors: ['D']
eligible after : ['C']

SYMBOL_1, trade n°10, step n°2
eligible before: ['C']
current: C
emit: False
emitted: ['A']
successors: ['E']
eligible after : []

SYMBOL_2, trade n°11, step n°0
eligible before: ['A']
current: A
emit: True
emitted: ['A']
successors: ['F', 'G']
eligible after : ['F', 'G']

SYMBOL_2, trade n°11, step n°1
eligible before: ['F', 'G']
current: F
emit: True
emitted: ['F', 'A']
successors: ['C']
eligible after : ['G', 'C']

SYMBOL_2, trade n°11, step n°2
eligible before: ['G', 'C']
current: G
emit: True
emitted: ['F', 'G', 'A']
successors: []
eligible after : ['C']

SYMBOL_2, trade n°11, step n°3
eligible before: ['C']
current: C
emit: True
emitted: ['C', 'F', 'G', 'A']
successors: []
eligible after : []

SYMBOL_1, trade n°12, step n°0
eligible before: ['A']
current: A
emit: True
emitted: ['A']
successors: ['B', 'C', 'E']
eligible after : ['B', 'C']

SYMBOL_1, trade n°12, step n°1
eligible before: ['B', 'C']
current: B
emit: True
emitted: ['B', 'A']
successors: ['D']
eligible after : ['C', 'D']

SYMBOL_1, trade n°12, step n°2
eligible before: ['C', 'D']
current: C
emit: True
emitted: ['C', 'B', 'A']
successors: ['E']
eligible after : ['D', 'E']

SYMBOL_1, trade n°12, step n°3
eligible before: ['D', 'E']
current: D
emit: False
emitted: ['C', 'B', 'A']
successors: ['F']
eligible after : ['E']

SYMBOL_1, trade n°12, step n°4
eligible before: ['E']
current: E
emit: False
emitted: ['C', 'B', 'A']
successors: ['F']
eligible after : []

SYMBOL_2, trade n°13, step n°0
eligible before: ['A']
current: A
emit: False
emitted: []
successors: ['F', 'G']
eligible after : []

Process finished with exit code 0
```


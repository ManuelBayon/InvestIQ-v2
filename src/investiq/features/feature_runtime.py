from investiq.events.trade_received import TradeReceived
from investiq.features.features import Feature

from tests.helpers.feature_runtime_trace import print_trace

class FeatureGraph:
    def __init__(self, root_key, root_value):
        self.root_symbol = root_key
        self.root_feature: Feature = root_value
        self.nodes: list[Feature] = [root_value]

    def add_node(self, node: Feature):
        self.nodes.append(node)

class FeatureRuntime:

    def __init__(self, graph: dict[str, FeatureGraph]):
        self._feature_graphs = graph


    def on_trade_received(self, trade: TradeReceived) -> None:

        graph = self._feature_graphs[trade.symbol]

        eligible: list[Feature] = [graph.root_feature]
        emitted = set()
        step: int = 0

        while len(eligible) > 0:

            eligible_before = eligible.copy()
            current = eligible.pop(0)
            emit = current.compute()

            if not emit:
                print_trace(
                    trade.symbol, trade.timestamp_utc, step, eligible_before,
                    current, emit, emitted, current.successors, eligible)

                step += 1
                continue

            emitted.add(current)

            for successor in current.successors:
                sources = successor.__dict__.get("_sources")

                if set(sources).issubset(emitted):
                    eligible.append(successor)

            print_trace(
                trade.symbol, trade.timestamp_utc, step, eligible_before,
                current, emit, emitted, current.successors, eligible)

            step += 1
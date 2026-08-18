from investiq.events.trade_received import TradeReceived
from investiq.features.feature_graph import FeatureGraph, Node
from tests.helpers.feature_runtime_trace import print_trace

class FeatureRuntime:

    def __init__(self, graph: FeatureGraph):
        self._graph = graph


    def on_trade_received(self, trade: TradeReceived) -> None:

        eligible: list[Node] = [successor for input_node in self._graph.input_nodes() for successor in input_node.successors]
        emitted: set[Node] = set()
        step: int = 0

        while len(eligible) > 0:

            eligible_before = eligible.copy()
            current = eligible.pop(0)
            emit = current.payload.compute()

            if not emit:
                print_trace(
                    trade.symbol, trade.timestamp_utc, step, eligible_before,
                    current, emit, emitted, current.successors, eligible)

                step += 1
                continue

            emitted.add(current)

            for successor in current.successors:

                if set(successor.parents).issubset(emitted):
                    eligible.append(successor)

            print_trace(
                trade.symbol, trade.timestamp_utc, step, eligible_before,
                current, emit, emitted, current.successors, eligible)

            step += 1
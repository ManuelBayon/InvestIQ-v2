from investiq.features.feature_graph import FeatureGraph, Node

class FeatureRuntime:

    def __init__(self, graph: FeatureGraph):
        self._graph = graph
        self.ready: bool = False


    def on_trade_received(self) -> None:

        eligible: list[Node] = [successor for input_node in self._graph.input_nodes() for successor in input_node.successors]
        emitted: set[Node] = set()

        self.ready = False

        while eligible:

            current = eligible.pop(0)
            emit = current.payload.compute()

            if not emit:
                continue

            emitted.add(current)

            for successor in current.successors:

                if set(successor.parents).issubset(emitted):
                    eligible.append(successor)
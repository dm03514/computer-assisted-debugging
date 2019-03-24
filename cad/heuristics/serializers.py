from cad.heuristics.evaulators import TransitionEvaluator


class Markdown:
    def __init__(self, heuristic):
        self.heuristic = heuristic

    def state_table(self):
        rows = [
            '| Node Name | Evaluator | Query Source | Yes Threshold |',
            '| ------- | --------- | -------- | ----------- |',
        ]

        graph = self.heuristic.graph()
        for node in graph.nodes:
            if isinstance(node, TransitionEvaluator):
                rows.append(
                    '|{}|{}|{}|{}|'.format(
                        node.name,
                        node.__class__.__name__,
                        node.query.__class__.__name__,
                        node.name,
                    )
                )
        return '\n'.join(rows)

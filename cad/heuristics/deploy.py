from datetime import datetime, timedelta

import networkx as nx

from cad.heuristics.evaulators import SingleValueThresholdEvaluator
from cad.heuristics.nodes import Yes, No, Start, Alert, End
from cad.heuristics.testing import StubQuery


class LastDeploy:
    def __init__(self, name, comparator):
        self.comparator = comparator
        self.name = name

    def value(self):
        return self.value

    def __repr__(self):
        return self.name


class Deploy:
    def __init__(self, last_deploy):
        self._graph = self._build_graph(last_deploy)

    def graph(self):
        return self._graph

    def _build_graph(self, last_deploy):
        G = nx.DiGraph()
        start = Start()
        end = End()
        alert = Alert()

        G.add_node(start)
        G.add_node(last_deploy)
        G.add_node(end)

        G.add_edge(start, last_deploy)
        G.add_edge(last_deploy, alert, object={'action': 'yes'}, data=Yes())
        G.add_edge(alert, end)
        G.add_edge(last_deploy, end, object={'action': 'no'}, data=No())
        return G


def build_for_display():
    return Deploy(
        SingleValueThresholdEvaluator(
            'LastDeploy < X hours',
            StubQuery(result=False),
            comparator=lambda x: x >= datetime.now() - timedelta(hours=6)
        )
    )


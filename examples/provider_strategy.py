import networkx as nx

from cad.heuristics.evaulators import OneOfManyValuesThresholdEvaluator, ManyValuesThresholdEvaluator
from cad.heuristics.nodes import Start, End, Alert, Yes, No
from cad.heuristics.testing import StubQuery


class ProviderOutage:
    def __init__(self, specific_strategy, many_regions, many_customers):
        self._graph = self._build_graph(
            specific_strategy,
            many_regions,
            many_customers
        )

    def graph(self):
        return self._graph

    def _build_graph(self, specific_strategy, many_regions, many_customers):
        G = nx.DiGraph()
        start = Start()
        end = End()
        alert = Alert()

        G.add_node(start)
        G.add_node(specific_strategy)
        G.add_node(many_regions)
        G.add_node(many_customers)
        G.add_node(end)

        G.add_edge(start, specific_strategy)
        G.add_edge(specific_strategy, many_regions, object={'action': 'yes'}, data=Yes())
        G.add_edge(specific_strategy, end, object={'action': 'no'}, data=No())

        G.add_edge(many_regions, many_customers, object={'action': 'yes'}, data=Yes())
        G.add_edge(many_regions, end, object={'action': 'no'}, data=No())

        G.add_edge(many_customers, alert, object={'action': 'yes'}, data=Yes())
        G.add_edge(many_customers, end, object={'action': 'no'}, data=No())
        G.add_edge(alert, end)

        return G


def build_for_display():
    return ProviderOutage(
        specific_strategy=OneOfManyValuesThresholdEvaluator(
            'Strategy Error Rate > 50%',
            StubQuery(result=True),
            comparator=lambda x: x >= 0.50
        ),
        many_regions=ManyValuesThresholdEvaluator(
            'Region Strategy Error Rate > 50%',
            StubQuery(result=True),
            comparator=lambda x: x >= 0.50
        ),
        many_customers=ManyValuesThresholdEvaluator(
            'Many Customers Error Rate > 50%',
            StubQuery(result=True),
            comparator=lambda x: x >= 0.50
        )
    )

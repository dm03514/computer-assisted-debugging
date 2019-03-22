from datetime import datetime, timedelta

import networkx as nx


class Value:
    def value(self):
        pass


class LastDeploy:
    def __init__(self, name, comparator):
        self.comparator = comparator
        self.name = name

    def value(self):
        return self.value

    def __repr__(self):
        return self.name


class Start:
    def __repr__(self):
        return 'start'


class End:
    def __repr__(self):
        return 'end'


class Alert:
    def __repr__(self):
        return 'alert'


class Yes:
    def evaluate(self, against):
        return against


class No:
    def evaluate(self, against):
        return not against


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
        LastDeploy(
            'LastDeploy < X hours',
            comparator=lambda x: x >= datetime.now() - timedelta(hours=6)
        )
    )


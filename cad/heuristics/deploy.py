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
    """
    def __init__(self):
        self['action'] = 'yes'
        self['evaluate'] = self.evaluate
    """

    def evaluate(self, against):
        return against


class No:
    """
    def __init__(self):
        self['action'] = 'no'
        self['evaluate'] = self.evaluate
    """

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


if __name__ == '__main__':
    deploy = Deploy(
        LastDeploy(
            'LastDeploy < 6 hours',
            comparator=lambda x: x >= datetime.now() - timedelta(hours=6)
        )
    )
    pdot = nx.drawing.nx_pydot.to_pydot(deploy.graph())
    for edge in pdot.get_edges():
        obj = edge.obj_dict.get('attributes', {}).get('object')
        if obj is None:
            continue
        edge.set_label(obj)
    pdot.write_png('deploy.png')


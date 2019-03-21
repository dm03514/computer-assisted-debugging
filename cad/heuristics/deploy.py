from datetime import datetime, timedelta

import networkx as nx


class LastDeploy:
    def __init__(self, name):
        self.name = name

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


class Operation:
    def __init__(self, name, comparator):
        self.comparator = comparator
        self.name = name

    def evaluate(self, against):
        return self.comparator(against)

    def repr(self):
        return self.name


class Noop:
    def __init__(self, name):
        self.name = name

    def evaluate(self, against):
        raise NotImplemented()

    def repr(self):
        return self.name


class Deploy:
    def __init__(self, alert_within=None):
        if alert_within is None:
            alert_within = timedelta(hours=6)

        self.alert_within = alert_within
        self.graph = self._build_graph(alert_within)

    def _build_graph(self, alert_within):
        G = nx.DiGraph()
        start = Start()
        end = End()
        last_deploy = LastDeploy('LastDeploy < 6 hours')
        alert = Alert()

        G.add_node(start)
        G.add_node(last_deploy)
        G.add_node(end)

        G.add_edge(start, last_deploy)
        G.add_edge(last_deploy, alert, object=Operation('yes', lambda x: x >= datetime.now() - timedelta(hours=6)))
        G.add_edge(alert, end)
        G.add_edge(last_deploy, end, object=Noop('no'))
        return G


if __name__ == '__main__':
    deploy = Deploy()

    '''
    G = nx.DiGraph()
    start = Start()
    end = End()
    last_deploy = LastDeploy('LastDeploy < 6 hours')
    alert = Alert()

    G.add_node(start)
    G.add_node(last_deploy)
    G.add_node(end)

    G.add_edge(start, last_deploy)
    G.add_edge(last_deploy, alert, object=Operation('yes', lambda x: x >= datetime.now() - timedelta(hours=6)))
    G.add_edge(alert, end)
    G.add_edge(last_deploy, end, object=Noop('no'))
    '''

    # P = nx.nx_pydot.to_pydot(G)
    nx.nx_pydot.write_dot(deploy.graph, 'out.dot')

    '''
    pos = nx.spectral_layout(G)
    nx.draw(G, pos, with_labels=True)

    nx.draw_networkx_edges(G, pos)
    nx.draw_networkx_nodes(G, pos)
    # nx.draw_networkx_labels(G, pos)
    pos = nx.spring_layout(G)
    nx.draw(G, pos, with_labels=True)
    nx.draw_networkx_edge_labels(G, pos)
    plt.savefig('deploy.png')
    '''

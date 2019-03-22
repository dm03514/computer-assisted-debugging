import logging

from cad.heuristics.deploy import Start, End

ROOT_NODE = 0
EDGE_TO = 1
EDGE_OBJECT_PAYLOAD = 2

logger = logging.getLogger(__name__)


class Executor:
    def __init__(self, heuristic):
        self.heuristic = heuristic

    def run(self):
        '''
        iterates through the graph each Valueable calls value()
        and checks its comparators

        Runs until the End Node has been reached.
        '''
        g = self.heuristic.graph()
        node = list(g.nodes)[ROOT_NODE]
        # traverse to end
        while not isinstance(node, End):
            logger.debug({'node': node})

            # get the edges and traverse to next
            edges = list(g.edges(node, data=True))
            if len(edges) > 2:
                raise Exception('graph must only have 2 edges max per node')

            # either have a single edge or 2 edges
            if len(edges) == 1:
                logger.debug({'edge': edges})
                node = edges[0][EDGE_TO]
                continue
            elif len(edges) == 2:
                # iterate edges data and evaluate()
                value = node.value()
                logger.debug({'node': node, 'value': value})
                for edge in edges:
                    if edge[EDGE_OBJECT_PAYLOAD]['data'].evaluate(value):
                        logger.debug({'node': node, 'value': value, 'edge': edge})
                        node = edge[EDGE_TO]
                        break
                else:
                    raise Exception('no edge evaluated')

        logger.debug({'node': node})
        return True





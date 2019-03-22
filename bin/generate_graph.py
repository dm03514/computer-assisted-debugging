import argparse
import importlib

import networkx as nx

parser = argparse.ArgumentParser(
    description='Generates a .png image from a heuristic graph'
)

parser.add_argument('heuristic', metavar='H', type=str, help='the heuristic to graph')


if __name__ == '__main__':
    args = parser.parse_args()
    print(args)
    module = importlib.import_module('cad.heuristics.{}'.format(args.heuristic))
    h = module.build_for_display()
    pdot = nx.drawing.nx_pydot.to_pydot(h.graph())
    for edge in pdot.get_edges():
        obj = edge.obj_dict.get('attributes', {}).get('object')
        if obj is None:
            continue
        edge.set_label(obj)

    name = 'build/{}.png'.format(args.heuristic)
    print('saving graph: "{}"'.format(name))
    pdot.write_png(name)

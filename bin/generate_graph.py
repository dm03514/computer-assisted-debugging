import argparse
import importlib

import networkx as nx
from networkx.drawing.nx_pydot import write_dot

from cad.heuristics.serializers import Markdown

parser = argparse.ArgumentParser(
    description='Generates a .png image from a heuristic graph'
)

parser.add_argument('heuristic', metavar='H', type=str, help='the heuristic to graph')
parser.add_argument('--type', default='image', metavar='T', type=str, choices=['image', 'md_table'], help='')


if __name__ == '__main__':
    """
    Example:
   
    $ python bin/generate_graph.py cad.heuristics.deploy:build_for_display
    
    Namespace(heuristic='cad.heuristics.deploy:build_for_display')
    saving graph: "build/cad.heuristics.deploy.png" 
    """
    args = parser.parse_args()
    print(args)
    path, fn_name = args.heuristic.split(':')
    build_fn = getattr(importlib.import_module(path), fn_name)

    if args.type == 'image':
        graph = build_fn().graph()
        pdot = nx.drawing.nx_pydot.to_pydot(graph)
        for edge in pdot.get_edges():
            obj = edge.obj_dict.get('attributes', {}).get('object')
            if obj is None:
                continue
            edge.set_label(obj)

        name = 'build/{}.png'.format(path)
        print('saving graph: "{}"'.format(name))
        pdot.write_png(name)

        name = 'build/{}.dot'.format(path)
        write_dot(graph, name)
        print('saving .dot: "{}"'.format(name))

    elif args.type == 'md_table':
        print(Markdown(build_fn()).state_table())


import argparse
import logging
import sys
from cache_wiki import Graph
import heapq

def dijkstra(graph : Graph, start, end):
    if start not in graph.data or end not in graph.data:
        return []
    if end in graph.data[start]:
        return [start, end]
    distances = {vertex: [float('infinity')] for vertex in graph.data}
    distances[start][0] = 0
    queue = [(0, start)]

    while queue:
        current_distance, current_vertex = heapq.heappop(queue)
        if current_distance > distances[current_vertex][0]:
            continue

        for neighbor in list(graph.data[current_vertex]):
            distance = current_distance + 1
            if distance < distances[neighbor][0]:
                distances[neighbor] = [distance, current_vertex]
                heapq.heappush(queue, (distance, neighbor))

    path = []
    if (len(distances[end]) > 1):
        path.append(end)
        while path[-1] != start:
            path.append(distances[path[-1]][1])

    return list(reversed(path))

def print_path(path : list, flag : bool):
    if len(path) == 0:
        logging.warning("Path not found")
    else:
        if flag:
            st = ""
            for i in path:
                st += i + (' -> ' if i != path[-1] else '')
            logging.info(st)
        logging.info(len(path) - 1)

def init_args(args):
    args.add_argument('-v',
                      help="""This flag show you path of shorted way. Default value is False""",
                      action='store_true', dest='v')
    args.add_argument('--from', type=str,
                      help="""This flag describes the starting node. Default value is not specified""",
                      required=True, dest='f')
    args.add_argument('--to', type=str,
                      help="""This flag describes the ending node. Default value is not specified""",
                      required=True, dest='t')
    args.add_argument('--non-directed',
                      help="""The flag enables bidirectional connections in the graph, if mentioned.
                      The default value means that the nodes are unidirectional""",
                      action='store_true', dest='nd')
    return args.parse_args()

def args_validation(args) -> bool:
    return len(args.f) != 0 and len(args.t) != 0

import networkx as nx

def main() -> None:
    parser = argparse.ArgumentParser(
        description='Shortcuts: find the shortest path length between two pages in serialized database')
    args = init_args(parser)
    if args_validation(args):
        path = '../materials/wiki.json'
        logging.info(f"Parsing graph starting, path to file: {path}")
        graph = Graph(args.nd)
        graph.load_graph(path)
        if args.f in graph.data and args.t in graph.data:
            print_path(dijkstra(graph, args.f, args.t), args.v)
        else:
            logging.error(f"""Graph doesn't have one/both of them : --from "{args.f}" or --to "{args.t}".""")
    else:
        logging.error("--from or --to is empty. This field is necessarily.")

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s", stream=sys.stdout)
    main()
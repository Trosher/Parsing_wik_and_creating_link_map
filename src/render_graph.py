import sys
import logging
import networkx as nx
import matplotlib.pyplot as plt
from cache_wiki import Graph
from collections import Counter

def count_link(graph : Graph):
    count = Counter()
    for i in graph.data:
        for j in list(graph.data[i]):
            count[j] += 1
    return count

def draw_png(graph : Graph):
    count = count_link(graph)
    option = {'node_size' : [100 * count[i] for i in graph.data]}
    scale = graph.data.number_of_nodes() * 0.035
    plt.figure(figsize=(scale, scale))
    nx.draw(graph.data, with_labels = True, arrows=True, **option)
    plt.savefig('wiki_graph.png')

def main():
    error = 0
    logging.info("Start work program")
    graph = Graph(True)
    graph.load_graph("../materials/wiki.json")
    if graph.data.number_of_nodes() > 0:
        draw_png(graph)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s", stream=sys.stdout)
    logging.info("The program terminated with a code: " + str(main()) + '\n')
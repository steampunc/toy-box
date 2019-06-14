import networkx as nx
import matplotlib.pyplot as plt
import operator
import math
import sys


print("Reading graph from " + str(sys.argv[1]))
value_graph = nx.read_gexf(sys.argv[1])

#how many how separated
#number of cycles, go through each individually
#look at vertices in cycle and identify which have the greatest and least number of neighbors, give some data on that
#

value_dict = {}
for value in value_graph:
    value_dict[value] = value_graph.out_degree(value)

sorted_values = sorted(value_dict.items(), key=operator.itemgetter(1), reverse=True)
for value in sorted_values:
    print("\t" + str(value[1]) + " " + str(value[0]))

cycles = list(nx.simple_cycles(value_graph))
print()

for cycle in cycles:
    print("Analyzing: " + str(cycle))
    print("Cycle Size: " + str(len(cycle)))
    in_rel = 0
    out_rel = 0
    value_dict = {}
    for value in cycle:
        in_deg = value_graph.in_degree(value)
        out_deg = value_graph.out_degree(value)
        value_dict[value] = out_deg
        in_rel += in_deg
        out_rel += out_deg
    sorted_values = sorted(value_dict.items(), key=operator.itemgetter(1), reverse=True)
    for value in sorted_values:
        print("\t" + str(value[1]) + " " + str(value[0]))

    cycle_rel = 1 / (1 - (len(cycle) / value_graph.number_of_nodes()))
    print("Cycle Rel: " + str(cycle_rel) + "\tOut Rel: " + str(out_rel))
    print("Relevance: " + str(out_rel / (value_graph.number_of_edges())))


pos = nx.circular_layout(value_graph)
nx.draw_networkx_nodes(value_graph, pos, cmap=plt.get_cmap('jet'), node_size = 500)
nx.draw_networkx_labels(value_graph, pos)
nx.draw_networkx_edges(value_graph, pos, arrowsize=20, arrowstyle='wedge')
plt.show()

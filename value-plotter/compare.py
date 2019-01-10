import networkx as nx
import matplotlib.pyplot as plt
import operator
import math
import sys


print("Reading graph 1 from " + str(sys.argv[1]))
print("Reading graph 2 from " + str(sys.argv[2]))
graph_one = nx.read_gexf(sys.argv[1])
graph_two = nx.read_gexf(sys.argv[2])


dict_one = {}
for value in graph_one:
    dict_one[value] = graph_one.out_degree(value)

dict_two = {}
for value in graph_two:
    dict_two[value] = graph_two.out_degree(value)

sorted_one = sorted(dict_one.items(), key=operator.itemgetter(1), reverse=True)
sorted_two = sorted(dict_two.items(), key=operator.itemgetter(1), reverse=True)


print("VH from " + str(sys.argv[1]))
for value in sorted_one:
    print("\t" + str(value[1]) + " " + str(value[0]))

print("\n")
print("VH from " + str(sys.argv[2]))
for value in sorted_two:
    print("\t" + str(value[1]) + " " + str(value[0]))


distances = []
max_dist = []
for value in dict_one:
    distance = abs(dict_one[value] - dict_two[value])
    max_distance = abs(9 - dict_one[value])
    max_dist.append(max_distance)
    distances.append(distance)

print("Similarity: " + str(1 - math.sqrt(sum(distances)/sum(max_dist))))


import networkx as nx
import itertools
import random
import matplotlib.pyplot as plt

value_file = open("./values_list.txt", "r")
value_list = []
i = 0
for val in value_file:
    value_list.append(val.rstrip())
    i += 1
print(i)

print(value_list)

value_graph = nx.DiGraph()
value_graph.add_nodes_from(value_list)

complement_graph = nx.Graph()
complement_graph.add_nodes_from(value_list)

name = input("What is your name? ")
ordered_comparison_list = list(itertools.combinations(value_list, 2))

comparison_list = sorted(ordered_comparison_list, key=lambda x: random.random())

num_compared = 0
len_compared = len(comparison_list)
for comparison in comparison_list:
    num_compared = num_compared + 1
    compared = sorted(comparison, key=lambda x: random.random())
    print("Number " + str(num_compared) + " of " + str(len_compared) + ".")
    not_valid = True
    result = ''
    while not_valid:
        print("[1]: " + str(compared[0]))
        print("[2]: " + str(compared[1]))
        print("[3]: Unresolved")
        try:
            result = int(input("Which do you value more? "))
            not_valid = False
        except ValueError:
            print("Not a valid response! Please enter 1 or 2.")
            print("Which do you value more:")
            continue
        
    if result != 3:
        value = (int(result) - 1) % 2
        print("So you value " + str(compared[value]) + " over " + str(compared[(value  + 1) % 2]))
        value_graph.add_edge(compared[value], compared[(value + 1 ) % 2])
    else:
        print("Adding edge between " + str(compared[0]) + " and " + str(compared[1]))
        complement_graph.add_edge(compared[0], compared[1])


# I am certain there is a better way to do this, but I just bodged together a solution to re-iterate over the unanswere values. Sorry to anyone reading the code!
        
len_compared = len_compared + len(complement_graph.edges())
for edge in complement_graph.edges():
    num_compared = num_compared + 1
    compared = sorted(edge, key=lambda x: random.random())
    print("Number " + str(num_compared) + " of " + str(len_compared) + ".")
    not_valid = True
    result = ''
    while not_valid:
        print("[1]: " + str(compared[0]))
        print("[2]: " + str(compared[1]))
        print("[3]: Unresolved")
        try:
            result = int(input("Which do you value more? "))
            not_valid = False
        except ValueError:
            print("Not a valid response! Please enter 1 or 2.")
            print("Which do you value more:")
            continue
        
    if result != 3:
        value = (int(result) - 1) % 2
        print("So you value " + str(compared[value]) + " over " + str(compared[(value  + 1) % 2]))
        value_graph.add_edge(compared[value], compared[(value + 1 ) % 2])

nx.write_gexf(value_graph, "./" + str(name) + "_values.txt")

pos = nx.circular_layout(value_graph)
nx.draw_networkx_nodes(value_graph, pos, cmap=plt.get_cmap('jet'), node_size = 500)
nx.draw_networkx_labels(value_graph, pos)
nx.draw_networkx_edges(value_graph, pos, arrowsize=20, arrowstyle='fancy')
plt.show()

pos = nx.circular_layout(complement_graph)
nx.draw_networkx_nodes(complement_graph, pos, cmap=plt.get_cmap('jet'), node_size = 500)
nx.draw_networkx_labels(complement_graph, pos)
nx.draw_networkx_edges(complement_graph, pos, arrowsize=20, arrowstyle='wedge')
plt.show()

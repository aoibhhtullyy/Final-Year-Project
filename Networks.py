import networkx as nx
import matplotlib.pyplot as plt
import random

g = nx.Graph()
node_list = []

def create_nodes_list(number):
    for value in range(number):
        var1 = 'N'+str(value)
        node_list.append(var1)
    return node_list

def add_nodes(graph, list1):
    graph.add_nodes_from(list1)

def add_edges_randomly(graph, probability):
    nodes = list(graph.nodes())
    for i in range(len(nodes)):
        for j in range(i+1, len(nodes)):
            if random.random() < probability:
                graph.add_edge(nodes[i], nodes[j])
    return graph

def nodes_with_influence(graph):
    node_colours = []
    for node in graph.nodes():
        if graph.degree(node) > 3:
            node_colours.append('red')
        else:
            node_colours.append('blue')
    return node_colours

def avg_node_connectivity(graph):
    if not nx.is_connected(graph):
        return 0
    avg_connectivity = nx.average_node_connectivity(graph)
    return avg_connectivity

def avg_shortest_path_length(graph):
    if not nx.is_connected(graph):
        return 0
    avg_path_length = nx.average_shortest_path_length(graph)
    return avg_path_length

def avg_cluster_coefficient(graph):
    cluster_coef = nx.average_clustering(graph)
    return cluster_coef

def generate_and_save_graph(numberOfNodes, increment):
    probabilities = []
    average_connectivities = []
    average_path_lengths = []
    node_list = create_nodes_list(numberOfNodes)
    add_nodes(g, node_list)
    for i in range(increment+1):
        probability = i/increment
        add_edges_randomly(g, probability)
        node_colours = nodes_with_influence(g)
        nx.draw(g, with_labels=1, node_color=node_colours)
        average_connectivity = avg_node_connectivity(g)
        avg_path_length = avg_shortest_path_length(g)
        clustering = avg_cluster_coefficient(g)
        probabilities.append(probability)
        average_connectivities.append(average_connectivity)
        average_path_lengths.append(avg_path_length)
        print(f'Average Node Connectivity for prob{probability:.2f}: {average_connectivity:.2f}')
        print(f'Average Path Length for prob{probability:.2f}: {avg_path_length:.2f}')
        print(f'Clustering Coefficient for prob{probability:.2f}: {clustering:.2f}')
        plt.savefig(f'graph_{numberOfNodes}_prob_{probability:.2f}.png')
        plt.clf()
    plt.close()

    plt.plot(probabilities, average_connectivities, label='Average Node Connectivity')
    plt.plot(probabilities, average_path_lengths, label='Average Path Length')
    plt.xlabel('Probability')
    plt.ylabel('Value')
    plt.title('Average Node Connectivity & Average Path Length vs Probability')
    plt.grid(True)
    plt.legend()
    plt.savefig(f'average_connectivity_vs_probability.png')

    plt.show()


generate_and_save_graph(10,10)


import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt
import networkx as nx
import random


def create_nodes_list(number):
    node_list = []
    for value in range(number):
        var1 = 'N'+str(value)
        node_list.append(var1)
    return node_list

def add_nodes(graph, list1):
    for node in list1:
        age = random.randint(1, 100)
        graph.add_node(node, age=age, state='V')

def add_edges_randomly(graph, probability):
    nodes = list(graph.nodes())
    for i in range(len(nodes)):
        for j in range(i+1, len(nodes)):
            if random.random() < probability:
                graph.add_edge(nodes[i], nodes[j])
    return graph

def initialiseStates(graph, I0):
    vulnerable_nodes = list(graph.nodes())
    influenced_nodes = random.sample(vulnerable_nodes, I0)
    for node in influenced_nodes:
        graph.nodes[node]['state'] = 'I'
    vulnerable_nodes = [node for node in vulnerable_nodes if node not in influenced_nodes]
    return vulnerable_nodes, influenced_nodes

N = 1000

I0 = 1


beta = 0.2
gamma = 1./50

timestep = 160

def deriv(graph, influenced_nodes,vulnerable_nodes, beta, gamma, t):
    V = [len(vulnerable_nodes)]
    I = [len(influenced_nodes)]
    E = [0]

    for i in range(t):
        new_influenced = 0
        recovered_nodes = []
        infection_occured = False
        for influenced_node in influenced_nodes:
            neighbours = list(graph.neighbors(influenced_node))
            for neighbour in neighbours:
                if graph.nodes[neighbour]['state'] == 'V':
                    age_factor = 1 - graph.nodes[neighbour]['age']/100
                    if np.random.rand() < beta * age_factor:
                        graph.nodes[neighbour]['state'] = 'I'
                        influenced_nodes.append(neighbour)
                        vulnerable_nodes.remove(neighbour)
                        new_influenced += 1
                        infection_occured = True
                        break
            if infection_occured:
                break
        for influenced_node in influenced_nodes:
            if np.random.rand() < gamma:
                age = graph.nodes[influenced_node]['age']
                recovery_rate = 1 - (age/100)
                if np.random.rand() < recovery_rate:
                    graph.nodes[influenced_node]['state'] = 'E'
                    recovered_nodes.append(influenced_node)
        for node in recovered_nodes:
            influenced_nodes.remove(node)
        V.append(len(vulnerable_nodes))
        I.append(len(influenced_nodes))
        E.append(len(graph.nodes()) - len(vulnerable_nodes) - len(influenced_nodes))
        if i == midpoint:
            plot_network_graph(g, 'MidWay Network Graph')
    return V, I, E

def plot_network_graph(graph, title):
    pos = nx.spring_layout(graph, seed=42)
    node_colours = ['blue' if graph.nodes[node]['state'] == 'V' else 'red' if graph.nodes[node]['state']== 'I' else 'green' for node in graph.nodes()]
    nx.draw(graph, pos, node_color=node_colours, with_labels=False)
    plt.title(title)
    plt.savefig(f'InfluencePlusNetworkGraphs{title}.png')
    plt.show()

g = nx.Graph()
node_list = create_nodes_list(N)
add_nodes(g, node_list)
add_edges_randomly(g, 0.1)
midpoint = timestep/2

plot_network_graph(g, 'Initial Graph')

vulnerable_nodes, influenced_nodes = initialiseStates(g, I0)



V, I, E = deriv(g,influenced_nodes, vulnerable_nodes, beta, gamma, timestep)

t = np.linspace(0, timestep, timestep +1)
plt.plot(t,V, label='Vulnerable')
plt.plot(t, I, label='Influenced')
plt.plot(t, E, label='Educated')
plt.title('SIR Model')
plt.xlabel('Time')
plt.ylabel('Population')
plt.legend()
plt.grid(True)
plt.savefig(f'InfluencePlusSIR1000.png')
plt.show()

plot_network_graph(g, 'Final Network Graph')
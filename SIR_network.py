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
        graph.add_node(node, state = 'S')

def add_edges_randomly(graph, probability):
    nodes = list(graph.nodes())
    for i in range(len(nodes)):
        for j in range(i+1, len(nodes)):
            if random.random() < probability:
                graph.add_edge(nodes[i], nodes[j])
    return graph

def initialiseStates(graph, I0):
    susceptible_nodes = list(graph.nodes())
    infected_nodes = random.sample(susceptible_nodes, I0)
    for node in infected_nodes:
        graph.nodes[node]['state'] = 'I'
    susceptible_nodes = [node for node in susceptible_nodes if node not in infected_nodes]
    return susceptible_nodes, infected_nodes

N = 1000

I0 = 1
R0 = 0

beta = 0.2
gamma = 1./10

timestep = 160

def deriv(graph, infected_nodes, susceptible_nodes, beta, gamma, t):
    S = [len(susceptible_nodes)]
    I = [len(infected_nodes)]
    R = [0]
    for i in range(t):
        new_infected = 0
        infection_occured = False
        for infected_node in infected_nodes:
            neighbours = list(graph.neighbors(infected_node))
            for neighbour in neighbours:
                if graph.nodes[neighbour]['state'] == 'S':
                    if np.random.rand() < beta:
                        graph.nodes[neighbour]['state'] = 'I'
                        infected_nodes.append(neighbour)
                        susceptible_nodes.remove(neighbour)
                        new_infected += 1
                        infection_occured = True
                        break
            if infection_occured:
                break
        for infected_node in list(infected_nodes):
            if np.random.rand() < gamma:
                graph.nodes[infected_node]['state'] = 'R'
                infected_nodes.remove(infected_node)
        S.append(len(susceptible_nodes))
        I.append(len(infected_nodes))
        R.append(len(graph.nodes()) - len(susceptible_nodes) - len(infected_nodes))
        if i == mid_point:
            plot_network_graph(graph, 'Midway Graph')
    return S, I, R

def plot_network_graph(graph, title):
    pos = nx.spring_layout(graph, seed=42)
    node_colours = ['blue' if graph.nodes[node]['state'] == 'S' else 'red' if graph.nodes[node]['state']== 'I' else 'green' for node in graph.nodes()]
    nx.draw(graph, pos, node_color=node_colours, with_labels=False)
    plt.title(title)
    plt.savefig(f'SIRNetwork{title}.png')
    plt.show()

g = nx.Graph()
node_list = create_nodes_list(N)
add_nodes(g,node_list)
add_edges_randomly(g, 0.1)

mid_point = timestep/2

plot_network_graph(g, 'Initial Graph')

susceptible_nodes, infected_nodes = initialiseStates(g,I0)

S, I, R = deriv(g, infected_nodes, susceptible_nodes, beta, gamma, timestep)

t = np.linspace(0, timestep, timestep +1)
plt.plot(t, S, label='Susceptible')
plt.plot(t, I, label='Infected')
plt.plot(t, R, label='Recovered')
plt.title('SIR Model')
plt.xlabel('Time')
plt.ylabel('Population')
plt.legend()
plt.savefig(f'SIRNetworkSIRGraph.png')
plt.show()

plot_network_graph(g, 'Final Network Graph')
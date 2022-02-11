# Authors:
# Paula R.
# Tatjana M.


import networkx as nx
import time
import operator
from networkx.algorithms.community import k_clique_communities
import CPM_Algorithm as cpm
import Vertex_Sim_Pagerank_Cen as vspc
import matplotlib.pyplot as plt


# ******************************************
# Task 1 - Dataset
# ******************************************


# 1.1 Load graph as a nx graph
# ****************************

email_graph_undirected = nx.read_edgelist('email-Eu-core.txt', nodetype=int)
email_graph_directed = nx.read_edgelist('email-Eu-core.txt', nodetype=int, create_using=nx.DiGraph())
toy_graph = nx.read_edgelist('toysize.txt', nodetype=int)


# 1.2 Explore the properties of the graph
# ****************************

print('***** Task 1 *****\n')
print('Informations on Email graph (undirected):\n' + nx.info(email_graph_undirected))
print('\nInformations on Email graph (directed):\n' + nx.info(email_graph_directed) + '\n')


# ******************************************
# Task 2 - Implementation
# ******************************************


# 2.1 CPM algorithm implementation and testing it on toysize graph
# ****************************

#print('***** Task 2 *****\n')

# Since computation is difficult with our equipment here we have manually changeable k parameters
cpm_parameter_k_toysize = 3
cpm_parameter_k_email = 11

# Test the Clique Percolation method with toy-sized graph
timer = time.time()
communities_toysize = cpm.cpm_algorithm_selfmade(toy_graph, cpm_parameter_k_toysize)
print('CPM algorithm\nk = ' + str(cpm_parameter_k_toysize) + ', Graph: Toy-sized' + '\nThere are ' + str(len(communities_toysize)) + ' communities in the graph: ')
cpm.print_list(communities_toysize)
ending = time.time()
print('Used time was: ' + str((ending-timer)) + ' sec\n')


# ******************************************
# Task 3 - Analysis
# ******************************************

print('***** Task 3 *****\n')

# 3.1 Identify users' communities in email network using networkx build in cpm function. Experiment with different k
# ****************************

# Since even with the build-in function of networkx it took too much time on whole dataset -> take a subgraph
# subgraph(graph, nodes) creates the subgraph of graph with nodes nodes (edges to other nodes will be erased)
email_subgraph = nx.Graph.subgraph(email_graph_undirected, range(335))  # a third of the original amount of nodes
print('Informations on Email subgraph:\n' + nx.info(email_subgraph) + '\n')

# Apply cpm with build in function on subgraph
timer_2 = time.time()
list_of_communities_networkx = list(k_clique_communities(email_subgraph, cpm_parameter_k_email))
print('CPM algorithm\nk = ' + str(cpm_parameter_k_email) + ', Graph: Email subgraph\nAmount of communities in Email subgraph: ' + str(len(list_of_communities_networkx)))
ending_2 = time.time()
print('Used time was: ' + str((ending_2-timer_2)/60) + ' min')


# 3.2 Identify top k users with highest pagerank centrality in directed graph
# ****************************

# Top 21 according to Page-Rank centrality
top_21_pageRank = sorted(vspc.get_pagerank_matrix(email_graph_directed).items(), key=operator.itemgetter(1), reverse=True)[:21]
print("\nTop 21 Nodes according to Page Rank:")
for node, pagerank in top_21_pageRank:
    print(node, pagerank)
top_21_pageRank = [item[0] for item in top_21_pageRank]


# ******************************************
# Task 4 - Visualization
# ******************************************

print('\n***** Task 4 *****')

# Visualize the with cpm generated communities
colors_six = ['b', 'g', 'r', 'c', 'm', 'y']  # for k = 11
colors_nine = ['b', 'g', 'r', 'c', 'm', 'y', 'k', 'w', 'b']  # for k = 9, 10
for community, color in zip(list_of_communities_networkx, colors_six):
    community_graph = nx.Graph()
    community_graph.add_nodes_from(community)
    nx.draw_networkx(email_subgraph, nx.spring_layout(email_subgraph, seed=1234), nodelist=list(community), node_color=color, with_labels=False)

#plt.savefig('CPM_k_10.png')
plt.show()


# 4.2 Visualize top k users with highest pagerank centrality and vertex similarity
# ****************************

# Vertex Similarity
top_pair_vertex_similarity = vspc.get_top_vertex_pair(email_graph_directed, top_21_pageRank)
print("\nTop Vertex Pair: ", top_pair_vertex_similarity)

# Plot highlighted results
vspc.plot_results(email_graph_directed, top_pair_vertex_similarity, top_21_pageRank)

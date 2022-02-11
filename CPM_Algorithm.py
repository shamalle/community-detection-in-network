# Authors:
# Paula R.
# Tatjana M.

import networkx as nx
import itertools
from itertools import combinations


# *****************
# This function uses predefined function from networkX and will only be used for the analysis part
def find_all_cliques_size_k(graph, k):
    dict_of_cliques_size_k = {}
    all_cliques = list(nx.enumerate_all_cliques(graph))  # finds all the cliques in graph

    cliques_k = [x for x in all_cliques if len(x) == k]  # pick only cliques of size k
    for i in range(len(cliques_k)):
        dict_of_cliques_size_k[i + 1] = cliques_k[i]  # each clique gets a number, starting from 1
    return dict_of_cliques_size_k


# *****************
# Returns a list of lists of the clique in the graph. Only cliques of size >2 are relevant
def find_cliques(graph):
    cliques = [{i, j} for i, j in graph.edges() if i != j]  # take all the edges from graph
    resulting_cliques = []

    while cliques:
        current_cliques = set()
        # Take always two cliques in order to compare them ( a,b is the same comparison as b,a)
        for clique_1, clique_2 in combinations(cliques, 2):
            # Erase common node such that one can check after if there is an edge between the other ones
            symmetric_difference = clique_1.symmetric_difference(clique_2)
            # Since graph.has_edge need two parameters, use * operator on symmetric_difference to make it a "tuple"
            if len(symmetric_difference) == 2 and graph.has_edge(*symmetric_difference):
                # Since we're working with sets no problem of duplicates
                current_cliques.add(tuple(clique_1 | symmetric_difference))

        cliques = list(map(set, current_cliques))
        resulting_cliques.append(cliques)

    # Note, the found cliques begin with size 3
    return resulting_cliques


# *****************
# In order to process the cliques a bit easier for generating a graph, convert them into a dictionary
def saving_cliques_as_dictionary(list_of_cliques):
    dictionary_of_cliques = {}
    for i in range(len(list_of_cliques)):
        dictionary_of_cliques[i+1] = list_of_cliques[i]
    return dictionary_of_cliques


# *****************
# This function creates a graph according to the given dictionary of cliques and returns a nx graph
def construct_clique_graph(dict_of_cliques, k):
    clique_graph = nx.Graph()  # Creates a networkx graph
    clique_graph.add_nodes_from(dict_of_cliques.keys())  # The nodes are the keys of the dictionary (clique number)

    for key1, key2 in itertools.combinations(dict_of_cliques, 2):
        list1 = dict_of_cliques[key1]
        list2 = dict_of_cliques[key2]

        # Check if the list of nodes share k-1 common nodes
        if len(set(list1) & set(list2)) == k - 1:
            clique_graph.add_edge(key1, key2)  # If yes, add the keys (clique number) to clique graph

    return clique_graph


# *****************
# Returns a list of the connected components of a graph
def find_connected_components(graph):
    communities = [{i, j} for i, j in graph.edges() if i!=j]
    resulting_communities = []

    # if communities is empty (only one node in clique graph):
    if len(communities) == 0:
        return [{node} for node in graph.nodes() if graph.degree(node) == 0]

    while communities:
        current_communities = set()
        for community_1, community_2 in combinations(communities, 2):
            if community_1.intersection(community_2):
                current_communities.add(tuple(community_1 | community_2))

        communities = list(map(set, current_communities))
        if communities:
            last_community = communities  # if communities not empty then overwrite at each step the communities
            # Note: first we only merge 2 size communities together, then 3 size, etc
            # therefore we only want the last, resulting one, containing the largest possible community)

    # Append the resulted communities that were found with edge analyzing into resulting_communities
    resulting_communities.extend(last_community)

    # There could be communities consisting only of 2 nodes (-> no intersection with any others)
    # but they also build a community themselves and should be therefore added
    community_of_2 = [{i, j} for i, j in graph.edges() if (graph.degree(i) ==1 and graph.degree(j) == 1)]
    resulting_communities.extend(community_of_2)

    # There could be nodes without any edges that were left out in the part above, include them now
    isolated_points = [{node} for node in graph.nodes() if graph.degree(node) == 0]
    resulting_communities.extend(isolated_points)

    return resulting_communities


# *****************
# Regain the original nodes from the list of communities that were extracted from clique graph
def find_original_nodes(list_of_communities, dict_of_nodes):
    original_nodes_as_communities = list()

    for community in list_of_communities:
        originals_within_community = set()
        for node in community:
            originals_within_community.update(dict_of_nodes[node])
        original_nodes_as_communities.append(originals_within_community)
    return original_nodes_as_communities


# *****************
# Applies the CPM method on the given graph and returns a list of the communities
def cpm_algorithm_selfmade(graph, k):
    cliques_of_graph = find_cliques(graph)
    cliques_of_size_k = cliques_of_graph[k-3] # -3 since cliques of size 0, 1 and 2 are not considered
    # (isolated nodes, belong to no community)
    clique_as_dict = saving_cliques_as_dictionary(cliques_of_size_k)

    resulting_clique_graph = construct_clique_graph(clique_as_dict, k)
    communities_of_clique_graph = find_connected_components(resulting_clique_graph)

    resulting_communities = find_original_nodes(communities_of_clique_graph, clique_as_dict)

    return resulting_communities


def print_list(list_to_print):
    for index in range(len(list_to_print)):
        print(list_to_print[index])

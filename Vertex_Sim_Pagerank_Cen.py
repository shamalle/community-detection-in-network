# Authors:
# Paula R.
# Tatjana M.


import networkx as nx
import numpy as np
import matplotlib.pyplot as plt


# This function computes Vertex Similarity between two nodes
def calculate_vertex_similarity(G, i, j):
    if i == j:
        return 0
    common_neighbours = len(set(G[i]) & set(G[j]))

    return common_neighbours


# This function computes the pair with the highest Vertex Similarity
def get_top_vertex_pair(G, nodes):
    max_pair = None
    max_sim = 0
    for i in nodes:
        for j in nodes:
            new_sim = calculate_vertex_similarity(G, i, j)  # take the values from the common_neighbours in calculate_vertec_similarity
            if max_sim < new_sim:
                max_pair = (i, j)
                max_sim = new_sim

    # returns the pair with most common neighbours, and the number of common neighbours
    return (max_pair, max_sim)


# Iterative PageRank computation based on Matrices. Better Preformance compared to loop based computation
def get_pagerank_matrix(G, alpha=0.85, max_iter=100, error=1e-06):
    pr_t = {}  # pagerank of a node t
    pr_t_plus_1 = {}  # pagerank of page t after another iteration
    n = len(G.nodes)  # number of nodes

    A = nx.to_numpy_matrix(G)  # Return the graph adjacency matrix as a NumPy matrix.
    diagonal = []  # creates a list
    for j, out_degree in G.out_degree:
        if (out_degree == 0):
            diagonal.append(1)
        else:
            diagonal.append(out_degree)  # check the degrees
    D = np.diag(diagonal)  # construct a diagonal array.

    mat_mult = np.matmul(np.linalg.inv(D), A).transpose()  # Matrix product of two arrays.
    # np.linalgo.inv-Compute the (multiplicative) inverse of a matrix.

    mat_pr = np.ones((n, 1)) / n  # Return a matrix (n,1)/n filled with ones
    ones = np.ones((n, 1))

    i = 0
    while (i < max_iter):
        diff = 0
        mat_pr_plus_1 = alpha * np.matmul(mat_mult, mat_pr) + ones * (1 - alpha) / float(n)
        diff = np.linalg.norm(mat_pr_plus_1 - mat_pr, 1)
        if (diff < error):
            R_t = mat_pr_plus_1.copy()
            break
        mat_pr = mat_pr_plus_1.copy()
        i = i + 1
    pr_List = [item[0] for item in mat_pr.tolist()]

    result = dict(zip(G.nodes, pr_List))

    return result


def plot_results(G, top_pair_vertex_similarity, top_21_pageRank):
    pos = nx.spring_layout(G)  # positions for all nodes

    # colors all nodes in blue
    nx.draw_networkx_nodes(G, pos, node_color='b', node_size=40, alpha=0.8)
    # top 21 nodes with the highest pagerank are highlighted in red
    nx.draw_networkx_nodes(G, pos, top_21_pageRank, node_color='r', node_size=40)
    # top vertex pair is highlighted in green
    nx.draw_networkx_nodes(G, pos, top_pair_vertex_similarity[0], node_color='g', node_size=40)
    nx.draw_networkx_edges(G, pos, width=1.0)

    plt.axis('off')
    #plt.savefig('Vertex_PageRank.png')
    plt.show()  # display

    return

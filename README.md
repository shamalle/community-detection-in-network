2020, Group project

# community-detection-in-network
 
Program, that loads a social graph, runs community detection and visualisez the network.

Algorithms used: 

* Clique Percolation Method (CPM) 
* Vertex Similarity Method.

Data set used:

* [Stanford email data set](https://snap.stanford.edu/data/email-Eu-core.html)

Goals:

* Experiment with different values of CPM parameter and choose best one
* Identify the top k users with highest Pagerank centrality in the directed graph. Experiment with different values of k and choose the most appropriate one
* Visualize output by coloring nodes according to communities
* Visualize top k users with the highest Pagerank centrality and vertex similarity in the graph


## Project structure

The project consists of 3 Python files:

_CPM\_Algorithm.py_: contains the defined functions for the Clique Perculation Method (CPM)

_Vertex\_Sim\_Pagerank\_Cen.py_: contains the defined functions for the Vertex Similarity as well as the Pagerank Centrality

_Project.py_: contains the logic of the program. It imports the other classes and invokes their functions where needed. To run the program, run the Project.py with all the other .py files as well as the .txt files in the same directory.
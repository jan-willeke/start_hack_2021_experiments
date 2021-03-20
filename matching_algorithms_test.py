#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar 20 01:06:49 2021

@author: klaudiamur
"""

#### for nodes already in the network:
#### pick somebody so that the own centrality is maximised! 
#### or pick somebody so that the overall average shortest path length of the network is reduced


#### pick somebody based on similarities: 
    

#### pick somebody based on complementing interests/knowledge


### pick somebody based on diversity of world views/mindsets! -> meeting in a group for idea bouncing?



import numpy as np
import networkx as nx
import random

n_features = 20
n = 100
indx_user = 5

features = np.random.random((n_features, n))

feature_mask = np.random.randint(2, size= n_features)

G_matrix = np.random.choice(2, p = [0.99, 0.01], size=(n, n))
for i in range(n):
    G_matrix[i][i] = 0
    
G = nx.from_numpy_matrix(G_matrix)

#### sort other nodes based on similarity, pick only the ones that do not have a connection yet

not_yet_connected = [i for i in range(n) if G_matrix[indx_user][i] == 0] ### users to potentially connect with







#### Increase connection in the network!

##check if network is one component or not:
def find_node_to_connect_increase_connectivity(G, node_indx):
    
    if not nx.is_connected(G): ## if the network is split into several components, connect to a different component
        node_sets = list(nx.connected_components(G))
        other_components_indx = [i for i in range(len(node_sets)) if not indx_user in node_sets[i]]
        component_to_connect_with_indx = random.choice(other_components_indx)
        component_to_connect_with = node_sets[component_to_connect_with_indx]
        node_to_connect_with = random.choice(list(component_to_connect_with))
        
    #else: ## find a node that is far away from node
        
        
     
    return node_to_connect_with
    #connected_components = [i.nodes for i in sorted(nx.connected_components(G), key=len, reverse=True)]
    
#else:
    
    
    

### pick users that are far away in the network, but similar to user!




#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar 20 01:06:49 2021

@author: klaudiamur
"""

### G_matrix is the adjacency matrix of all users! (even new user)

import numpy as np
import networkx as nx
import random
import matplotlib.pyplot as plt
from sklearn.metrics.pairwise import cosine_similarity

n_features = 20
n = 100
indx_user = 5

feature_matrix = np.random.random((n, n_features))

feature_mask = np.random.randint(2, size= n_features)

G_matrix = np.random.choice(2, p = [0.9, 0.1], size=(n, n))
for i in range(n):
    G_matrix[i][i] = 0
    
G = nx.from_numpy_matrix(G_matrix)

#### sort other nodes based on similarity, pick only the ones that do not have a connection yet

not_yet_connected = [i for i in range(n) if G_matrix[indx_user][i] == 0] ### users to potentially connect with


### onboarding:
### connect with nodes with high eigenvector centrality! (and high closeness)
### if there is more than 1 component: pick biggest, connect two! (ideally?)
n_new_connections = 6

def pick_nodes_onboarding(G, indx_user, n_new_connections): ### user is not part of network yet! returns a list of n_new_connections nodes to connect to
    
    old_nodes = [i for i in G.nodes if i != indx_user]
    old_G = G.subgraph(old_nodes).copy()

    if nx.is_connected(old_G): ## check if there is more than 1 component
        G1 = old_G
    else:
        S = [old_G.subgraph(c).copy() for c in nx.connected_components(old_G)]
        S_sizes = np.array([c.size() for c in S])
        size_order_indx = np.argsort(S_sizes)
        S_sizes = S_sizes[size_order_indx][::-1]
        S = [S[i] for i in size_order_indx[::-1]]
        ### S is a list of connected components as subgraphs, ordered with S[0] as the biggest
        G1 = S[0]
        
    ### pick a good positioned node to connect from subgraph1:

    degree_centralities = {i[0]:i[1] for i in G1.degree()}
    eigenvector_centralities = nx.eigenvector_centrality(G1)
    closeness_centralities = nx.closeness_centrality(G1)
    
    ### normalize them all:
    degree_centralities = {k:(v/max(degree_centralities.values())) for k, v in degree_centralities.items()}
    eigenvector_centralities = {k:(v/max(eigenvector_centralities.values())) for k, v in eigenvector_centralities.items()}
    closeness_centralities = {k:(v/max(closeness_centralities.values())) for k, v in closeness_centralities.items()}
        
    ## pick good matches! high closeness/eigenvector centrality, but not to high degree!
    optimal_match_function_closeness = [(2*cc - dg**2)/2 for cc, dg in zip(closeness_centralities.values(), degree_centralities.values())]
    optimal_match_function_eigenvector = [(2*ec - dg**2)/2 for ec, dg in zip(closeness_centralities.values(), eigenvector_centralities.values())]
    
    
    indx_optimal_match = [k for k in degree_centralities.keys()]
    optimal_match_closeness_dict = {(indx_optimal_match[i]):optimal_match_function_closeness[i] for i in range(len(indx_optimal_match))}
    optimal_match_eigenvector_dict =  {(indx_optimal_match[i]):optimal_match_function_eigenvector[i] for i in range(len(indx_optimal_match))}
    
    sorted_c_dict = {k: v for k, v in sorted(optimal_match_closeness_dict.items(), reverse=True, key=lambda item: item[1])}
    sorted_e_dict = {k: v for k, v in sorted(optimal_match_eigenvector_dict.items(), reverse=True, key=lambda item: item[1])}
    
    n_ec = int(np.floor(n_new_connections / 2))
    n_cc = n_new_connections - n_ec
    
    new_connections_ec = [k for k in sorted_e_dict.keys()][:n_ec]
    new_connections_cc = [k for k in sorted_c_dict.keys() if k not in new_connections_ec][:n_cc]
    
    new_connections = new_connections_ec + new_connections_cc
        
    return new_connections



def match_making_friday_informal_meeting(G, indx_user, n_new_connections):
    new_connections = []
    G0 = G ## G0 is component in with the node indx_user is
    if not nx.is_connected(G): ## if the network is split into several components, connect to a different component
        S = [G.subgraph(c).copy() for c in nx.connected_components(G)]
        G0 = [i for i in S if indx_user in i][0]
               
        if len(S) > n_new_connections +1: ### pick other people at random from different components in the network
            S_others = [i for i in S if not indx_user in i]
            new_connections_subgraph = random.sample(S_others, n_new_connections)
            new_connections = [random.choice([j for j in i.nodes]) for i in new_connections_subgraph]
        
        else:
            S_others = [i for i in S if not indx_user in i]
            new_connections = [random.choice([j for j in i.nodes]) for i in S_others]
   
    
    nodes_picked = []
    if len(new_connections) < n_new_connections: ### find nodes in the same component that are far from each other
        n_nodes_to_find = n_new_connections - len(new_connections)
        nodes_at_highest_distance = sort_nodes_distance(G, indx_user)[: 2 *n_nodes_to_find]
        distance_matrix = np.zeros((2*n_nodes_to_find, 2*n_nodes_to_find))
        for i in range(len(nodes_at_highest_distance)):
            for j in range(i +1, len(nodes_at_highest_distance)):
                node0 = nodes_at_highest_distance[i]
                node1 = nodes_at_highest_distance[j]
                s = nx.shortest_path_length(G0, node0, node1)
                distance_matrix[i][j] = s
                distance_matrix[j][i] = s
                
        nodes_picked = []
        max_pair = np.unravel_index(np.argmax(distance_matrix, axis=None), distance_matrix.shape)
        nodes_picked.append(max_pair[0])
        nodes_picked.append(max_pair[1])
        
        while len(nodes_picked) < n_nodes_to_find:
            indx_node_1 = nodes_picked[-1]
            indx_node_2 = nodes_picked[-2]
            
            max_new_list = np.argsort(distance_matrix[indx_node_1])[::-1]
            max_new_list = [i for i in max_new_list if i not in nodes_picked]       
            nodes_picked.append(max_new_list[0])
            
            max_new_list = np.argsort(distance_matrix[indx_node_2])[::-1]
            max_new_list = [i for i in max_new_list if i not in nodes_picked]       
            nodes_picked.append(max_new_list[0])
            
        nodes_picked = nodes_picked[:n_new_connections]
            
    new_connections = np.concatenate((new_connections, nodes_picked))
    new_connections = new_connections.astype(np.int32)
    
    return new_connections
    
                
                
                
        
        
        
        
        
        
            
        
        
   # else:
        
    
        #node_sets = list(nx.connected_components(G))
        #other_components_indx = [i for i in range(len(node_sets)) if not indx_user in node_sets[i]]
        #component_to_connect_with_indx = random.choice(other_components_indx)
        #component_to_connect_with = node_sets[component_to_connect_with_indx]
        #nodes_to_connect_with = [random.choice(i) for i in node_sets[other_components_indx]]



#### Increase connection in the network!

##check if network is one component or not:
def increase_connectivity(G, indx_user):
    
    ### return a list of nodes to connect with to increase connectivity in overall network
        
    if not nx.is_connected(G): ## if the network is split into several components, connect to a different component
    
        node_sets = list(nx.connected_components(G))
        other_components_indx = [i for i in range(len(node_sets)) if not indx_user in node_sets[i]]
        #component_to_connect_with_indx = random.choice(other_components_indx)
        #component_to_connect_with = node_sets[component_to_connect_with_indx]
        nodes_to_connect_with = [random.choice(i) for i in node_sets[other_components_indx]]
        #node_to_connect_with = random.choice(list(component_to_connect_with))
        
    #else: ## find a node that is far away from node
    else: 
        nodes_to_connect_with = find_nodes_high_distance_same_component(G, indx_user)
            
        #
     
    return nodes_to_connect_with
    #connected_components = [i.nodes for i in sorted(nx.connected_components(G), key=len, reverse=True)]
    
#else:
    
def find_nodes_high_distance_same_component(G, indx_user):
    dist_dict = nx.single_source_shortest_path_length(G, indx_user, cutoff=None)
    highest_distance = max(dist_dict.values())
    nodes_at_highest_distance = [k for k, v in dist_dict.items() if v == highest_distance]
    
    return nodes_at_highest_distance

def sort_nodes_distance(G, indx_user): ## return a dict
    dist_dict = nx.single_source_shortest_path_length(G, indx_user, cutoff=None)
    highest_distance = max(dist_dict.values())
    nodes_at_distance_sorted = [[k for k, v in dist_dict.items() if v == i] for i in np.arange(1, highest_distance +1)[::-1]]
    nodes_at_distance_sorted = [item for sublist in nodes_at_distance_sorted for item in sublist]
    #nodes_at_distance_sorted = dict(sorted(dist_dict.items(), reverse=True, key=lambda item: item[1]))
    
    return nodes_at_distance_sorted
    


def find_nodes_similarity(feature_matrix, feature_mask, indx_user):
### find way of weighting the feature matrix with the feature mask, X is result
    X = feature_matrix*feature_mask    
    similarity = cosine_similarity(X)    
    nodes_similarity = similarity[indx_user]    





### create two functions, 1 for connectivity in the network and 1 for distance in feature vector!    

    

    

### pick users that are far away in the network, but similar to user!




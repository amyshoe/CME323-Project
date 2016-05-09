# -*- coding: utf-8 -*-
"""
Created on Mon May  2 19:06:40 2016

@author: sagarvare
"""

##FOrest is a list of graphs

import networkx as nx
def finding_aug_path(G,M):
    Forest = [] #Storing the Forests
    Path = []# The final path - HOW DO WE STORE A PATH?? as a Graph in itself? List of Nodes!!
    
    
    unmarked_edges = list(set(G.edges()) - set(M.edges()))
    unmarked_nodes = G.nodes()
    roots = unmarked_nodes##False - roots are exposed vertices
    ##we need a map from v to the tree
    tree_to_root = {}
    root_to_tree = {}
        
    ##List of exposed vertices - ROOTS OF TREES
    exp_vertex = list(set(G.nodes()) - set(M.nodes()))
    
    counter = 0
    #List of trees with the exposed vertices as the roots
    for v in exp_vertex:
        temp = nx.Graph()
        temp.add_node(v)
        Forest.append(temp)
        
        #link each root to its tree
        tree_to_root[counter] = v
        root_to_tree[v] = counter
        counter = counter + 1

    
    for vertex_number in xrange(len(unmarked_nodes)): #Explicitly need a while loop?
        v = unmarked_nodes[vertex_number]
        in_Forest = 0; #boolean for if unmarked v is 'within the forest or not'
        root_of_v = None
        tree_number_of_v = None
        for tree_number in range(len(Forest)):
            tree_in = Forest[tree_number]
            if tree_in.has_node(v) == True:
                in_Forest = 1
                root_of_v =tree_to_root[tree_number]
                tree_num_of_v = tree_number
                break #Break out of the for loop
                
        
        if (in_Forest==1 and dist_to_root(v,root_of_v,Forest[node_to_tree[v]])%2 == 0):
            ##Do something
            edges_v = Forest[tree_number_of_v].edges(v)
            for edge_number in xrange(len(edges_v)):
                e = edges_v[edge_number]
                if (e in unmarked_edges and not(e==[]):
                    #DO something
                    w = e[1]# the other vertex of the unmarked edge
                    w_in_Forest = 0; ##Indicator for w in F or not
                    
                    ##Go through all the trees in the forest
                    tree_of_w = None
                    for tree_number in xrange(len(Forest)):
                        tree = Forest[tree_number]
                        if tree.has_node(w) == True:
                            w_in_Forest = 1
                            root_of_w = tree_to_root[tree_number]
                            tree_num_of_w = tree_number
                            break #Break the outer for loop
                    
                    if w_in_Forest ==  0:
                        ##w is matched, so add e and w's matched edge to F
                        Forest[tree_num_of_v].add_node(w)#node{w}
                        Forest[tree_num_of_v].add_edge(e)#edge {v,w}
                        edge_w = M.edges(w)
                        Forest[tree_num_of_v].add_edge(edge_w)#edge{w,x}
                        ##Forest[tree_num_of_v].add_node(edge_w[0][1])#node{x}- NOT NEEDED??
                    else: ## w is in Forest
                        if dist_to_root(w,root_of_w,Forest[tree_num_of_w])%2 == 1:
                            ##Do Nothing
                        else:
                            if (tree_num_of_v == tree_num_of_w):
                                ##Shortest path from root(v)--->(v)-->w---->root(w)
                                Path = #The actual path
                                return Path
                            else:
                                ##Contract the blossom: TODO : Amy working on it
                                B = #Blossom
                                G_bar, M_bar = #Contract G and M by B
                                Path_bar = finding_aug_path(G_bar,M_bar)
                                Path = #Lift Path_bar to the original
                                return Path
                                
                ##Mark the Edge e
                unmarked_edges[edge_number] = []
                
            ##MArk vertex v
            unmarked_nodes[vertex_number] = [] ## DO I need to do this?? - Check with Amy
        
        ##IF Nothing is Found
        return Path ##Empty Path
                    
                            
                            
                            
                            
                        

                        
                            
                
        
        
    
    
        
    
    

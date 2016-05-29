# -*- coding: utf-8 -*-
"""
Created on Sun May 29 14:31:24 2016

@author: sagarvare
"""


import networkx as nx
import numpy as np
import copy
from multiprocessing import Pool


def find_maximum_matching(G,M):
    P = finding_aug_path(G,M)
    if P == []:#Base Case
        print "Base Case: " #, list(M.edges()) 
        return M
    else: #Augment P to M
        print " P is:",P,"\n M is :"#, list(M.edges())

        ##Add the alternating edges of P to M
        for i in xrange(0,len(P)-2,2): #Parallel For
            M.add_edge(P[i],P[i+1])
            M.remove_edge(P[i+1],P[i+2])
        M.add_edge(P[-2],P[-1])
        print "M after adding path:"#, list(M.edges())
        return find_maximum_matching(G,M)

def dist_to_root(point,root,Graph):
    path = nx.shortest_path(Graph, source = point, target = root)
    return (len(path)-1)
    
def generate_random_graph(n,density=0.5):
    ## n - number of nodes
    ## d - "density" of the graph [0,1]
    graph = nx.Graph()
    for i in xrange(n):
        for j in xrange(i+1,n):
            if np.random.uniform() < density:
                graph.add_edge(i,j)
    print "graph nodes: ", list(graph.nodes())
    return graph 
    
def finding_aug_path(G,M,Blossom_stack=[]):
    print '-------------------------------\nfinding aug path was called\n G: '#, list(G.nodes()), "\n M:", list(M.edges()),"\nBlossom Stack is:" ,Blossom_stack
    Forest = [] #Storing the Forests
    Path = [] # The final path 

    unmarked_edges = list(set(G.edges()) - set(M.edges()))
    #print "all the edges in G are:",G.edges()
    #print "all the unmarked edges are:", unmarked_edges
    unmarked_nodes = list(G.nodes())
    Forest_nodes = []
    ## we need a map from v to the tree
    tree_to_root = {} # key=idx of tree in forest, val=root
    root_to_tree = {} # key=root, val=idx of tree in forest
        
    ##List of exposed vertices - ROOTS OF TREES
    exp_vertex = list(set(G.nodes()) - set(M.nodes()))
    print "\n Exposed vertices:"#, exp_vertex
    
    counter = 0
    #List of trees with the exposed vertices as the roots
    for v in exp_vertex:  #<------------ Completely PARALLEL For loop -----change counter to the index of v in exp_vertex
        temp = nx.Graph()
        temp.add_node(v)
        Forest.append(temp)
        Forest_nodes.append(v)

        #link each root to its tree
        tree_to_root[counter] = v
        root_to_tree[v] = counter
        counter = counter + 1

    
    for v in Forest_nodes:  ## <----------- we cant trivially change this...
        print "The nodes in Forest are:" #,Forest_nodes
        root_of_v = None
        tree_num_of_v = None
        for tree_number in xrange(len(Forest)): ## <------- completely parallel : figuring out the tree of v
            tree_in = Forest[tree_number]
            if tree_in.has_node(v) == True:
                root_of_v = tree_to_root[tree_number]
                tree_num_of_v = tree_number
                break #Break out of the for loop
        print "here's v: ", v
        edges_v = list(G.edges(v))
        print "edges of v: "#, edges_v
        print "the length of edges_v list is:" ,len(edges_v)
        pool = Pool(processes =4)
        edge_data = edges_v
        
        temp = pool.map(edge_function, edge_data)
        
        for i in xrange(len(temp)):
            if temp[i][0] == 2 or temp[i][0]:
                return temp[i][1]
        ##check for blossoms of 3-length
        for i in xrange(len(temp)):
            if temp[i][0] == 1 and G.has_edge(v,temp[i][1][1]):
                #contract len 3 blossom
                w = temp[i][1][0]                
                blossom = [v,w,temp[i][1][1],v]
                contracted_G = copy.deepcopy(G)
                contracted_M = copy.deepcopy(M)
                print "w is: ", w
                for node in blossom[0:len(blossom)-1]:
                    print "\t Blossom node: ", node
                    if node != w:
                        contracted_G = nx.contracted_nodes(contracted_G, w, node, self_loops=False)
                        print "contracted", node, "into", w
                        if node in contracted_M.nodes(): 
                           print "removing", node, "from M"
                           edge_rm = list(M.edges(node))[0] #this will be exactly one edge
                           print "and also", edge_rm[1], "from M"
                           print "SINGLE EDGE: edges = "#, list(M.edges(node))
                           print "edge rm = ", edge_rm
                           contracted_M.remove_node(node)
                           contracted_M.remove_node(edge_rm[1])
                           assert(len(list(contracted_M.nodes()))%2 == 0)

                    # print "M:", list(M.nodes()),"\nContracted_M:", list(contracted_M.nodes())
                    # print "M:", list(M.edges()),"\nContracted_M:", list(contracted_M.edges())
                    # print "G:", list(G.edges()),"\nContracted_G:", list(contracted_G.edges())

                print "out of the for LOOP"
                # add blossom to our stack
                Blossom_stack.append(w)
                print "Blossom_stack after contraction: ", Blossom_stack

                # recurse
                aug_path = finding_aug_path(contracted_G, contracted_M, Blossom_stack)
                print "\t \t ~~~"
                print "Blossom_stack after recursion: ", Blossom_stack
                print "Augmented path after recursion: ", aug_path

                # check if blossom exists in aug_path 
                v_B = Blossom_stack.pop()
                if (v_B in aug_path):
                    #blossom.append(w) ### - WHY ARE WE DOING THIS???? w is inside the blossom anyway??
                    print "Blossom_stack after pop: ", Blossom_stack

                    ##Define the L_stem and R_stem
                    L_stem = aug_path[0:aug_path.index(v_B)]
                    R_stem = aug_path[aug_path.index(v_B)+1:]
                    print "L_stem: ", L_stem
                    print "R_stem: ", R_stem
                    lifted_blossom = [] #stores the path within the blossom to take

                    # Find base of blossom
                    i = 0
                    base = None
                    base_idx = -1
                    blossom_ext = blossom + [blossom[1]] 
                    while base == None and i < len(blossom) - 1:
                        if not(M.has_edge(blossom[i],blossom[i+1])):
                            if not(M.has_edge(blossom[i+1],blossom_ext[i+2])): 
                                base = blossom[i+1]
                                base_idx = i+1
                            else:
                                i += 2
                        else:
                            i += 1
                    print "Blossom is: ", blossom
                    print "\tBlossom base is: ", base 

                    # if needed, create list of blossom nodes starting at base
                    if blossom[0] != base:
                        based_blossom = []
                        base_idx = blossom.index(base)
                        for i in xrange(base_idx,len(blossom)-1):
                            based_blossom.append(blossom[i])
                        for i in xrange(0,base_idx):
                            based_blossom.append(blossom[i])
                        based_blossom.append(base)
                        print "\tbase index in original:", base_idx
                        print "\tBlossom base-ified: ", based_blossom
                        print "\toriginal Blossom is:", blossom 
                    else:
                        print "It was already base-ified"
                        based_blossom = blossom

                    # CHECK IF BLOSSOM IS ENDPT
                    if L_stem == [] or R_stem == []:
                        print "Left or Right is empty"
                        if L_stem != []:
                            print "Left is not empty, R is empty"
                            if G.has_edge(base, L_stem[-1]):
                                # CASE OH NO:
                                if M.has_edge(base, L_stem[-1]):
                                    print "WE THOUGHT THIS CASE WAS IMPOSSIBLE!!!!!!!!!!!!!!!!!!!!"
                                # CASE 1:
                                print "Chuck the blossom. Return: ", L_stem + [base]
                                return L_stem + [base]
                            else:
                                # CASE 2:
                                # find where Lstem is connected
                                i = 1
                                while (lifted_blossom == []):
                                    print "THIS IS G: ", G.edges()
                                    print "searching for this:", (based_blossom[i],L_stem[-1])
                                    assert(i < len(based_blossom)-1)
                                    if G.has_edge(based_blossom[i],L_stem[-1]):
                                        # make sure we're adding the even part to lifted path
                                        if i%2 == 0: # same dir path
                                            lifted_blossom = list(reversed(based_blossom))[-i-1:] ####################
                                        else: # opposite dir path
                                            lifted_blossom = based_blossom[i:]##########################
                                    i += 1
                                print "Successful lifting: ", L_stem + (lifted_blossom)
                                return L_stem + lifted_blossom

                        else:
                            print "R is not empty, L is empty"
                            if G.has_edge(base, R_stem[0]):
                                # CASE OH NO:
                                if M.has_edge(base, R_stem[0]):
                                    print "WE THOUGHT THIS CASE WAS IMPOSSIBLE!!!!!!!!!!!!!!!!!!!!"
                                # CASE 1:
                                print "Chuck the blossom. Return: ", [base] + R_stem
                                return [base] + R_stem
                            else:
                                # CASE 2:
                                # find where R_stem is connected
                                i = 1
                                while (lifted_blossom == []):
                                    print "THIS IS G: "#, G.edges()
                                    print "searching for this:",(based_blossom[i],R_stem[-0])
                                    assert(i < len(based_blossom)-1)
                                    if G.has_edge(based_blossom[i],R_stem[0]):
                                        # make sure we're adding the even part to lifted path
                                        if i%2 == 0: # same dir path
                                            lifted_blossom = based_blossom[:i+1]
                                            print lifted_blossom
                                        else: # opposite dir path
                                            lifted_blossom = list(reversed(based_blossom))[:-i]
                                    i += 1
                                print "Successful lifting: ", lifted_blossom + R_stem
                                return lifted_blossom + R_stem

                    else: # blossom is in the middle
                        # LIFT the blossom
                        print "Blossom is neither L nor R endpt"
                        # check if L_stem attaches to base
                        if M.has_edge(base, L_stem[-1]):
                            # find where right stem attaches
                            if G.has_edge(base, R_stem[0]):
                                # blossom is useless
                                print "Useless blossom. return: ", L_stem + [base] + R_stem
                                return L_stem + [base] + R_stem
                            else:
                                # blossom needs to be lifted
                                i = 1
                                while (lifted_blossom == []):
                                    print "THIS IS G: "#, G.edges()
                                    print "searching for this:", (based_blossom[i],R_stem[-0])
                                    assert(i < len(based_blossom)-1)
                                    if G.has_edge(based_blossom[i],R_stem[0]):
                                        print "found the edge man!!!!"
                                        # make sure we're adding the even part to lifted path
                                        if i%2 == 0: # same dir path
                                            lifted_blossom = based_blossom[:i+1] 
                                            print lifted_blossom
                                        else: # opposite dir path
                                            lifted_blossom = list(reversed(based_blossom))[:-i]
                                            print lifted_blossom

                                    i += 1
                                print "Successful lifting: ", L_stem + lifted_blossom + R_stem
                                return L_stem + lifted_blossom + R_stem
                        else: 
                            # R stem to base is in matching
                            assert(M.has_edge(base, R_stem[0]))
                            # check where left stem attaches
                            if G.has_edge(base, L_stem[-1]):
                                # blossom is useless
                                print "Useless blossom. return: ", L_stem + [base] + R_stem
                                return L_stem + [base] + R_stem
                            else:
                                # blossom needs to be lifted
                                i = 1
                                while (lifted_blossom == []):
                                    print "THIS IS G: "#, G.edges()
                                    print "searching for this:", (based_blossom[i],L_stem[-1])
                                    assert(i < len(based_blossom)-1)
                                    if G.has_edge(based_blossom[i],L_stem[-1]):
                                        # make sure we're adding the even part to lifted path
                                        if i%2 == 0: # same dir path
                                            lifted_blossom = list(reversed(based_blossom))[-i-1:] 
                                        else: # opposite dir path
                                            lifted_blossom = based_blossom[i:] 
                                    i += 1
                                print "Successful lifting: ", L_stem + list(reversed(lifted_blossom)) + R_stem
                                return L_stem + list((lifted_blossom)) + R_stem

                else: # blossom is not in aug_path
                    print "Blossom not in aug path"
                    return aug_path
                        
   ########################################## case 1 -> blossom ############################
        for i in xrange(len(temp)):
            if temp[i][0] ==1:
                Forest[tree_num_of_v].add_edge(v,temp[i][1][0])
                Forest[tree_num_of_v].add_edge(temp[i][1][0],temp[i][1][1])
                Forest_nodes.append(temp[i][1][1])

                

            
        
                
        
            
    return [] #Empty Path
    
    
def edge_function(e):
    e2 = (e[1],e[0]) #the edge in the other order
    print "\tConsidering the edge", e
    if ((e in unmarked_edges or e2 in unmarked_edges) and e!=[]):
        w = e[1] # the other vertex of the unmarked edge
        w_in_Forest = 0; ##Indicator for w in F or not
        print "here's w: ", w

        ##Go through all the trees in the forest to check if w in F
        tree_of_w = None
        tree_num_of_w = None
        for tree_number in xrange(len(Forest)):
            tree = Forest[tree_number]
            if tree.has_node(w) == True:
                w_in_Forest = 1
                root_of_w = tree_to_root[tree_number]
                print "root of w is:", root_of_w
                tree_num_of_w = tree_number
                tree_of_w = Forest[tree_num_of_w]
                break #Break the outer for loop
        
        print "w in Forest?: ", w_in_Forest
        if w_in_Forest == 0:
            print "w not in Forest"
            ## w is matched, so add e and w's matched edge to F
            Forest[tree_num_of_v].add_edge(e[0],e[1]) # edge {v,w} <---------NOT ALLOWED
            print "edge added to forest: ", e
            # Note: we don't add w to forest nodes b/c it's odd dist from root
            assert(M.has_node(w))
            print "Nodes of M: "#, list(M.nodes())
            print "Edges of M incident to w: "#, list(M.edges(w))
            edge_w = list(M.edges(w))[0] # get edge {w,x}
            #Forest[tree_num_of_v].add_edge(edge_w[0],edge_w[1]) # add edge{w,x}
            print "edge added to forest: ", edge_w
            #Forest_nodes.append(edge_w[1]) ## add {x} to the list of forest nodes
            print "node added to forest: ", edge_w[1]
            return (1,edge_w) ## <-----------------------------------Instead doing this!!!!!!

        else: ## w is in Forest
            print "w in Forest"
            # if odd, do nothing.
            if dist_to_root(w,root_of_w,Forest[tree_num_of_w])%2 == 0:
                print "dist to root is even"
                if (tree_num_of_v != tree_num_of_w):
                    ##Shortest path from root(v)--->v-->w---->root(w)
                    path_in_v = nx.shortest_path(Forest[tree_num_of_v], source = root_of_v, target = v)
                    path_in_w = nx.shortest_path(Forest[tree_num_of_w], source = w, target = root_of_w)
                    print "Path is:"#, path_in_v + path_in_w

                    return (2,path_in_v + path_in_w)
                #w = e[0][1] # the other vertex of the unmarked edge
                else: ##Contract the blossom
                    print "\nBLOOOOOOOOOOSSSSSSSOOOOOOMMMMMMMMMM\n"
                    # create blossom
                    blossom = nx.shortest_path(tree_of_w, source=v, target=w)
                    blossom.append(v)
                    print "Blossom created: ", blossom
                    assert(len(blossom)%2 == 0)

                    # contract blossom into single node w
                    contracted_G = copy.deepcopy(G)
                    contracted_M = copy.deepcopy(M)
                    print "w is: ", w
                    for node in blossom[0:len(blossom)-1]:
                        print "\t Blossom node: ", node
                        if node != w:
                            contracted_G = nx.contracted_nodes(contracted_G, w, node, self_loops=False)
                            print "contracted", node, "into", w
                            if node in contracted_M.nodes(): 
                               print "removing", node, "from M"
                               edge_rm = list(M.edges(node))[0] #this will be exactly one edge
                               print "and also", edge_rm[1], "from M"
                               print "SINGLE EDGE: edges = "#, list(M.edges(node))
                               print "edge rm = ", edge_rm
                               contracted_M.remove_node(node)
                               contracted_M.remove_node(edge_rm[1])
                               assert(len(list(contracted_M.nodes()))%2 == 0)

                    # print "M:", list(M.nodes()),"\nContracted_M:", list(contracted_M.nodes())
                    # print "M:", list(M.edges()),"\nContracted_M:", list(contracted_M.edges())
                    # print "G:", list(G.edges()),"\nContracted_G:", list(contracted_G.edges())

                    print "out of the for LOOP"
                    # add blossom to our stack
                    Blossom_stack.append(w)
                    print "Blossom_stack after contraction: ", Blossom_stack

                    # recurse
                    aug_path = finding_aug_path(contracted_G, contracted_M, Blossom_stack)
                    print "\t \t ~~~"
                    print "Blossom_stack after recursion: ", Blossom_stack
                    print "Augmented path after recursion: ", aug_path

                    # check if blossom exists in aug_path 
                    v_B = Blossom_stack.pop()
                    if (v_B in aug_path):
                        #blossom.append(w) ### - WHY ARE WE DOING THIS???? w is inside the blossom anyway??
                        print "Blossom_stack after pop: ", Blossom_stack

                        ##Define the L_stem and R_stem
                        L_stem = aug_path[0:aug_path.index(v_B)]
                        R_stem = aug_path[aug_path.index(v_B)+1:]
                        print "L_stem: ", L_stem
                        print "R_stem: ", R_stem
                        lifted_blossom = [] #stores the path within the blossom to take

                        # Find base of blossom
                        i = 0
                        base = None
                        base_idx = -1
                        blossom_ext = blossom + [blossom[1]] 
                        while base == None and i < len(blossom) - 1:
                            if not(M.has_edge(blossom[i],blossom[i+1])):
                                if not(M.has_edge(blossom[i+1],blossom_ext[i+2])): 
                                    base = blossom[i+1]
                                    base_idx = i+1
                                else:
                                    i += 2
                            else:
                                i += 1
                        print "Blossom is: ", blossom
                        print "\tBlossom base is: ", base 

                        # if needed, create list of blossom nodes starting at base
                        if blossom[0] != base:
                            based_blossom = []
                            base_idx = blossom.index(base)
                            for i in xrange(base_idx,len(blossom)-1):
                                based_blossom.append(blossom[i])
                            for i in xrange(0,base_idx):
                                based_blossom.append(blossom[i])
                            based_blossom.append(base)
                            print "\tbase index in original:", base_idx
                            print "\tBlossom base-ified: ", based_blossom
                            print "\toriginal Blossom is:", blossom 
                        else:
                            print "It was already base-ified"
                            based_blossom = blossom

                        # CHECK IF BLOSSOM IS ENDPT
                        if L_stem == [] or R_stem == []:
                            print "Left or Right is empty"
                            if L_stem != []:
                                print "Left is not empty, R is empty"
                                if G.has_edge(base, L_stem[-1]):
                                    # CASE OH NO:
                                    if M.has_edge(base, L_stem[-1]):
                                        print "WE THOUGHT THIS CASE WAS IMPOSSIBLE!!!!!!!!!!!!!!!!!!!!"
                                    # CASE 1:
                                    print "Chuck the blossom. Return: ", L_stem + [base]
                                    return L_stem + [base]
                                else:
                                    # CASE 2:
                                    # find where Lstem is connected
                                    i = 1
                                    while (lifted_blossom == []):
                                        print "THIS IS G: ", G.edges()
                                        print "searching for this:", (based_blossom[i],L_stem[-1])
                                        assert(i < len(based_blossom)-1)
                                        if G.has_edge(based_blossom[i],L_stem[-1]):
                                            # make sure we're adding the even part to lifted path
                                            if i%2 == 0: # same dir path
                                                lifted_blossom = list(reversed(based_blossom))[-i-1:] ####################
                                            else: # opposite dir path
                                                lifted_blossom = based_blossom[i:]##########################
                                        i += 1
                                    print "Successful lifting: ", L_stem + (lifted_blossom)
                                    return (3,L_stem + lifted_blossom)

                            else:
                                print "R is not empty, L is empty"
                                if G.has_edge(base, R_stem[0]):
                                    # CASE OH NO:
                                    if M.has_edge(base, R_stem[0]):
                                        print "WE THOUGHT THIS CASE WAS IMPOSSIBLE!!!!!!!!!!!!!!!!!!!!"
                                    # CASE 1:
                                    print "Chuck the blossom. Return: ", [base] + R_stem
                                    return (3,[base] + R_stem)
                                else:
                                    # CASE 2:
                                    # find where R_stem is connected
                                    i = 1
                                    while (lifted_blossom == []):
                                        print "THIS IS G: "#, G.edges()
                                        print "searching for this:",(based_blossom[i],R_stem[-0])
                                        assert(i < len(based_blossom)-1)
                                        if G.has_edge(based_blossom[i],R_stem[0]):
                                            # make sure we're adding the even part to lifted path
                                            if i%2 == 0: # same dir path
                                                lifted_blossom = based_blossom[:i+1]
                                                print lifted_blossom
                                            else: # opposite dir path
                                                lifted_blossom = list(reversed(based_blossom))[:-i]
                                        i += 1
                                    print "Successful lifting: ", lifted_blossom + R_stem
                                    return (3,lifted_blossom + R_stem)

                        else: # blossom is in the middle
                            # LIFT the blossom
                            print "Blossom is neither L nor R endpt"
                            # check if L_stem attaches to base
                            if M.has_edge(base, L_stem[-1]):
                                # find where right stem attaches
                                if G.has_edge(base, R_stem[0]):
                                    # blossom is useless
                                    print "Useless blossom. return: ", L_stem + [base] + R_stem
                                    return (3,L_stem + [base] + R_stem)
                                else:
                                    # blossom needs to be lifted
                                    i = 1
                                    while (lifted_blossom == []):
                                        print "THIS IS G: "#, G.edges()
                                        print "searching for this:", (based_blossom[i],R_stem[-0])
                                        assert(i < len(based_blossom)-1)
                                        if G.has_edge(based_blossom[i],R_stem[0]):
                                            print "found the edge man!!!!"
                                            # make sure we're adding the even part to lifted path
                                            if i%2 == 0: # same dir path
                                                lifted_blossom = based_blossom[:i+1] 
                                                print lifted_blossom
                                            else: # opposite dir path
                                                lifted_blossom = list(reversed(based_blossom))[:-i]
                                                print lifted_blossom

                                        i += 1
                                    print "Successful lifting: ", L_stem + lifted_blossom + R_stem
                                    return (3,L_stem + lifted_blossom + R_stem)
                            else: 
                                # R stem to base is in matching
                                assert(M.has_edge(base, R_stem[0]))
                                # check where left stem attaches
                                if G.has_edge(base, L_stem[-1]):
                                    # blossom is useless
                                    print "Useless blossom. return: ", L_stem + [base] + R_stem
                                    return (3,L_stem + [base] + R_stem)
                                else:
                                    # blossom needs to be lifted
                                    i = 1
                                    while (lifted_blossom == []):
                                        print "THIS IS G: "#, G.edges()
                                        print "searching for this:", (based_blossom[i],L_stem[-1])
                                        assert(i < len(based_blossom)-1)
                                        if G.has_edge(based_blossom[i],L_stem[-1]):
                                            # make sure we're adding the even part to lifted path
                                            if i%2 == 0: # same dir path
                                                lifted_blossom = list(reversed(based_blossom))[-i-1:] 
                                            else: # opposite dir path
                                                lifted_blossom = based_blossom[i:] 
                                        i += 1
                                    print "Successful lifting: ", L_stem + list(reversed(lifted_blossom)) + R_stem
                                    return (3,L_stem + list((lifted_blossom)) + R_stem)

                    else: # blossom is not in aug_path
                        print "Blossom not in aug path"
                        return (3,aug_path)
                            
        ##Mark the Edge e
        #unmarked_edges[edge_number] = []
    
    ##MArk vertex v
    ##unmarked_nodes[vertex_number] = [] ## DO I need to do this?? - Check with Amy

    
if __name__ == '__main__':
    G = generate_random_graph(10,0.15)
    M = nx.Graph()
    Blossom_stack = []
    # print "This is our graph: ", list(G.edges())
    MM = find_maximum_matching(G, M)
    print "Here it is M edges:", list(MM.edges())
    print "Matching has ", MM.number_of_edges(), "edges, covering ", MM.number_of_nodes(), "nodes."
    if MM.number_of_nodes() == G.number_of_nodes():
        print "We found a perfect matching!"
    for edge in list(MM.edges()):
        if G.has_edge(edge[0], edge[1]):
            print "Good"
        else:
            print "baaad boy"
    print list(G.edges())

                    
                            
        
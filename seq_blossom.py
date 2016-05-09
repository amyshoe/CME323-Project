
import networkx as nx

def dist_to_root(point,root,Graph):
    path = nx.shortest_path(Graph, source = point, target = root)
    return (len(path)-1)
    
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
                if (e in unmarked_edges and e!=[]):
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
                        # if odd, do nothing.
                        if dist_to_root(w,root_of_w,Forest[tree_num_of_w])%2 == 0:
                            if (tree_num_of_v == tree_num_of_w):
                                ##Shortest path from root(v)--->(v)-->w---->root(w)
                                Path = []#The actual path (I made this empy for now so it would compile)
                                return Path
                            else:
                                ##Contract the blossom: TODO : Amy working on it
								# create blossom
								blos_path = tree.subgraph(nx.shortest_path(tree, source=v, target=w))
								blossom = blos_path.copy()
								blossom.add_edge(v,w)

								# contract blossom into node w
								contracted_G = G.copy()
								contracted_M = M.copy()
								for node in blossom.nodes():
									if node != v and node != w:
										contracted_G = nx.contracted_nodes(contracted_G, w, node, self_loops=False)
										if node in contracted_M.nodes(): 
											contracted_M = nx.contracted_nodes(contracted_M, w, node, self_loops=False)

								### From the examples, it seems like we should be contracting into w, 
								### but maybe it'll end up being easier to contract to a separate node...
								### not sure yet, but here's the code for that just in case

								# # contract blossom into single node "Blossom"
								# contracted_G = G.copy()
								# contracted_M = M.copy()
								# v_b = "Blossom"
								# contracted_G.add_node(v_b)
								# contracted_M.add_node(v_b)
								# for node in blossom.nodes():
								# 	contracted_G = nx.contracted_nodes(contracted_G, v_b, node, self_loops=False)
								# 	if node in contracted_M.nodes(): 
								# 		contracted_M = nx.contracted_nodes(contracted_M, v_b, node, self_loops=False)

								# recurse
								aug_path = find_augmenting_path(contracted_G, contracted_M)

								# lift
								L_stem_idx = aug_path.index((v,w))
								# TODO: need right stem... R_stem_idx = 

								#lift: 
								lifted_path = []
								for edge in aug_path:
									if edge[1] == v:
										for e in blos_path: ## TODO: this is the line that's currently incorrect, 
															##		 since blos_path is a graph object, whose edge
															##		 list is not nec ordered how we want it
											lifted_path.append(e)
									else:
										lifted_path.append(edge)

								return lifted_path
                                
                ##Mark the Edge e
                unmarked_edges[edge_number] = []
                
            ##MArk vertex v
            unmarked_nodes[vertex_number] = [] ## DO I need to do this?? - Check with Amy
        
        ##IF Nothing is Found
        return Path ##Empty Path
                    
                            
                            
                            
                            
                        

                        
                            
                
        
        
    
    
        
    
    



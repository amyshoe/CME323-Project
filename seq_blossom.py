
import networkx as nx
import numpy as np

def find_maximum_matching(G,M):
    P = finding_aug_path(G,M)
    if P == []:#Base Case
        return M
    else: #Augment P to M
        ##Add the edges of P to M
        for i in xrange(len(P)-1):
            M.add_edge(P[i],P[i+1])
        return find_maximum_matching(G,M)

def dist_to_root(point,root,Graph):
    path = nx.shortest_path(Graph, source = point, target = root)
    return (len(path)-1)
    
def generate_random_graph(n,density=0.5):
    ## n - number of nodes
    ## d - "density" of the graph [0,1]
    graph = nx.Graph()
    for i in xrange(n):
        for j in xrange(i,n):
            if np.random.uniform < density:
                graph.add_edge(i,j)

    return graph 
    
def finding_aug_path(G,M,Blossom_stack):
    Forest = [] #Storing the Forests
    Path = [] # The final path 

    unmarked_edges = list(set(G.edges()) - set(M.edges()))
    unmarked_nodes = list(G.nodes())
    ## we need a map from v to the tree
    tree_to_root = {} # key=idx of tree in forest, val=root
    root_to_tree = {} # key=root, val=idx of tree in forest
        
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

    for vertex_number in xrange(len(unmarked_nodes)): ##TODO: add while loop!!!!!!!
        v = unmarked_nodes[vertex_number]
        in_Forest = 0; #boolean for if unmarked v is 'within the forest or not'
        root_of_v = None
        tree_number_of_v = None
        for tree_number in xrange(len(Forest)):
            tree_in = Forest[tree_number]
            if tree_in.has_node(v) == True:
                in_Forest = 1
                root_of_v = tree_to_root[tree_number]
                tree_num_of_v = tree_number
                break #Break out of the for loop
                
        
        if (in_Forest==1 and dist_to_root(v,root_of_v,Forest[node_to_tree[v]])%2 == 0):
            ##Do something
            edges_v = Forest[tree_number_of_v].edges(v)
            for edge_number in xrange(len(edges_v)):
                e = edges_v[edge_number]
                if (e in unmarked_edges and e!=[]):
                    w = e[1] # the other vertex of the unmarked edge
                    w_in_Forest = 0; ##Indicator for w in F or not
                    
                    ##Go through all the trees in the forest to check if w in F
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
                        Forest[tree_num_of_v].add_edge(e)#edge {v,w}
                        edge_w = M.edges(w) #get edge {w,x}
                        Forest[tree_num_of_v].add_edge(edge_w)#add edge{w,x}
                    else: ## w is in Forest
                        # if odd, do nothing.
                        if dist_to_root(w,root_of_w,Forest[tree_num_of_w])%2 == 0:
                            if (tree_num_of_v != tree_num_of_w):
                                ##Shortest path from root(v)--->v-->w---->root(w)
                                path_in_v = nx.shortest_path(Forest[tree_num_of_v], source = root_of_v, target = v)
                                path_in_w = nx.shortest_path(Forest[tree_num_of_w], source = w, target = root_of_w)
                                return path_in_w + path_in_v
                            else: ##Contract the blossom
                                # create blossom
                                blossom = nx.shortest_path(tree, source=v, target=w)
                                blossom.append(v)
                                print "Blossom created: ", blossom

                                # contract blossom into single node w
                                contracted_G = G.copy()
                                contracted_M = M.copy()
                                for node in blossom:
                                    if node != w:
                                        contracted_G = nx.contracted_nodes(contracted_G, w, node, self_loops=False)
                                        if node in contracted_M.nodes(): 
                                           contracted_M = nx.contracted_nodes(contracted_M, w, node, self_loops=False)

                                # add blossom to our stack
                                Blossom_stack.append(w)
                                print "Blossom_stack after contraction: ", Blossom_stack

                                # recurse
                                aug_path = finding_aug_path(contracted_G, contracted_M, Blossom_stack)
                                print "Blossom_stack after recursion: ", Blossom_stack

                                # check if blossom exists in aug_path
                                v_B = Blossom_stack.pop()
                                if (v_B in aug_path):
                                    blossom.append(w)
                                    print "Blossom_stack after pop: ", Blossom_stack
                                    print "Blossom in aug path: ", Blossom

                                    # find base of blossom 
                                    i = 0
                                    base = None
                                    while base == None and i < len(blossom) - 1:
                                        if not(M.has_edge(blossom[i],blossom[i+1])):
                                            if not(M.has_edge(blossom[i+1],blossom[i+2])):
                                                base = blossom[i+1]
                                            else:
                                                i += 2
                                        else:
                                            i += 1
                                    # create list of blossom nodes starting at base
                                    based_blossom = [base]
                                    base_idx = blossom.index(base)
                                    for i in xrange(1,len(blossom)-base_idx):
                                        based_blossom.append(blossom[base_idx + i])
                                    for i in xrange(1,base_idx):
                                        based_blossom.append(blossom[i])
                                    print "Base: ", base
                                    print "Blossom base-ified: ", based_blossom

                                    # lift
                                    L_stem = aug_path[0:aug_path.index(v_B)]
                                    R_stem = aug_path[aug_path.index(v_B)+1:]
                                    print "L_stem: ", L_stem
                                    print "R_stem: ", R_stem
                                    lifted_blossom = []
                                    if L_stem != []:
                                        if M.has_edge(base,L_stem[-2]): # lift with base matched to left stem
                                            # find where right stem attaches (or find that blossom is right endpt)
                                            while (lifted_blossom == [] and i < len(based_blossom)-1):
                                                if G.has_edge(based_blossom[i+2],R_stem[0]):
                                                    lifted_blossom = based_blossom[:i+2]
                                                i += 2
                                            print "L+lift+R; here's lift: ", lifted_blossom
                                            return L_stem + lifted_blossom + R_stem
                                        else: # lift with base matched to right stem
                                            # find where left stem attaches
                                            while (lifted_blossom == [] and i < len(based_blossom)-1):
                                                if G.has_edge(based_blossom[i+2],L_stem[-2]):
                                                    lifted_blossom = based_blossom[:i+2]
                                                i += 2
                                            print "R+lift+L; here's lift: ", lifted_blossom
                                            return R_stem.reverse() + lifted_blossom + L_stem.reverse()
                                    else: # blossom is left endpt
                                        while (lifted_blossom == [] and i < len(based_blossom)-1):
                                            if G.has_edge(based_blossom[i+2],L_stem[-2]):
                                                lifted_blossom = based_blossom[:i+2]
                                            i += 2
                                        print "R+lift; here's lift: ", lifted_blossom
                                        return R_stem.reverse() + lifted_blossom

                                else: # blossom is not in aug_path
                                    print "Blossom not in aug path"
                                    return aug_path
                                
                ##Mark the Edge e
                unmarked_edges[edge_number] = []
                
            ##MArk vertex v
            unmarked_nodes[vertex_number] = [] ## DO I need to do this?? - Check with Amy
        
        ##IF Nothing is Found
        return Path ##Empty Path

if __name__ == '__main__':
    G = generate_random_graph(500)
    M = nx.Graph()
    Blossom_stack = []
    P = finding_aug_path(G, M, Blossom_stack)
    print P

                    
                            
                            
                            
                            
                        

                        
                            
                
        
        
    
    
        
    
    



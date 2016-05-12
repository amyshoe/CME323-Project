
import networkx as nx
import numpy as np

def find_maximum_matching(G,M):
    P = finding_aug_path(G,M)
    if P == []:#Base Case
        print "Base Case: print M" 
        return M.edges()
    else: #Augment P to M
        print " P is:",P,"\n M is :",M.edges()

        ##Add the edges of P to M
        for i in xrange(0,len(P)-2,2):
            M.add_edge(P[i],P[i+1])
            M.remove_edge(P[i+1],P[i+2])
        M.add_edge(P[len(P)-2],P[len(P)-1])
        print "M after adding path:", M.edges()
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
    print '-------------------------------\nfinding aug path was called\n G: ', list(G.nodes()), "\n M:", list(M.nodes())
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
    print "\n Exposed vertices:", exp_vertex
    
    counter = 0
    #List of trees with the exposed vertices as the roots
    for v in exp_vertex:
        temp = nx.Graph()
        temp.add_node(v)
        Forest.append(temp)
        Forest_nodes.append(v)

        #link each root to its tree
        tree_to_root[counter] = v
        root_to_tree[v] = counter
        counter = counter + 1

    
    for v in Forest_nodes: 
        print "The nodes in Forest are:" ,Forest_nodes
        root_of_v = None
        tree_num_of_v = None
        for tree_number in xrange(len(Forest)):
            tree_in = Forest[tree_number]
            if tree_in.has_node(v) == True:
                root_of_v = tree_to_root[tree_number]
                tree_num_of_v = tree_number
                break #Break out of the for loop
        print "here's v: ", v
        edges_v = list(G.edges(v))
        print "edges of v: ", edges_v
        print "the length of edges_v list is:" ,len(edges_v)
        for edge_number in xrange(len(edges_v)):
            e = edges_v[edge_number]
            e2 = (e[1],e[0]) #the edge in the other order
            print "\tConsidering the edge", e
            if ((e in unmarked_edges or e2 in unmarked_edges) and e!=[]):
                w = e[1] # the other vertex of the unmarked edge
                w_in_Forest = 0; ##Indicator for w in F or not
                print "here's w", w

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
                    ##w is matched, so add e and w's matched edge to F
                    Forest[tree_num_of_v].add_edge(e[0],e[1])#edge {v,w}
                    edge_w = M.edges(w)[0] #get edge {w,x}
                    print edge_w
                    Forest[tree_num_of_v].add_edge(edge_w[0],edge_w[1])#add edge{w,x}
                    
                    Forest_nodes.append(edge_w[1]) ##add {x} to the list of forest nodes

                else: ## w is in Forest
                    print "w in Forest"
                    # if odd, do nothing.
                    if dist_to_root(w,root_of_w,Forest[tree_num_of_w])%2 == 0:
                        print "dist to root is even"
                        if (tree_num_of_v != tree_num_of_w):
                            ##Shortest path from root(v)--->v-->w---->root(w)
                            path_in_v = nx.shortest_path(Forest[tree_num_of_v], source = root_of_v, target = v)
                            path_in_w = nx.shortest_path(Forest[tree_num_of_w], source = w, target = root_of_w)
                            print "Path is:", path_in_w + path_in_v

                            return path_in_w + path_in_v
                        #w = e[0][1] # the other vertex of the unmarked edge
                        else: ##Contract the blossom
                            print "returning an empty list--------> @ Blossom right now"
                            print "BLOOOOOOOOOOSSSSSSSOOOOOOMMMMMMMMMM"
                            # create blossom
                            blossom = nx.shortest_path(tree_of_w, source=v, target=w)
                            blossom.append(v)
                            print "Blossom created: ", blossom

                            # contract blossom into single node w
                            contracted_G = G.copy()
                            contracted_M = M.copy()
                            w_old = w + 0
                            print "w is :", w
                            for node in blossom[0:len(blossom)-1]:
                                print "\t Blossom node: ", node
                                if node != w_old:
                                    contracted_G = nx.contracted_nodes(contracted_G, w, node, self_loops=False)
                                    print "here it is"
                                    if node in contracted_M.nodes(): 
                                       #contracted_M = nx.contracted_nodes(contracted_M, w, node, self_loops=False)
                                       print "is it here"
                                       edge_rm = M.edges(node)
                                       contracted_M.remove_node(node)
                                       contracted_M.remove_node(edge_rm[0][1])

                            print "M : ",M.nodes(),"\nContracted_M :",contracted_M.nodes()
                            ## Go through the edges in the blossom and contract the ones in the matching
                            #for i in xrange(len(blossom)-1):
                            #    node = blossom[i]
                            #    if M.has_edge(blossom[i],blossom[i+1]):
                            #        Contracted_M = nx.contracted_nodes(M)

                            print "out of the for LOOP"
                            # add blossom to our stack
                            Blossom_stack.append(w)
                            print "Blossom_stack after contraction: ", Blossom_stack

                            # recurse
                            aug_path = finding_aug_path(contracted_G, contracted_M, Blossom_stack)
                            print "Blossom_stack after recursion: ", Blossom_stack

                            # check if blossom exists in aug_path 
                            v_B = Blossom_stack.pop()
                            if (v_B in aug_path):
                                #blossom.append(w) ### - WHY ARE WE DOING THIS???? w is inside the blossom anyway??
                                print "Blossom_stack after pop: ", Blossom_stack
                                print "Blossom in aug path: ", blossom

                                # find base of blossom 
                                i = 0
                                base = None
                                base_idx = -1
                                blossom_ext = blossom + [blossom[1]] ##Needed at exactly one place
                                while base == None and i < len(blossom) - 1:
                                    if not(M.has_edge(blossom[i],blossom[i+1])):
                                        if not(M.has_edge(blossom[i+1],blossom_ext[i+2])): # <-- needed here
                                            base = blossom[i+1]
                                            base_idx = i
                                        else:
                                            i += 2
                                    else:
                                        i += 1

                                # create list of blossom nodes starting at base
                                based_blossom = [base]
                                ##base_idx = blossom.index(base) - computed in the For loop
                                for i in xrange(1,len(blossom)-base_idx):
                                    based_blossom.append(blossom[base_idx + i])
                                for i in xrange(1,base_idx):
                                    based_blossom.append(blossom[i])
                                    
                                print "Base: ", base
                                print "Blossom base-ified: ", based_blossom
                                print "original Blossom is:", blossom 

                                # lift - v_B is the BLossom node
                                L_stem = aug_path[0:aug_path.index(v_B)]
                                R_stem = aug_path[aug_path.index(v_B)+1:]
                                print "L_stem: ", L_stem
                                print "R_stem: ", R_stem
                                lifted_blossom = [] #stores the path within the blossom to take

                                ##NEED TO REWRITE THIS L_stem [-2] need not exist!!
                                if L_stem != []:
                                    if M.has_edge(base,L_stem[-1]): # Base connected to Left stem
                                        # find the first pt at which its connected to the right side
                                        # find where right stem attaches (or find that blossom is right endpt)

                                        ##check in one direction
                                        if R==[]:
                                            lifted_blossom = based_bloss[:3] # we just need the first two edges and we are done
                                        i = 0
                                        while (lifted_blossom == [] and i < len(based_blossom and R!=[])):
                                            if G.has_edge(based_blossom[i+2],R_stem[0]):
                                                lifted_blossom = based_blossom[:i+2]
                                                break #we found the place of connection
                                            i += 2
                                        #Check in the other direction
                                        i = len(blossom)-2
                                        while (lifted_blossom == [] and i > 0 and R!=[]):
                                            if G.has_edge(based_blossom[i],R_stem[0]):
                                                lifted_blossom = based_blossom[:i+2]
                                                break #we found the place of connection
                                            i -= 2


                                        print "L+lift+R; here's lift: ", lifted_blossom
                                        return L_stem + lifted_blossom + R_stem
                                    else: # Base connected to Right stem
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
        #unmarked_edges[edge_number] = []
    
    ##MArk vertex v
    ##unmarked_nodes[vertex_number] = [] ## DO I need to do this?? - Check with Amy

    ##IF Nothing is Found
    print "Path is:", Path
    return Path ##Empty Path

if __name__ == '__main__':
    G = generate_random_graph(10,0.5)
    M = nx.Graph()
    Blossom_stack = []
    MM = find_maximum_matching(G, M)
    print "Here it is M:" ,MM
    print "Here is the Graph:", G.edges()

                    
                            
        
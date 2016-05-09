import networkx as nx

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


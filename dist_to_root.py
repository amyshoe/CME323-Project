# -*- coding: utf-8 -*-
"""
Created on Mon May  9 11:03:08 2016

@author: sagarvare
"""

def dist_to_root(point,root,Graph):
    path = nx.shortest_path(Graph, source = point, target = root)
    return (len(path)-1)
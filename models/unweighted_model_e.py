import math
import random
import os
import sys

from models.model import Graph

class UnweightedGraphE(Graph):

    def init_specific(self, m, initialize = True):
        self.m = m
        self.adjacency_list = [set() for _ in range(self.n)]
        self.interesting_range_check()
        self.start_vertex = 0
        self.end_vertex = self.n - 1
        self.edges = ListDict()
        self.initialize = initialize

    def interesting_range_check(self, m_subtraction = 0, n_subtraction = 0):
        if self.m - m_subtraction < (self.n - n_subtraction) * math.log(self.n - n_subtraction):
            if m_subtraction == 0:
                print("The range of parameters is not interesting: Number of edges m is lower than n log n")
            return 1
        if self.m - m_subtraction > math.pow((self.n - n_subtraction), 3/2):
            if m_subtraction == 0:
                print("The range of parameters is not interesting: Number of edges m is higher than n^(3/2)")
            return 2
        return 0

    """
    Randomly creates m edges. Each edge appears with equal probability m/n.
    """
    def construct_random_graph(self):
        if not self.initialize:
            return
        for edge in range(self.m):
            non_edge_found = False
            while not non_edge_found:
                v = random.randint(0, self.n - 1)
                v2 = random.randint(0, self.n - 1)
                if v == v2 or v2 in self.adjacency_list[v]:
                    continue
                non_edge_found = True
                self.adjacency_list[v].add(v2)
                self.adjacency_list[v2].add(v)
                self.edges.add_item((min(v, v2), max(v, v2)))

    def probe(self, v):
        return self.adjacency_list[v]
    
    def change(self):
        possible_actions = ["swap-edge"]
        # edge removal is only allowed if the interesting range of parameters would be retained
        if self.interesting_range_check(m_subtraction = 1) == 0:
            possible_actions.append("remove-edge")

        action = possible_actions[random.randint(0, len(possible_actions) - 1)]
        if action == "swap-edge":
            self.change_swap_edge()
        elif action == "remove-edge":
            self.change_remove_edge()
    
    def change_swap_edge(self):
        removed_edge = self.edges.choose_random_item()
        v1 = removed_edge[0]
        v2 = removed_edge[1]
        if v1 not in self.adjacency_list[v2]:
            return RuntimeError
        self.edges.remove_item(removed_edge)
        
        v3 = v4 = -1
        nonedge_found = False
        while not nonedge_found:
            v3 = random.randint(0, self.n-1)
            v4 = random.randint(0, self.n-1)
            if v4 not in self.adjacency_list[v3] and v3 != v4:
                nonedge_found = True
        
        self.adjacency_list[v1].remove(v2)
        self.adjacency_list[v2].remove(v1)
        self.adjacency_list[v3].add(v4)
        self.adjacency_list[v4].add(v3)
        self.edges.add_item((min(v3, v4), max(v3, v4)))

    def change_remove_edge(self):
        removed_edge = self.edges.choose_random_item()
        v1 = removed_edge[0]
        v2 = removed_edge[1]
        if v1 not in self.adjacency_list[v2]:
            return RuntimeError
        self.m = self.m - 1
        self.edges.remove_item(removed_edge)
        self.adjacency_list[v1].remove(v2)
        self.adjacency_list[v2].remove(v1)

    def validate(self, path):
        """
        Checks whether the answer of path from path_v1 to path_v2 is valid in the current state of the graph.
        If path does not follow the right structure, returns -1
        If the answer is invalid, returns 1
        If the answer is valid, returns 0

        The answer is valid if one of the conditions holds:
            1) path = [], and start and end vertices are not connected
            2) path != [], and the path between start and end vertices is valid
        """
        if len(path) > 0:
            if path[0] != self.start_vertex:
                print("Algorithm error: Returned Path does not start with start_vertex!")
                return -1
            if path[len(path)-1] != self.end_vertex:
                print("Algorithm error: Returned Path does not end with end_vertex!")
                return -1
            path_vertices = set()
            for v in path:
                if v < 0 or v >= self.n:
                    print("Algorithm error: Vertex out of range!")
                    return -1
                if v in path_vertices:
                    print("Algorithm error: Vertex appears twice!")
                    return -1
                path_vertices.add(v)

        if len(path) == 0:     # Case 1: path = []
            visited = [0 for i in range(self.n)]
            visited[0] = 1
            new_vertices = [0]
            for v in new_vertices:
                for v2 in self.adjacency_list[v]:
                    if visited[v2] == 0:
                        visited[v2] = 1
                        new_vertices.append(v2)
                        if v2 == self.n - 1:
                            return 1
        else:    # Case 2: path != []
            for i in range(0, len(path)-1):
                if path[i+1] not in self.adjacency_list[path[i]]:
                    return 1
        return 0
    
    def import_edges(self, edges):
        for edge in edges:
            if edge[1] not in self.adjacency_list[edge[0]]:
                self.adjacency_list[edge[0]].add(edge[1])
            if edge[0] not in self.adjacency_list[edge[1]]:
                self.adjacency_list[edge[1]].add(edge[0])
            self.edges.add_item((min(edge[0], edge[1]), max(edge[0], edge[1])))

# Data structure that supports addition, removal, random selection in constant time
class ListDict(object):
    def __init__(self):
        self.item_to_position = {}
        self.items = []

    def add_item(self, item):
        if item in self.item_to_position:
            return
        self.items.append(item)
        self.item_to_position[item] = len(self.items) - 1

    def remove_item(self, item):
        position = self.item_to_position.pop(item)
        last_item = self.items.pop()
        if position != len(self.items):
            self.items[position] = last_item
            self.item_to_position[last_item] = position

    def choose_random_item(self):
        return random.choice(self.items)
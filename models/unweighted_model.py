import math
import random
import os
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

from model import Graph

class UnweightedGraph(Graph):

    def init_specific(self, m):
        self.m = m
        self.adjacency_list = [set() for _ in range(self.n)]
        self.interesting_range_check()
        self.start_vertex = 0
        self.end_vertex = self.n - 1

    def interesting_range_check(self):
        if self.m < self.n * math.log(self.n):
            print("The range of parameters is not interesting: Number of edges m is lower than n log n")
            return 1
        if self.m > math.pow(self.n, 3/2):
            print("The range of parameters is not interesting: Number of edges m is higher than n^(3/2)")
            return 2
        return 0

    """
    Randomly creates m edges. Each edge appears with equal probability m/n.
    """
    def construct_random_graph(self):
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

    def probe(self, v):
        return set(self.adjacency_list[v])
    
    def change(self):
        edge_found = False
        v1 = v2 = v3 = v4 = -1
        while not edge_found:
            v1 = random.randint(0, self.n-1)
            v2 = random.randint(0, self.n-1)
            if v2 in self.adjacency_list[v1]:
                edge_found = True
        
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
            if path[0] != self.start_vertex or path[len(path)-1] != self.end_vertex:
                return -1
            path_vertices = set()
            for v in path:
                if v < 0 or v >= self.n:
                    return -1
                if v in path_vertices:
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

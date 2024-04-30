import math
import random

from model import Graph

class UnweightedGraph(Graph):
    
    def init_specific(self, m):
        self.m = m
        self.adjacency_list = [dict() for v in range(self.n)]
        self.interesting_range_check()

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
                self.adjacency_list[v][v2] = 1
                self.adjacency_list[v2][v] = 1

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
        
        del self.adjacency_list[v1][v2]
        del self.adjacency_list[v2][v1]
        self.adjacency_list[v3][v4] = 1
        self.adjacency_list[v4][v3] = 1
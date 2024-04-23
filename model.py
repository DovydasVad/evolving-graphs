import math
import random

class Graph:
    n: int
    m: int
    weighted: bool

    def __init__(self, n, m, rand_seed, weighted = False):
        random.seed(rand_seed)
        self.n = n
        self.m = m
        self.weighted = weighted
        self.adjacency_list = [dict() for v in range(n)]
        self.edge_range_check()
        self.build_adjacency_list_ER()

    def edge_range_check(self):
        if self.m < self.n * math.log(self.n):
            print("The range of parameters is not interesting: Number of edges m is lower than n log n")
        if self.m > math.pow(self.n, 3/2):
            print("The range of parameters is not interesting: Number of edges m is higher than n^(3/2)")

    def build_adjacency_list_ER(self):
        for edge in range(m):
            non_edge_found = False
            while not non_edge_found:
                v = math.randint(0, n)
                v2 = math.randint(0, n)
                if v == v2 or v2 in adjacency_list[v]:
                    continue
                non_edge_found = True
                adjacency_list[v] = edge if self.weighted else 1
                        
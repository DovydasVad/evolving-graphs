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
        self.interesting_range_check()
        self.build_adjacency_list_ER()

    def interesting_range_check(self):
        if self.m < self.n * math.log(self.n):
            print("The range of parameters is not interesting: Number of edges m is lower than n log n")
            return 1
        if self.m > math.pow(self.n, 3/2):
            print("The range of parameters is not interesting: Number of edges m is higher than n^(3/2)")
            return 2
        return 0

    def build_adjacency_list_ER(self):
        for edge in range(self.m):
            non_edge_found = False
            while not non_edge_found:
                v = random.randint(0, self.n - 1)
                v2 = random.randint(0, self.n - 1)
                if v == v2 or v2 in self.adjacency_list[v]:
                    continue
                non_edge_found = True
                self.adjacency_list[v][v2] = edge if self.weighted else 1
                self.adjacency_list[v2][v] = edge if self.weighted else 1           
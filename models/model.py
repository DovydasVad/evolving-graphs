import math
import random

class Graph:
    n: int
    m: int

    def __init__(self, rand_seed, n, *args):
        random.seed(rand_seed)
        self.n = n
        self.init_specific(*args)
        self.construct_random_graph()

    def init_specific(self):
        pass
    
    def construct_random_graph(self):
        pass

    def probe(self):
        pass

    def change(self):
        pass

    def validate(self):
        pass



class GraphOld:
    n: int
    m: int
    weighted: bool

    def __init__(self, n, m, rand_seed, weighted = False):
        random.seed(rand_seed)
        self.n = n
        self.m = m
        self.weighted = weighted
        self.adjacency_list = [dict() for v in range(n)]
        self.weights_to_edges = [(-1, -1)]
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

    """
    Randomly creates m edges. Each edge appears with equal probability m/n.
    """
    def build_adjacency_list_ER(self):
        for edge in range(self.m):
            non_edge_found = False
            while not non_edge_found:
                v = random.randint(0, self.n - 1)
                v2 = random.randint(0, self.n - 1)
                if v == v2 or v2 in self.adjacency_list[v]:
                    continue
                non_edge_found = True
                self.adjacency_list[v][v2] = edge + 1 if self.weighted else 1
                self.adjacency_list[v2][v] = edge + 1 if self.weighted else 1
                if self.weighted:
                    self.weights_to_edges.append((v, v2))

    def probe(self, *args):
        return self.probe_unweighted(*args) if not self.weighted else self.probe_weighted(*args)

    """Returns set of neighbors of v"""
    def probe_unweighted(self, v):
        return set(self.adjacency_list[v])
    
    """
    Compares weights of edges (a1,b1) and (a2,b2):
       - If w(a1,b1) < w(a2,b2), returns 1
       - If w(a1,b1) > w(a2,b2), returns 0
       - If w(a1,b1) = w(a2,b2), returns -1
       - If (a1,b1) or (a2,b2) does not exist, returns -2
    """
    def probe_weighted(self, a1, b1, a2, b2):
        if b1 not in self.adjacency_list[a1] or b2 not in self.adjacency_list[a2]:
            return -2
        if self.adjacency_list[a1][b1] == self.adjacency_list[a2][b2]:
            return -1
        return self.adjacency_list[a1][b1] < self.adjacency_list[a2][b2]
    
    def change(self):
        if not self.weighted:
            self.change_unweighted()
        else:
            self.change_weighted()

    def change_unweighted(self):
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

    def change_weighted(self):
        w_lower = random.randint(1, self.m - 1)
        w_higher = w_lower + 1
        e_lower = self.weights_to_edges[w_lower]
        e_higher = self.weights_to_edges[w_higher]
        self.adjacency_list[e_lower[0]][e_lower[1]] = w_higher
        self.adjacency_list[e_lower[1]][e_lower[0]] = w_higher
        self.adjacency_list[e_higher[0]][e_higher[1]] = w_lower
        self.adjacency_list[e_higher[1]][e_higher[0]] = w_lower
        self.weights_to_edges[w_higher] = e_lower
        self.weights_to_edges[w_lower] = e_higher
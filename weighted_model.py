import random

from model import Graph

class WeightedGraph(Graph):

    def init_specific(self):
        self.m = int(self.n*(self.n-1)/2)
        self.weights_to_edges = [(-1, -1) for _ in range(self.m + 1)]

    def construct_random_graph(self):
        self.adjacency_matrix = [[0 for _ in range(self.n)] for _ in range(self.n)]
        edge_weights = [int(i) for i in range(1, self.m + 1)]
        random.shuffle(edge_weights)
        edge_count = 0
        for v1 in range(self.n):
            for v2 in range(self.n):
                if v1 >= v2:
                    continue
                w = edge_weights[edge_count]
                self.adjacency_matrix[v1][v2] = w
                self.adjacency_matrix[v2][v1] = w
                self.weights_to_edges[w] = (v1, v2)
                edge_count += 1

    def probe(self, a1, b1, a2, b2): 
        """ Compares weights of edges (a1,b1) and (a2,b2):
        - If w(a1,b1) < w(a2,b2),  returns 1
        - If w(a1,b1) > w(a2,b2),  returns 0
        - If w(a1,b1) = w(a2,b2),  returns -1
        - If a1 == b1 or a2 == b2, returns -2
        """
        if a1 == b1 or a2 == b2:
            return -2
        if self.adjacency_matrix[a1][b1] == self.adjacency_matrix[a2][b2]:
            return -1
        return self.adjacency_matrix[a1][b1] < self.adjacency_matrix[a2][b2]
    
    def change(self):
        w_lower = random.randint(1, self.m - 1)
        w_higher = w_lower + 1
        e_lower = self.weights_to_edges[w_lower]
        e_higher = self.weights_to_edges[w_higher]
        self.adjacency_matrix[e_lower[0]][e_lower[1]] = w_higher
        self.adjacency_matrix[e_lower[1]][e_lower[0]] = w_higher
        self.adjacency_matrix[e_higher[0]][e_higher[1]] = w_lower
        self.adjacency_matrix[e_higher[1]][e_higher[0]] = w_lower
        self.weights_to_edges[w_higher] = e_lower
        self.weights_to_edges[w_lower] = e_higher
     
    def validate(self):
        return NotImplementedError
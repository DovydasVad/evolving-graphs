import random

from models.model import Graph

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
     
    def get_MST(self):
        component_leader = [i for i in range(self.n)]
        component_size = [1 for _ in range(self.n)]

        def get_component_leader(a):
            if component_leader[a] == a:
                return a
            component_leader[a] = get_component_leader(component_leader[a])
            return component_leader[a]

        def is_in_same_component(a, b):
            return get_component_leader(a) == get_component_leader(b)

        def merge_components(a, b):
            a = get_component_leader(a)
            b = get_component_leader(b)
            if component_size[b] > component_size[a]:
                a, b = b, a
            component_leader[b] = a

        edges_remaining = self.n - 1
        mst_weight = 0
        for w in range(1, self.m + 1):
            edge = self.weights_to_edges[w]
            if not is_in_same_component(edge[0], edge[1]):
                mst_weight += w
                edges_remaining -= 1
                merge_components(edge[0], edge[1])
                if edges_remaining == 0:
                    break
        return mst_weight

    def validate(self, edges):
        """
        Checks whether the answer of MST is a tree, and returns value of the ordinal measure D that compares the given solution against the optimal solution.
        If the edge list does not form a tree, returns -1
        Otherwise, returns the ordinal measure D = sum(I_optimal - I_solution)
            D = 0 means the solution is optimal (= MST)
        """
        if len(edges) != self.n - 1:
            return -1
        # check that all vertices are reachable from vertex 0 (condition for a tree)
        adjacency_list = [dict() for v in range(self.n)]
        tree_weight = 0
        for edge in edges:
            if edge[0] < 0 or edge[0] >= self.n:
                return -1
            if edge[1] < 0 or edge[1] >= self.n:
                return -1
            adjacency_list[edge[0]][edge[1]] = 1
            adjacency_list[edge[1]][edge[0]] = 1
            tree_weight += self.adjacency_matrix[edge[0]][edge[1]]
        visited = [0 for i in range(self.n)]
        visited[0] = 1
        new_vertices = [0]
        for v in new_vertices:
            for v2 in adjacency_list[v]:
                if visited[v2] == 0:
                    visited[v2] = 1
                    new_vertices.append(v2)
        if len(new_vertices) != self.n:
            return -1
        return tree_weight - self.get_MST()
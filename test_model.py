import copy
import unittest

from unweighted_model import UnweightedGraph
from weighted_model import WeightedGraph

class TestGeneration(unittest.TestCase):
    def test_interesting_range_check_unweighted(self):
        """
        Test interesting range of parameters check
        """
        n = 150
        graph = UnweightedGraph(0, n, 751)
        self.assertEqual(graph.interesting_range_check(), 1)
        graph = UnweightedGraph(0, n, 752)
        self.assertEqual(graph.interesting_range_check(), 0)
        graph = UnweightedGraph(0, n, 1837)
        self.assertEqual(graph.interesting_range_check(), 0)
        graph = UnweightedGraph(0, n, 1838)
        self.assertEqual(graph.interesting_range_check(), 2)

    def test_graph_generation_constraints_unweighted_ER(self):
        """
        Test ER unweighted graph generation:
        1) Range of vertex values in adjacency_list dictionary is [0, n)
        2) m edges are generated, with weight 1
        """
        n = 150
        m = 1507
        graph = UnweightedGraph(0, n, m)
        self.assertEqual(len(graph.adjacency_list), n)
        edge_count = 0
        for v in range(n):
            edge_count += len(graph.adjacency_list[v])
            vertices = set()
            for v2 in graph.adjacency_list[v].keys():
                self.assertLess(-1, v2)
                self.assertLess(v2, n)
                self.assertFalse(v2 in vertices)
                self.assertEqual(graph.adjacency_list[v][v2], 1)
                vertices.add(v2)
        self.assertEqual(edge_count / 2, m)

    def test_graph_generation_constraints_weighted_ER(self):
        """
        Test ER weighted graph generation:
        1) Adjacency matrix is of size n x n
        2) m = n*(n-1)/2 edges are generated, with unique weights in [1, m]
        """
        n = 89
        graph = WeightedGraph(0, n)
        self.assertEqual(len(graph.adjacency_matrix), n)
        edge_weights_half_1 = set()
        edge_weights_half_2 = set()
        for v in range(n):
            self.assertEqual(len(graph.adjacency_matrix[v]), n)
            for v2 in range(n):
                if v == v2:
                    self.assertEqual(graph.adjacency_matrix[v][v2], 0)
                else:
                    w = graph.adjacency_matrix[v][v2]
                    self.assertLess(0, w)
                    self.assertLess(w, graph.m + 1)
                    if v < v2:
                        self.assertFalse(w in edge_weights_half_1)
                        edge_weights_half_1.add(w)
                    if v > v2:
                        self.assertFalse(w in edge_weights_half_2)
                        edge_weights_half_2.add(w)


class TestProbe(unittest.TestCase):
    def test_probe_unweighted_1(self):
        """
        Tests probing of a small fixed unweighted graph. Each probe should return list of neighbors of v.
        """
        adjacency_list = [{1: 1, 5: 1, 6: 1},
                          {0: 1, 2: 1, 5: 1, 6: 1},
                          {1: 1, 5: 1},
                          {6: 1},
                          {},
                          {0: 1, 1: 1, 2: 1},
                          {0: 1, 1: 1, 3: 6}]
        n = len(adjacency_list)
        graph = UnweightedGraph(0, n, 8)
        graph.adjacency_list = adjacency_list
        for v in range(n):
            self.assertSetEqual(set(adjacency_list[v].keys()), graph.probe(v))
    
    def test_probe_unweighted_2(self):
        """
        Tests probing of a random unweighted graph. Each probe should return list of neighbors of v.
        """
        n = 303
        m = 3007
        graph = UnweightedGraph(0, n, m)
        for v in range(n):
            neighbors_v = set(graph.adjacency_list[v].keys())
            self.assertSetEqual(neighbors_v, graph.probe(v))

    def test_probe_weighted(self):
        """
        Tests probing of a small fixed unweighted graph. Each probe should return return True if w1 < w2, and False otherwise.
        """
        adjacency_matrix = [[0, 7, 5, 1, 8],
                            [7, 0, 4, 2, 6],
                            [5, 4, 0, 10,3],
                            [1, 2, 10,0, 9],
                            [8, 6, 3, 9, 0]]
        n = len(adjacency_matrix)
        graph = WeightedGraph(0, n)
        graph.adjacency_matrix = adjacency_matrix
        for v1 in range(n):
            for v2 in range(n):
                for v3 in range(n):
                    for v4 in range(n):
                        if adjacency_matrix[v1][v2] == 0:
                            self.assertEqual(graph.probe(v1, v2, v3, v4), -2)
                        elif adjacency_matrix[v3][v4] == 0:
                            self.assertEqual(graph.probe(v1, v2, v3, v4), -2)
                        elif adjacency_matrix[v1][v2] == adjacency_matrix[v3][v4]:
                            self.assertEqual(graph.probe(v1, v2, v3, v4), -1)
                        else:
                            if adjacency_matrix[v1][v2] < adjacency_matrix[v3][v4]:
                                self.assertEqual(graph.probe(v1, v2, v3, v4), 1)
                            else:
                                self.assertEqual(graph.probe(v1, v2, v3, v4), 0)
    

def num_changes(adj_list1, adj_list2):
    n = len(adj_list1)
    changes = 0
    for v in range(n):
        for v2 in adj_list1[v].keys():
            if v2 not in adj_list2[v]:
                changes += 1
    for v in range(n):
        for v2 in adj_list2[v].keys():
            if v2 not in adj_list1[v]:
                changes += 1
    return changes / 2

def num_swaps(adj_matrix1, adj_matrix2):
    n = len(adj_matrix1)
    swaps = 0
    for v1 in range(n):
        for v2 in range(n):
            for v3 in range(n):
                for v4 in range(n):
                    if (v1 == v2) or (v3 == v4):
                        continue
                    if (v1 == v3 and v2 == v4) or (v1 == v4 and v2 == v3):
                        continue
                    if adj_matrix1[v1][v2] < adj_matrix1[v3][v4] and adj_matrix2[v1][v2] > adj_matrix2[v3][v4]:
                        swaps += 1
                    if adj_matrix1[v1][v2] > adj_matrix1[v3][v4] and adj_matrix2[v1][v2] < adj_matrix2[v3][v4]:
                        swaps += 1
    # There are 8 ways to have (a1,b1) (a2,b2) (swap vertices in edges, swap edge order)
    return swaps / 8

class TestChange(unittest.TestCase):
    def test_change_unweighted_1(self):
        """
        Tests change of unweighted graph.
        After each change, only a single edge should be moved to a place of previous non-edge.
        """
        n = 83
        m = 507
        iterations = 500
        graph = UnweightedGraph(0, n, m)
        for i in range(iterations):
            old_adj_list = copy.deepcopy(graph.adjacency_list)
            graph.change()
            self.assertEqual(num_changes(old_adj_list, graph.adjacency_list), 2)

    def test_change_unweighted_2(self):
        """
        Tests change of unweighted graph.
        Eventually, every initial edge should become nonedge, and vice-versa.
        """
        adjacency_list = [{1: 1, 5: 1, 6: 1},
                          {0: 1, 2: 1, 5: 1, 6: 1},
                          {1: 1, 5: 1},
                          {6: 1},
                          {},
                          {0: 1, 1: 1, 2: 1},
                          {0: 1, 1: 1, 3: 1}]
        initial_adjacency_matrix = [[0,1,0,0,0,1,1],
                                    [1,0,1,0,0,1,1],
                                    [0,1,0,0,0,1,0],
                                    [0,0,0,0,0,0,1],
                                    [0,0,0,0,0,0,0],
                                    [1,1,1,0,0,0,0],
                                    [1,1,0,1,0,0,0]]
        n = len(adjacency_list)
        for v in range(n):
            for v2 in range(n):
                if initial_adjacency_matrix[v][v2] >= 1:
                    self.assertTrue(v in adjacency_list[v2])
                    self.assertTrue(v2 in adjacency_list[v])
        graph = UnweightedGraph(0, n, 8)
        graph.adjacency_list = adjacency_list
        iterations = 100000
        changes_left = n*n - n
        for i in range(iterations):
            graph.change()
            for v in range(n):
                for v2 in range(n):
                    if v == v2:
                        continue
                    if initial_adjacency_matrix[v][v2] == 0 and v2 in graph.adjacency_list[v]:
                        changes_left -= 1
                        initial_adjacency_matrix[v][v2] = -1
                    if initial_adjacency_matrix[v][v2] == 1 and v2 not in graph.adjacency_list[v]:
                        changes_left -= 1
                        initial_adjacency_matrix[v][v2] = -1
            if changes_left == 0:
                break
        self.assertEqual(changes_left, 0)

    def test_change_weighted_1(self):
        """
        Tests change of weighted graph.
        After each change, only weights of a single pair of consecutive edges should be swapped.
        """
        n = 16
        iterations = 100
        graph = WeightedGraph(0, n)
        for i in range(iterations):
            old_adj_list = copy.deepcopy(graph.adjacency_matrix)
            graph.change()
            self.assertEqual(num_swaps(old_adj_list, graph.adjacency_matrix), 1)
        
    def test_change_weighted_2(self):
        """
        Tests change of weighted graph.
        Eventually, the weight of each edge should change.
        """
        initial_adjacency_matrix = [[0, 7, 5, 1, 8],
                                    [7, 0, 4, 2, 6],
                                    [5, 4, 0, 10,3],
                                    [1, 2, 10,0, 9],
                                    [8, 6, 3, 9, 0]]
        n = len(initial_adjacency_matrix)
        graph = WeightedGraph(0, n)
        graph.adjacency_matrix = copy.deepcopy(initial_adjacency_matrix)
        for v in range(n):
            for v2 in range(v):
                w = initial_adjacency_matrix[v][v2]
                graph.weights_to_edges[w] = (v2, v)
        max_iterations = 10000
        changes_left = 2 * graph.m
        for i in range(max_iterations):
            graph.change()
            for v in range(n):
                for v2 in range(n):
                    if v == v2:
                        continue
                    if initial_adjacency_matrix[v][v2] != -1 and initial_adjacency_matrix[v][v2] != graph.adjacency_matrix[v][v2]:
                        changes_left -= 1
                        initial_adjacency_matrix[v][v2] = -1
            if changes_left == 0:
                break
        self.assertEqual(changes_left, 0)

class TestValidate(unittest.TestCase):
    def test_validate_unweighted_wrong_structure(self):
        """
        Checks whether path validation function discards paths with the wrong structure.
        """
        adjacency_list = [{1: 1, 5: 1, 6: 1},
                        {0: 1, 2: 1, 5: 1, 6: 1},
                        {1: 1, 5: 1},
                        {6: 1},
                        {},
                        {0: 1, 1: 1, 2: 1},
                        {0: 1, 1: 1, 3: 1}]
        n = len(adjacency_list)
        m = 8
        graph = UnweightedGraph(0, n, m)
        graph.adjacency_list = adjacency_list
        self.assertEqual(graph.validate([1, 6]), -1)  # first vertex should be 0
        self.assertEqual(graph.validate([0, 5]), -1)  # last vertex should be n
        self.assertEqual(graph.validate([0, 1, 1, 6]), -1)  # no repeated vertices are allowed
        self.assertEqual(graph.validate([0, -1, 6]), -1)  # no negative vertice values
        self.assertEqual(graph.validate([0, 7, 6]), -1)  # no vertice values >= n
        self.assertEqual(graph.validate([5, 0, 6]), -1)
        self.assertEqual(graph.validate([0, 6, 3]), -1)
        self.assertEqual(graph.validate([6, 0]), -1)
        self.assertEqual(graph.validate([0, 6, 0, 6]), -1)

    
    def test_validate_unweighted_invalid_existing_path(self):
        """
        Checks whether path validation function correctly classifies given paths as incorrect.
        """
        adjacency_list = [{1: 1, 5: 1, 6: 1},
                        {0: 1, 2: 1, 5: 1, 6: 1},
                        {1: 1, 5: 1},
                        {6: 1},
                        {},
                        {0: 1, 1: 1, 2: 1},
                        {0: 1, 1: 1, 3: 1}]
        n = len(adjacency_list)
        m = 8
        graph = UnweightedGraph(0, n, m)
        graph.adjacency_list = adjacency_list
        self.assertEqual(graph.validate([0, 5, 2, 6]), 0)
        self.assertEqual(graph.validate([0, 1, 3, 6]), 0)
        self.assertEqual(graph.validate([0, 5, 2, 3, 6]), 0)
        self.assertEqual(graph.validate([0, 4, 6]), 0)

    
    def test_validate_unweighted_invalid_empty_path(self):
        """
        Checks whether path validation function does not accept an empty list when there is a path between start and end vertices.
        """
        adjacency_list = [{1: 1, 5: 1, 6: 1},
                        {0: 1, 2: 1, 5: 1, 6: 1},
                        {1: 1, 5: 1},
                        {6: 1},
                        {},
                        {0: 1, 1: 1, 2: 1},
                        {0: 1, 1: 1, 3: 1}]
        n = len(adjacency_list)
        m = 8
        graph = UnweightedGraph(0, n, m)
        graph.adjacency_list = adjacency_list
        self.assertEqual(graph.validate([]), 0)


    def test_validate_unweighted_valid_existing_path(self):
        """
        Checks whether path validation function correctly validates an existing path between start and end vertex.
        """
        adjacency_list = [{1: 1, 5: 1, 6: 1},
                        {0: 1, 2: 1, 5: 1, 6: 1},
                        {1: 1, 5: 1},
                        {6: 1},
                        {},
                        {0: 1, 1: 1, 2: 1},
                        {0: 1, 1: 1, 3: 1}]
        n = len(adjacency_list)
        m = 8
        graph = UnweightedGraph(0, n, m)
        graph.adjacency_list = adjacency_list
        self.assertEqual(graph.validate([0, 6]), 1)
        self.assertEqual(graph.validate([0, 1, 6]), 1)
        self.assertEqual(graph.validate([0, 5, 1, 6]), 1)
        self.assertEqual(graph.validate([0, 5, 2, 1, 6]), 1)
    
    def test_validate_unweighted_valid_empty_path(self):
        """
        Checks whether path validation function accepts an empty list when there is no path between start and end vertex.
        """
        adjacency_list = [{1: 1, 5: 1},
                        {0: 1, 5: 1},
                        {6: 1},
                        {5: 1},
                        {},
                        {0: 1, 1: 1, 3: 1},
                        {2: 1}]
        n = len(adjacency_list)
        m = 5
        graph = UnweightedGraph(0, n, m)
        graph.adjacency_list = adjacency_list
        self.assertEqual(graph.validate([]), 1)
        adjacency_list = [{1: 1, 3: 1, 5: 1},
                        {0: 1, 3: 1, 5: 1},
                        {6: 1, 4: 1},
                        {0: 1, 3: 1, 5: 1},
                        {2: 1, 6: 1},
                        {0: 1, 1: 1, 3: 1},
                        {2: 1, 4: 1}]
        n = len(adjacency_list)
        m = 9
        graph = UnweightedGraph(0, n, m)
        graph.adjacency_list = adjacency_list
        self.assertEqual(graph.validate([]), 1)

if __name__ == '__main__':
    unittest.main()
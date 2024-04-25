import copy
import unittest

from model import Graph

class TestGeneration(unittest.TestCase):
    def test_interesting_range_check(self):
        """
        Test interesting range of parameters check
        """
        n = 150
        graph = Graph(n, 751, 0, False)
        self.assertEqual(graph.interesting_range_check(), 1)
        graph = Graph(n, 752, 0, False)
        self.assertEqual(graph.interesting_range_check(), 0)
        graph = Graph(n, 1837, 0, False)
        self.assertEqual(graph.interesting_range_check(), 0)
        graph = Graph(n, 1838, 0, False)
        self.assertEqual(graph.interesting_range_check(), 2)

    def test_graph_generation_constraints_unweighted_ER(self):
        """
        Test ER unweighted graph generation:
        1) Range of vertex values in adjacency_list dictionary is [0, n)
        2) m edges are generated, with weight 1
        """
        n = 150
        m = 1007
        graph = Graph(n, m, 0, False)
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
        1) Range of vertex values in adjacency_list dictionary is [0, n)
        2) m edges are generated, with unique weights in (1, m]
        """
        n = 150
        m = 1007
        graph = Graph(n, m, 0, True)
        self.assertEqual(len(graph.adjacency_list), n)
        edge_count = 0
        for v in range(n):
            edge_count += len(graph.adjacency_list[v])
            vertices = set()
            for v2 in graph.adjacency_list[v].keys():
                self.assertNotEqual(v, v2)
                self.assertLess(-1, v2)
                self.assertLess(v2, n)
                self.assertFalse(v2 in vertices)
        self.assertEqual(edge_count / 2, m)

        edge_weights = set()
        for v in range(n):
            for v2 in graph.adjacency_list[v].keys():
                if v > v2:
                    continue
                w = graph.adjacency_list[v][v2]
                self.assertFalse(w in edge_weights)
                self.assertLess(0, w)
                self.assertLess(w, m + 1)
                edge_weights.add(w)
        
        for edge_index in range(1, len(graph.weights_to_edges)):
            v1 = graph.weights_to_edges[edge_index][0]
            v2 = graph.weights_to_edges[edge_index][1]
            self.assertTrue(v2 in graph.adjacency_list[v1])
            self.assertEqual(graph.adjacency_list[v1][v2], edge_index)


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
        graph = Graph(n, 8, 0, False)
        graph.adjacency_list = adjacency_list
        for v in range(n):
            self.assertSetEqual(set(adjacency_list[v].keys()), graph.probe(v))
    
    def test_probe_unweighted_2(self):
        """
        Tests probing of a random unweighted graph. Each probe should return list of neighbors of v.
        """
        n = 303
        m = 2007
        graph = Graph(n, m, 0, False)
        for v in range(n):
            neighbors_v = set(graph.adjacency_list[v].keys())
            self.assertSetEqual(neighbors_v, graph.probe(v))

    def test_probe_weighted(self):
        """
        Tests probing of a small fixed unweighted graph. Each probe should return return True if w1 < w2, and False otherwise.
        """
        adjacency_list = [{1: 8, 5: 4, 6: 1},
                          {0: 8, 2: 2, 5: 7, 6: 6},
                          {1: 2, 5: 3},
                          {6: 5},
                          {},
                          {0: 4, 1: 7, 2: 3},
                          {0: 1, 1: 6, 3: 5}]
        adjacency_matrix = [[0,8,0,0,0,4,1],
                            [8,0,2,0,0,7,6],
                            [0,2,0,0,0,3,0],
                            [0,0,0,0,0,0,5],
                            [0,0,0,0,0,0,0],
                            [4,7,3,0,0,0,0],
                            [1,6,0,5,0,0,0]]
        n = len(adjacency_list)
        graph = Graph(n, 8, 0, True)
        graph.adjacency_list = adjacency_list
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

def num_swaps(adj_list1, adj_list2):
    n = len(adj_list1)
    swaps = 0
    for v1 in range(n):
        for v2 in adj_list1[v1].keys():
            for v3 in range(n):
                for v4 in adj_list1[v3].keys():
                    if (v1 == v3 and v2 == v4) or (v1 == v4 and v2 == v3):
                        continue
                    if adj_list1[v1][v2] < adj_list1[v3][v4] and adj_list2[v1][v2] > adj_list2[v3][v4]:
                        swaps += 1
                    if adj_list1[v1][v2] > adj_list1[v3][v4] and adj_list2[v1][v2] < adj_list2[v3][v4]:
                        swaps += 1
    # There are 8 ways to have (a1,b1) (a2,b2) (swap vertices in edges, swap edge order)
    return swaps / 8

class TestChange(unittest.TestCase):
    def test_change_unweighted_1(self):
        """
        Tests change of unweighted graph.
        After each change, only a single edge should be moved to a place of previous non-edge.
        """
        n = 303
        m = 2007
        iterations = 1000
        graph = Graph(n, m, 0, False)
        for i in range(iterations):
            old_adj_list = copy.deepcopy(graph.adjacency_list)
            graph.change()
            self.assertEqual(num_changes(old_adj_list, graph.adjacency_list), 2)

    def test_change_unweighted_2(self):
        """
        Tests change of unweighted graph.
        Eventually, every initial edge should become nonedge, and vice-versa.
        """
        adjacency_list = [{1: 8, 5: 4, 6: 1},
                          {0: 8, 2: 2, 5: 7, 6: 6},
                          {1: 2, 5: 3},
                          {6: 5},
                          {},
                          {0: 4, 1: 7, 2: 3},
                          {0: 1, 1: 6, 3: 5}]
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
        graph = Graph(n, 8, 0, False)
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
        self.assertEqual(changes_left, 0)

    def test_change_weighted_1(self):
        """
        Tests change of weighted graph.
        After each change, only weights of a single pair of consecutive edges should be swapped.
        """
        n = 30
        m = 207
        iterations = 100
        graph = Graph(n, m, 0, True)
        for i in range(iterations):
            old_adj_list = copy.deepcopy(graph.adjacency_list)
            graph.change()
            self.assertEqual(num_swaps(old_adj_list, graph.adjacency_list), 1)
        
    def test_change_weighted_2(self):
        """
        Tests change of weighted graph.
        Eventually, the weight of each edge should change.
        """
        adjacency_list = [{1: 8, 5: 4, 6: 1},
                          {0: 8, 2: 2, 5: 7, 6: 6},
                          {1: 2, 5: 3},
                          {6: 5},
                          {},
                          {0: 4, 1: 7, 2: 3},
                          {0: 1, 1: 6, 3: 5}]
        initial_adjacency_matrix = [[0,8,0,0,0,4,1],
                                    [8,0,2,0,0,7,6],
                                    [0,2,0,0,0,3,0],
                                    [0,0,0,0,0,0,5],
                                    [0,0,0,0,0,0,0],
                                    [4,7,3,0,0,0,0],
                                    [1,6,0,5,0,0,0]]
        n = len(adjacency_list)
        m = 8
        for v in range(n):
            for v2 in range(n):
                if initial_adjacency_matrix[v][v2] >= 1:
                    self.assertTrue(v in adjacency_list[v2])
                    self.assertTrue(v2 in adjacency_list[v])
        graph = Graph(n, m, 0, True)
        graph.adjacency_list = adjacency_list
        max_iterations = 100000
        changes_left = 2 * m
        for i in range(max_iterations):
            graph.change()
            for v in range(n):
                for v2 in range(n):
                    if v == v2 or v2 not in graph.adjacency_list[v]:
                        continue
                    if initial_adjacency_matrix[v][v2] != -1 and initial_adjacency_matrix[v][v2] != graph.adjacency_list[v][v2]:
                        changes_left -= 1
                        initial_adjacency_matrix[v][v2] = -1
        self.assertEqual(changes_left, 0)

if __name__ == '__main__':
    unittest.main()
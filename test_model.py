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
        2) m edges are generated, with unique weights in [0, m)
        """
        n = 150
        m = 1007
        graph = Graph(n, m, 0, True)
        self.assertEqual(len(graph.adjacency_list), n)
        edge_count = 0
        edge_weights = set()
        for v in range(n):
            edge_count += len(graph.adjacency_list[v])
            vertices = set()
            for v2 in graph.adjacency_list[v].keys():
                self.assertNotEqual(v, v2)
                self.assertLess(-1, v2)
                self.assertLess(v2, n)
                self.assertFalse(v2 in vertices)
        self.assertEqual(edge_count / 2, m)

        for v in range(n):
            edge_count += len(graph.adjacency_list[v])
            vertices = set()
            for v2 in graph.adjacency_list[v].keys():
                if v > v2:
                    continue
                w = graph.adjacency_list[v][v2]
                self.assertFalse(w in edge_weights)
                self.assertLess(-1, w)
                self.assertLess(w, m)
                edge_weights.add(w)

if __name__ == '__main__':
    unittest.main()
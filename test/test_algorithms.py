import unittest
import sys

sys.path.append("..")

from algorithms.one_path import AlgorithmOnePath
from models.unweighted_model import UnweightedGraph

def edges_to_adj_list(edges, n):
    adjacency_list = [set() for _ in range(n)]
    for edge in edges:
        adjacency_list[edge[0]].add(edge[1])
        adjacency_list[edge[1]].add(edge[0])
    return adjacency_list

def perform_probe(algorithm: AlgorithmOnePath, graph: UnweightedGraph):
    algorithm.set_probe_result(graph.probe(algorithm.get_probe_input()))

class OnePath(unittest.TestCase):
    def test_one_path_1(self):
        """
        Solution path has always 4 edges.
        Solution should be always correct after 2R = 8 probes.
        """
        n = 10
        R = 4
        edges = [(0, 1), (0, 3), (1, 3), (0, 4), (2, 4), (2, 6), (6, 5), (6, 8), (5, 8), (7, 8)]
        graph = UnweightedGraph(0, n, len(edges))
        graph.adjacency_list = edges_to_adj_list(edges, n)
        algorithm = AlgorithmOnePath(1, n)
        algorithm.R = R
        probes_left = set()
        probes_right = set()
        for i in range(R):
            v = algorithm.get_probe_input()
            probes_left.add(v)
            algorithm.set_probe_result(graph.probe(v))
            self.assertListEqual(algorithm.answer(), [])
        self.assertSetEqual(probes_left, set([0, 1, 3, 4]))
        for i in range(R):
            v = algorithm.get_probe_input()
            probes_right.add(v)
            if i < R - 1:
                answer = algorithm.answer()
                self.assertListEqual(answer, [])
                self.assertTrue(graph.validate(answer) == 1)
            else:
                answer = algorithm.answer()
                self.assertTrue(len(answer) == 4)
                self.assertTrue(graph.validate(algorithm.answer()) == 0)
        self.assertSetEqual(probes_right, set([5, 6, 7, 8]))
        for i in range(100):
            perform_probe(algorithm, graph)
            answer = algorithm.answer()
            self.assertTrue(len(answer) == 4)
            self.assertTrue(graph.validate(algorithm.answer()) == 0)

    def test_one_path_2(self):
        """
        Unconnected graph, algorithm outputs empty path as the solution, until the edge connecting the graph is added.
        """
        n = 10
        R = 15
        edges = [(0, 1), (0, 3), (1, 3), (0, 4), (2, 4), (6, 5), (6, 8), (5, 8), (7, 8)]
        graph = UnweightedGraph(0, n, len(edges))
        graph.adjacency_list = edges_to_adj_list(edges, n)
        algorithm = AlgorithmOnePath(1, n)
        algorithm.R = R
        probes_left = set()
        probes_right = set()
        for i in range(100):
            v = algorithm.get_probe_input()
            probes_left.add(v)
            algorithm.set_probe_result(graph.probe(v))
            answer = algorithm.answer()
            self.assertListEqual(answer, [])
            self.assertTrue(graph.validate(answer) == 1)
        self.assertSetEqual(probes_left, set([0, 1, 3, 4]))
        graph.adjacency_list[6].add(2)
        graph.adjacency_list[2].add(6)
        for i in range(2*R):
            perform_probe(algorithm, graph)
        for i in range(100):
            perform_probe(algorithm, graph)
            answer = algorithm.answer()
            self.assertTrue(len(answer) == 4)
            self.assertTrue(graph.validate(algorithm.answer()) == 0)


    def test_one_path_3(self):
        """
        Connected graph (line), but R is too small to find a solution.
        """
        n = 6
        R = 2
        edges = [(0, 2), (2, 1), (1, 3), (3, 4), (4, 5)]
        graph = UnweightedGraph(0, n, len(edges))
        graph.adjacency_list = edges_to_adj_list(edges, n)
        algorithm = AlgorithmOnePath(1, n)
        algorithm.R = R
        probes_left = set()
        probes_right = set()
        for i in range(100):
            v = algorithm.get_probe_input()
            if i % 4 == 0 or i % 4 == 1:
                probes_left.add(v)
            else:
                probes_right.add(v)
            algorithm.set_probe_result(graph.probe(v))
            self.assertListEqual(algorithm.answer(), [])
        self.assertSetEqual(probes_left, set([0, 1]))
        self.assertSetEqual(probes_right, set([5, 4]))
    
    def test_one_path_4(self):
        """
        Connected graph (line), and solution exists.
        """
        n = 6
        R = 3
        edges = [(0, 2), (2, 1), (1, 3), (3, 4), (4, 5)]
        graph = UnweightedGraph(0, n, len(edges))
        graph.adjacency_list = edges_to_adj_list(edges, n)
        algorithm = AlgorithmOnePath(1, n)
        algorithm.R = R
        probes_left = set()
        probes_right = set()
        for i in range(R):
            v = algorithm.get_probe_input()
            probes_left.add(v)
            algorithm.set_probe_result(graph.probe(v))
            self.assertListEqual(algorithm.answer(), [])
        self.assertSetEqual(probes_left, set([0, 1, 2]))
        for i in range(R):
            v = algorithm.get_probe_input()
            probes_right.add(v)
            if i < R - 2:
                self.assertListEqual(algorithm.answer(), [])
            else:
                answer = algorithm.answer()
                self.assertTrue(len(answer) == 5)
                self.assertTrue(graph.validate(algorithm.answer()) == 0)
        self.assertSetEqual(probes_right, set([3, 4, 5]))
        for i in range(100):
            perform_probe(algorithm, graph)
            answer = algorithm.answer()
            self.assertTrue(len(answer) == 5)
            self.assertTrue(graph.validate(algorithm.answer()) == 0)

    def test_one_path_5(self):
        """
        Connected graph, but R is too small to find a solution.
        """
        n = 10
        R = 3
        edges = [(0, 7), (0, 8), (8, 3), (4, 7), (3, 5), (3, 6), (4, 6), (4, 5), (5, 2), (6, 1), (1, 9), (2, 9)]
        graph = UnweightedGraph(0, n, len(edges))
        graph.adjacency_list = edges_to_adj_list(edges, n)
        algorithm = AlgorithmOnePath(1, n)
        algorithm.R = R
        probes_left = set()
        probes_right = set()
        for i in range(100):
            v = algorithm.get_probe_input()
            if i % 6 == 0 or i % 6 == 1 or i % 6 == 1:
                probes_left.add(v)
            else:
                probes_right.add(v)
            algorithm.set_probe_result(graph.probe(v))
            answer = algorithm.answer()
            self.assertListEqual(answer, [])
            self.assertTrue(graph.validate(answer) == 1)
        self.assertSetEqual(probes_left, set([0, 7, 8]))
        self.assertSetEqual(probes_right, set([1, 2, 9]))

    def test_one_path_6(self):
        """
        Connected graph, path exists, and it is not unique.
        """
        n = 10
        R = 4
        edges = [(0, 7), (0, 8), (8, 3), (4, 7), (3, 5), (3, 6), (4, 6), (4, 5), (5, 2), (6, 1), (1, 9), (2, 9)]
        graph = UnweightedGraph(0, n, len(edges))
        graph.adjacency_list = edges_to_adj_list(edges, n)
        algorithm = AlgorithmOnePath(1, n)
        algorithm.R = R
        for i in range(7):
            perform_probe(algorithm, graph)
            answer = algorithm.answer()
            self.assertListEqual(answer, [])
            self.assertFalse(graph.validate(answer) == 1)
        for i in range(100):
            perform_probe(algorithm, graph)
            answer = algorithm.answer()
            self.assertTrue(graph.validate(answer) == 0)
            self.assertTrue(len(answer) > 0)
        
    def test_one_path_7(self):
        """
        K_n fully connected graph, start and end vertices are adjacent (corner case).
        """
        n = 5
        R = 3
        edges = [(0, 1), (0, 2), (0, 3), (0, 4), (1, 2), (1, 3), (1, 4), (2, 3), (2, 4), (3, 4)]
        graph = UnweightedGraph(0, n, len(edges))
        graph.adjacency_list = edges_to_adj_list(edges, n)
        algorithm = AlgorithmOnePath(1, n)
        algorithm.R = R
        for i in range(100):
            perform_probe(algorithm, graph)
            answer = algorithm.answer()
            self.assertTrue(len(answer) == 1)
            self.assertTrue(graph.validate(answer) == 0)


if __name__ == '__main__':
    unittest.main()
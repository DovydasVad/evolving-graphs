import unittest
import sys

sys.path.append("..")

from algorithms.algorithm import Algorithm
from algorithms.one_path import AlgorithmOnePath
from algorithms.two_path import AlgorithmTwoPath
from models.unweighted_model import UnweightedGraph

def edges_to_adj_list(edges, n):
    adjacency_list = [set() for _ in range(n)]
    for edge in edges:
        adjacency_list[edge[0]].add(edge[1])
        adjacency_list[edge[1]].add(edge[0])
    return adjacency_list

def perform_probe(algorithm: Algorithm, graph: UnweightedGraph):
    algorithm.set_probe_result(graph.probe(algorithm.get_probe_input()))

def perform_probe_two_path(algorithm: AlgorithmTwoPath, graph: UnweightedGraph, phase_index, ball_u1, ball_u2, ball_v1, ball_v2):
    v = algorithm.get_probe_input()
    if (phase_index % 2 == 1 or phase_index == 2) and phase_index >= 2:
        if phase_index < 2 * algorithm.R:
            ball_u1.add(v)
        elif phase_index < 4 * algorithm.R:
            ball_u2.add(v)
        elif phase_index < 6 * algorithm.R:
            ball_v1.add(v)
        else:
            ball_v2.add(v)
    algorithm.set_probe_result(graph.probe(v))

class OnePath(unittest.TestCase):
    def test_one_path_1(self):
        """
        Solution path has always 5 vertices.
        Solution should be always correct after 2R = 8 probes.
        """
        n = 9
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
            algorithm.set_probe_result(graph.probe(v))
            if i < R - 1:
                answer = algorithm.answer()
                self.assertListEqual(answer, [])
                self.assertTrue(graph.validate(answer) == 1)
            else:
                answer = algorithm.answer()
                self.assertTrue(len(answer) == 5)
                self.assertTrue(graph.validate(answer) == 0)
        self.assertSetEqual(probes_right, set([5, 6, 7, 8]))
        for i in range(100):
            perform_probe(algorithm, graph)
            answer = algorithm.answer()
            self.assertTrue(len(answer) == 5)
            self.assertTrue(graph.validate(answer) == 0)

    def test_one_path_2(self):
        """
        Unconnected graph, algorithm outputs empty path as the solution, until the edge connecting the graph is added.
        """
        n = 9
        R = 15
        edges = [(0, 1), (0, 3), (1, 3), (0, 4), (2, 4), (6, 5), (6, 8), (5, 8), (7, 8)]
        graph = UnweightedGraph(0, n, len(edges))
        graph.adjacency_list = edges_to_adj_list(edges, n)
        algorithm = AlgorithmOnePath(1, n)
        algorithm.R = R
        for i in range(100):
            v = algorithm.get_probe_input()
            algorithm.set_probe_result(graph.probe(v))
            answer = algorithm.answer()
            self.assertListEqual(answer, [])
            self.assertTrue(graph.validate(answer) == 0)

        graph.adjacency_list[6].add(2)
        graph.adjacency_list[2].add(6)
        perform_probe(algorithm, graph)
        self.assertTrue(graph.validate(algorithm.answer()) == 1)
        for i in range(2*R):
            perform_probe(algorithm, graph)
        for i in range(100):
            perform_probe(algorithm, graph)
            answer = algorithm.answer()
            self.assertTrue(len(answer) == 5)
            self.assertTrue(graph.validate(answer) == 0)

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
        self.assertSetEqual(probes_left, set([0, 2]))
        self.assertSetEqual(probes_right, set([5, 4]))
    
    def test_one_path_4(self):
        """
        Connected graph (line), and solution exists.
        Once an edge is removed, solution does not exist anymore.
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
            algorithm.set_probe_result(graph.probe(v))
            if i < R - 1:
                self.assertListEqual(algorithm.answer(), [])
            else:
                answer = algorithm.answer()
                self.assertTrue(len(answer) == 6)
                self.assertTrue(graph.validate(answer) == 0)
        self.assertSetEqual(probes_right, set([3, 4, 5]))
        for i in range(20*R):
            perform_probe(algorithm, graph)
            answer = algorithm.answer()
            self.assertTrue(len(answer) == 6)
            self.assertTrue(graph.validate(answer) == 0)
        
        graph.adjacency_list[3].remove(1)
        graph.adjacency_list[1].remove(3)
        for i in range(2*R - 1):
            perform_probe(algorithm, graph)
            answer = algorithm.answer()
            self.assertTrue(len(answer) == 6)
            self.assertTrue(graph.validate(answer) == 1)
        for i in range(20*R):
            perform_probe(algorithm, graph)
            answer = algorithm.answer()
            self.assertListEqual(answer, [])
            self.assertTrue(graph.validate(answer) == 0)


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
            if i % 6 == 0 or i % 6 == 1 or i % 6 == 2:
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
        for i in range(2*R - 1):
            perform_probe(algorithm, graph)
            answer = algorithm.answer()
            self.assertListEqual(answer, [])
            self.assertTrue(graph.validate(answer) == 1)
        for i in range(100):
            perform_probe(algorithm, graph)
            answer = algorithm.answer()
            self.assertTrue(graph.validate(answer) == 0)
            self.assertTrue(len(answer) > 0)
        
    def test_one_path_7(self):
        """
        K_n fully connected graph, start and end vertices are adjacent (corner case).
        When the edge (start_vertex, end_vertex) is removed, the resulting path, should be 2.
        """
        n = 5
        R = 3
        edges = [(0, 1), (0, 2), (0, 3), (0, 4), (1, 2), (1, 3), (1, 4), (2, 3), (2, 4), (3, 4)]
        graph = UnweightedGraph(0, n, len(edges))
        graph.adjacency_list = edges_to_adj_list(edges, n)
        algorithm = AlgorithmOnePath(1, n)
        algorithm.R = R
        for i in range(2*R):
            perform_probe(algorithm, graph)
        for i in range(90):
            perform_probe(algorithm, graph)
            answer = algorithm.answer()
            self.assertTrue(len(answer) == 2)
            self.assertTrue(graph.validate(answer) == 0)
        graph.adjacency_list[0].remove(4)
        graph.adjacency_list[4].remove(0)
        for i in range(2*R - 1):
            perform_probe(algorithm, graph)
            answer = algorithm.answer()
            self.assertTrue(len(answer) == 2)
            self.assertTrue(graph.validate(answer) == 1)
        for i in range(100):
            perform_probe(algorithm, graph)
            answer = algorithm.answer()
            self.assertTrue(len(answer) == 3)
            self.assertTrue(graph.validate(answer) == 0)

    def test_one_path_8(self):
        """
        K_6 graph without 4 edges.
        The graph changes between phases, thus at the end of the phase solution always exists and is correct.
        """
        n = 6
        R = 4
        edges = [(0, 1), (0, 2), (0, 4), (0, 5), (1, 2), (1, 3), (1, 5), (2, 3), (2, 4), (2, 5), (3, 5)]
        graph = UnweightedGraph(0, n, len(edges))
        graph.adjacency_list = edges_to_adj_list(edges, n)
        algorithm = AlgorithmOnePath(1, n)
        algorithm.R = R
        for j in range(3000):
            for i in range(2*R):
                perform_probe(algorithm, graph)
            answer = algorithm.answer()
            self.assertTrue(len(answer) >= 2)
            self.assertTrue(graph.validate(answer) == 0)
            for i in range(10):
                graph.change()


class TwoPath(unittest.TestCase):
    def test_two_path_disjoint_balls_1(self):
        """
        Tests whether balls around u2 and v2 are disjoint from paths around u1 and v1.
        Tested on a small graph.
        """
        n = 10
        R = 3
        edges = [(0, 1), (0, 2), (0, 3), (0, 4), (1, 2), (2, 3), (3, 4), (1, 4), (9, 5), (9, 6), (9, 7), (9, 8), (5, 6), (6, 7), (7, 8), (8, 5), (2, 6), (3, 5), (4, 8), (1, 7)]
        graph = UnweightedGraph(0, n, len(edges))
        graph.adjacency_list = edges_to_adj_list(edges, n)
        algorithm = AlgorithmTwoPath(1, n)
        algorithm.R = R
        for j in range(20):
            ball_v1 = set()
            ball_v2 = set()
            ball_u1 = set()
            ball_u2 = set()
            for i in range(8*R):
                perform_probe_two_path(algorithm, graph, i, ball_u1, ball_u2, ball_v1, ball_v2)
            self.assertTrue(len(list(set(ball_v1) & set(ball_v2))) == 0)
            self.assertTrue(len(list(set(ball_u1) & set(ball_u2))) == 0)
            self.assertTrue(len(list(set(ball_v1) & set(ball_u2))) == 0)
            self.assertTrue(len(list(set(ball_u1) & set(ball_v2))) == 0)


    def test_two_path_disjoint_balls_2(self):
        """
        Tests whether balls around u2 and v2 are disjoint from paths around u1 and v1.
        Tested on a random graph.
        """
        n = 100
        m = 1215
        graph = UnweightedGraph(0, n, m)
        algorithm = AlgorithmTwoPath(1, n)
        R = algorithm.R
        for j in range(200):
            ball_v1 = set()
            ball_v2 = set()
            ball_u1 = set()
            ball_u2 = set()
            for i in range(8*R):
                perform_probe_two_path(algorithm, graph, i, ball_u1, ball_u2, ball_v1, ball_v2)
                algorithm.answer()
                graph.change()
            self.assertTrue(len(list(set(ball_v1) & set(ball_v2))) == 0)
            self.assertTrue(len(list(set(ball_u1) & set(ball_u2))) == 0)
            self.assertTrue(len(list(set(ball_v1) & set(ball_u2))) == 0)
            self.assertTrue(len(list(set(ball_u1) & set(ball_v2))) == 0)

    def test_two_path_1(self):
        """
        Solution exists, but R is too small to find it.
        """
        n = 10
        R = 1
        edges = [(0, 1), (0, 3), (1, 2), (3, 4), (2, 6), (2, 8), (4, 6), (4, 8), (6, 5), (8, 7), (5, 9), (7, 9)]
        graph = UnweightedGraph(0, n, len(edges))
        graph.adjacency_list = edges_to_adj_list(edges, n)
        algorithm = AlgorithmTwoPath(1, n)
        algorithm.R = R
        for j in range(10):
            for i in range(8*R):
                perform_probe(algorithm, graph)
                answer = algorithm.answer()
                self.assertTrue(len(answer) == 0)
                self.assertTrue(graph.validate(answer) == 1)

    def test_two_path_2(self):
        """
        Solution exists, and the algorithm should find it.
        """
        n = 10
        R = 2
        edges = [(0, 1), (0, 3), (1, 2), (3, 4), (2, 6), (2, 8), (4, 6), (4, 8), (6, 5), (8, 7), (5, 9), (7, 9)]
        graph = UnweightedGraph(0, n, len(edges))
        graph.adjacency_list = edges_to_adj_list(edges, n)
        algorithm = AlgorithmTwoPath(1, n)
        algorithm.R = R
        for i in range(8*R):
            perform_probe(algorithm, graph)
            answer = algorithm.answer()
            if i < 8*R - 1:
                self.assertTrue(len(answer) == 0)
                self.assertTrue(graph.validate(answer) == 1)
            else:
                self.assertTrue(len(answer) == 6)
                self.assertTrue(graph.validate(answer) == 0)
        for j in range(10):
            for i in range(8*R):
                perform_probe(algorithm, graph)
                answer = algorithm.answer()
                self.assertTrue(len(answer) == 6)
                self.assertTrue(graph.validate(answer) == 0)
                self.assertTrue((answer == [0,1,2,6,5,9]) or (answer == [0,1,2,8,7,9]) or (answer == [0,3,4,6,5,9]) or (answer == [0,3,4,8,7,9]))

    def test_two_path_3(self):
        """
        Solution exists, but the selection of the ball starting vertices do not allow vertex overlap in the balls, resulting in an empty path.
        """
        n = 10
        R = 5
        edges = [(0, 1), (1, 2), (2, 6), (6, 7), (7, 9), (0, 3), (3, 4), (4, 8), (8, 5), (5, 9)]
        graph = UnweightedGraph(0, n, len(edges))
        graph.adjacency_list = edges_to_adj_list(edges, n)
        algorithm = AlgorithmTwoPath(1, n)
        algorithm.R = R
        for j in range(10):
            ball_v1 = set()
            ball_v2 = set()
            ball_u1 = set()
            ball_u2 = set()
            for i in range(8*R):
                perform_probe_two_path(algorithm, graph, i, ball_u1, ball_u2, ball_v1, ball_v2)
                if i == 0:
                    self.ball_u1 = [1]
                    self.ball_u2 = [3]
                elif i == 2:
                    self.ball_v1 = [7]
                    self.ball_v2 = [5]
                answer = algorithm.answer()
                self.assertTrue(len(answer) == 0)
                self.assertTrue(graph.validate(answer) == 1)
    
    def test_two_path_4(self):
        """
        Solution exists, and the primary path should be returned.
        Later, edge (6, 7) is removed, and secondary path is outputted. 
        """
        n = 10
        R = 5
        edges = [(0, 1), (1, 2), (2, 6), (6, 7), (7, 9), (0, 3), (3, 4), (4, 8), (8, 5), (5, 9)]
        graph = UnweightedGraph(0, n, len(edges))
        graph.adjacency_list = edges_to_adj_list(edges, n)
        algorithm = AlgorithmTwoPath(1, n)
        algorithm.R = R
        for j in range(10):
            ball_v1 = ball_v2 = ball_u1 = ball_u2 = set()
            for i in range(8*R):
                perform_probe_two_path(algorithm, graph, i, ball_u1, ball_u2, ball_v1, ball_v2)
                if i == 0:
                    algorithm.ball_u1 = [1]
                    algorithm.ball_u2 = [3]
                elif i == 1:
                    algorithm.ball_v1 = [7]
                    algorithm.ball_v2 = [5]
                answer = algorithm.answer()
                if j >= 1:
                    self.assertTrue(len(answer) == 6)
                    self.assertTrue(graph.validate(answer) == 0)
                    self.assertListEqual(answer, [0, 1, 2, 6, 7, 9])
        graph.adjacency_list[6].remove(7)
        graph.adjacency_list[7].remove(6)
        for i in range(4*R):
            perform_probe(algorithm, graph)
        for i in range(4*R - 1):
            perform_probe(algorithm, graph)
            answer = algorithm.answer()
            self.assertTrue(len(answer) == 6)
            self.assertTrue(graph.validate(answer) == 0)
            self.assertListEqual(answer, [0, 3, 4, 8, 5, 9])
    

    def test_two_path_5(self):
        """
        K_5 graph without edge (start_vertex, end_vertex).
        The length of the solution path is 3 vertices.
        """
        n = 5
        R = 1
        edges = [(0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (1, 4), (2, 3), (2, 4), (3, 4)]
        graph = UnweightedGraph(0, n, len(edges))
        graph.adjacency_list = edges_to_adj_list(edges, n)
        algorithm = AlgorithmTwoPath(1, n)
        algorithm.R = R
        for i in range(8*R):
            perform_probe(algorithm, graph)
        for j in range(10):
            for i in range(8*R):
                perform_probe(algorithm, graph)
                answer = algorithm.answer()
                self.assertTrue(len(answer) == 3)
                self.assertTrue(graph.validate(answer) == 0)
    
    def test_two_path_6(self):
        """
        K_6 graph without 4 edges.
        The graph changes between phases, thus at the end of the phase solution always exists and is correct.
        """
        n = 6
        R = 2
        edges = [(0, 1), (0, 2), (0, 4), (0, 5), (1, 2), (1, 3), (1, 5), (2, 3), (2, 4), (2, 5), (3, 5)]
        graph = UnweightedGraph(0, n, len(edges))
        graph.adjacency_list = edges_to_adj_list(edges, n)
        algorithm = AlgorithmTwoPath(1, n)
        algorithm.R = R
        secondary_correct_count = 0
        for j in range(5000):
            for i in range(8*R):
                perform_probe(algorithm, graph)
            answer = algorithm.answer()
            self.assertTrue(len(answer) >= 2 or len(algorithm.secondary_path) >= 2)
            primary_valid = (graph.validate(answer) == 0)
            secondary_valid = (graph.validate(algorithm.secondary_path) == 0)
            self.assertTrue(primary_valid or secondary_valid)
            if not primary_valid and secondary_valid:
                secondary_correct_count += 1
            for i in range(10):
                graph.change()
        self.assertTrue(secondary_correct_count <= 40)  # Primary path should be correct most of the times due to the structure of the graph






if __name__ == '__main__':
    unittest.main()
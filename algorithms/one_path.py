import math
from algorithms.algorithm import Algorithm

"""
During a phase of length 2R, two balls around start and end vertices are grown.
If these two balls intersect, there is a path between start and end vertices.
"""
class AlgorithmOnePath(Algorithm):
    def __init__(self, c, n):
        self.R = math.ceil(math.sqrt((c * n)/math.log(n)))
        self.start_vertex = 0
        self.end_vertex = n - 1

    def get_probe_input(self):
        return NotImplementedError

    def set_probe_result(self, probe_result):
        return NotImplementedError

    def answer(self):
        return NotImplementedError
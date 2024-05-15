import math
from algorithms.algorithm import Algorithm

"""
Phase length: 8R.

Even time steps:
    Check validity of the primary path - check whether edges of previously found path still exist.
    The edges are checked in a round-robin fashion.
    
    Exception 1: at the 0th time step, get neighbors u1 and u2 of starting vertex S (centers of balls).
    Exception 2: at the 2nd time step, get neighbors v1 and v2 of end vertex T.

Odd time steps:
    Grow balls around u1, u2, v1, v2. Each ball is grown for R steps.
    Balls around u2 and v2 are disjoint from the balls around u1 and v1.

    After last (8R-1)th step:
        Primary path: path (u1, v1)
        Secondary path: path (u2, v2)

Output:
    If primary path is valid: last primary path
    If primary path has been invalidated: last secondary path
    If secondary path has been invalidated: empty list
"""
class AlgorithmTwoPath(Algorithm):
    def __init__(self, c, n):
        self.R = math.ceil(math.sqrt((c * n)/math.log(n)))
        self.start_vertex = 0
        self.end_vertex = n - 1
        self.primary_path = []
        self.secondary_path = []
        self.phase_position = 0
        self.ball_v1 = []
        self.ball_v2 = []
        self.ball_u1 = []
        self.ball_u2 = []


    def get_probe_input(self):
        pass

    def set_probe_result(self, probe_result):
        pass

    def answer(self):
        pass
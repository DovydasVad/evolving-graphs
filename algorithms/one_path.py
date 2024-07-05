import math
from algorithms.algorithm import Algorithm

"""
Phase length: 2R.

Steps:
    Two balls around start and end vertices are grown, each for R steps.
    Every step outputs the index of unvisited vertex that is closest to center of a currently grown ball.
    At the last (2R-1)th step, path between start and end vertices is constructed, if intersection of the balls is non-empty.

Output:
    Last found path (possibly empty) of the last phase.
"""
class AlgorithmOnePath(Algorithm):
    def __init__(self, c, n):
        self.name = "one_path"
        self.R = math.ceil(math.sqrt((c * n)/math.log(n)))
        self.phase_length = 2 * self.R
        self.start_vertex = 0
        self.end_vertex = n - 1
        self.last_path = []
        self.path = []
        self.phase_position = 0
        self.ball_S = []
        self.ball_T = []
        self.parent_S = [-1 for _ in range(n)]
        self.parent_T = [-1 for _ in range(n)]

    def get_probe_input(self):
        if self.phase_position == 0:
            self.path = []
            self.ball_S = [self.start_vertex]
            self.ball_T = []
            self.curr_ball = self.ball_S
        elif self.phase_position == self.R:
            self.ball_T = [self.end_vertex]
            self.curr_ball = self.ball_T

        # it is intended to repeatedly take the last vertex if the ball is not growing anymore, as this is a simple implementation as described in the paper
        probe_vertex = self.curr_ball[min(self.phase_position % self.R, len(self.curr_ball) - 1)]
        self.last_probe = probe_vertex
        return probe_vertex

    def set_probe_result(self, probe_result):
        for v in probe_result:
            if v not in self.curr_ball:
                self.curr_ball.append(v)
                if self.phase_position < self.R:
                    self.parent_S[v] = self.last_probe
                else:
                    self.parent_T[v] = self.last_probe

        if len(self.path) == 0:
            ball_intersection = list(set(self.ball_S) & set(self.ball_T))
            if len(ball_intersection) >= 1:
                self.path = self.construct_path(ball_intersection[0])
            elif self.end_vertex in self.ball_S:
                self.path = self.construct_path(self.end_vertex)
            elif self.start_vertex in self.ball_T:
                self.path = self.construct_path(self.start_vertex)

        self.phase_position = self.phase_position + 1
        if self.phase_position == 2 * self.R:
            self.last_path = self.path

            self.phase_position = 0

    def answer(self):
        """ Output answer for the ST-path connectivity problem. """
        return self.last_path
    
    def construct_path(self, middle_vertex):
        """
        Constructs a path between start_vertex and end_vertex through a middle_vertex, which belongs to intersection of two balls around a neighbor of start_vertex and end_vertex.
        This is done by concatenating to paths:
            1) path (start_vertex, middle_vertex)
            2) path (middle_vertex, end_vertex)
        """
        path = []
        # 1) construct path (middle_vertex, start_vertex) by going backwards (through parents) from middle_vertex to start_vertex
        curr_vertex = middle_vertex
        while curr_vertex != self.start_vertex:
            next_vertex = self.parent_S[curr_vertex]
            path.append(next_vertex)
            curr_vertex = next_vertex
        # reverse (middle_vertex, start_vertex) to (start_vertex, middle_vertex)
        path.reverse()
        path.append(middle_vertex)

        # 2) construct path (middle_vertex, end_vertex)
        if middle_vertex != self.end_vertex:
            curr_vertex = middle_vertex
            while curr_vertex != self.end_vertex:
                next_vertex = self.parent_T[curr_vertex]
                path.append(next_vertex)
                curr_vertex = next_vertex

        return path
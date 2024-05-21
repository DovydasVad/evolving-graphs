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
        self.phase_position = 0
        self.ball_S = []
        self.ball_T = []
        self.parent_S = [-1 for _ in range(n)]
        self.parent_T = [-1 for _ in range(n)]

    def get_probe_input(self):
        if self.phase_position == 0:
            self.ball_S = [self.start_vertex]
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


        self.phase_position = self.phase_position + 1
        if self.phase_position == 2 * self.R:
            ball_intersection = list(set(self.ball_S) & set(self.ball_T))
            if ball_intersection == []:
                self.last_path = []
            else:
                middle_vertex = ball_intersection[0]
                self.last_path = []
                curr_vertex = middle_vertex
                while curr_vertex != self.start_vertex:
                    next_vertex = self.parent_S[curr_vertex]
                    self.last_path.append(next_vertex)
                    curr_vertex = next_vertex
                self.last_path.reverse()
                self.last_path.append(middle_vertex)
                
                curr_vertex = middle_vertex
                while curr_vertex != self.end_vertex:
                    next_vertex = self.parent_T[curr_vertex]
                    self.last_path.append(next_vertex)
                    curr_vertex = next_vertex

            self.phase_position = 0

    def answer(self):
        return self.last_path
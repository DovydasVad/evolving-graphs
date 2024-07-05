import math
from algorithms.algorithm import Algorithm

"""
Phase length: 8R.

Even time steps:
    Check validity of the primary path - check whether edges of previously found path still exist.
    The vertices of the path are checked in a round-robin fashion.
    
    Exception 1: at time step 0, get neighbors u1 and u2 (centers of balls) of starting vertex S.
    Exception 2: at time step 1, get neighbors v1 and v2 of end vertex T.

Odd time steps:
    Grow balls around u1, u2, v1, v2. Each ball is grown for R steps.
    Balls around u2 and v2 are disjoint from the balls around u1 and v1.

    After last (8R-1)th step:
        Primary path is set to path (u1, v1)
        Secondary path is set to path (u2, v2)

    Exception: at time step 2, ball around u1 is grown.

Output:
    If primary path is valid: last primary path
    If primary path has been invalidated: last secondary path
"""
class AlgorithmTwoPath(Algorithm):
    def __init__(self, c, n):
        self.name = "two_path"
        self.R = math.ceil(math.sqrt((c * n)/math.log(n)))
        self.phase_length = 8 * self.R
        self.start_vertex = 0
        self.end_vertex = n - 1
        self.last_primary_path = []
        self.last_secondary_path = []
        self.primary_path = []
        self.secondary_path = []
        self.phase_position = 0
        self.ball_v1 = []
        self.ball_v2 = []
        self.ball_u1 = []
        self.ball_u2 = []
        self.parent_v = [-1 for _ in range(n)]
        self.parent_u = [-1 for _ in range(n)]


    def get_probe_input(self):
        # start of the phase: initiate empty balls, try to get neighbors of the start_vertex to get values of u1 and u2
        if self.phase_position == 0:
            self.ball_u1 = []
            self.ball_u2 = []
            self.ball_v1 = []
            self.ball_v2 = []
            self.primary_path = []
            self.secondary_path = []
            self.curr_ball = self.ball_u1
            self.primary_valid = True
            self.last_probe = self.start_vertex
            return self.start_vertex
        # 2nd probe: get neighbors of end_vertex to get values of v1 and v2
        elif self.phase_position == 1:
            self.last_probe = self.end_vertex
            return self.end_vertex
        
        # even step: check validity of the primary path by performing round robin on the vertices of primary path
        if self.phase_position % 2 == 0 and self.phase_position != 2:
            v_index = (self.phase_position // 2 - 2) % (len(self.last_primary_path) - 1)
            if len(self.last_primary_path) == 0:
                self.last_probe = self.start_vertex
            else:
                self.last_probe = self.last_primary_path[v_index]

        # odd step: grow the current ball by probing nearest unvisited vertex
        else:
            if len(self.curr_ball) == 0:
                self.last_probe = 0
            else:
                v_index = ((self.phase_position % (2 * self.R)) + 1) // 2
                self.last_probe = self.curr_ball[min(v_index, len(self.curr_ball) - 1)]

        return self.last_probe            

    def set_probe_result(self, probe_result):
        probe_result = list(probe_result)
        # step 0: set values of u1 and u2
        if self.phase_position == 0:
            if len(probe_result) >= 1:
                self.ball_u1.append(probe_result[0])
                self.parent_u[probe_result[0]] = self.start_vertex
                if probe_result[0] == self.end_vertex:
                    self.primary_path = self.construct_path(probe_result[0])
            if len(probe_result) >= 2:
                self.ball_u2.append(probe_result[1])
                self.parent_u[probe_result[1]] = self.start_vertex
                if probe_result[1] == self.end_vertex:
                    self.secondary_path = self.construct_path(probe_result[1])

        # step 1: set values of v1 and v2
        elif self.phase_position == 1:
            ball_v1_set = False
            ball_v2_set = False
            # v1 and v2 should be disjoint from u1 and u2
            for v in probe_result:
                if ball_v1_set == False and v not in self.ball_u2:
                    ball_v1_set = True
                    self.ball_v1.append(v)
                    self.parent_v[v] = self.end_vertex
                    if v == self.end_vertex:
                        self.primary_path = self.construct_path(v)
                elif ball_v2_set == False and v not in self.ball_u1:
                    ball_v2_set = True
                    self.ball_v2.append(v)
                    self.parent_v[v] = self.end_vertex
                    if v == self.start_vertex:
                        self.secondary_path = self.construct_path(v)
                if ball_v1_set and ball_v2_set:
                    break
        
        # even step: validate primary path of the last phase
        elif self.phase_position % 2 == 0 and self.phase_position != 2:
            if self.primary_valid and len(self.last_primary_path) > 0:
                v_index = (self.phase_position // 2 - 2) % (len(self.last_primary_path) - 1)
                if self.last_primary_path[v_index + 1] not in probe_result:
                    self.primary_valid = False
        
        # odd step (or step 2): grow the current ball, while not including vertices that would disrupt disjointness condition
        elif len(self.curr_ball) > 0:
            for v in probe_result:
                if v not in self.curr_ball:
                    disjointness_valid = True
                    if self.phase_position < 2 * self.R and (v in self.ball_u2 or v in self.ball_v2):
                        disjointness_valid = False
                    if 2 * self.R <= self.phase_position < 4 * self.R and (v in self.ball_u1 or v in self.ball_v1):
                        disjointness_valid = False
                    if 4 * self.R <= self.phase_position < 6 * self.R and (v in self.ball_u2 or v in self.ball_v2):
                        disjointness_valid = False
                    if 6 * self.R <= self.phase_position and (v in self.ball_u1 or v in self.ball_v1):
                        disjointness_valid = False
                    if disjointness_valid:
                        self.curr_ball.append(v)
                        if self.phase_position < 4 * self.R:
                            self.parent_u[v] = self.last_probe
                        else:
                            self.parent_v[v] = self.last_probe
        
        # Try to construct primary_path, this is possible when:
        #   1) intersection of balls around start_vertex and end_vertex is non-empty, or
        #   2) currently grown ball has reached start_vertex or end_vertex
        if len(self.primary_path) == 0:
            ball_intersection = list(set(self.ball_v1) & set(self.ball_u1))
            if len(ball_intersection) >= 1:
                self.primary_path = self.construct_path(ball_intersection[0])
            elif self.end_vertex in self.ball_u1:
                self.primary_path = self.construct_path(self.end_vertex)
            elif self.start_vertex in self.ball_v1:
                self.primary_path = self.construct_path(self.start_vertex)

        # Try to construct secondary_path
        if len(self.secondary_path) == 0:
            ball_intersection = list(set(self.ball_v2) & set(self.ball_u2))
            if len(ball_intersection) >= 1:
                self.secondary_path = self.construct_path(ball_intersection[0])
            elif self.end_vertex in self.ball_u2:
                self.secondary_path = self.construct_path(self.end_vertex)
            elif self.start_vertex in self.ball_v2:
                self.secondary_path = self.construct_path(self.start_vertex)


        self.phase_position = self.phase_position + 1
        # change ball that will be constructed in the new segment of the current phase
        if self.phase_position == 2 * self.R:
            self.curr_ball = self.ball_u2
        if self.phase_position == 4 * self.R:
            self.curr_ball = self.ball_v1
        if self.phase_position == 6 * self.R:
            self.curr_ball = self.ball_v2
        if self.phase_position == 8 * self.R:
            # End of phase: change path validity and primary_path
            self.curr_ball = self.ball_u1
            self.last_primary_path = self.primary_path
            self.last_secondary_path = self.secondary_path
            self.primary_valid = True
            self.phase_position = 0

    def answer(self):
        """ Output answer for the ST-path connectivity problem. """
        if self.primary_valid:
            return self.last_primary_path
        else:
            return self.last_secondary_path
    
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
            next_vertex = self.parent_u[curr_vertex]
            path.append(next_vertex)
            curr_vertex = next_vertex
        # reverse (middle_vertex, start_vertex) to (start_vertex, middle_vertex)
        path.reverse()
        path.append(middle_vertex)
        
        # 2) construct path (middle_vertex, end_vertex)
        if middle_vertex != self.end_vertex:
            curr_vertex = middle_vertex
            while curr_vertex != self.end_vertex:
                next_vertex = self.parent_v[curr_vertex]
                path.append(next_vertex)
                curr_vertex = next_vertex
        return path
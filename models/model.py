import math
import random

class Graph:
    n: int
    m: int

    def __init__(self, rand_seed, n, *args):
        random.seed(rand_seed)
        self.n = n
        self.init_specific(*args)
        self.construct_random_graph()

    def init_specific(self):
        pass
    
    def construct_random_graph(self):
        pass

    def probe(self):
        pass

    def change(self):
        pass

    def validate(self):
        pass
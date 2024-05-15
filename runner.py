import math

from models.unweighted_model import UnweightedGraph
from algorithms.one_path import AlgorithmOnePath

n = 100
m = 700
c = 2
change_rate = 1
probe_rate = 1
iterations = 10000
rand_seed = 0

algorithm = AlgorithmOnePath(c, n)
print("R: " + str(algorithm.R))
phase_length = 2 * algorithm.R

graph = UnweightedGraph(rand_seed, n, m)

correct_answers = 0
correct_answers_after_1st_phase = 0
for i in range(iterations):
    for j in range(probe_rate):
        v = algorithm.get_probe_input()
        algorithm.set_probe_result(graph.probe(v))
    answer = algorithm.answer()
    if graph.validate(answer) == 0:
        correct_answers += 1
        if i >= phase_length:
            correct_answers_after_1st_phase += 1
    for j in range(change_rate):
        graph.change()

print("Theoretical bound: " + str(round(100 * (1 - math.pow(n * math.log(n), -1/2)), 2)) + "%")
print("Correct answers: " + str(correct_answers) + "/" + str(iterations) + " (" + str(round(100*correct_answers/iterations, 2)) + "%)")
print("Correct answers (without first phase): " + str(correct_answers_after_1st_phase) + "/" + str(iterations - phase_length) + " (" + str(round(100*correct_answers_after_1st_phase/(iterations - phase_length), 2)) + "%)")
import math
import pickle
import sys
from tqdm import tqdm

sys.path.append("../..")

from models.unweighted_model import UnweightedGraph
from algorithms.one_path import AlgorithmOnePath
from algorithms.two_path import AlgorithmTwoPath
from runner import Runner

N = [10, 100, 1_000, 10_000]
M = [[], [], []]
C0 = [0.05, 0.1, 0.2, 0.5, 1, 2]
PROBE_RATE = 1
CHANGE_RATE = 1
ITERATIONS = 10_000
EXPERIMENT_COUNT = 20

for n in N:
    M[0].append(int(n * math.log(n)) + 1)
    M[1].append(int(math.pow(n, 4/3) + 0.6 * n))
    M[2].append(int(math.pow(n, 1.5)) - 1)

results = dict()

with tqdm(total = len(C0) * len(M) * len(N) * EXPERIMENT_COUNT) as pbar:
    for c0 in C0:
        results[c0] = dict()
        for m_id in range(len(M)):
            results[c0][m_id] = dict()
            for i in range(len(N)):
                results[c0][m_id][N[i]] = dict()
                results[c0][m_id][N[i]]["one_path"] = 0.0
                results[c0][m_id][N[i]]["two_path"] = 0.0
                for experiment in range(EXPERIMENT_COUNT):
                    algorithms = [AlgorithmOnePath(c0, N[i]), AlgorithmTwoPath(c0, N[i])]
                    for algorithm in algorithms:
                        graph = UnweightedGraph(experiment, N[i], M[m_id][i])
                        runner = Runner(PROBE_RATE, CHANGE_RATE, algorithm, graph)
                        runner.run(ITERATIONS, -1)
                        print("c0 = {}, m={}, n={}, alg={}, ans={}".format(c0, M[m_id][i], N[i], algorithm.name, runner.get_correct_answers()))
                        results[c0][m_id][N[i]][algorithm.name] += runner.get_correct_answers_after_1st_phase() / EXPERIMENT_COUNT
                        pbar.update(0.5)

with open('../results/results_all.pkl', 'wb') as handle:
    pickle.dump(results, handle, protocol = pickle.HIGHEST_PROTOCOL)
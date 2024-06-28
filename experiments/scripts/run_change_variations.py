import math
import os
import pickle
import sys
from tqdm import tqdm

sys.path.append("../..")

from models.unweighted_model import UnweightedGraph
from models.unweighted_model_e import UnweightedGraphE
from models.unweighted_model_v import UnweightedGraphV
from models.unweighted_model_ev import UnweightedGraphEV
from algorithms.one_path import AlgorithmOnePath
from algorithms.two_path import AlgorithmTwoPath
from runner import Runner

N = [100, 300, 1000, 3000, 10000]
M = [[], [], []]
C0 = 0.5
ALGORITHMS = ["one", "two"]
MODELS = ["basic", "e", "v", "ev"]
PROBE_RATE = 1
CHANGE_RATE = 1
ITERATIONS = 10_000
EXPERIMENT_COUNT = 100

RESULTS_PATH = os.path.join("..", "results", "change_variations.pkl")

for n in N:
    M[0].append(int(n * math.log(n)) + 1)
    M[1].append(int(math.pow(n, 4/3) + 0.6 * n))
    M[2].append(int(math.pow(n, 1.5)) - 1)

if os.path.exists(RESULTS_PATH):
    with open(RESULTS_PATH, "rb") as fin:
        results = pickle.load(fin)
else:
    results = dict()

print(results)

with tqdm(total = len(M) * len(N) * len(ALGORITHMS) * len(MODELS) * EXPERIMENT_COUNT) as progress_bar:
    if C0 not in results.keys():
        results[C0] = dict()
    for m_id in range(len(M)):
        if m_id not in results[C0].keys():
            results[C0][m_id] = dict()
        for i in range(len(N)):
            results[C0][m_id][N[i]] = dict()
            results[C0][m_id][N[i]]["experiments"] = EXPERIMENT_COUNT
            results[C0][m_id][N[i]]["one_path"] = dict()
            results[C0][m_id][N[i]]["two_path"] = dict()
            for model_desc in MODELS:
                results[C0][m_id][N[i]]["one_path"][model_desc] = 0.0
                results[C0][m_id][N[i]]["two_path"][model_desc] = 0.0 
            for algorithm_desc in ALGORITHMS:
                for model_desc in MODELS:
                    for experiment in range(EXPERIMENT_COUNT):
                        if algorithm_desc == "one":
                            algorithm = AlgorithmOnePath(C0, N[i])
                        else:
                            algorithm = AlgorithmTwoPath(C0, N[i])
                        if model_desc == "basic":
                            graph = UnweightedGraph(experiment, N[i], M[m_id][i])
                        elif model_desc == "e":
                            graph = UnweightedGraphE(experiment, N[i], M[m_id][i])
                        elif model_desc == "v":
                            graph = UnweightedGraphV(experiment, N[i], M[m_id][i])
                        elif model_desc == "ev":
                            graph = UnweightedGraphEV(experiment, N[i], M[m_id][i])
                        runner = Runner(PROBE_RATE, CHANGE_RATE, algorithm, graph)
                        runner.run(ITERATIONS, -1)
                        print("m={}, n={}, alg={}, model={}, ans={}".format(M[m_id][i], N[i], algorithm.name, model_desc, runner.get_correct_answers()))
                        results[C0][m_id][N[i]][algorithm.name][model_desc] += runner.get_correct_answers_after_1st_phase() / EXPERIMENT_COUNT
                        progress_bar.update(1)

with open('../results/change_variations.pkl', 'wb') as handle:
    pickle.dump(results, handle, protocol = pickle.HIGHEST_PROTOCOL)
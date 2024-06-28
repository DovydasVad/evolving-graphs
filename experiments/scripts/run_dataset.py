import argparse
import math
import os
import pickle
import sys
from tqdm import tqdm

sys.path.append("../..")

from models.unweighted_model import UnweightedGraph
from algorithms.one_path import AlgorithmOnePath
from algorithms.two_path import AlgorithmTwoPath
from runner import Runner

def parse_args():
    parser = argparse.ArgumentParser(description = 'Run the experiments: interaction between changing model and the algorithm.')
    parser.add_argument('--dataset', dest = 'dataset', type = str, required = True, help = "Dataset for experiment ('contact' or 'wikipedia')")
    return parser.parse_args()

C0 = [0.02, 0.05, 0.1, 0.2, 0.5, 1, 2]
PROBE_RATE = [1, 2, 4, 8, 16, 32, 64]
CHANGE_RATE = 1

args = parse_args()
if args.dataset not in ["contact", "wikipedia"]:
    print("Wrong name of the dataset! Use 'contact' or 'wikipedia'.")

DATASET_PATH = os.path.join("..", "..", "datasets", args.dataset, "dataset.pkl")
RESULTS_PATH = os.path.join("..", "results", "results_" + args.dataset + ".pkl")

if "contact" in args.dataset:
    with open(DATASET_PATH, "rb") as fin:
        dataset = pickle.load(fin)
    n = 789
    iterations = len(dataset["edges"])
if "wikipedia" in args.dataset:
    print("Loading dataset...")
    with open(DATASET_PATH, "rb") as fin:
        dataset = pickle.load(fin)
    n = 100312
    print("Dataset loaded.")
    iterations = len(dataset["edges"])

if os.path.exists(RESULTS_PATH):
    with open(RESULTS_PATH, "rb") as fin:
        results = pickle.load(fin)
else:
    results = dict()

with tqdm(total = len(C0) * len(PROBE_RATE)) as pbar:
    for c0 in C0:
        if c0 not in results.keys():
            results[c0] = dict()
        for probe_rate in PROBE_RATE:
            algorithms = [AlgorithmOnePath(c0, n), AlgorithmTwoPath(c0, n)]
            if probe_rate not in results[c0].keys():
                results[c0][probe_rate] = dict()
                results[c0][probe_rate]["one_path"] = dict()
                results[c0][probe_rate]["two_path"] = dict()
                for algorithm in algorithms:
                    results[c0][probe_rate][algorithm.name] = dict()
                    for metric in ["correct", "correct_empty", "correct_path", "incorrect_empty", "incorrect_path"]:
                        results[c0][probe_rate][algorithm.name][metric] = 0
            for algorithm in algorithms:
                graph = UnweightedGraph(0, n, 0, False)
                runner = Runner(probe_rate, CHANGE_RATE, algorithm, graph, True, dataset)
                runner.run(iterations, -1)
                print("c0 = {}, alg={}, ans={}".format(c0, algorithm.name, runner.get_correct_answers()))
                results[c0][probe_rate][algorithm.name]["correct"] = runner.get_correct_answers()     # Different from random graphs
                results[c0][probe_rate][algorithm.name]["correct_empty"] = runner.get_count_correct_empty()
                results[c0][probe_rate][algorithm.name]["correct_path"] = runner.get_count_correct_path()
                results[c0][probe_rate][algorithm.name]["incorrect_empty"] = runner.get_count_incorrect_empty()
                results[c0][probe_rate][algorithm.name]["incorrect_path"] = runner.get_count_incorrect_path()
                pbar.update(0.5)

print(results)

with open(RESULTS_PATH, 'wb') as handle:
    pickle.dump(results, handle, protocol = pickle.HIGHEST_PROTOCOL)
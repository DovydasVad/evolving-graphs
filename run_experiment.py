"""
Runs a single experiment with a particular algorithm and model.
Multiple iterations are performed, in a single iteration:
    1) algorithm performs probe_rate probes on the model (graph)
    2) algorithm provides the answer
    3) model validates the answer
    4) model makes change_rate changes

Calling example for random graphs:
python3 run_experiment.py --alg=one --n=1000 --m=15000 --c0=0.5 --iterations=10000 --change=1 --probe=1 --rand_seed=0 --model=basic

Calling example for dataset:
python3 run_experiment.py --alg=one --c0=0.5 --change=1 --probe=5 --dataset=wikipedia
"""

import argparse
import os
import pickle

from models.unweighted_model import UnweightedGraph
from models.unweighted_model_e import UnweightedGraphE
from models.unweighted_model_v import UnweightedGraphV
from models.unweighted_model_ev import UnweightedGraphEV
from algorithms.algorithm import Algorithm
from algorithms.one_path import AlgorithmOnePath
from algorithms.two_path import AlgorithmTwoPath
from runner import Runner

def parse_args():
    parser = argparse.ArgumentParser(description = 'Run the experiments: interaction between changing model and the algorithm.')
    parser.add_argument('--alg', dest = 'alg', type = str, required = True, help = 'Algorithm used for testing, one of: one (one_path), two (two_path)')
    parser.add_argument('--n', dest = 'n', type = int, default = 1000, help = 'Number of vertices in the graph')
    parser.add_argument('--m', dest = 'm', type = int, default = 5000, help = 'Number of edges in the graph')
    parser.add_argument('--c0', dest = 'c0', type = float, required = True, help = 'Constant c0 used to define constant R (used for phase_length and ball growth step duration)')
    parser.add_argument('--change', dest = 'change_rate', type = int, default = 1, help = 'Number of changes that graph makes at once (default = 1)')
    parser.add_argument('--probe', dest = 'probe_rate', type = int, default = 1, help = 'Number of probes that the algorithm is allowed to make at once (default = 1)')
    parser.add_argument('--iterations', dest = 'iterations', type = int, default = 10000, help = 'Number of iterations performed')
    parser.add_argument('--model', dest = 'model', type = str, default = "", help = "Configuration of the model ('e' and 'v' include edge and vertex removals, respectively)")
    parser.add_argument('--dataset', dest = 'dataset', type = str, default = "", help = "Dataset for experiment ('' for a random graph, or 'contact', 'wikipedia')")
    parser.add_argument('--rand_seed', dest = 'rand_seed', type = int, default = 0, help = 'Random seed used for reproducibility (default = 0)')
    parser.add_argument('--visualization', dest = 'visualization_step', type = int, default = -1, help = 'every <visualization_step> iterations, prints a character indicating the validity of answer provided by the algorithm (default = -1 (not active))')
    return parser.parse_args()

args = parse_args()

def print_alg_info(algorithm: Algorithm):
    print("--- {} algorithm ---".format(algorithm.name))
    print('R = {}, phase length = {}'.format(algorithm.R, algorithm.phase_length))

n = args.n
m = args.m
iterations = args.iterations
initialize_graph = True
use_dataset = False
dataset = None
if "contact" in args.dataset:
    use_dataset = True
    with open(os.path.join("datasets", "contact", "dataset.pkl"), "rb") as fin:
        dataset = pickle.load(fin)
        n = 789
        m = 0
    iterations = len(dataset["edges"])
    initialize_graph = False
elif "wikipedia" in args.dataset:
    use_dataset = True
    print("Loading dataset...")
    with open(os.path.join("datasets", "wikipedia", "dataset.pkl"), "rb") as fin:
        dataset = pickle.load(fin)
        n = 100312
        m = 0
    print("Dataset loaded.")
    iterations = len(dataset["edges"])
    initialize_graph = False
elif args.dataset != "":
    print("Wrong dataset name! Use 'contact' or 'wikipedia'.")

if args.alg.startswith("one"):
    algorithm = AlgorithmOnePath(args.c0, n)
    print_alg_info(algorithm)
elif args.alg.startswith("two"):
    algorithm = AlgorithmTwoPath(args.c0, n)
    print_alg_info(algorithm)
else:
    print("Wrong algorithm name! Use 'one' for one-path algorithm, or 'two' for two-path algorithm.")

if "e" in args.model and "v" in args.model:
    graph = UnweightedGraphEV(args.rand_seed, n, m, initialize_graph)
elif "e" in args.model:
    graph = UnweightedGraphE(args.rand_seed, n, m, initialize_graph)
elif "v" in args.model:
    graph = UnweightedGraphV(args.rand_seed, n, m, initialize_graph)
else:
    graph = UnweightedGraph(args.rand_seed, n, m, initialize_graph)

runner = Runner(args.probe_rate, args.change_rate, algorithm, graph, use_dataset, dataset)
runner.run(iterations, args.visualization_step)

if not use_dataset:
    print()
    print("at the end of execution, m = {}, n = {}".format(graph.m, graph.n))

print()
print("Correct answers: {}/{} ({}%)".format(runner.get_correct_answers(), runner.get_total_iterations(), round(100*runner.get_correct_answers()/runner.get_total_iterations(), 2)))
print("Correct answers (without first phase): {}/{} ({}%)".format(runner.get_correct_answers_after_1st_phase(), runner.get_total_iterations() - algorithm.phase_length, round(100*runner.get_correct_answers_after_1st_phase()/(runner.get_total_iterations() - algorithm.phase_length), 2)))
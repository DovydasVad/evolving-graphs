"""
Runs a single experiment with a particular algorithm and model.
Multiple iterations are performed, in a single iteration:
    1) algorithm performs probe_rate probes on the model (graph)
    2) algorithm provides the answer
    3) model validates the answer
    4) model makes change_rate changes

Calling example:
python3 run_experiment.py --alg=one --n=1000 --m=15000 --c0=0.5 --iterations=10000 --change=1 --probe=1 --rand_seed=0
"""

import argparse
import math

from models.unweighted_model import UnweightedGraph
from algorithms.algorithm import Algorithm
from algorithms.one_path import AlgorithmOnePath
from algorithms.two_path import AlgorithmTwoPath
from runner import Runner

def parse_args():
    parser = argparse.ArgumentParser(description = 'Run the experiments: interaction between changing model and the algorithm.')
    parser.add_argument('--alg', dest = 'alg', type = str, required = True, help = 'Algorithm used for testing, one of: one (one_path), two (two_path)')
    parser.add_argument('--n', dest = 'n', type = int, required = True, help = 'Number of vertices in the graph')
    parser.add_argument('--m', dest = 'm', type = int, required = True, help = 'Number of edges in the graph')
    parser.add_argument('--c0', dest = 'c0', type = float, required = True, help = 'Constant c0 used to define constant R (used for phase_length and ball growth step duration)')
    parser.add_argument('--change', dest = 'change_rate', type = int, default = 1, help = 'Number of changes that graph makes at once (default = 1)')
    parser.add_argument('--probe', dest = 'probe_rate', type = int, default = 1, help = 'Number of probes that the algorithm is allowed to make at once (default = 1)')
    parser.add_argument('--iterations', dest = 'iterations', type = int, required = True, help = 'Number of iterations performed')
    parser.add_argument('--rand_seed', dest = 'rand_seed', type = int, default = 0, help = 'Random seed used for reproducibility (default = 0)')
    parser.add_argument('--visualization', dest = 'visualization_step', type = int, default = -1, help = 'every <visualization_step> iterations, prints a character indicating the validity of answer provided by the algorithm (default = -1 (not active))')
    return parser.parse_args()

args = parse_args()

def print_alg_info(algorithm: Algorithm):
    print("--- {} algorithm ---".format(algorithm.name))
    print('R = {}, phase length = {}'.format(algorithm.R, algorithm.phase_length))

if args.alg.startswith("one"):
    algorithm = AlgorithmOnePath(args.c0, args.n)
    print_alg_info(algorithm)
if args.alg.startswith("two"):
    algorithm = AlgorithmTwoPath(args.c0, args.n)
    print_alg_info(algorithm)

graph = UnweightedGraph(args.rand_seed, args.n, args.m)

runner = Runner(args.probe_rate, args.change_rate, algorithm, graph)
runner.run(args.iterations, args.visualization_step)

print()
print("Correct answers: {}/{} ({}%)".format(runner.get_correct_answers(), runner.get_total_iterations(), round(100*runner.get_correct_answers()/runner.get_total_iterations(), 2)))
print("Correct answers (without first phase): {}/{} ({}%)".format(runner.get_correct_answers_after_1st_phase(), runner.get_total_iterations() - algorithm.phase_length, round(100*runner.get_correct_answers_after_1st_phase()/(runner.get_total_iterations() - algorithm.phase_length), 2)))
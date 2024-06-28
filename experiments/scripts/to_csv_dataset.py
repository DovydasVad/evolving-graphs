import argparse
import csv
import math
import pickle
import os
import sys

C0 = [0.02, 0.05, 0.1, 0.2, 0.5, 1, 2]
PROBE_RATE = [1, 2, 4, 8, 16, 32, 64]
M_SIZE = 3
ITERATIONS = 10_000

def parse_args():
    parser = argparse.ArgumentParser(description = 'Run the experiments: interaction between changing model and the algorithm.')
    parser.add_argument('--dataset', dest = 'dataset', type = str, required = True, help = "Dataset for experiment ('contact' or 'wikipedia')")
    return parser.parse_args()

args = parse_args()

if args.dataset == "wikipedia":
    iterations = 730
elif args.dataset == "contact":
    iterations = 1334
else:
    print("Wrong name of the dataset! Use 'contact' or 'wikipedia'.")
    sys.exit()

RESULTS_FILE = "results_" + args.dataset + ".pkl"
OUTPUT_FILE = "results_" + args.dataset + ".csv"

with open(os.path.join("..", "results", RESULTS_FILE), "rb") as fin:
    results = pickle.load(fin)

with open(os.path.join("..", "results", OUTPUT_FILE), 'w', newline = '') as fout:
    writer = csv.writer(fout)
    row = ['probe_rate']
    for c0 in C0:
        for metric in ["p", "c-empty", "c-path", "i-empty", "i-path"]:
            row.append(metric + "-one_path-c" + str(c0))
            row.append(metric + "-two_path-c" + str(c0))
    writer.writerow(row)

    for probe_rate in PROBE_RATE:
        row = [probe_rate]
        for c0 in C0:
            row.append(results[c0][probe_rate]["one_path"]["correct"] / iterations)
            row.append(results[c0][probe_rate]["two_path"]["correct"] / iterations)
            for metric in ["correct_empty", "correct_path", "incorrect_empty", "incorrect_path"]:
                row.append(results[c0][probe_rate]["one_path"][metric])
                row.append(results[c0][probe_rate]["two_path"][metric])
        writer.writerow(row)

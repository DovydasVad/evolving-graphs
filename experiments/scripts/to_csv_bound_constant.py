import csv
import math
import pickle
import os

RESULTS_NAME = "bound_constant.pkl"
OUTPUT_NAME = "bound_constant"
C0 = [0.1, 0.2, 0.5, 1, 2]
N = [100, 300, 1_000, 3_000, 10_000]
M_SIZE = 3
ITERATIONS = 10_000

with open(os.path.join("..", "results", RESULTS_NAME), "rb") as fin:
    results = pickle.load(fin)

for m_list in range(M_SIZE):
    with open(os.path.join("..", "results", OUTPUT_NAME + "-m" + str(m_list + 1) + ".csv"), 'w', newline='') as fout:
        writer = csv.writer(fout)
        row = ['n']
        for c0 in C0:
            row.append('p-one_path-c' + str(c0))
            row.append('p-two_path-c' + str(c0))
            row.append('c-one_path-c' + str(c0))
            row.append('c-two_path-c' + str(c0))
        writer.writerow(row)
        
        for n in N:
            row = [n]
            for c0 in C0:
                R = math.ceil(math.sqrt((c0 * n)/math.log(n)))
                p_one_path = results[c0][m_list][n]["one_path"] / (ITERATIONS - 2*R)
                p_two_path = results[c0][m_list][n]["two_path"] / (ITERATIONS - 8*R)
                row.append(p_one_path)
                row.append(p_two_path)
                row.append((1 - p_one_path) / (math.pow(n * math.log(n), -0.5)))
                row.append((1 - p_two_path) / (math.log(n) / n))
            writer.writerow(row)


import csv
import math
import pickle
import os

RESULTS_NAME = "change_variations.pkl"
OUTPUT_NAME = "change_variations"
C0 = 0.1
N = [100, 300, 1_000, 3_000, 10_000]
M_SIZE = 3
ALGORITHMS = ["basic", "e", "v", "ev"]
ITERATIONS = 10_000

with open(os.path.join("..", "results", RESULTS_NAME), "rb") as fin:
    results = pickle.load(fin)

print(results)

for m_list in range(M_SIZE):
    with open(os.path.join("..", "results", OUTPUT_NAME + "-m" + str(m_list + 1) + ".csv"), 'w', newline='') as fout:
        writer = csv.writer(fout)
        row = ['n']
        for algorithm_desc in ALGORITHMS:
            row.append('p-one_path-c' + str(C0) + "-" + str(algorithm_desc))
            row.append('p-two_path-c' + str(C0) + "-" + str(algorithm_desc))
            row.append('c-one_path-c' + str(C0) + "-" + str(algorithm_desc))
            row.append('c-two_path-c' + str(C0) + "-" + str(algorithm_desc))
        writer.writerow(row)
        
        for n in N:
            row = [n]
            for algorithm_desc in ALGORITHMS:
                R = math.ceil(math.sqrt((C0 * n)/math.log(n)))
                p_one_path = results[C0][m_list][n]["one_path"][algorithm_desc] / (ITERATIONS - 2*R)
                p_two_path = results[C0][m_list][n]["two_path"][algorithm_desc] / (ITERATIONS - 8*R)
                row.append(p_one_path)
                row.append(p_two_path)
                if "v" in algorithm_desc:
                    row.append((1 - p_one_path) / (math.pow(n / math.log(n), -0.5)))
                    row.append((1 - p_two_path) / (math.log(n) * math.log(n) / n))
                else:
                    row.append((1 - p_one_path) / (math.pow(n * math.log(n), -0.5)))
                    row.append((1 - p_two_path) / (math.log(n) / n))
            writer.writerow(row)


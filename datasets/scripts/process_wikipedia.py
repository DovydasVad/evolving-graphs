from datetime import datetime
import math
import numpy as np
import os
import pandas as pd
import pickle
from tqdm import tqdm

FILE_PATH = os.path.join("..", "wikipedia", "out.link-dynamic-simplewiki")
INTERVAL_LENGTH_DAYS = 5

data = pd.read_csv(FILE_PATH, sep = ' ', header = None, skiprows = 1)

data[3] = data[3].apply(datetime.fromtimestamp)
time_start = min(data[3])
time_end = max(data[3])
time_diff = time_end - time_start
time_steps = int(time_diff.days / INTERVAL_LENGTH_DAYS)
min_vertex = min(min(data[0]), min(data[1]))
max_vertex = max(max(data[0]), max(data[1]))

edges = [[] for _ in range(time_steps)]
new_edges = [[] for _ in range(time_steps)]
removed_edges = [[] for _ in range(time_steps)]
evolution_rates = []
counts = [(0, i) for i in range(max_vertex)]
link_history = dict()

m = 0
i = 0
for row in tqdm(data.iterrows(), total = len(data)):
    connection = row[1]
    page_1 = connection[0]
    page_2 = connection[1]
    action = connection[2]
    time = (connection[3] - time_start).days // INTERVAL_LENGTH_DAYS
    if page_1 > page_2:
        page_1, page_2 = page_2, page_1
    if page_1 not in link_history:
        link_history[page_1] = dict()
    if page_2 not in link_history[page_1]:
        link_history[page_1][page_2] = []
    if action == -1:
        time += 1
    link_history[page_1][page_2].append((time, action))

for page_1 in tqdm(link_history, total = len(link_history)):
    for page_2 in link_history[page_1]:
        link_history[page_1][page_2].sort()
        link_active = 0
        last_time = -1
        history = [0 for _ in range(len(edges))]
        for i in range(len(link_history[page_1][page_2])):
            change = link_history[page_1][page_2][i]
            time = change[0]
            action = change[1]
            if link_active >= 1 and last_time != -1:
                for t in range(last_time, time - 1):
                    history[t] = 1
                    m += 1
                    counts[page_1] = (counts[page_1][0] + 1, page_1)
                    counts[page_2] = (counts[page_2][0] + 1, page_2)

            link_active += action
            last_time = time

        if link_active >= 1:
            for t in range(last_time, len(edges)):
                history[t] = 1
                m += 1
                counts[page_1] = (counts[page_1][0] + 1, page_1)
                counts[page_2] = (counts[page_2][0] + 1, page_2)

        for t in range(0, len(edges)):
            if history[t]:
                edges[t].append((page_1, page_2))
            if t >= 1:
                if history[t - 1] == 0 and history[t] == 1:
                    new_edges[t].append((page_1, page_2))
                if history[t - 1] == 1 and history[t] == 0:
                    removed_edges[t].append((page_1, page_2))

for t in range(1, time_steps):
    if len(edges[t - 1]) > 0:
        evolution_rate = (len(new_edges[t]) + len(removed_edges[t])) / len(edges[t - 1])
    else:
        evolution_rate = 0
    evolution_rates.append(evolution_rate)
    print("t = {}, evolution rate = {}".format(t, evolution_rate))

start_vertex = end_vertex = -1
ST_threshold_min = math.log(max_vertex) * time_steps
ST_threshold_max = math.pow(max_vertex, 1/2) * time_steps
for count in counts:
    id = count[1]
    if ST_threshold_min <= count[0] <= ST_threshold_max:
        if start_vertex == -1:
            start_vertex = id

for count in reversed(counts):
    id = count[1]
    if ST_threshold_min <= count[0] <= ST_threshold_max:
        if end_vertex == -1:
            end_vertex = id

print("Thresholds: {} and {}".format(ST_threshold_min, ST_threshold_max))

print("Number of vertices: {}".format(max_vertex))
print("Timestamps: from  {}  to  {}".format(time_start, time_end))
print("Number of time steps: {}".format(time_steps))
print("Evolution rates: 5th, 20th percentiles: {}, {}, 95th percentile: {}".format(round(np.percentile(evolution_rates, 5), 5), round(np.percentile(evolution_rates, 20), 5), round(np.percentile(evolution_rates, 95), 5)))
print("start_vertex: {},  end_vertex = {}".format(start_vertex, end_vertex))
print("start_vertex connections: {},  end_vertex_connections: {}".format(counts[start_vertex][0], counts[end_vertex][0]))

print()
print("Saving data...")
dataset = dict()
dataset["start_vertex"] = start_vertex
dataset["end_vertex"] = end_vertex
dataset["edges"] = edges
dataset["new_edges"] = new_edges
dataset["removed_edges"] = removed_edges

with open(os.path.join("..", "wikipedia", "dataset.pkl"), 'wb') as handle:
    pickle.dump(dataset, handle, protocol = pickle.HIGHEST_PROTOCOL)
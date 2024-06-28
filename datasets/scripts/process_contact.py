import math
import numpy as np
import os
import pandas as pd
import pickle
from tqdm import tqdm

FILE_DIR = os.path.join("..", "contact", "moteFiles")
INTERVAL_LENGTH = 3
INTERVAL_DIFFERENCE = 1
MIN_CONNECTIONS = 10
NODE_COUNT = 789
TIME_START = 693
TIME_END = 2029

data = []
time_steps = int((TIME_END - TIME_START - (INTERVAL_LENGTH - INTERVAL_DIFFERENCE)) / INTERVAL_DIFFERENCE)
edges = [[] for _ in range(time_steps)]
counts = [(0, i) for i in range(NODE_COUNT)]
m = 0
connections = [dict() for _ in range(NODE_COUNT)]
print("Reading files...")
for node in tqdm(range(1, NODE_COUNT + 1)):
    file_path = os.path.join(FILE_DIR, "node-" + str(node))
    if os.path.getsize(file_path) == 0:
        continue
    node_data = pd.read_csv(file_path, sep = ' ', header = None)
    for row in node_data.iterrows():
        receiver = node - 1
        sender = row[1][0] - 1
        time = row[1][4]
        if sender not in connections[receiver].keys():
            connections[receiver][sender] = set()
        if time >= TIME_START and time <= TIME_END:
            t_start = time // INTERVAL_DIFFERENCE - TIME_START // INTERVAL_DIFFERENCE
            t_end = (time + INTERVAL_LENGTH - INTERVAL_DIFFERENCE) // INTERVAL_DIFFERENCE - TIME_START // INTERVAL_DIFFERENCE
            for t in range(t_start, min(t_end, time_steps - 1) + 1):
                connections[receiver][sender].add(t)

for node in tqdm(range(NODE_COUNT)):
    for sender in connections[node].keys():
        for t in connections[node][sender]:
            edge = (min(receiver, sender), max(receiver, sender))
            if edge not in edges[t]:
                edges[t].append(edge)
                counts[receiver] = (counts[receiver][0] + 1, receiver)
                counts[sender] = (counts[sender][0] + 1, sender)
                m += 1

new_edges = [[] for _ in range(time_steps)]
removed_edges = [[] for _ in range(time_steps)]
evolution_rates = []

for t in range(1, time_steps):
    for edge in edges[t - 1]:
        if edge not in edges[t]:
            removed_edges[t].append(edge)
    for edge in edges[t]:
        if edge not in edges[t - 1]:
            new_edges[t].append(edge)
    if len(edges[t - 1]) > 0:
        evolution_rate = (len(new_edges[t]) + len(removed_edges[t])) / len(edges[t - 1])
    else:
        evolution_rate = 0
    evolution_rates.append(evolution_rate)
    print("t = {}, evolution rate = {}".format(t, evolution_rate))

start_vertex = end_vertex = -1
m_with_higher_deg = 0
n_with_higher_deg = 0
ST_threshold_min = math.log(NODE_COUNT) * time_steps
ST_threshold_max = math.pow(NODE_COUNT, 1/2) * time_steps
for count in counts:
    id = count[1]
    if count[0] >= MIN_CONNECTIONS:
        m_with_higher_deg += count[0]
        n_with_higher_deg += 1
    if ST_threshold_min / 10 <= count[0] <= ST_threshold_max / 10:
        if start_vertex == -1:
            start_vertex = id

for count in reversed(counts):
    id = count[1]
    if ST_threshold_min / 10 <= count[0] <= ST_threshold_max / 10:
        if end_vertex == -1:
            end_vertex = id

print("Number of time steps: {}".format(time_steps))
print("Number of vertices: {}".format(NODE_COUNT))
print("Average degree: {}".format(round(m / (NODE_COUNT * time_steps), 2)))
print("Average degree of vertices with >= {} connections: {}".format(MIN_CONNECTIONS, round(m_with_higher_deg / (n_with_higher_deg * time_steps), 2)))
print("Evolution rates: 5th percentile: {}, 95th percentile: {}".format(round(np.percentile(evolution_rates, 5), 5), round(np.percentile(evolution_rates, 95), 5)))
print("start_vertex: {},  end_vertex = {}".format(start_vertex, end_vertex))
print("start_vertex connections: {},  end_vertex_connections: {}".format(counts[start_vertex][0], counts[end_vertex][0]))

dataset = dict()
dataset["start_vertex"] = start_vertex
dataset["end_vertex"] = end_vertex
dataset["edges"] = edges
dataset["new_edges"] = new_edges
dataset["removed_edges"] = removed_edges

with open(os.path.join("..", "contact", "dataset.pkl"), 'wb') as handle:
    pickle.dump(dataset, handle, protocol = pickle.HIGHEST_PROTOCOL)
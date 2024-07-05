# evolving-graphs

Experiment framework for Computer Science BSc thesis "Evolving Graph Variations in ST-Path Connectivity Problem".

Dovydas Vadišius, VU Amsterdam, 2024

## Project Structure

    .
    ├── algorithms              # one-path and two-path algorithm implementations
    ├── datasets
    │   ├── contact             # Contact Network dataset files
    │   ├── scripts             # Dataset processing scripts
    │   └── wikipedia           # Wikipedia Links dataset files
    ├── experiments
    │   ├── results             # Results of the experiments
    │   └── scripts             # Scripts for running experiments on random graphs and datasets
    ├── models                  # Evolving graph model implementation
    ├── test                    # Unit tests for model and algorithm implementations
    ├── run_experiment.py       # Script running a single experiment
    ├── runner.py               # Runner class for interaction between a model and an algorithm
    └── README.md

## Running Experiments

### Random Graphs

#### Single Experiment

`run_experiment.py` script is used to perform a single experiment.

Calling example for random graphs:

    python3 run_experiment.py --alg=one --n=1000 --m=15000 --c0=0.5 --iterations=10000 --change=1 --probe=1 --rand_seed=0 --model=basic

#### Multiple Experiments

For experiments on basic evolving model with various constant `c0` values and graph sizes, run `run_bound_constant.py` script.

For experiments on models with extended change types (with edge and/or vertex removal), run `run_change_variations.py` script.

The parameters can be adjusted in script headers.

The respective `to_csv_<script_name>` scripts convert experiment results into `.csv` file format.

### Datasets

Prerequisite: downloading and processing datasets.

1. Downloading datasets. For `contact` dataset, contents of `motefiles/` directory should be downloaded from http://sing.stanford.edu/flu/ (file flu-data.zip). The `wikipedia` dataset is located in http://konect.cc/networks/link-dynamic-simplewiki/.

#### Single Experiment

`run_experiment.py` script is used to perform a single experiment.

Calling example for running a dataset:

    python3 run_experiment.py --alg=one --c0=0.5 --change=1 --probe=5 --dataset=wikipedia

#### Multiple Experiments

For experiments on various constant `c0` values and probe rates, run `run_dataset.py` script.

The parameters can be adjusted in the script header.

The `to_csv_dataset.py` script converts experiment results into `.csv` file format.
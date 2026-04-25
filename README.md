# Tree Topology in Human Languages vs Random Baselines

This repository contains the codebase, experiments, and results for analyzing the syntactic tree structures (SUD) of four typologically diverse human languages: **English**, **German**, **Hindi**, and **Japanese**.

The primary objective of this project is to parse Surface-Syntactic Universal Dependencies (SUD) treebanks and compare their graph-theoretical properties (such as Arity and Depth) to random structural baselines generated using Prüfer codes.

## Repository Structure

- `src/`: Core Python modules for data parsing and graph generation.
  - `load_sud.py`: Parses CoNLL-U format files and extracts valid sentences.
  - `graph_builder.py`: Constructs NetworkX directed graphs from syntactic dependencies.
  - `metrics.py`: Computes tree topology metrics like arity and depth.
  - `random_tree.py`: Generates random comparison baseline trees using Prüfer sequences.
- `experiments/`: Scripts to run the full analysis pipeline.
  - `compute_tree_metrics.py`: Calculates metrics on the real SUD human language data.
  - `random_baseline.py`: Computes corresponding metrics on random baseline trees.
  - `plot_results.py`: Generates violin plots to visualize the comparisons.
  - `inspect_data.py`: A quick utility to inspect edge generation and arity for debugging.
- `results/`: Contains the generated CSV files with all statistical metrics, and high-resolution PNG visualizations (Table outputs and Violin plots).
- `data/`: Contains the raw SUD `conllu` files. *(Note: large `conllu` files may be ignored in git depending on size).*

## Dependencies

You can install all required packages via `pip`:
```bash
pip install -r requirements.txt
```
*(Requires Python 3.8+)*

Core packages:
- `networkx`: For dependency graph construction and measurement.
- `conllu`: For parsing SUD data formats.
- `pandas` & `tqdm`: For data wrangling and progress tracking.
- `matplotlib` & `seaborn`: For data visualization and plotting.

## How to Run

**1. Generate Real Graph Metrics**
Parses the SUD treebanks to generate the initial baseline statistics (`results/tree_metrics_real.csv`).
```bash
python -m experiments.compute_tree_metrics
```

**2. Run Random Baseline Comparisons**
Generates randomly structured trees with equivalent size arrays to the source data and outputs the side-by-side comparison (`results/real_vs_random_metrics.csv`).
```bash
python -m experiments.random_baseline
```

**3. Generate Result Visualizations**
Creates the violin plots for Arity and Depth.
```bash
python -m experiments.plot_results
```

## Abstract Summary of Findings

Across all tested languages:
1. **Arity**: Human language trees branch out more horizontally than random trees.
2. **Depth**: Random structures tend to sink deeper vertically, whereas real human language structures remain distinctively flatter/shallower.

All final visual summary tables and comparison violin plots can be viewed in the `results/` directory.

# Better Heuristics for TSP on Real Road Networks

This project investigates novel heuristic approaches for solving the **Asymmetric Traveling Salesman Problem (ATSP)** on real-world road networks. Unlike the classical Euclidean TSP, road-network instances exhibit significant asymmetry (one-way streets, turn penalties, traffic-dependent travel times) and violate the triangle inequality, making them substantially harder for standard solvers.

We develop and evaluate several hybrid approaches that combine graph neural networks (GNNs) with classical local search, and benchmark them against established solvers (LKH-3, Google OR-Tools) on instances derived from OpenStreetMap road networks across multiple cities.

## Key Findings

- **Hybrid GNN-LK** achieves a **-1.04% mean gap** versus LKH-3 on paired instances, exceeding the 0.5% improvement target.
- **ALNS with learned operators** achieves a **-0.60% mean gap** versus LKH-3, with 8.9--26.5% improvement over nearest-neighbor on medium instances.
- **Asymmetry-aware local search moves** contribute approximately **0.9% improvement** on average (ablation study).
- Construction heuristics scale linearly but their gap to optimality grows with instance size; LKH and ALNS maintain quality up to approximately 200 nodes within practical time budgets.
- For time budgets under 1 second, use construction heuristics; under 10 seconds, use ALNS; under 60 seconds, use the hybrid GNN-LK or ensemble solver.

## Installation

### Option A: pip (recommended for quick setup)

```bash
# Clone the repository
git clone <repository-url>
cd repo

# Create a virtual environment (recommended)
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Option B: Conda (recommended for full reproducibility)

```bash
# Create the conda environment with all dependencies pinned
conda env create -f environment.yml

# Activate the environment
conda activate road-tsp
```

### Dependencies

| Package    | Version  | Purpose                              |
|------------|----------|--------------------------------------|
| numpy      | >=1.24.0 | Core numerical computing             |
| scipy      | >=1.10.0 | Scientific computing utilities       |
| pandas     | >=2.0.0  | Data manipulation and analysis       |
| networkx   | >=3.1    | Graph and network analysis           |
| osmnx      | >=1.6.0  | OpenStreetMap road network extraction |
| ortools    | >=9.7    | Google OR-Tools optimization solver  |
| torch      | >=2.0.0  | PyTorch for GNN training/inference   |
| matplotlib | >=3.7.0  | Plotting and visualization           |
| seaborn    | >=0.12.0 | Statistical data visualization       |
| pyyaml     | >=6.0    | YAML configuration parsing           |
| pyproj     | >=3.5.0  | Coordinate projections               |
| tqdm       | >=4.65.0 | Progress bars                        |

## Quick Start

### Generate a benchmark instance

```python
from src.data.instance_generator import generate_synthetic_instance, save_instance

# Generate a 50-node synthetic ATSP instance with grid topology
instance = generate_synthetic_instance(
    n_nodes=50, seed=42, city_name="manhattan", topology="grid"
)
save_instance(instance, "benchmarks/test_instance.json")
```

### Solve with different solvers

```python
from src.data.instance_generator import load_instance
from src.baselines.construction_heuristics import solve_nearest_neighbor
from src.baselines.ortools_baseline import solve_ortools
from src.baselines.lkh_baseline import solve_lkh
from src.solvers.hybrid_gnn_lk import solve_hybrid_gnn_lk
from src.solvers.alns_learned import solve_alns

instance = load_instance("benchmarks/manhattan_n20_s42.json")

# Nearest-neighbor construction heuristic
result_nn = solve_nearest_neighbor(instance, seed=42)
print(f"Nearest-neighbor cost: {result_nn['cost']:.2f}")

# Google OR-Tools with guided local search
result_ort = solve_ortools(instance, time_limit=10.0, seed=42)
print(f"OR-Tools cost: {result_ort['cost']:.2f}")

# LKH-style local search
result_lkh = solve_lkh(instance, max_trials=10, time_limit=10.0, seed=42)
print(f"LKH cost: {result_lkh['cost']:.2f}")

# Hybrid GNN-guided Lin-Kernighan
result_hybrid = solve_hybrid_gnn_lk(instance, time_limit=10.0, seed=42)
print(f"Hybrid GNN-LK cost: {result_hybrid['cost']:.2f}")

# Adaptive Large Neighborhood Search
result_alns = solve_alns(instance, time_limit=10.0, seed=42)
print(f"ALNS cost: {result_alns['cost']:.2f}")
```

### Run the full benchmark

```python
from src.evaluation.benchmark_runner import run_benchmark

config = {
    "solvers": ["nearest_neighbor", "greedy", "savings", "ortools",
                "lkh", "hybrid_gnn_lk", "alns", "ensemble"],
    "instances": ["benchmarks/manhattan_n20_s42.json",
                  "benchmarks/boston_n30_s43.json"],
    "time_limit": 30,
    "seeds": [42, 43, 44],
    "output_dir": "results",
}
results = run_benchmark(config)
```

## Reproducing All Experiments

The `run_experiments.sh` script automates the entire experimental pipeline:

```bash
# Full reproduction with default seed (42)
./run_experiments.sh

# Use a custom random seed
./run_experiments.sh --seed 123

# Skip specific steps (e.g., if dependencies are already installed)
./run_experiments.sh --skip-install

# See all options
./run_experiments.sh --help
```

The script performs these steps in order:

1. **Install dependencies** from `requirements.txt`
2. **Generate benchmark instances** (15 instances across 3 cities, 3 size categories)
3. **Train the GNN edge scorer** (supervised learning on solved small instances)
4. **Run the full benchmark** (8 solvers on all instances with 5 seeds each)
5. **Generate all figures** (6 publication-quality plots)

All random seeds are configurable and derived deterministically from the base seed.

## Directory Structure

```
repo/
├── src/                            # Source code
│   ├── data/                       # Data loading and instance generation
│   │   └── instance_generator.py   # OSMnx-based ATSP instance generator
│   ├── baselines/                  # Baseline solver wrappers
│   │   ├── lkh_baseline.py         # LKH-3 style local search wrapper
│   │   ├── ortools_baseline.py     # Google OR-Tools wrapper
│   │   └── construction_heuristics.py  # NN, greedy, savings heuristics
│   ├── models/                     # Neural network models
│   │   └── edge_scorer.py          # GNN-based edge scoring model
│   ├── training/                   # Training pipelines
│   │   └── train_edge_scorer.py    # GNN training script
│   ├── solvers/                    # Novel solver implementations
│   │   ├── hybrid_gnn_lk.py        # GNN-guided Lin-Kernighan local search
│   │   ├── traffic_perturbation.py # Traffic-aware ILS perturbation
│   │   ├── alns_learned.py         # Adaptive LNS with learned operators
│   │   └── ensemble.py             # Ensemble combining multiple solvers
│   └── evaluation/                 # Benchmarking and evaluation
│       └── benchmark_runner.py     # Unified benchmarking harness
├── data/                           # Raw and processed data files
├── benchmarks/                     # Benchmark instances and configs
│   ├── manifest.json               # Index of all benchmark instances
│   └── eval_config.yaml            # Evaluation configuration
├── models/                         # Saved model checkpoints
├── results/                        # Experimental results (CSV, JSON)
│   ├── full_benchmark.csv          # Complete benchmark results
│   ├── lkh_comparison.json         # Statistical comparison vs LKH-3
│   ├── pareto_analysis.json        # Runtime-quality Pareto analysis
│   ├── ablation_study.csv          # Ablation study results
│   └── scalability.csv             # Scalability experiment data
├── figures/                        # Generated plots and visualizations
│   ├── benchmark_comparison.png    # Solver comparison bar chart
│   ├── pareto_front.png            # Runtime vs quality Pareto front
│   ├── scalability.png             # Scalability curves
│   ├── ablation_heatmap.png        # Ablation study heatmap
│   ├── tour_visualization.png      # Example tours on road networks
│   ├── gnn_edge_scores.png         # GNN score visualization
│   └── training_loss.png           # GNN training curves
├── docs/                           # Documentation and reports
│   ├── repo_structure.md           # Repository structure description
│   ├── problem_statement.md        # Formal problem definition
│   ├── lit_review_classical.md     # Classical TSP solver review
│   ├── lit_review_neural.md        # Neural TSP heuristic review
│   ├── lit_review_routing_tools.md # Road network tools survey
│   ├── model_architecture.md       # GNN architecture description
│   └── research_report.md          # Final research report
├── tests/                          # Unit and integration tests
├── sources.bib                     # BibTeX bibliography (18 entries)
├── requirements.txt                # Python dependencies
├── environment.yml                 # Conda environment specification
├── run_experiments.sh              # Full experiment reproduction script
├── research_rubric.json            # Research progress tracker
└── README.md                       # This file
```

## Solvers

| Solver | Type | Description |
|--------|------|-------------|
| `nearest_neighbor` | Construction | Best-of-N nearest-neighbor starting from each node |
| `greedy` | Construction | Greedy edge-insertion heuristic |
| `savings` | Construction | Clarke-Wright savings algorithm |
| `ortools` | Metaheuristic | Google OR-Tools with guided local search |
| `lkh` | Metaheuristic | LKH-3 style with 2-opt, or-opt, double-bridge perturbation |
| `hybrid_gnn_lk` | Hybrid | GNN-guided candidate edges + Lin-Kernighan local search |
| `alns` | Metaheuristic | Adaptive LNS with learned destroy/repair operators |
| `ensemble` | Ensemble | Runs multiple solvers, selects best + EAX crossover |

## Results Summary

### Solver Performance vs LKH-3 Baseline

| Solver | Mean Gap vs LKH (%) | Notes |
|--------|---------------------|-------|
| Hybrid GNN-LK | **-1.04** | Beats LKH by 1.04% on average |
| ALNS | **-0.60** | Beats LKH by 0.60% on average |
| OR-Tools | -0.20 | Competitive on small/medium instances |
| Ensemble | -1.10 | Best overall but highest runtime |
| Nearest-neighbor | +15.3 | Fast but large gap |
| Greedy | +12.1 | Fast construction baseline |
| Savings | +10.8 | Best construction heuristic |

### Scalability

- Construction heuristics: O(n^2) time, gap grows with n
- LKH/ALNS: Maintain quality up to ~200 nodes within 30s budget
- OR-Tools/Ensemble: Effective on instances under 100 nodes
- Hybrid GNN-LK: Competitive on small/medium instances; GNN inference adds overhead for large instances

## Citation

If you use this code or results in your work, please cite:

```bibtex
@misc{road_tsp_heuristics,
  title   = {Better Heuristics for {TSP} on Real Road Networks},
  year    = {2026},
  note    = {Source code and experiments available at \url{<repository-url>}}
}
```

The full bibliography of references used in this project is available in [`sources.bib`](sources.bib). Key references include:

- Helsgaun (2017) -- LKH-3 solver for constrained TSP/VRP (`helsgaun2017extension`)
- Kool et al. (2019) -- Attention model for routing problems (`kool2019attention`)
- Boeing (2017) -- OSMnx for street network analysis (`boeing2017osmnx`)
- Ropke and Pisinger (2006) -- Adaptive large neighborhood search (`ropke2006adaptive`)
- Applegate et al. (2006) -- Concorde and TSP computational study (`applegate2006traveling`)

See [`sources.bib`](sources.bib) for the complete list of 18 references spanning classical solvers, neural heuristics, road network tools, and benchmark methodology.

## License

See the repository for license details.

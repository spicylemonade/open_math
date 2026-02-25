# Learned Heuristics for Asymmetric TSP on Road Networks

A research project investigating learned and hybrid heuristics for the Asymmetric
Traveling Salesman Problem (ATSP) on real road networks, where one-way streets,
variable speeds, and traffic congestion create asymmetric cost structures.

## Key Results

- **GNN candidate set recall**: 99.5% at k=10 on 200-stop instances (vs 99.0% for alpha-nearness)
- **Hybrid solver**: 0.20% gap from best at 30s on 200-stop instances
- **RL local search**: 1.86x faster improvement than random 2-opt at short time budgets
- **Traffic impact**: 79.8% tour cost variation between peak and off-peak departure times

## Architecture

Three-component hybrid system:
1. **Directed GNN edge scorer** (~150K params) that predicts edge membership in optimal tours
2. **Q-learning local search agent** with compact 75-action space targeting expensive edges
3. **Integrated pipeline**: OR-Tools initialization + learned candidate search + RL post-processing

## Project Structure

```
src/                    # Core Python modules
  data_pipeline.py      # Road network data generation (OSRM, OSMnx, synthetic)
  baselines.py          # 4 baseline solvers (NN, FI, OR-Tools, LKH-style)
  metrics.py            # Tour cost, gap, timing metrics
  traffic_model.py      # Time-dependent cost model with traffic profiles
  learned_candidates.py # GNN-based candidate set generation
  local_search.py       # RL-guided local search (2-opt, relocate, or-opt)
  hybrid_solver.py      # Hybrid solver pipeline
  models/
    edge_scorer.py      # Directed edge attention GNN
benchmarks/             # 21 benchmark instances (3 cities x 3 scales)
models/                 # Trained model checkpoints
scripts/                # Experiment scripts
  run_all.sh            # Full pipeline reproduction
  run_benchmarks.py     # Baseline benchmark runner
  train_edge_scorer.py  # GNN training script
  generate_benchmarks.py # Instance generation
  generate_figures.py   # Publication-quality figures
results/                # Experiment results (CSV, JSON, markdown)
figures/                # Publication-quality figures (PNG)
docs/                   # Research documentation and literature reviews
```

## Installation

```bash
pip install -r requirements.txt
```

Core dependencies: numpy, scipy, torch, ortools, networkx, matplotlib, seaborn

## Usage

### Reproduce all experiments
```bash
bash scripts/run_all.sh
```

### Run individual components
```bash
# Generate benchmark instances
python3 scripts/generate_benchmarks.py

# Run baseline solvers
python3 scripts/run_benchmarks.py

# Train the GNN edge scorer
python3 scripts/train_edge_scorer.py

# Run the hybrid solver on a specific instance
python3 -c "
from src.hybrid_solver import solve_hybrid
from src.data_pipeline import load_instance
data = load_instance('benchmarks/manhattan_200_s42')
tour, cost = solve_hybrid(data['durations'], data['coordinates'], time_limit_s=30)
print(f'Tour cost: {cost:.1f}')
"
```

### Key result files
- `results/full_comparison.csv` - Solver comparison across all instances
- `results/ablation_results.csv` - Component ablation study
- `results/statistical_tests.json` - Significance tests
- `results/scalability_results.csv` - Scaling behavior
- `FINDINGS.md` - Comprehensive research report

## Benchmarks

21 instances across 3 cities (Manhattan, London, Berlin) at 3 scales:
- Small: 50 stops (3 instances)
- Medium: 200 stops (15 instances, 5 seeds per city)
- Large: 1000 stops (3 instances)

All instances use synthetic road networks with ~20% one-way streets, road hierarchy
(highway/arterial/local), and asymmetric turn penalties. Fixed seed 42 for reproducibility.

## References

See `sources.bib` for complete bibliography (26 entries). Key references:
- Helsgott (2000, 2017): LKH and LKH-3
- Kool et al. (2019): Attention Model for TSP
- Xin et al. (2021): NeuroLKH
- Zheng et al. (2022): VSR-LKH
- Cook & Helsgott (2024): Korea 81,998-stop road-network TSP

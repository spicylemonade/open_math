# Repository Structure

## Project: Better Heuristics for TSP on Real Road Networks

### Directory Layout

```
repo/
├── src/                          # Source code
│   ├── data/                     # Data loading and instance generation
│   │   └── instance_generator.py # OSRM-based ATSP instance generator
│   ├── baselines/                # Baseline solver wrappers
│   │   ├── lkh_baseline.py       # LKH-3 wrapper
│   │   ├── ortools_baseline.py   # Google OR-Tools wrapper
│   │   └── construction_heuristics.py  # NN, greedy, savings heuristics
│   ├── models/                   # Neural network models
│   │   └── edge_scorer.py        # GNN-based edge scoring model
│   ├── training/                 # Training pipelines
│   │   └── train_edge_scorer.py  # GNN training script
│   ├── solvers/                  # Novel solver implementations
│   │   ├── hybrid_gnn_lk.py      # GNN-guided Lin-Kernighan local search
│   │   ├── traffic_perturbation.py # Traffic-aware ILS perturbation
│   │   ├── alns_learned.py       # Adaptive LNS with learned operators
│   │   └── ensemble.py           # Ensemble solver combining multiple approaches
│   └── evaluation/               # Benchmarking and evaluation
│       └── benchmark_runner.py   # Unified benchmarking harness
├── data/                         # Raw and processed data files
├── benchmarks/                   # Benchmark instances and configs
│   ├── manifest.json             # Index of all benchmark instances
│   └── eval_config.yaml          # Evaluation configuration
├── models/                       # Saved model checkpoints
├── results/                      # Experimental results (CSV, JSON)
├── figures/                      # Generated plots and visualizations (PNG, PDF)
├── docs/                         # Documentation and reports
│   ├── repo_structure.md         # This file
│   ├── problem_statement.md      # Formal problem definition
│   ├── lit_review_classical.md   # Classical TSP solver review
│   ├── lit_review_neural.md      # Neural TSP heuristic review
│   ├── lit_review_routing_tools.md # Road network tools survey
│   ├── model_architecture.md     # GNN architecture description
│   └── research_report.md        # Final research report
├── tests/                        # Unit and integration tests
├── sources.bib                   # BibTeX bibliography
├── requirements.txt              # Python dependencies
├── research_rubric.json          # Research progress tracker
└── README.md                     # Project overview and setup
```

### Directory Purposes

| Directory | Purpose |
|-----------|---------|
| `src/` | All Python source code organized by function |
| `src/data/` | Instance generation from OpenStreetMap/OSRM |
| `src/baselines/` | Wrappers for existing solvers (LKH-3, OR-Tools, construction heuristics) |
| `src/models/` | Neural network architectures (GNN edge scorer) |
| `src/training/` | Training pipelines and data preparation |
| `src/solvers/` | Novel hybrid solvers (GNN-LK, ALNS, traffic-aware, ensemble) |
| `src/evaluation/` | Benchmarking harness and metric computation |
| `data/` | Downloaded OSM data and intermediate files |
| `benchmarks/` | Standardized ATSP instances for evaluation |
| `models/` | Trained model checkpoints |
| `results/` | Experimental outputs (CSV tables, JSON summaries) |
| `figures/` | Publication-quality plots (PNG at 300 DPI, PDF) |
| `docs/` | Literature reviews, problem statement, final report |
| `tests/` | Automated tests for solver correctness |

# Module Map: TSP on Real Road Networks

## Directory Structure

### `src/`
Core Python modules for the research project.
- `src/data_pipeline.py` — OSRM/OSM data pipeline for generating asymmetric distance/duration matrices
- `src/baselines.py` — Baseline solver implementations (LKH-3, OR-Tools, nearest-neighbor, OSRM Trip)
- `src/metrics.py` — Evaluation metrics: tour cost, optimality gap, timing, memory
- `src/traffic_model.py` — Time-dependent and traffic-aware edge cost models
- `src/learned_candidates.py` — GNN-based candidate set generation for LKH
- `src/local_search.py` — RL-guided local search move selection for ATSP
- `src/hybrid_solver.py` — Hybrid solver combining learned candidates + LKH + RL local search
- `src/models/` — Neural network model definitions
  - `src/models/edge_scorer.py` — Directed GNN for edge-scoring on road-network graphs

### `data/`
Raw and processed data files. Cached OSRM responses, OSM extracts, and generated matrices.

### `benchmarks/`
Benchmark instance suite. Each instance includes coordinates, asymmetric cost matrices, and metadata.
- `benchmarks/README.md` — Description of each benchmark instance

### `models/`
Trained model checkpoints (PyTorch `.pt` files).

### `scripts/`
Executable scripts for running experiments.
- `scripts/run_benchmarks.py` — Benchmark runner harness
- `scripts/train_edge_scorer.py` — GNN training script
- `scripts/run_all.sh` — Full pipeline reproduction script

### `tests/`
Unit and integration tests for all modules.

### `docs/`
Research documentation, literature reviews, and design documents.
- `docs/lit_review_classical.md` — Classical TSP/ATSP solver survey
- `docs/lit_review_learned.md` — Learned and hybrid TSP heuristic survey
- `docs/data_survey.md` — Real-world ATSP datasets and OSRM pipeline survey
- `docs/problem_statement.md` — Formal problem statement and hypotheses
- `docs/model_architecture.md` — GNN edge-scorer architecture description
- `docs/rl_local_search.md` — RL local search design document
- `docs/limitations.md` — Limitations and future directions

### `results/`
Experimental results in CSV/JSON format and analysis documents.

### `figures/`
Publication-quality figures in PNG and PDF format.

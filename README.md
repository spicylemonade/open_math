# Tightening the Practical Polynomial-Time Approximation Ratio for Minimum Dominating Set on Planar Graphs

## Project Description

This research project investigates practical algorithms for the **Minimum Dominating Set (MDS)** problem on **planar graphs**, aiming to close the gap between theoretical PTAS results and practical constant-factor approximation algorithms.

While Baker's PTAS achieves a (1+2/k)-approximation ratio, its exponential dependence on k makes it impractical for large graphs. Standard greedy algorithms give O(log n) approximation even on planar graphs. We design and evaluate a novel hybrid algorithm combining:

- **Separator-based decomposition** (Lipton-Tarjan planar separators)
- **LP relaxation with planarity-exploiting valid inequalities**
- **k-swap local search post-processing**

Our goal is a practical O(n·polylog(n))-time algorithm achieving approximation ratio ≤ 5 on planar graphs.

## Directory Structure

```
src/           - Core algorithm implementations
tests/         - Unit and integration tests
data/          - Graph instance files (PACE format, generated instances)
docs/          - Research documents, proofs, and reports
benchmarks/    - Benchmark framework and experimental scripts
results/       - Experimental result JSON files
figures/       - Publication-quality figures (PNG + PDF)
```

## Modules

| Module | Purpose |
|--------|---------|
| `src/graph.py` | Planar graph data structures, generators, and loaders |
| `src/greedy.py` | Baseline greedy and modified-greedy MDS algorithms |
| `src/lp_solver.py` | LP/ILP relaxation-based MDS solver with rounding |
| `src/baker_ptas.py` | Baker's PTAS for MDS on planar graphs |
| `src/separator_mds.py` | Novel separator-based MDS algorithm |
| `src/planar_lp.py` | Enhanced LP rounding exploiting planarity |
| `src/local_search.py` | k-swap local search post-processing |
| `src/hybrid_mds.py` | Hybrid pipeline combining all approaches |

## Quick Start

```bash
pip install -r requirements.txt
make test        # Run all tests
make benchmark   # Run benchmark suite
make figures     # Generate publication figures
```

## Reproducibility

All random generators use fixed seed (42). Results can be reproduced via:
```bash
make install && make test && make benchmark && make figures
```

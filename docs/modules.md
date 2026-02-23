# Module Descriptions

## Core Algorithm Modules (`src/`)

### `src/graph.py` — Graph Data Structures and Generators
- Adjacency-list `Graph` class with node/edge operations
- Planarity testing via Boyer-Myrvold (wrapping NetworkX)
- Random planar graph generators: triangulation, Delaunay-based, grid-based
- PACE 2025 `.gr` format file loader
- Utility functions: BFS, connected components, degree statistics

### `src/greedy.py` — Baseline Greedy Algorithms
- Standard greedy MDS: repeatedly select highest-degree undominated vertex
- Modified greedy with degree-ratio selection (Jones et al. variant)
- Domination validity checker

### `src/lp_solver.py` — LP/ILP Relaxation Solver
- LP relaxation of MDS ILP formulation using PuLP
- Deterministic rounding schemes (threshold-based)
- Exact ILP solver for small instances (≤ 500 nodes) to compute OPT
- LP lower bound computation

### `src/baker_ptas.py` — Baker's PTAS
- BFS-layering decomposition into k-outerplanar subgraphs
- Dynamic programming on tree decompositions for exact sub-solutions
- Configurable parameter k for ratio/runtime trade-off

### `src/separator_mds.py` — Novel Separator-Based Algorithm
- Lipton-Tarjan planar separator computation
- Recursive decomposition with exact base-case solving
- Merge strategy for combining sub-solutions across separators

### `src/planar_lp.py` — Enhanced Planar LP Rounding
- LP with planar-specific valid inequalities (face-based, Euler formula)
- Tighter rounding scheme exploiting bounded planar integrality gap

### `src/local_search.py` — Local Search Post-Processing
- 1-swap: remove redundant vertices from dominating set
- 2-swap: replace pairs of vertices with single vertices
- Configurable iteration limit and convergence criterion

### `src/hybrid_mds.py` — Hybrid Pipeline
- Full pipeline: LP → separator-based rounding → local search
- Configurable parameters for all sub-components
- Best-of-all selection among individual algorithm outputs

## Test Modules (`tests/`)

### `tests/test_graph.py` — Graph module tests
### `tests/test_greedy.py` — Greedy algorithm tests
### `tests/test_lp_solver.py` — LP solver tests
### `tests/test_baker_ptas.py` — Baker PTAS tests
### `tests/test_separator_mds.py` — Separator algorithm tests
### `tests/test_local_search.py` — Local search tests
### `tests/test_hybrid_mds.py` — Integration tests

## Benchmark Framework (`benchmarks/`)

### `benchmarks/run_all.py` — Full benchmark execution
### `benchmarks/analysis.py` — Statistical analysis of results
### `benchmarks/scalability.json` — Scalability experiment results

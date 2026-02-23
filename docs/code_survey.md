# Code Survey: Open-Source MDS Implementations and Graph Libraries

## 1. NetworkX Dominating Set Module

- **URL:** https://networkx.org/documentation/stable/reference/algorithms/dominating.html
- **Language:** Python
- **Algorithmic Approach:**
  - `networkx.algorithms.dominating.dominating_set`: Greedy heuristic that finds *a* dominating set (not necessarily minimum). Iteratively selects undominated vertices.
  - `networkx.algorithms.approximation.dominating_set.min_weighted_dominating_set`: Greedy set-cover-style approximation. Gives O(log n) approximation ratio. Runs in O(m) time.
  - `networkx.algorithms.approximation.dominating_set.min_edge_dominating_set`: Edge dominating set approximation.
- **Performance:** Fast (linear time for greedy), but no planarity-aware optimization. Approximation guarantee is O(log Δ).
- **License:** BSD 3-Clause
- **Relevance:** Provides baseline greedy implementation and graph infrastructure we can wrap/extend.

## 2. PACE 2025 Solver: Bad Dominating Set Maker (Dobler, Fink, Rocton)

- **URL:** https://github.com/Doblalex/pace2025
- **Language:** C++ (with Python wrapper possible)
- **Algorithmic Approach:**
  - Reduction rules (crown, twin, pendant, LP-based)
  - Tree decomposition with bounded width (≤ 13) for DP
  - MaxSAT fallback via EvalMaxSat for remaining hard instances
- **Performance:** Exact solver; solves PACE 2025 instances (including planar/OSM graphs) within 30-minute time limit. Particularly effective on structured instances.
- **License:** Open source (PACE requirement)
- **Relevance:** State-of-the-art exact solver. Tree decomposition DP approach can be adapted for our Baker's PTAS base case.

## 3. PACE 2025 Solver: UzL Solver (Bannach, Chudigiewitsch, Wienöbst)

- **URL:** https://github.com/mwien/PACE2025
- **Language:** Rust
- **Algorithmic Approach:**
  - MaxSAT formulation of MDS
  - Hitting-set-based reduction rules
  - Clique solver for small vertex cover instances
- **Performance:** Competitive exact solver in PACE 2025. Efficient on sparse/structured graphs.
- **License:** Open source (PACE requirement)
- **Relevance:** MaxSAT approach provides alternative exact solving strategy for validation.

## 4. OGDF — Open Graph Drawing Framework

- **URL:** https://github.com/ogdf/ogdf
- **Language:** C++
- **Algorithmic Approach:**
  - Extensive planar graph infrastructure: linear-time planarity testing (Boyer-Myrvold), planar embedding, SPQR-trees, BC-trees
  - Graph augmentation, crossing minimization, planar separator computation
  - No built-in dominating set solver, but provides the graph decomposition primitives needed to implement one
- **Performance:** Highly optimized C++ with efficient data structures for planar graphs.
- **License:** GPL v2/v3
- **Relevance:** Provides planar separator computation and tree decomposition that we could wrap from Python, though for our purposes NetworkX suffices.

## 5. AWS Labs: Minimum Dominating Set with OR-Tools

- **URL:** https://github.com/awslabs/minimum-dominating-set-with-ortools
- **Language:** Python (using Google OR-Tools)
- **Algorithmic Approach:**
  - ILP formulation of MDS with group constraints
  - Uses OR-Tools CP-SAT or MIP solver
  - Binary variables per vertex, domination constraints
- **Performance:** Exact ILP solver. Effective for small-to-medium instances.
- **License:** Apache 2.0
- **Relevance:** Ready-made ILP formulation that can be adapted. We use PuLP instead for consistency.

## 6. PuLP — LP/ILP Modeling Library

- **URL:** https://github.com/coin-or/pulp
- **Language:** Python
- **Algorithmic Approach:**
  - General-purpose LP/ILP modeler
  - Default solver: COIN-OR CBC (included)
  - Supports GLPK, CPLEX, Gurobi, HiGHS, SCIP
- **Performance:** CBC solver handles ILP instances up to ~10,000 variables efficiently.
- **License:** BSD
- **Relevance:** Our primary tool for LP relaxation and exact ILP solving on small instances.

## 7. PACE 2025 Instance Repository

- **URL:** https://github.com/MarioGrobler/PACE2025-instances
- **Language:** N/A (data files)
- **Format:** PACE `.gr` format (DIMACS-like: `p ds <n> <m>` header, `<u> <v>` edge lines)
- **Content:** Public exact instances with structural properties similar to private evaluation instances. Includes planar (OSM-derived) graphs.
- **License:** Open (competition data)
- **Relevance:** Benchmark instances for evaluating our algorithms against PACE 2025 participants.

## Summary Table

| Implementation | Language | Approach | Exact? | Planar-Aware? | License |
|---------------|----------|----------|--------|---------------|---------|
| NetworkX dominating_set | Python | Greedy | No | No | BSD |
| Bad DS Maker (PACE) | C++ | Reduction + TD-DP + MaxSAT | Yes | Partially | Open |
| UzL Solver (PACE) | Rust | MaxSAT + Reductions | Yes | Partially | Open |
| OGDF | C++ | Planar infrastructure | N/A | Yes | GPL |
| AWS Labs OR-Tools | Python | ILP (OR-Tools) | Yes | No | Apache 2.0 |
| PuLP + CBC | Python | LP/ILP modeling | Yes (ILP) | No | BSD |

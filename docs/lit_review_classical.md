# Literature Review: Classical TSP/ATSP Solvers

## Overview
Brief overview of the state of classical exact and heuristic solvers for TSP and ATSP.

## Summary Table

| Solver | Type | Key Algorithm | Problem Variants | Best Known Results | Limitations on Road Networks |
|--------|------|---------------|------------------|-------------------|------------------------------|
| Concorde | Exact | Branch-and-cut with LP relaxation | Symmetric TSP only | Solved pla85900 (85,900 cities) optimally | Cannot handle asymmetric costs natively; requires ATSP-to-STSP transformation doubling problem size |
| LKH-3 | Heuristic | Variable-depth k-opt local search (Lin-Kernighan) | TSP, ATSP, CVRP, TSPTW, many VRP variants | Near-optimal on TSPLIB instances up to millions of nodes | ATSP solved via Jonker-Volgenant transformation; road-network-specific features (traffic, turns) not modeled |
| OR-Tools | Heuristic/Meta | Guided local search, simulated annealing, tabu search | VRP, CVRP, VRPTW, ATSP natively | Practical quality on industrial VRP instances | General-purpose; may not exploit road network structure; no learned components |
| Lin-Kernighan (1973) | Heuristic | Variable-depth edge exchanges (k-opt) | Symmetric TSP | Foundation for all LK-based methods | Original formulation symmetric only; requires adaptation for ATSP |
| Christofides (1976) | Approx | Minimum spanning tree + matching | Symmetric metric TSP | 3/2-approximation guarantee | Requires metric (triangle inequality); fails on asymmetric road networks |

## Detailed Reviews

### 1. Concorde (Applegate, Bixby, Chvátal, Cook, 2006)
- **Algorithm**: Branch-and-cut with cutting planes from LP relaxation. Uses Chained Lin-Kernighan for initial tours.
- **Strengths**: Exact solver, can prove optimality. Solved instances with 85,900 cities.
- **ATSP handling**: Cannot handle ATSP directly. Requires doubling transformation that doubles problem size.
- **Road network limitations**: Designed for Euclidean/symmetric instances. No support for one-way streets, turn penalties, or traffic.
- **Reference**: Applegate et al. (2006), "The Traveling Salesman Problem: A Computational Study"

### 2. LKH-3 (Helsgaun, 2017)
- **Algorithm**: Extension of Lin-Kernighan-Helsgaun with variable-depth k-opt moves. Uses candidate edge lists based on alpha-nearness. Handles ATSP via Jonker-Volgenant transformation to symmetric TSP.
- **Strengths**: State-of-the-art heuristic quality for TSP and many variants. Handles ATSP, TSP with time windows, and many VRP variants.
- **ATSP handling**: Transforms ATSP to symmetric TSP using well-known doubling construction. This increases problem size but preserves optimal tour.
- **Road network limitations**: Candidate edge selection based on alpha-nearness assumes geometric structure. Road network asymmetry may not be well-captured by the transformation.
- **Reference**: Helsgaun (2017), "An Extension of the Lin-Kernighan-Helsgaun TSP Solver for Constrained Traveling Salesman and Vehicle Routing Problems"

### 3. Google OR-Tools (Perron, Furnon, 2023)
- **Algorithm**: Constraint programming with local search. Uses first-solution strategies (cheapest arc, savings) followed by metaheuristics (guided local search, simulated annealing, tabu search).
- **Strengths**: Industrial-grade solver. Natively supports asymmetric costs, time windows, capacity constraints. Highly configurable.
- **ATSP handling**: Native support for asymmetric cost matrices. No transformation needed.
- **Road network limitations**: General-purpose solver without road-network-specific optimizations. Does not learn from instance structure.
- **Reference**: Perron and Furnon (2023), "OR-Tools' Vehicle Routing Solver: A Generic Constraint-Programming Solver with Heuristic Search for Routing Problems"

### 4. Lin-Kernighan (1973) - Original
- **Algorithm**: Variable-depth local search. At each step, attempts to improve the tour by exchanging sequences of edges (k-opt moves) guided by a gain criterion.
- **Strengths**: Foundation of all modern LK-based methods. Elegant gain criterion prunes search effectively.
- **Limitations**: Original formulation is for symmetric TSP only. Modern extensions (LKH) needed for ATSP.
- **Reference**: Lin and Kernighan (1973), "An Effective Heuristic Algorithm for the Traveling-Salesman Problem"

### 5. Jonker-Volgenant ATSP Transformation
- **Algorithm**: Transforms an n-city ATSP into a 2n-city symmetric TSP by creating dummy nodes. Each city i is paired with a dummy i', with c(i,i') = -M (large negative) to force pairing, and inter-dummy costs derived from the asymmetric matrix.
- **Strengths**: Allows any symmetric TSP solver to handle ATSP. Preserves optimal solution.
- **Limitations**: Doubles problem size. Candidate edge structures designed for geometric instances may perform poorly on the artificial symmetric instance.
- **Reference**: Jonker and Volgenant (1983), "Transforming asymmetric into symmetric traveling salesman problems"

## Key Gaps for Road Network TSP
1. Classical solvers treat costs as static numbers; road networks have time-dependent costs
2. Candidate edge selection (alpha-nearness in LKH) assumes geometric structure lost in ATSP transformation
3. No exploitation of road network topology (highway hierarchy, grid vs radial structure)
4. General-purpose solvers (OR-Tools) don't learn from distribution of similar instances

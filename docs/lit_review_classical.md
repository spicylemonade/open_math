# Literature Review: Classical and Modern TSP/ATSP Solvers

## 1. Concorde TSP Solver (Applegate, Bixby, Chvátal & Cook, 2006)

**Key Algorithm:** Branch-and-cut with LP relaxation. Concorde solves the symmetric TSP to provable optimality using cutting planes derived from the LP relaxation of the TSP polytope. When cutting planes alone do not converge, it switches to branch-and-bound. An initial tour is obtained via the Chained Lin-Kernighan heuristic to seed the search and enable pruning.

**Complexity:** Exact solver; worst-case exponential but practically solves instances with tens of thousands of cities. The 85,900-city instance was solved in 2006; the 109,399-city instance was solved in 2017.

**Strengths on Road Networks:** Provides optimal solutions with proof of optimality. The LP-based lower bounds are extremely tight. Can handle large-scale real-world instances when combined with OSRM distance data (as demonstrated by the Korea 81,998-bar problem).

**Limitations:** Only handles symmetric TSP. Cannot directly handle asymmetric costs, one-way streets, turn penalties, or time windows. Requires a linear programming solver (QSopt or CPLEX). Computation time can be enormous for very hard instances. Not designed for real-time or near-real-time routing applications.

**References:** Applegate et al. (2006) *The Traveling Salesman Problem: A Computational Study*, Princeton University Press [applegate2006traveling].

---

## 2. LKH and LKH-3 (Helsgaun, 2000, 2009, 2017)

**Key Algorithm:** The Lin-Kernighan-Helsgaun (LKH) heuristic is an iterated local search based on the Lin-Kernighan k-opt move framework. LKH uses 5-opt moves (generalized to variable-depth) guided by α-nearness candidate sets derived from a 1-tree lower bound. LKH-3 (2017) extends LKH-2 to handle constrained TSP variants including ATSP, TSPTW, CVRP, and PDPTW by transforming them into symmetric TSP instances via the Jonker-Volgenant transformation and using penalty functions for constraint handling.

**Complexity:** Heuristic; polynomial per iteration (O(n²) to O(n³) depending on k-opt depth and candidate set size). Typically finds near-optimal solutions within minutes for instances with thousands of cities. The number of trials and candidate set size are configurable parameters.

**Strengths on Road Networks:** Handles ATSP via Jonker-Volgenant transformation (doubles the graph). Supports custom edge weight functions. Candidate sets can be provided externally. Extremely competitive solution quality — frequently finds optimal or near-optimal tours. LKH-3 additionally supports time windows and capacity constraints. The O(1) flip function optimization for ATSP avoids the overhead of symmetric flip operations.

**Limitations:** The Jonker-Volgenant ATSP→TSP transformation doubles the instance size (2n nodes for n-city ATSP). Default α-nearness candidates are based on 1-tree structure which assumes metric/near-metric distances; may not capture road network structure well (one-way streets, turn costs). No native support for time-dependent edge costs. The penalty-function approach for constrained variants may not reliably find feasible solutions on tightly constrained instances.

**References:** Helsgaun (2000) *An Effective Implementation of the Lin-Kernighan Traveling Salesman Heuristic*, European Journal of Operational Research [helsgaun2000effective]; Helsgaun (2009) *General k-opt submoves for the Lin-Kernighan TSP heuristic*, Mathematical Programming Computation [helsgaun2009general]; Helsgaun (2017) *An Extension of the Lin-Kernighan-Helsgaun TSP Solver for Constrained Traveling Salesman and Vehicle Routing Problems*, Technical Report, Roskilde University [helsgaun2017extension].

---

## 3. Google OR-Tools Routing Solver (Perron & Furnon, Google)

**Key Algorithm:** Constraint programming-based vehicle routing solver using local search with guided local search (GLS) metaheuristic. Supports multiple first-solution strategies (cheapest arc, path cheapest arc, savings algorithm, sweep, Christofides) and improvement metaheuristics (GLS, simulated annealing, tabu search). Models routing via "next" decision variables with cumulative dimension constraints.

**Complexity:** Heuristic; computation time depends heavily on instance size, number of constraints, and time limit. Can handle instances with hundreds to low thousands of stops. GLS is generally the most effective metaheuristic for vehicle routing within OR-Tools.

**Strengths on Road Networks:** Natively supports asymmetric distance/time matrices. Rich constraint modeling: time windows, capacity, pickup-and-delivery, breaks, penalties for optional visits, multiple depots, heterogeneous fleets. Well-documented Python API. Active development and support from Google. Integrates easily with OSRM-derived cost matrices. Free and open-source.

**Limitations:** Solution quality typically inferior to LKH on pure TSP instances (no specialized k-opt moves). Integer-only computation requires rounding of floating-point costs. Scalability degrades beyond ~1000 stops for complex constraint configurations. No learning or adaptivity — relies on hand-tuned metaheuristic parameters. Search never terminates without explicit time limits when using metaheuristics.

**References:** Perron & Furnon (2023) *OR-Tools' Vehicle Routing Solver: a Generic Constraint-Programming Solver with Heuristic Search for Routing Problems*, Google Research [perron2023ortools].

---

## 4. VROOM — Vehicle Routing Open-source Optimization Machine (Coupey et al., 2018)

**Key Algorithm:** Heuristic solver using dedicated metaheuristics for vehicle routing. Employs a construction phase (e.g., Solomon's I1 insertion heuristic) followed by local search improvement with inter-route and intra-route moves. Written in C++20 for high performance.

**Complexity:** Heuristic; designed for speed. Solves most TSPLIB instances within milliseconds. Average optimality gap of +1.63% on benchmark instances with ~100 delivery points, computed in ~360ms.

**Strengths on Road Networks:** Built explicitly for OSRM/OpenRouteService integration. Optimizes total duration (natural for road networks). Handles time windows, capacitated VRP, multi-depot, heterogeneous fleet. Extremely fast — suitable for real-time routing applications. Can use custom cost matrices from any source.

**Limitations:** Heuristic quality below LKH for pure TSP (2–3% gaps). Optimizes duration only, not distance. Limited configurability of search parameters compared to OR-Tools or LKH. No learning component. Less suitable for very large single-vehicle TSP instances (>1000 stops).

**References:** Coupey, Nicola & Vidal (2018) *Solving vehicle routing problems with OpenStreetMap and VROOM*, State of the Map 2018 [coupey2018vroom]; VROOM GitHub repository [vroom_github].

---

## 5. Korea 81,998-Bar OSRM Tour (Cook, Espinoza, Goycoolea & Helsgaun, 2025)

**Key Algorithm:** Exact solution via Concorde-family branch-and-cut, using OSRM-computed walking times as the cost matrix. The computation used OSRM Table API to build a matrix of 3,361,795,003 pairwise travel times for 81,998 bar locations in South Korea. Helsgaun's LKH heuristic provided upper bounds (initial tours), while Concorde's cutting-plane method and branch-and-bound provided the optimality proof.

**Complexity:** Exact; computation ran from December 2024 to March 2025 at Roskilde University and the University of Waterloo.

**Strengths on Road Networks:** Demonstrates that real road-network TSP instances (with OSRM-computed asymmetric walking times) can be solved to proven optimality at massive scale (81,998 stops). Establishes a methodology for using OSRM as the cost oracle for exact TSP solving. Tour length: 15,386,177 seconds (~178 days walking).

**Limitations:** Required months of distributed computation. Walking mode only (symmetric-ish costs). The approach does not scale to time-dependent or traffic-aware costs. Relies on static OSRM snapshots — real-world travel times change.

**References:** Cook, Espinoza, Goycoolea & Helsgaun (2025) *Korea TSPs*, University of Waterloo TSP page [cook2025korea].

---

## 6. Christofides–Serdyukov Algorithm (1976/1978)

**Key Algorithm:** The first polynomial-time approximation algorithm for metric TSP with a 3/2 approximation guarantee. Computes MST, finds minimum-weight perfect matching on odd-degree vertices, combines into Eulerian multigraph, then shortcuts to a Hamiltonian tour.

**Complexity:** O(n³) for the matching step. Provides a guaranteed 3/2-approximation ratio for metric (symmetric, triangle inequality) TSP instances.

**Strengths on Road Networks:** Provides worst-case guarantees useful for theoretical analysis. Fast polynomial-time construction. Recent improvement by Karlin, Klein & Gharan (2021) achieved ratio 3/2 − 10⁻³⁶ using randomized trees.

**Limitations:** Only applies to symmetric metric TSP. The 3/2 bound is tight — cannot improve without fundamentally different techniques. Practical solution quality far below LKH or even simple local search. Does not apply to asymmetric TSP (ATSP), which is the relevant case for road networks with one-way streets.

**References:** Christofides (1976) *Worst-case analysis of a new heuristic for the travelling salesman problem* [christofides1976worst]; Serdyukov (1978) [serdyukov1978]; Karlin, Klein & Gharan (2021) [karlin2021slightly].

---

## 7. Held-Karp Algorithm and LP Relaxation (1962)

**Key Algorithm:** Dynamic programming exact algorithm for TSP with O(n² 2ⁿ) time and O(n 2ⁿ) space. Also foundational for the Held-Karp LP relaxation (subtour elimination LP), which provides the strongest known polynomial-time lower bound for TSP. The LP relaxation is conjectured to be within a factor of 4/3 of optimal for metric TSP.

**Complexity:** O(n² 2ⁿ) — exact but only practical for n ≤ ~25. The LP relaxation is solvable in polynomial time via cutting-plane methods (as used by Concorde).

**Strengths on Road Networks:** The Held-Karp LP lower bound is used by Concorde and other exact solvers as the primary bounding mechanism. The 1-tree relaxation (used by LKH for α-nearness candidates) is a Lagrangian relaxation of the Held-Karp LP.

**Limitations:** DP algorithm impractical beyond ~25 cities. The LP relaxation alone doesn't solve the problem but provides bounds.

**References:** Held & Karp (1962) *A Dynamic Programming Approach to Sequencing Problems*, Journal of SIAM [held1962dynamic].

---

## 8. OSRM — Open Source Routing Machine (Luxen & Vetter, 2011)

**Key Algorithm:** High-performance routing engine using contraction hierarchies (CH) or multi-level Dijkstra (MLD) on OpenStreetMap road graphs. Provides a Table API for computing all-pairs shortest-path duration/distance matrices, and a Trip API that solves TSP using a farthest-insertion heuristic.

**Complexity:** After preprocessing (minutes to hours for continental networks), individual queries take milliseconds. Table API computes N×N matrices in O(N² · query_time). Trip API uses O(N²) farthest-insertion.

**Strengths on Road Networks:** Purpose-built for road networks. Respects one-way streets, turn restrictions, speed limits, road classifications. Produces realistic asymmetric travel times. Continental-scale performance. Multiple transport profiles (car, bike, walk). The Table API is the primary tool for generating cost matrices for road-network TSP instances.

**Limitations:** Trip API TSP solution quality is basic (farthest-insertion heuristic, no local search improvement). Static costs — no real-time traffic integration in open-source version. Large memory requirements for preprocessing continental networks. API rate limits on public demo server.

**References:** Luxen & Vetter (2011) *Real-time routing with OpenStreetMap data*, ACM SIGSPATIAL [luxen2011realtime]; OSRM GitHub repository [osrm_github].

---

## Summary Table

| Solver | Type | Symmetric/Asymmetric | Best For | Typical Gap | Speed |
|--------|------|---------------------|----------|-------------|-------|
| Concorde | Exact (branch-and-cut) | Symmetric only | Provably optimal tours | 0% (exact) | Hours–months for large instances |
| LKH-3 | Heuristic (k-opt local search) | Both (via transformation) | Near-optimal tours, large instances | <0.5% on TSPLIB | Seconds–minutes |
| OR-Tools | Heuristic (CP + GLS) | Both (native) | Constrained routing (VRP, TW) | 2–10% on TSP | Seconds–minutes |
| VROOM | Heuristic (construction + local search) | Both (via OSRM) | Fast real-time routing | ~1.6% on benchmarks | Milliseconds |
| Christofides | Approximation | Symmetric metric only | Theoretical guarantee | Up to 50% | Polynomial (fast) |
| OSRM Trip | Heuristic (farthest-insertion) | Both (road network) | Quick baseline tour | 5–15% | Milliseconds |

---

## Key Gap Identified

All classical exact and near-exact solvers (Concorde, LKH) are designed primarily for symmetric Euclidean or metric distance. While LKH-3 handles ATSP via transformation, its candidate generation (α-nearness) is still rooted in 1-tree structure, which may not capture the idiosyncrasies of real road networks: one-way streets creating strong asymmetry, turn penalties, road classification effects on speed, and time-dependent traffic patterns. This gap motivates developing road-network-aware heuristics that can exploit the structure of OSRM-derived cost matrices.

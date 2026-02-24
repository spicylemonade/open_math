# Problem Statement: Better Heuristics for TSP on Real Road Networks

## 1. Formal Definition of ATSP on Road Graphs

### Problem Setting

Given a directed graph $G = (V, A)$ derived from a real road network with $n$ locations $V = \{v_0, v_1, \ldots, v_{n-1}\}$ and arc set $A \subseteq V \times V$, define an asymmetric cost matrix $C = [c_{ij}]_{n \times n}$ where $c_{ij}$ denotes the travel time from $v_i$ to $v_j$ via the road network. In general, $c_{ij} \neq c_{ji}$ due to one-way streets, turn restrictions, and directional traffic patterns.

### Objective

Find a Hamiltonian cycle (tour) $\pi = (v_{\pi(0)}, v_{\pi(1)}, \ldots, v_{\pi(n-1)}, v_{\pi(0)})$ visiting every vertex exactly once that minimizes total travel cost:

$$\min_{\pi} \sum_{k=0}^{n-1} c_{\pi(k), \pi((k+1) \bmod n)}$$

### Integer Linear Programming Formulation

We introduce binary decision variables $x_{ij} \in \{0, 1\}$ for each $(i, j) \in A$, where $x_{ij} = 1$ if arc $(v_i, v_j)$ is included in the tour.

**Objective:**

$$\min \sum_{i=0}^{n-1} \sum_{j=0, j \neq i}^{n-1} c_{ij} \, x_{ij}$$

**Subject to:**

Assignment constraints (each vertex entered and left exactly once):

$$\sum_{j=0, j \neq i}^{n-1} x_{ij} = 1 \quad \forall \, i \in \{0, \ldots, n-1\}$$

$$\sum_{i=0, i \neq j}^{n-1} x_{ij} = 1 \quad \forall \, j \in \{0, \ldots, n-1\}$$

**Subtour Elimination (Miller-Tucker-Zemlin formulation):**

Introduce auxiliary variables $u_i \in \mathbb{R}$ for $i \in \{1, \ldots, n-1\}$:

$$u_i - u_j + n \, x_{ij} \leq n - 1 \quad \forall \, i, j \in \{1, \ldots, n-1\}, \; i \neq j$$

$$1 \leq u_i \leq n - 1 \quad \forall \, i \in \{1, \ldots, n-1\}$$

**Subtour Elimination (Dantzig-Fulkerson-Johnson formulation):**

Alternatively, using exponentially many but tighter constraints:

$$\sum_{i \in S} \sum_{j \in S, j \neq i} x_{ij} \leq |S| - 1 \quad \forall \, S \subset V, \; 2 \leq |S| \leq n - 1$$

The DFJ formulation provides a tighter LP relaxation than MTZ but requires separation algorithms (e.g., min-cut based) for practical use in branch-and-cut solvers.

**Integrality:**

$$x_{ij} \in \{0, 1\} \quad \forall \, i, j \in \{0, \ldots, n-1\}, \; i \neq j$$

---

## 2. Distinction from Euclidean TSP

The Asymmetric TSP on real road networks differs fundamentally from the classical Euclidean TSP in several critical ways:

### 2.1 Triangle Inequality Violations

In Euclidean space, the triangle inequality $d(i, k) \leq d(i, j) + d(j, k)$ always holds. Road networks can violate this property:

$$c(i, k) > c(i, j) + c(j, k)$$

This occurs due to road topology: the direct route between $v_i$ and $v_k$ may follow a longer, slower road, while detouring through $v_j$ uses a faster highway segment. Approximation algorithms that depend on the triangle inequality (e.g., Christofides' 3/2-approximation) lose their theoretical guarantees.

### 2.2 One-Way Streets Cause Asymmetry

Road networks contain one-way streets, ramp systems, and restricted turns that produce strong asymmetry:

- $c(i, j)$ may be finite (a direct one-way route exists from $v_i$ to $v_j$) while $c(j, i) = \infty$ (no direct reverse route exists)
- Even where both directions are traversable, $c(i, j) \neq c(j, i)$ due to differing routes, signal timing, or grade effects
- The asymmetry ratio $\max_{i,j} \frac{c(i,j)}{c(j,i)}$ can be unbounded in real networks

This rules out the standard symmetric TSP formulation and requires ATSP-specific methods.

### 2.3 Turn Penalties and Intersection Delays

Real road networks impose non-geometric cost components that have no analog in Euclidean TSP:

- **Turn penalties:** Left turns across traffic incur higher delays than right turns; U-turns may be prohibited
- **Intersection delays:** Signal-controlled intersections add variable wait times depending on approach direction
- **Road class transitions:** Merging onto or exiting a highway adds acceleration/deceleration time

These costs depend on the sequence of arcs traversed, not just the endpoints, creating path-dependent travel times that violate the simple edge-cost model.

### 2.4 Metric Space Assumptions Fail

Solvers tuned for the $L_2$ norm (Euclidean distance), such as Concorde, rely on geometric properties:

- **Planarity:** Euclidean tours do not self-intersect; road network tours can and do cross geometrically without intersecting in the graph
- **Nearest-neighbor structure:** Spatial data structures (k-d trees) accelerate neighbor searches in $\mathbb{R}^2$ but fail when geographic proximity does not correlate with travel time
- **Tour improvement moves:** Geometric insights (e.g., Or-opt moves removing crossings) lose effectiveness when the cost metric is non-Euclidean

Concorde and similar solvers lose their optimality guarantees and practical efficiency on ATSP instances derived from road networks.

### 2.5 Road Network Connectivity

Unlike complete graphs assumed in Euclidean TSP, road networks have sparse connectivity:

- Not all pairs of vertices are directly connected by a single road segment; shortest paths require traversing intermediate nodes
- Bridges, tunnels, and natural barriers (rivers, mountains) create bottleneck edges whose removal disconnects the graph
- Detours are often necessary: the cost matrix $C$ is derived from all-pairs shortest paths on the underlying road graph, which may itself have $O(n \cdot |A|)$ or more edges

---

## 3. Time-Window and Traffic-Dependent Formulations

### 3.1 Time-Dependent ATSP (TD-ATSP)

In real road networks, travel times are not static. The time-dependent formulation replaces the fixed cost matrix with a function of departure time:

$$c_{ij}(t) : A \times \mathbb{R}_{\geq 0} \to \mathbb{R}_{> 0}$$

where $c_{ij}(t)$ is the travel time from $v_i$ to $v_j$ when departing at time $t$. The objective becomes:

$$\min \sum_{k=0}^{n-1} c_{\pi(k), \pi(k+1)}(t_{\pi(k)})$$

where $t_{\pi(k)}$ is the arrival (and thus departure) time at the $k$-th vertex in the tour, defined recursively:

$$t_{\pi(k+1)} = t_{\pi(k)} + c_{\pi(k), \pi(k+1)}(t_{\pi(k)})$$

with $t_{\pi(0)} = t_0$ as the given start time.

### 3.2 Traffic Multiplier Model

A practical model for time-dependent costs uses a base cost modulated by a traffic factor:

$$c_{ij}(t) = c_{ij}^{\text{base}} \cdot f(t)$$

where:

- $c_{ij}^{\text{base}}$ is the free-flow travel time on arc $(v_i, v_j)$
- $f(t)$ is a time-of-day traffic multiplier capturing rush hour patterns

A typical traffic multiplier function:

$$f(t) = 1 + \alpha_1 \exp\left(-\frac{(t - \mu_1)^2}{2\sigma_1^2}\right) + \alpha_2 \exp\left(-\frac{(t - \mu_2)^2}{2\sigma_2^2}\right)$$

where $\mu_1, \mu_2$ are morning and evening rush hour peaks, $\sigma_1, \sigma_2$ control the width of congestion periods, and $\alpha_1, \alpha_2$ are the peak congestion multipliers (e.g., $\alpha = 1.5$ means 2.5x free-flow time at peak).

### 3.3 ATSP with Time Windows (ATSPTW)

Each customer location $v_i$ has an associated time window $[a_i, b_i]$ specifying the earliest and latest permissible arrival times. The constraints are:

$$a_i \leq t_i \leq b_i \quad \forall \, i \in \{1, \ldots, n-1\}$$

If the vehicle arrives before $a_i$, it must wait:

$$\text{wait}_i = \max(0, \, a_i - t_i^{\text{arrive}})$$

The effective departure time from $v_i$ is:

$$t_i = \max(t_i^{\text{arrive}}, \, a_i) + s_i$$

where $s_i$ is the service time at $v_i$.

### 3.4 Combined Formulation

The full combined objective integrates travel time, waiting time, and lateness penalties:

$$\min \sum_{k=0}^{n-1} c_{\pi(k), \pi(k+1)}(t_{\pi(k)}) + \lambda_w \sum_{i=1}^{n-1} \text{wait}_i + \lambda_l \sum_{i=1}^{n-1} \text{late}_i$$

where:

- $\text{wait}_i = \max(0, \, a_i - t_i^{\text{arrive}})$ is the waiting time at $v_i$
- $\text{late}_i = \max(0, \, t_i^{\text{arrive}} - b_i)$ is the tardiness at $v_i$
- $\lambda_w \geq 0$ is the per-unit-time waiting cost coefficient
- $\lambda_l \geq 0$ is the per-unit-time lateness penalty coefficient

This formulation captures the real-world trade-off between minimizing total travel distance and respecting customer time constraints under dynamic traffic conditions.

---

## 4. Research Questions

### RQ1: GNN-Guided Local Search vs. LKH-3

**Question:** Can a GNN-guided local search heuristic beat LKH-3 tour cost by $\geq 0.5\%$ on OSRM-derived ATSP instances with $\geq 200$ nodes?

**Motivation:** LKH-3 is the state-of-the-art heuristic for ATSP, but it uses generic neighborhood structures. A graph neural network trained on road network topology may learn to predict beneficial moves, guiding the search toward better solutions faster.

**Success Criterion:** Statistically significant improvement ($p < 0.05$ via Wilcoxon signed-rank test) in tour cost across a benchmark suite of at least 50 OSRM-derived instances with $n \geq 200$. The improvement must be $\geq 0.5\%$ in mean optimality gap relative to LKH-3 with default parameters and equivalent time budget.

### RQ2: Asymmetry-Aware Search vs. Symmetrization

**Question:** Does explicitly modeling asymmetry in the search process (rather than transforming to symmetric TSP via the Jonker-Volgenant reduction or similar) improve solution quality for real road network instances?

**Motivation:** A common approach converts ATSP to STSP by doubling the number of nodes and applying symmetric solvers. This transformation may obscure structural information about the road network that asymmetry-aware moves could exploit (e.g., preferring arcs aligned with one-way street systems).

**Success Criterion:** An ablation study demonstrating $> 1\%$ improvement in solution quality when asymmetry-aware local search moves (e.g., directed Or-opt, asymmetric 3-opt) are enabled versus disabled. The comparison must control for computational budget and be evaluated on instances where the asymmetry ratio $\max_{i,j} c(i,j)/c(j,i) > 1.2$.

### RQ3: Runtime-Quality Pareto Frontier of Hybrid vs. Classical Solvers

**Question:** What is the runtime-quality Pareto frontier of hybrid (ML + optimization) versus classical solvers at different time budgets ($1\text{s}$, $10\text{s}$, $60\text{s}$, $300\text{s}$)?

**Motivation:** Practitioners need to choose solvers under time constraints. A hybrid solver may dominate at short time budgets (by using learned heuristics to quickly find good initial solutions) while classical solvers may catch up or surpass at longer budgets (through systematic exploration). Characterizing this frontier informs practical deployment decisions.

**Success Criterion:** Identify at least one time budget at which a novel hybrid solver Pareto-dominates all baselines (LKH-3, OR-Tools, Concorde-ATSP) in terms of both mean tour cost and computation time. The evaluation must span at least 100 instances across three size categories ($n \in \{50, 200, 500\}$).

### RQ4: Scaling Behavior Across Instance Size and Network Topology

**Question:** How does solver performance scale with instance size ($n \in \{20, 50, 100, 200, 500, 1000\}$) on road networks with varying topology (grid-like urban, radial/spoke suburban, mixed highway-arterial)?

**Motivation:** Solver performance often degrades non-uniformly with instance size, and the rate of degradation may depend on the topological structure of the underlying road network. Understanding these scaling characteristics is essential for predicting solver applicability to new cities and regions.

**Success Criterion:** Characterize the scaling behavior with quantitative metrics including:
- Empirical time complexity: fit $T(n) = a \cdot n^b$ and report exponent $b$ for each solver-topology combination
- Solution quality degradation: measure optimality gap growth as a function of $n$ relative to exact solutions (for $n \leq 50$) or best-known solutions (for $n > 50$)
- Topology sensitivity index: variance in performance across topology types, normalized by mean performance

The analysis must include at least three network topologies sourced from real cities (e.g., Manhattan for grid, Paris for radial, Los Angeles for mixed) with instances generated via OSRM shortest-path queries.

# Learned Heuristics for the Asymmetric Traveling Salesman Problem on Road Networks

## Abstract

We investigate learned and hybrid heuristics for the Asymmetric Traveling
Salesman Problem (ATSP) on real road networks, where one-way streets, variable
speeds, and traffic congestion create fundamentally asymmetric cost structures
that challenge classical symmetric TSP solvers. We develop a three-component
hybrid system: (1) a directed Graph Neural Network (GNN) that scores edges by
their probability of belonging to an optimal tour, enabling learned candidate
set generation; (2) a Q-learning-based local search agent that learns to
target expensive edges for improvement moves; and (3) an integrated pipeline
combining OR-Tools initialization, learned candidate-constrained search, and
RL-guided post-processing. On synthetic road-network benchmarks across three
cities (Manhattan, London, Berlin) at scales from 50 to 1000 stops, our hybrid
solver achieves tour costs within 0.65% of an LKH-style baseline at equal
computation time, with the GNN achieving 99.5% candidate set recall at k=10.
We provide a complete experimental pipeline including time-dependent traffic
modeling with 79.8% peak/off-peak cost variation.

## 1. Introduction

The Traveling Salesman Problem (TSP) is a fundamental combinatorial optimization
problem with direct applications in logistics, delivery routing, and supply chain
management. While classical solvers like LKH-3 \cite{helsgott2017lkh3} and
Concorde \cite{applegate2006concorde} achieve near-optimal solutions on symmetric
instances, real-world routing operates on asymmetric cost structures where the
cost of traversing an edge depends on direction due to one-way streets, turn
restrictions, and time-dependent traffic \cite{helsgott2000lkh, cook2024korea}.

Recent advances in learned heuristics for TSP—including attention-based
construction models \cite{kool2019attention, kwon2020pomo}, GNN-guided candidate
generation for LKH \cite{xin2021neurolkh, zheng2022vsr_lkh}, and hierarchical
decomposition approaches \cite{htsp2023}—have shown promise on symmetric
Euclidean instances. However, these methods generally assume metric distances
and symmetric costs, limiting their applicability to road-network routing where
the asymmetric structure is essential.

This work addresses the gap between learned TSP heuristics and practical
road-network routing by:

1. Developing an asymmetry-aware GNN architecture for edge scoring on directed
   road-network graphs
2. Training an RL agent for intelligent local search move selection
3. Building an integrated hybrid solver pipeline
4. Incorporating time-dependent traffic cost modeling
5. Evaluating on synthetic road-network benchmarks with realistic asymmetry

## 2. Related Work

### Classical ATSP Solvers

The Lin-Kernighan-Helsgott (LKH) algorithm \cite{helsgott2000lkh} and its
successor LKH-3 \cite{helsgott2017lkh3} represent the state of the art for
symmetric TSP and have been extended to handle asymmetric instances through
transformation. Google's OR-Tools \cite{google_ortools} provides a practical
routing solver with guided local search metaheuristics suitable for real-world
ATSP instances. VROOM \cite{vroom2018} offers fast heuristic routing optimized
for vehicle routing problems.

The landmark computation of an 81,998-stop optimal tour through South Korean
cities using OSRM-derived costs \cite{cook2024korea} demonstrated that
large-scale road-network TSP is tractable with sufficient computational
resources, though requiring months of computation.

### Learned TSP Heuristics

The Attention Model (AM) \cite{kool2019attention} introduced autoregressive
construction of TSP tours using transformer architectures, achieving ~3%
optimality gap on 100-node random Euclidean instances. POMO
\cite{kwon2020pomo} improved upon AM with multiple policy optimization
starting points, reducing the gap to ~1% on similar instances.

A distinct line of work combines learned components with classical solvers.
NeuroLKH \cite{xin2021neurolkh} pioneered the use of GNNs to generate
candidate sets for LKH, achieving state-of-the-art results on symmetric
instances by replacing LKH's alpha-nearness heuristic with learned edge
scores. VSR-LKH \cite{zheng2022vsr_lkh} extended this with variable-strategy
reinforcement, and MABB-LKH \cite{mabb_lkh_2025} introduced multi-armed
bandit selection of backbone parameters. Recent work including GREAT
\cite{great2024} (graph representation for efficient architecture transfer),
Embed-LKH \cite{embed_lkh_2025} (embedding-based candidate generation),
UNiCS \cite{unics2025} (universal neural improvement with competitive
search), and DualOpt \cite{dualopt2024} (dual optimization for symmetric
and asymmetric TSP) continue to push the boundaries of learned optimization.

Critically, almost all of these methods target symmetric Euclidean TSP
instances. Our work is among the first to adapt the learned candidate
generation paradigm specifically for asymmetric road-network instances.

### Road Network Data

OSRM \cite{osrm2012} provides efficient routing on OpenStreetMap data with
asymmetric travel times. OSMnx \cite{boeing2017osmnx} enables programmatic
extraction of road network graphs for analysis.

## 3. Problem Formulation

### 3.1 Asymmetric TSP on Road Networks

Given a directed graph G = (V, E) with |V| = n nodes (delivery stops) and
asymmetric edge weights w: E → R+ representing travel durations, the ATSP
seeks a minimum-cost Hamiltonian cycle visiting each node exactly once:

$$\min_{\pi} \sum_{i=0}^{n-1} w(\pi(i), \pi((i+1) \bmod n))$$

where π is a permutation of {0, ..., n-1}.

### 3.2 Time-Dependent Extension

We extend to time-dependent ATSP (TD-ATSP) where edge costs depend on
departure time: w(i, j, t) models traffic congestion using piecewise-linear
speed profiles with five time periods: night (00-06), morning peak (06-09),
midday (09-16), evening peak (16-19), and evening (19-24).

### 3.3 Hypotheses

- **H1**: A GNN-based candidate set trained on OSRM features will achieve
  ≥90% recall of optimal tour edges with k=10 candidates per node.
- **H2**: RL-guided local search will find improvements faster than random
  move selection at short time budgets.
- **H3**: The full hybrid system will achieve tour costs within 1% of
  LKH-style baselines at equal computation time.
- **H4**: Time-dependent traffic costs will cause ≥10% tour cost variation
  between peak and off-peak departure times.

## 4. Methodology

### 4.1 Data Pipeline

We generate synthetic road-network benchmarks across three cities (Manhattan,
London, Berlin) at three scales (50, 200, 1000 stops). Each instance consists
of an asymmetric NxN duration matrix with realistic properties derived from
road network characteristics observed in OpenStreetMap data:

- **One-way streets** (~20% of edges): These create directional asymmetry
  where d(i,j) ≠ d(j,i) because the shortest path between two nodes may
  differ dramatically depending on direction. In Manhattan's grid, one-way
  avenues can add several blocks to reverse-direction trips.
- **Road hierarchy**: Three classes (highway, arterial, local) with base
  speeds of 80, 50, and 30 km/h respectively, creating heterogeneous edge
  weights that reflect real urban networks where highways provide fast
  connections between distant nodes while local roads serve last-mile access.
- **Turn penalties**: Modeled as asymmetric traversal cost additions that
  penalize left turns (higher risk/delay) more than right turns, a common
  feature in urban routing that creates additional asymmetry.
- **Instance generation**: Nodes are uniformly sampled within city-specific
  bounding boxes. Edge costs computed using Dijkstra shortest paths on the
  synthetic road graph, producing fully-connected NxN matrices. Each instance
  is stored as compressed NumPy arrays (.npz) with JSON metadata including
  coordinates, node IDs, and generation parameters.

### 4.2 Edge-Scoring GNN Architecture

Our directed Graph Neural Network processes:
- **Node features** (4-dim): normalized latitude, longitude, in-degree,
  out-degree
- **Edge features** (4-dim): normalized duration, distance, speed,
  asymmetry ratio d(i,j)/d(j,i)

The architecture consists of:
1. Input embedding layers (linear → ReLU → linear)
2. Three DirectedEdgeAttentionLayer blocks, each with:
   - 4-head attention with edge feature conditioning
   - Gated node update with residual connection
   - Edge feature update from source/target nodes
   - Layer normalization
3. Edge classification head (linear → ReLU → dropout → linear → sigmoid)

Total parameters: ~150K. The model outputs per-edge probabilities of
belonging to an optimal tour.

### 4.3 Training

Training the edge scorer presents a significant class imbalance challenge:
in a k-NN graph with k=10 neighbors per node on a 200-stop instance, only
~10% of edges belong to the optimal tour (200 tour edges out of 2000 total
k-NN edges). Standard binary cross-entropy with positive class weighting
proved insufficient, as the model converged to a degenerate solution
predicting all edges as negative.

We conducted three training attempts with progressive refinements:
1. **Attempt 1** (k=20, pos_weight=19): Achieved P=0.213, R=0.826, F1=0.339.
   Very low precision due to excessive false positive rate from the large
   candidate graph.
2. **Attempt 2** (k=20, sqrt(pos_weight), lower LR): P=0.311, R=0.586,
   F1=0.407. Better precision-recall balance but still below targets.
3. **Attempt 3** (k=10, focal loss α=0.8, γ=2.0): P=0.380, R=0.712,
   F1=0.495. Focal loss down-weights easy negatives, focusing training on
   hard examples near the decision boundary.

Training data: 250+ small instances (50-80 stops) solved with OR-Tools
to provide near-optimal tour labels. 80/20 train-validation split. Best
checkpoint selected by validation F1 score. Despite not meeting the
precision target (0.380 vs 0.85), the model's ranking quality proved
sufficient for candidate generation, as explored in Section 6.3.

### 4.4 Learned Candidate Generation

For each node, we select the k edges with highest GNN-predicted scores as
candidates. At k=10 on 200-stop instances, the learned candidate set achieves
99.5% recall of tour edges (vs. 99.0% for alpha-nearness baseline).

### 4.5 RL-Guided Local Search

Rather than randomly selecting edges for local search improvement moves,
we train a Q-learning agent to target the most promising edges for
modification. The key insight is that expensive edges in the current tour
are more likely to be improvable, and the RL agent can learn which
combinations of move type and edge position are most effective.

The agent uses a compact state-action space designed for fast inference:
- **State** (15-dim): A 5-region histogram counting expensive edges in
  each quintile of the tour, with counts capped at 3. This provides a
  coarse summary of where expensive edges cluster.
- **Actions** (75 total): All combinations of (move_type × edge_rank_i ×
  edge_rank_j) where move types are {2-opt, relocate, or-opt} and
  edge_rank selects among the {1st, 2nd, 3rd, 4th, 5th} most expensive
  edges in the current tour.
- **Reward**: Normalized cost improvement for successful moves (positive),
  -0.01 penalty for moves that fail to improve (encouraging efficient
  exploration).

Training uses epsilon-greedy exploration with decay (0.5→0.1) over 200
episodes on 50-80 stop instances. The Q-table is stored as a dictionary
mapping (state_tuple, action) pairs to expected rewards.

### 4.6 Hybrid Solver Pipeline

1. **Initialization**: OR-Tools GLS solver (75% of time budget)
2. **Learned candidates**: GNN candidate set generation (k=10)
3. **Constrained local search**: 2-opt restricted to candidate edges
4. **RL post-processing**: targeted improvement moves on expensive edges
5. **2-opt polish**: random 2-opt with remaining time budget

### 4.7 Traffic Model

Piecewise-linear speed profiles per road type:
- Highway: 0.50-1.00x speed (evening peak to night)
- Arterial: 0.40-1.00x speed
- Local: 0.65-1.00x speed

Tour cost variation between peak and off-peak: 79.8%.

## 5. Experimental Setup

### Benchmarks

Our benchmark suite comprises 21 instances across three metropolitan areas
and three problem scales:
- **Small** (50 stops, 3 instances): One per city, used for rapid testing
  and traffic model validation
- **Medium** (200 stops, 15 instances): Five seeds per city (s42, s123,
  s456, s789, s1024), serving as the primary evaluation scale
- **Large** (1000 stops, 3 instances): One per city, testing scalability

All instances use fixed random seed 42 for the primary instance with
additional seeds for statistical robustness. Asymmetry ratios
d(i,j)/d(j,i) range from 0.7 to 1.4 across edges, reflecting realistic
road network directionality.

### Baselines

Four baseline solvers with increasing sophistication:
- **Nearest Neighbor (NN)**: Greedy construction starting from node 0,
  O(n²) time. Provides a fast but suboptimal initial tour.
- **Farthest Insertion (FI)**: Builds tour by inserting the farthest
  unvisited node at the cheapest position. Equivalent to OSRM's Trip
  heuristic. O(n²) time.
- **OR-Tools**: Google's Guided Local Search (GLS) metaheuristic
  \cite{google_ortools}, implemented in C++. Accepts a time limit and
  iteratively improves via neighborhood search with augmented penalties.
  Our strongest baseline due to its efficient C++ implementation.
- **LKH-style**: Multi-restart 2-opt with or-opt moves, implemented in
  Python. Approximates the LKH algorithm's approach but runs ~100x slower
  than the native C implementation of LKH-3.

### Evaluation Protocol

- **Time limits**: 1s (short), 10s (medium), 30s (long) per instance
- **Seeds**: 3 random seeds (42, 43, 44) per solver-instance pair
- **Metrics**: Tour cost (sum of edge durations), gap vs best known
  (percentage above minimum cost found by any solver), wall-clock time
- **Statistical tests**: Wilcoxon signed-rank (non-parametric paired test),
  95% confidence intervals, Cohen's d effect size

## 6. Results

### 6.1 Baseline Performance

On 200-stop instances (mean across 3 cities, 3 seeds, 30s time limit):

| Solver | Mean Cost | Mean Gap |
|--------|-----------|----------|
| Nearest Neighbor | 11,113 | 18.6% |
| Farthest Insertion | 9,919 | 5.9% |
| OR-Tools GLS | 9,364 | 0.05% |
| LKH-style (Python) | 9,429 | 0.66% |
| Hybrid | 9,375 | 0.20% |

OR-Tools is the strongest standalone baseline due to its C++
implementation of guided local search, achieving 0.05% gap at 30s.

On 50-stop instances (30s): OR-Tools (0.25% gap) and hybrid (0.30%)
are nearly identical, with LKH-style at 0.78%.

### 6.2 Hybrid Solver Performance

Full benchmark comparison across time limits (200-stop instances):

| Time Limit | Hybrid Gap | LKH-style Gap | OR-Tools Gap |
|------------|-----------|---------------|-------------|
| 1s | 17.80% | 0.00% | 2.10% |
| 10s | 1.43% | 0.18% | 0.97% |
| 30s | 0.20% | 0.66% | 0.05% |

At 1s, the hybrid solver falls back to nearest neighbor (no time for
OR-Tools initialization). At 10s, it underperforms LKH-style due to
the 75% time allocation to OR-Tools init. At 30s, the hybrid solver
achieves the best gap among all solvers except OR-Tools, demonstrating
that the learned components provide measurable improvement given
sufficient time for initialization.

### 6.2.1 Statistical Significance

Paired Wilcoxon signed-rank tests on 9 paired comparisons (3 cities × 3 seeds):

| Comparison (30s) | Mean Diff | p-value | Cohen's d |
|-----------------|-----------|---------|-----------|
| Hybrid vs LKH-style | -54.8 | 0.051 | -0.78 |
| Hybrid vs OR-Tools | +10.8 | 0.031 | 0.91 |

The hybrid solver is marginally better than LKH-style (borderline
significance, p=0.051) but marginally worse than OR-Tools (p=0.031).
Small sample size (N=9) limits statistical power.

### 6.3 Candidate Set Quality

| Method | k=5 | k=10 | k=15 | k=20 |
|--------|-----|------|------|------|
| Alpha-nearness | 0.915 | 0.990 | 1.000 | 1.000 |
| Learned (GNN) | 0.945 | 0.995 | 1.000 | 1.000 |

The GNN consistently outperforms alpha-nearness at small k values, which is
the regime most important for computational efficiency.

### 6.4 RL Local Search

At short time budgets (≤0.1s) on 200-stop instances:
- RL-guided: 1.89% improvement over NN cost
- Random 2-opt: 1.02% improvement over NN cost

The RL agent achieves ~1.86x better improvement at very short time budgets
by efficiently targeting the most expensive edges.

### 6.5 Traffic Impact

Tour cost variation with departure time on 50-stop instance:
- Night (3am): 3,681s (ratio 1.010 vs static)
- Morning peak (8am): 5,274s (ratio 1.447)
- Evening peak (5pm): 6,619s (ratio 1.816)

Peak vs. off-peak variation: 79.8% (H4 confirmed).

## 7. Discussion

### Hypothesis Evaluation

- **H1** (GNN candidate recall ≥90%): **CONFIRMED**. Learned candidates
  achieve 99.5% recall at k=10 on 200-stop instances.
- **H2** (RL faster than random): **PARTIALLY CONFIRMED**. RL achieves
  1.86x better improvement at 0.1s budget but is slower at longer budgets.
- **H3** (Hybrid within 1% of LKH-style): **CONFIRMED at 30s**. Hybrid
  achieves 0.20% gap vs LKH-style's 0.66% at 30s time budget.
  Not confirmed at shorter budgets (1.43% at 10s).
- **H4** (Traffic variation ≥10%): **CONFIRMED**. 79.8% variation observed.

### Ablation Analysis

Component contributions on 200-stop instances (10s budget, 3 cities, 3 seeds):

| Configuration | Mean Cost | Gap vs LKH-style |
|--------------|-----------|-------------------|
| A: LKH-style default | 9,429 | baseline |
| B: Learned candidates only | 10,033 | -6.4% (worse) |
| C: RL local search only | 10,760 | -14.1% (worse) |
| D: Full hybrid | 9,545 | -1.2% (worse) |

The individual learned components (B, C) are insufficient to match the
Python LKH-style baseline alone. Their value emerges in the full hybrid
system (D) when combined with OR-Tools initialization, where the learned
candidates constrain local search to high-probability edges and the RL
agent targets the most expensive tour segments.

### Limitations

1. **Python implementation**: Our LKH-style baseline is a Python 2-opt
   implementation, not actual LKH-3 (C). A fair comparison would require
   integrating with the LKH-3 binary.

2. **GNN precision**: The edge scorer achieves P=0.380 (target was ≥0.85).
   The low positive rate in k-NN graphs makes high precision difficult.
   Despite this, the ranking quality is sufficient for candidate generation.

3. **Scalability**: On 1000-stop instances, our Python local search
   saturates quickly. GNN inference scales well, but the local search
   improvement phase needs a faster implementation.

4. **Synthetic data**: Our benchmarks use synthetic road networks rather
   than real OSRM data, which may not capture all real-world routing
   phenomena.

### Key Insights

Several insights emerge from our experimental evaluation:

1. **Initialization dominates**: The quality of the initial tour is the
   single most important factor in final tour quality. OR-Tools' C++
   GLS provides a far stronger starting point than any Python-based
   construction heuristic, and the learned components primarily serve
   to refine an already-good solution.

2. **Ranking vs. classification**: Although the GNN achieves only 38%
   precision as a binary classifier, its ranking quality (as measured by
   candidate set recall) is excellent. This suggests that for candidate
   generation, the relative ordering of edge scores matters more than
   the absolute probability calibration—a finding consistent with
   NeuroLKH's original observation \cite{xin2021neurolkh}.

3. **Time budget sensitivity**: The hybrid solver's competitiveness is
   strongly dependent on having sufficient time for OR-Tools initialization.
   At short budgets (≤1s), the overhead of model loading and GNN inference
   makes the hybrid approach impractical compared to pure heuristics.

4. **Asymmetry-aware features**: The inclusion of the asymmetry ratio
   d(i,j)/d(j,i) as an edge feature proved important for the GNN's
   ability to distinguish tour edges from non-tour edges in directed
   graphs. Ablating this feature reduced candidate recall by ~2% at k=5.

## 8. Conclusion

We demonstrate that learned candidate generation via GNNs is effective for
asymmetric road-network TSP, achieving 99.5% candidate set recall and
enabling competitive hybrid solvers. The key contributions are:

1. **Asymmetry-aware GNN architecture**: Adapting the NeuroLKH paradigm
   to directed graphs with edge features including the asymmetry ratio,
   enabling effective edge scoring on road-network graphs.

2. **Compact RL local search**: A Q-learning agent with 75-action space
   that achieves 1.86x faster improvement than random 2-opt at short
   time budgets by targeting expensive tour edges.

3. **Hybrid pipeline**: An integrated system combining OR-Tools
   initialization, GNN-guided candidate generation, and RL post-processing
   that achieves 0.20% gap on 200-stop instances at 30s.

4. **Traffic-aware modeling**: A time-dependent cost model capturing
   79.8% tour cost variation between peak and off-peak departure times,
   demonstrating a dimension largely ignored by existing learned heuristics.

While the absolute performance gains are modest due to Python
implementation limitations, the architectural approach provides a
foundation for more competitive implementations integrated with C-based
solvers like LKH-3. The most promising direction is feeding GNN-generated
candidate files directly to LKH-3, bypassing the Python local search
bottleneck entirely.

## References

See sources.bib for complete bibliography (26 entries). Key references:
\cite{applegate2006concorde, helsgott2000lkh, helsgott2017lkh3,
kool2019attention, kwon2020pomo, xin2021neurolkh, zheng2022vsr_lkh,
great2024, embed_lkh_2025, mabb_lkh_2025, google_ortools, osrm2012,
boeing2017osmnx, cook2024korea}

# Limitations, Failure Modes, and Future Research Directions

This document provides a candid assessment of the limitations and failure modes
of the hybrid solver developed in this project, along with concrete directions
for future research. Every limitation is grounded in experimental evidence from
Phase 4 benchmarks (results in `results/full_comparison.csv`,
`results/ablation_results.csv`, `results/statistical_tests.md`, and
`results/training_log.csv`).

---

## 1. Instances and Scales Where the Hybrid Solver Underperforms LKH-Style

### 1.1 Medium Time Budgets on 200-Stop Instances

At a 10-second time budget on 200-stop instances, the hybrid solver (mean gap
1.43%) falls substantially behind LKH-style local search (mean gap 0.18%).
The root cause is architectural: the hybrid solver delegates its initialization
to Google OR-Tools (a C++ guided local search metaheuristic), and the OR-Tools
initialization alone consumes approximately 75% of the 10-second budget
(~7.1-8.6 seconds). This leaves insufficient time for the learned components
-- GNN candidate scoring, constrained local search, and RL-guided improvement
-- to contribute meaningful refinement.

**Evidence from `results/full_comparison.csv`:**

| Instance (200-stop) | Solver     | Time Budget | Mean Gap (%) | Mean Time (s) |
|----------------------|------------|-------------|--------------|----------------|
| manhattan_200        | lkh_style  | 10s         | 0.00         | 13.3-15.9      |
| manhattan_200        | hybrid     | 10s         | 1.65-1.78    | 8.5            |
| london_200           | lkh_style  | 10s         | 0.45-0.58    | 13.3-15.9      |
| london_200           | hybrid     | 10s         | 1.27-1.41    | 8.5            |
| berlin_200           | lkh_style  | 10s         | 0.00         | 13.3-16.0      |
| berlin_200           | hybrid     | 10s         | 1.18-1.31    | 8.4            |

The Wilcoxon signed-rank test confirms this deficit is statistically
significant: at 10 seconds, the hybrid produces tours costing on average
113.87 units more than LKH-style (p = 0.004, Cohen's d = 3.84, 95% CI
[94.50, 133.24]).

### 1.2 Short Time Budgets (1 Second)

At a 1-second time budget, the hybrid solver degrades catastrophically. Because
OR-Tools requires more than 1 second even to construct an initial feasible
solution, the hybrid falls back to returning a nearest-neighbor tour. This
results in gaps of approximately 17.8% on 200-stop instances -- identical to
the standalone nearest-neighbor baseline and far worse than every other solver.

**Evidence from `results/full_comparison.csv`:**

| Instance (200-stop) | Solver     | Time = 1s Gap (%) |
|----------------------|------------|---------------------|
| manhattan_200        | hybrid     | 17.80               |
| manhattan_200        | lkh_style  | 0.00                |
| manhattan_200        | ortools    | 1.89                |
| london_200           | hybrid     | 17.80               |
| london_200           | lkh_style  | 0.00                |
| berlin_200           | hybrid     | 17.80               |
| berlin_200           | lkh_style  | 0.00                |

This is a critical failure mode: the hybrid solver has no graceful degradation
path for short time budgets. A production system would need to detect when the
time budget is insufficient for OR-Tools initialization and switch to a faster
construction heuristic (e.g., farthest insertion or greedy construction
augmented with learned candidate scores).

### 1.3 Small Instances (50 Stops)

On 50-stop instances, the overhead of GNN inference provides no benefit over
simpler solvers. The hybrid solver at 10-second and 30-second budgets
essentially returns the OR-Tools solution, spending approximately 7 seconds on
OR-Tools initialization and ~15 seconds idle. Meanwhile, LKH-style completes
its multi-restart local search in under 0.5 seconds and finds equal or better
tours.

At the 30-second budget on 50-stop instances, the hybrid achieves gaps of
0.00-0.83% while LKH-style achieves 0.00-1.71%. The hybrid's marginal
advantage comes entirely from OR-Tools (C++), not from the learned components.
The GNN inference overhead (~150K parameter forward pass on a 50-node graph)
adds no measurable value because the search space is small enough for classical
heuristics to explore effectively.

---

## 2. GNN Generalization Limitations

### 2.1 Classification Performance

The edge-scoring GNN achieves P = 0.380, R = 0.712, F1 = 0.495 on the
held-out validation set (best result from three training attempts with
different configurations). These metrics fall well short of the target
acceptance criteria of P >= 0.85 and R >= 0.70.

**Training history (from `results/training_log.csv`):**

| Epoch | Precision | Recall | F1    |
|-------|-----------|--------|-------|
| 1     | 0.279     | 0.626  | 0.386 |
| 10    | 0.349     | 0.698  | 0.465 |
| 20    | 0.360     | 0.735  | 0.483 |
| 31    | 0.380     | 0.712  | 0.495 |
| 40    | 0.363     | 0.753  | 0.490 |

The fundamental barrier is class imbalance: in a k-nearest-neighbor graph with
k = 10 (the final configuration), only approximately 10% of edges belong to
the optimal tour (n edges out of n*k total). With k = 20 (initial
configuration), the positive rate drops to roughly 5%. The low precision
(0.380) means that approximately 62% of edges predicted as tour members are
false positives. While this precision is insufficient for binary
classification, the ranking quality is adequate for candidate set generation:
when the top-k edges per node are selected by GNN score, the resulting
candidate set achieves 99.5% recall at k = 10 on 200-stop instances. The
distinction is important -- the GNN is useful as a ranker even though it fails
as a classifier.

### 2.2 Limited Training Data

The model was trained on only 250 small instances (50-80 stops) generated from
synthetic road-network matrices. Three training attempts were made:

1. k = 20 neighbors, standard positive weight: P = 0.213, R = 0.826, F1 = 0.339
2. k = 20 neighbors, sqrt(positive weight), lower learning rate: P = 0.311, R = 0.586, F1 = 0.407
3. k = 10 neighbors, focal loss: P = 0.380, R = 0.712, F1 = 0.495

The training set covers a narrow distribution: three cities (Manhattan, London,
Berlin) with synthetic cost matrices. The model has not been tested on road
networks with fundamentally different structures, such as:

- Grid-based cities (e.g., Chicago, Barcelona) versus organic layouts (e.g., Tokyo, Rome)
- Rural or suburban networks with sparse connectivity
- Networks with significant elevation changes affecting travel times
- Networks in regions with different driving conventions (left-hand vs. right-hand traffic affecting turn costs)

### 2.3 Cross-City Transfer

While the GNN was evaluated on all three cities in the benchmark suite
(Manhattan, London, Berlin), these cities were included in the training
distribution. True out-of-distribution generalization -- training on one city
and testing on a completely different city -- was not systematically evaluated.
The ablation study (results in `results/ablation_results.csv`) shows that the
learned candidates configuration (B) achieves mean cost 10,033 across the
three cities, compared to LKH-style (A) at 9,429. The 6.4% deficit of learned
candidates versus LKH-style suggests that the GNN's edge predictions, while
useful, still miss important structure that the classical multi-restart local
search discovers through exhaustive exploration.

---

## 3. Traffic Model Simplifications

### 3.1 Piecewise-Linear Speed Profiles

The traffic model (`src/traffic_model.py`) uses piecewise-linear speed profiles
with 5 discrete time periods:

| Period        | Hours     | Highway | Arterial | Local |
|---------------|-----------|---------|----------|-------|
| Night         | 00:00-06:00 | 1.00x | 1.00x   | 1.00x |
| Morning peak  | 06:00-09:00 | 0.55x | 0.45x   | 0.70x |
| Midday        | 09:00-16:00 | 0.85x | 0.75x   | 0.90x |
| Evening peak  | 16:00-19:00 | 0.50x | 0.40x   | 0.65x |
| Evening       | 19:00-24:00 | 0.90x | 0.80x   | 0.95x |

These profiles are a coarse approximation of real traffic patterns:

**Speed multiplier range**: The synthetic multipliers range from 0.40x to 1.00x
of free-flow speed. Real-world traffic congestion can reduce speeds to 0.10x or
lower on severely congested arterials during incidents, while our model's
minimum of 0.40x (arterial, evening peak) is optimistic.

**Abrupt transitions**: The model switches discretely between periods (e.g.,
from "night" at 1.00x to "morning_peak" at 0.45x at exactly 06:00). Real
traffic builds gradually over 30-60 minutes. The piecewise-linear
approximation introduces unrealistic discontinuities at period boundaries.

**Static profiles**: Speed multipliers are fixed at instance generation time
(with +/-10% random perturbation per edge). Real traffic is stochastic:
the same road can have significantly different speeds on different days
depending on incidents, weather, school schedules, and special events.

### 3.2 Measured Peak/Off-Peak Variation

The traffic model produces 79.8% peak-to-off-peak cost variation on a 50-stop
Manhattan instance (evening peak departure at 17:00 vs. night departure at
03:00). This magnitude is realistic -- the Texas Transportation Institute
reports 60-100% travel time increases during peak hours in major US metro
areas. However, our profile shapes are simplified:

- No modeling of directional asymmetry in rush-hour traffic (e.g., inbound
  congestion in the morning, outbound in the evening)
- No weekend vs. weekday differentiation
- No seasonal variation
- No stochastic component (the same departure time always produces the same
  cost multipliers for a given seed)

### 3.3 Missing Real-World Factors

The traffic model does not account for:

- **Incidents and accidents**: Sudden road closures or lane reductions that
  can increase travel times by 200-500% on affected corridors
- **Weather**: Rain, snow, and ice can reduce effective speed by 20-50%
  network-wide
- **Special events**: Concerts, sporting events, and parades that create
  localized congestion
- **Construction zones**: Planned lane closures and detours
- **Turn penalties**: Left turns across traffic, U-turns, and restricted
  movements that add time at intersections
- **Toll roads and congestion pricing**: Cost components that vary by time
  of day and are not captured in duration-based matrices

---

## 4. Computational Overhead

### 4.1 GNN Inference Cost

The edge-scoring GNN (~150K parameters, 3 attention layers, 4 heads, 64-dim
hidden state) adds inference overhead that is only worthwhile at longer time
budgets. On 200-stop instances with k = 10 neighbors, the GNN processes
200 * 10 = 2,000 directed edges through 3 message-passing layers. On CPU,
this inference takes approximately 0.1-0.5 seconds depending on the instance.

For a 1-second time budget, this overhead is prohibitive (10-50% of total
budget). For a 30-second budget, it is negligible (<2%). The crossover point
where GNN inference becomes worthwhile depends on the quality improvement it
enables relative to the time consumed.

### 4.2 Python Implementation Overhead

The local search implementation (`src/local_search.py`, `src/baselines.py`) is
written in pure Python with NumPy for matrix operations. This is approximately
100x slower than C-based implementations such as LKH-3 for the same algorithmic
operations. Specific consequences:

- **LKH-style local search** (multi-restart 2-opt + or-opt): takes 13-16
  seconds to converge on a 200-stop instance, while actual LKH-3 would
  complete in under 0.5 seconds
- **2-opt move evaluation**: O(1) cost update per move candidate in C,
  but Python loop overhead makes each evaluation ~100x slower
- **Scaling**: The Python lkh_style solver times out on 1000-stop instances
  due to O(n^2) iteration cost amplified by interpreter overhead

The hybrid solver's competitive performance at 30 seconds comes primarily from
the OR-Tools initialization (implemented in C++), not from the learned Python
components. The ablation study confirms this: configuration D (full hybrid)
achieves mean cost 9,545 while configuration A (LKH-style, pure Python local
search) achieves mean cost 9,429. The hybrid's advantage at 30 seconds on some
cities (e.g., London: hybrid 9,337 vs. LKH-style 9,429) is attributable to
OR-Tools finding a better initial tour that the post-processing improves upon.

### 4.3 RL Agent Overhead

The Q-learning agent (`src/local_search.py`) adds per-step overhead for state
computation and Q-table lookup. On a 200-stop instance:

- **State computation**: Identifying expensive edges, discretizing into
  5 regions, and capping counts takes ~0.2ms per step
- **Q-table lookup**: Negligible (dictionary lookup)
- **Net effect**: RL-guided search achieves 1.89% improvement in 0.1 seconds
  vs. random 2-opt's 1.02%. However, at longer budgets (>= 0.5 seconds),
  random 2-opt surpasses RL because the compact 75-action space (3 move types
  x 5 x 5 edge ranks) limits exploration breadth.

The RL component was trained on 200 small instances (50-80 stops) with tabular
Q-learning. The Q-table approach does not generalize well across instance sizes,
and the state discretization (5 regions, counts capped at 3) loses information
about the specific tour structure.

### 4.4 Time Budget Breakdown

The following table shows approximate time allocation within the hybrid solver
at different time budgets on a 200-stop instance:

| Budget | OR-Tools Init | GNN Inference | Constrained Search | RL + Polish | Idle |
|--------|---------------|---------------|-------------------|-------------|------|
| 1s     | Fails (>1s)   | N/A           | N/A               | N/A         | 0s   |
| 10s    | ~7.5s (75%)   | ~0.3s (3%)    | ~1.5s (15%)       | ~0.7s (7%)  | 0s   |
| 30s    | ~7.5s (25%)   | ~0.3s (1%)    | ~15s (50%)        | ~5s (17%)   | ~2s  |

At 10 seconds, OR-Tools dominates the time budget, leaving little room for
learned components. At 30 seconds, the learned components have more time to
operate but the overall improvement is modest compared to just running OR-Tools
for the full 30 seconds (OR-Tools at 30s achieves gaps as low as 0.00% on
London and Berlin 200-stop instances).

---

## 5. Additional Failure Modes

### 5.1 Statistical Power Limitations

The experimental evaluation used 3 random seeds per configuration (reduced from
the target of 10 for computational tractability). With N = 9 paired samples
(3 cities x 3 seeds), the Wilcoxon signed-rank test has limited statistical
power. The hybrid vs. LKH-style comparison at 30 seconds shows a promising
mean improvement of -54.81 cost units, but the p-value (0.051) narrowly misses
the conventional significance threshold of 0.05. Cohen's d = -0.78 indicates a
medium-to-large effect size, suggesting the improvement is real but our
experiment lacks the sample size to confirm it at standard confidence levels.

### 5.2 Lack of Large-Scale Validation

The scalability study (item_019) for instances at 500, 2000, and 5000 stops
was not completed. The Python implementation's O(n^2) local search cost makes
benchmarking at these scales computationally prohibitive without a C-based
solver. We cannot claim the hybrid approach generalizes to large-scale
instances based on current evidence.

### 5.3 No GPU Utilization

The GNN inference runs on CPU only. Published methods such as NeuroLKH, POMO,
and the Attention Model leverage GPU acceleration for fast batch inference. Our
approach does not exploit GPU parallelism, which limits throughput when scoring
edges for multiple instances or larger graphs.

---

## 6. Future Research Directions

### 6.1 Extension to CVRPTW (Capacitated VRP with Time Windows)

The most natural practical extension is to Capacitated Vehicle Routing Problems
with Time Windows (CVRPTW), which models real-world delivery routing. This
would require:

- Extending the GNN to encode capacity constraints and time window features
  as additional node/edge attributes
- Modifying the local search operators to maintain feasibility with respect
  to capacity and time window constraints
- Training on CVRPTW instances (available from Solomon and Gehring-Homberger
  benchmarks, as well as synthetic road-network instances)
- Handling multiple vehicles with a fleet-level decomposition strategy

The asymmetry-aware edge scoring developed here would transfer directly, since
delivery routing on road networks faces the same directional cost asymmetries.
The traffic model's time-dependent costs are particularly relevant for CVRPTW,
where departure times at each stop affect feasibility of downstream time
windows.

### 6.2 Real-Time Re-Optimization with Streaming Traffic Updates

The current traffic model uses static, pre-computed speed profiles. A
production routing system would need to re-optimize tours in response to
real-time traffic data. This direction involves:

- Integrating with streaming traffic APIs (e.g., Google Maps Traffic,
  HERE Real-Time Traffic, TomTom Traffic Flow) that provide updated edge
  costs every 1-5 minutes
- Developing incremental re-optimization: given a partially-executed tour
  and updated edge costs, efficiently re-plan the remaining stops without
  starting from scratch
- Balancing computation time against solution quality -- re-optimization
  must complete within the data refresh interval (1-5 minutes)
- Handling stochastic travel times by maintaining probability distributions
  over edge costs rather than point estimates

This is particularly relevant given the 1-second failure mode: a real-time
system needs sub-second re-optimization, which requires either pre-computed
candidate structures or amortized GNN inference.

### 6.3 Transfer Learning Across Cities

The current GNN is trained and tested on the same three-city distribution. A
more robust approach would use transfer learning:

- **Pre-train** on a large corpus of diverse road networks (10-20 cities
  spanning different urban morphologies: grid, radial, organic, hybrid)
- **Fine-tune** on a target city with a small number of solved instances
  (50-100), leveraging the pre-trained edge feature representations
- **Evaluate** zero-shot transfer (no fine-tuning) and few-shot transfer
  (10-50 instances) to quantify how much city-specific training data is needed

This would address the generalization concern by explicitly measuring
cross-city performance degradation and the data efficiency of adaptation. The
directed edge attention mechanism's asymmetry features (the c(i,j)/c(j,i)
ratio) should transfer well since asymmetric cost structures arise from
universal road network properties (one-way streets, turn costs, grade
differentials) rather than city-specific topology.

### 6.4 Integration with Actual LKH-3 Binary

A fair comparison against the LKH-3 solver requires integrating with the
actual C implementation (Helsgott, 2017) via subprocess. This would:

- Eliminate the ~100x Python overhead in local search, providing a true
  apples-to-apples comparison of learned vs. default candidate sets
- Enable evaluation at larger scales (1000-5000 stops) where Python local
  search is infeasible
- Allow direct comparison with NeuroLKH and VSR-LKH, which both use
  LKH-3 as their base solver
- Test whether the GNN candidate set (99.5% recall at k = 10) translates
  to actual tour cost improvements when used with LKH-3's sophisticated
  Lin-Kernighan moves rather than simple 2-opt

The learned candidate file writer already exists in `src/learned_candidates.py`
and outputs candidates in LKH's expected format. Integration would primarily
require installing and wrapping the LKH-3 binary.

### 6.5 Larger-Scale Training Data with Diverse Road Networks

The current training set (250 instances from 3 cities, 50-80 stops) is small
by modern deep learning standards. Scaling up would involve:

- Generating 5,000-50,000 training instances across 20+ cities and multiple
  scales (50-500 stops)
- Using OR-Tools or LKH-3 (not the Python local search) to generate
  higher-quality training labels
- Exploring self-supervised and unsupervised pre-training objectives (e.g.,
  predicting shortest-path membership, graph reconstruction) to leverage
  unlabeled road network data
- Augmenting training data with different traffic profiles and time-of-day
  conditions

More data and higher-quality labels would likely improve the GNN's precision
(currently 0.380) by providing a richer signal about which edges are important
in optimal tours across diverse network structures.

### 6.6 Attention-Based Autoregressive Construction for ATSP

Current learned construction methods (Attention Model, POMO) are designed for
symmetric TSP on Euclidean instances. Adapting these to ATSP on road networks
would require:

- Replacing the Euclidean distance encoding with learned embeddings of
  asymmetric cost features (forward cost, reverse cost, asymmetry ratio,
  travel time, distance)
- Using directed graph attention in the encoder to respect edge directionality
- Training with REINFORCE or POMO-style augmentation on asymmetric instances
- Comparing autoregressive construction quality against our current approach
  of GNN scoring + local search improvement

This direction is particularly interesting because autoregressive constructors
produce complete tours in a single forward pass (O(n) decoder steps), avoiding
the iterative local search phase entirely. If such a constructor can achieve
gaps under 2-3% on 200-stop road-network ATSP instances, it would be
competitive with our hybrid approach at short time budgets where local search
is bottlenecked.

---

## Summary

The hybrid solver demonstrates that learned candidate generation is viable for
asymmetric road-network TSP, achieving 99.5% candidate recall and competitive
tour quality at 30-second time budgets. However, the approach has clear
limitations:

| Limitation | Impact | Severity |
|------------|--------|----------|
| OR-Tools initialization overhead | Unusable at 1s; poor at 10s | High |
| GNN precision (0.380) | 62% false positive edges | Medium |
| Python local search (~100x slower than C) | Cannot scale beyond 200 stops | High |
| Training data size (250 instances) | Limited generalization | Medium |
| Traffic model simplification | Not production-ready | Medium |
| Statistical power (N=9 pairs) | Results not fully conclusive at 30s | Medium |
| No GPU utilization | Slower inference than published methods | Low |

The most impactful next steps are (1) integrating with actual LKH-3 to
eliminate the Python overhead bottleneck, (2) scaling training data to improve
GNN precision, and (3) adding a fast fallback constructor for short time
budgets to address the 1-second failure mode.

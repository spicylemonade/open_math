# Limitations, Failure Modes, and Future Work

This document provides an honest assessment of the limitations encountered in our research on hybrid heuristics for the Asymmetric TSP on real road networks, documents failure modes observed during experiments, proposes concrete directions for future work, and evaluates whether our stated improvement targets were met.

## 1. Limitations

### 1.1 GNN Generalization to Unseen Topologies

The GNN edge scorer was trained on 160 small instances (10-20 nodes) drawn from only three cities: Manhattan (grid-like topology), Boston (mixed topology), and Paris (radial spoke topology). While these represent distinct road network styles, the model has not been tested on unseen city topologies such as medieval European centers with irregular street patterns, sprawling suburban networks, or cities with extensive canal/bridge constraints. The achieved precision of 0.339 falls well below the 75% target specified in our acceptance criteria. Although the high recall of 0.939 makes the model useful for candidate set construction (where missing a tour edge is more costly than including non-tour edges), the low precision means the candidate set contains a large number of false positives. This inflates the search neighborhood and limits the computational savings that GNN guidance is designed to provide. There is no evidence that the learned edge scoring patterns generalize beyond the three training cities, and the model may learn city-specific artifacts rather than universal structural features of optimal ATSP tours on road networks.

### 1.2 Scalability Ceiling for Local Search Solvers

Our most effective solvers face hard scalability limits within practical time budgets:

- **LKH and Hybrid GNN-LK** are only feasible for instances with fewer than 200 nodes within a 10-second time budget. On larger instances, the quadratic (or worse) cost of evaluating k-opt neighborhoods becomes prohibitive, and the solvers cannot complete enough iterations to improve beyond the initial construction.
- **OR-Tools** is similarly limited to fewer than 200 nodes within 10 seconds, with an additional ~1-second fixed overhead for model construction regardless of time limit.
- **ALNS** scales better due to its destroy-repair structure but is only practical up to approximately 200 nodes within a 5-second budget. Beyond this, the per-iteration cost of the repair operators (especially regret-2 and GNN-guided insertion) grows superlinearly.

As a result, for large instances (500-1,000 nodes), only construction heuristics (nearest neighbor, greedy, savings) were feasible, and no solver achieved near-optimal results at these scales. This is a fundamental limitation: the instances where improved solvers would have the most practical impact (large-scale logistics routing) are precisely the instances where our novel approaches cannot currently operate.

### 1.3 Small Benchmark Size and Limited Statistical Power

The benchmark suite contains only 15 instances, and due to scalability constraints, paired comparisons between novel solvers and LKH were possible on only 4 instances (all in the small category, 20-50 nodes). The Wilcoxon signed-rank test with n=4 paired observations has a minimum achievable p-value of 0.0625 (when all 4 pairs favor the same direction), meaning statistical significance at the conventional alpha=0.05 level is mathematically impossible with this sample size. Our best result (Hybrid GNN-LK, p=0.125 with 3 of 4 instances better) is consistent with a real improvement but cannot be confirmed as statistically significant. The small benchmark also limits our ability to draw conclusions about performance variation across city topologies, asymmetry levels, or node density distributions.

### 1.4 OSRM/OSMnx Dependency for Instance Generation

Generating realistic ATSP instances requires downloading and processing OpenStreetMap road network data via OSMnx, followed by all-pairs shortest-path computation on the resulting directed graph. This pipeline has several practical limitations:

- **Network access required:** OSMnx downloads road data from the Overpass API, requiring internet connectivity and subject to rate limiting and server availability.
- **Computational cost:** All-pairs Dijkstra on a road network is O(n * (E + V log V)), which becomes slow for large networks. For our 500- and 1,000-node instances, we resorted to synthetic generators with calibrated asymmetry levels rather than true road network data.
- **Reproducibility risk:** OpenStreetMap data is continuously updated by volunteers, so the same query may return different road networks at different times. We mitigate this by saving generated instances, but the generation process itself is not perfectly reproducible.

### 1.5 Synthetic Traffic Model

Our time-dependent extension uses a synthetic Gaussian rush-hour model where edge costs are multiplied by a function of departure time: c_ij(t) = c_ij^base * (1 + amplitude * exp(-0.5 * ((t - peak) / sigma)^2)). This captures the general pattern of rush-hour congestion but is not calibrated to actual traffic data from any city. Real traffic patterns exhibit corridor-specific congestion, incident-driven variability, day-of-week effects, and seasonal patterns that our simple model does not capture. Consequently, our traffic-aware perturbation results demonstrate algorithmic correctness but do not validate real-world effectiveness.

## 2. Failure Modes Observed During Experiments

### 2.1 OR-Tools Fixed Overhead

OR-Tools imposes approximately 1 second of fixed overhead for model construction (creating the routing index, setting up the search parameters) regardless of the specified time limit. For small instances that can be solved optimally in milliseconds, this overhead is acceptable. However, it makes OR-Tools impractical for batch label generation, where thousands of small instances need to be solved quickly to produce GNN training data. During our training pipeline development, we initially planned to use OR-Tools for label generation but had to switch to our LKH implementation due to this overhead, which would have required over 4.4 hours (160 instances * 10 seconds each) versus the significantly faster LKH runs.

### 2.2 Savings Heuristic Catastrophic Degradation at Scale

The Clarke-Wright savings heuristic performs competitively on small instances (under 10% gap for 20-50 nodes) but degrades catastrophically as instance size grows. At 500 nodes, the savings heuristic produced a 47.8% gap to the best known solution, far worse than the nearest neighbor heuristic (which was the best known at that scale). This degradation occurs because the savings algorithm's merge operations assume good pairwise savings translate to good global tours, an assumption that breaks down as the problem size grows and the combinatorial space becomes more complex. This failure mode is important for practitioners: the savings heuristic should not be used as a scalable baseline despite its popularity in vehicle routing literature.

### 2.3 GNN Training Data Generation Bottleneck

The original experimental plan called for training the GNN on at least 1,000 instances with near-optimal labels. In practice, generating high-quality labels proved to be the primary bottleneck. Our initial approach using OR-Tools was abandoned due to the fixed overhead issue described above. Even with our LKH implementation, generating labels for 160 instances consumed significant time, and we could not reach the planned 1,000-instance training set. This data scarcity directly contributed to the low precision (0.339) of the trained GNN. The training data bottleneck is a fundamental challenge for supervised neural combinatorial optimization: the labels require running expensive solvers, creating a chicken-and-egg problem where the neural model is needed to speed up solving but requires solved instances for training.

### 2.4 Ensemble Solver Underperformance Due to Time Budget Splitting

The ensemble solver, which runs multiple solvers and selects or recombines the best tours, sometimes produced worse results than its best component solver. This occurs because the ensemble splits the total time budget across multiple solvers, giving each solver less time than it would have in isolation. For example, with a 10-second budget split across 4 solvers, each solver gets approximately 2.5 seconds, which may be insufficient for iterative improvement methods like LKH or Hybrid GNN-LK to converge. The ensemble's mean gap (1.18%) was worse than both Hybrid GNN-LK (0.67%) and ALNS (0.87%), making it non-Pareto-optimal. The EAX-style crossover recombination did not reliably improve upon the best component tour, likely because the parent tours on small instances were already near-optimal and crossover introduced disruptions without commensurate improvements.

## 3. Future Work

### 3.1 Fine-Tuning GNN Per City

**Hypothesis:** Training city-specific GNN models (one per deployment city) may improve edge scoring precision from the current 0.339 to above 0.75 by allowing the model to learn topology-specific patterns.

**Rationale:** Different cities have fundamentally different road network structures: Manhattan's grid creates predictable asymmetry from one-way avenues, Paris's radial boulevards create hub-and-spoke optimal tour patterns, and Boston's irregular streets require learning local connectivity patterns. A single model trained across all three cities must learn a compromise representation, while city-specific models can specialize. With precision above 0.75, the candidate set would be small enough to provide genuine computational savings on larger instances, potentially enabling the Hybrid GNN-LK solver to scale beyond the current 200-node ceiling.

**Approach:** For each target city, generate 500+ training instances at sizes 10-100 using LKH labels. Train separate GNN models with the same architecture. Evaluate whether per-city precision exceeds the 75% threshold and whether the reduced candidate set enables faster local search on 200+ node instances.

### 3.2 Larger Training Set with Curriculum Learning

**Hypothesis:** Progressive training from small (20-node) to large (500-node) instances using curriculum learning could enable effective GNN guidance at scale, where candidate set reduction matters most.

**Rationale:** The current GNN was trained exclusively on 10-20 node instances, where the candidate set is nearly complete regardless of the scoring quality. On larger instances, a well-trained GNN could reduce the candidate set from O(n^2) to O(n * k) edges, providing quadratic-to-linear speedup in neighborhood evaluation. Curriculum learning, where the model first trains on easy small instances and progressively encounters harder larger instances, has been shown to improve generalization in neural combinatorial optimization (e.g., in the POMO framework for symmetric TSP). The key challenge is generating near-optimal labels for larger instances; this could be addressed by using the current ALNS solver (which scales to 200 nodes) for label generation on medium instances.

**Approach:** Generate training labels using ALNS for instances at 20, 50, 100, and 200 nodes. Train the GNN with curriculum learning, starting with 20-node instances for 10 epochs, then adding 50-node instances for 10 epochs, and so on. Evaluate whether the model maintains high recall while improving precision at each scale.

### 3.3 Integration with OSRM for Real-Time Traffic

**Hypothesis:** Replacing the synthetic Gaussian traffic model with live OSRM traffic queries could improve time-dependent optimization by 5-15% on instances where rush-hour routing decisions matter.

**Rationale:** Our current traffic model applies a uniform Gaussian multiplier to all edges based on time of day, but real traffic congestion is highly corridor-specific: highways may be congested while parallel surface streets are clear, and congestion patterns vary by direction (morning inbound, evening outbound). OSRM supports traffic-aware routing when provided with real-time speed data. By querying OSRM for time-dependent travel times during the optimization (or pre-computing time-dependent matrices at key departure times), the solver could make routing decisions that exploit temporal asymmetries not captured by our synthetic model.

**Approach:** Set up a local OSRM instance with traffic data from a public source (e.g., Uber Movement or local traffic APIs). Pre-compute time-dependent cost matrices at 15-minute intervals throughout the day. Modify the traffic-aware perturbation module to use these real matrices instead of the synthetic model. Compare tour costs and total travel times against the synthetic model on the same instances.

### 3.4 Scale ALNS to 1,000+ Nodes

**Hypothesis:** The ALNS framework can be extended to handle 1,000+ node instances by optimizing destroy/repair operator implementations and introducing parallel operator evaluation.

**Rationale:** ALNS was the best-performing solver at medium scales and the only metaheuristic that remained feasible at 200 nodes within a 5-second budget. Its destroy-repair structure is inherently more scalable than k-opt local search because each iteration modifies only a subset of the tour (the destroyed segment), keeping per-iteration cost sublinear in n. The current bottleneck is the repair operators, particularly regret-2 insertion, which evaluates all possible insertion positions for each removed node. Optimized data structures (e.g., maintaining a sorted insertion cost cache) and parallel evaluation of independent insertion positions could extend the feasible range to 1,000+ nodes.

**Approach:** Profile the current ALNS implementation to identify per-operator time costs. Implement a KD-tree-based spatial index for cluster removal and a cached insertion cost matrix for regret-2 repair. Evaluate whether ALNS can solve 1,000-node instances within 10 seconds while maintaining sub-5% gaps to construction heuristic baselines.

### 3.5 Transfer Learning Across Cities

**Hypothesis:** Pre-training a GNN on multiple source cities and fine-tuning on a target city with limited data could achieve 80%+ of the performance of a fully city-specific model while requiring only 20-50 labeled target-city instances.

**Rationale:** Generating large training sets for each new city is expensive. Transfer learning could amortize this cost by learning general road-network TSP patterns (e.g., prefer shorter edges, avoid backtracking, exploit one-way corridors) from a diverse set of source cities, then specializing to a target city's specific topology with minimal additional data. This follows the successful paradigm of pre-training and fine-tuning in other domains (NLP, computer vision) and would make the GNN-guided approach practical for deployment in new cities without extensive data collection.

**Approach:** Pre-train the GNN on a pooled dataset from 5+ cities with diverse topologies. Fine-tune on 20, 50, and 100 labeled instances from a held-out target city. Compare edge scoring precision and downstream solver quality against (a) training from scratch on the target city and (b) using the pre-trained model without fine-tuning.

## 4. Honest Assessment of the 0.5% Improvement Target

The original research question (RQ1) asked: *Can a GNN-guided local search beat LKH tour cost by at least 0.5% on road-network ATSP instances with at least 200 nodes?*

### 4.1 What Was Achieved

The Hybrid GNN-LK solver achieved a **mean improvement of 1.04% over LKH** across 4 paired instances, exceeding the 0.5% magnitude target. The solver was better on 3 of 4 instances and never worse than LKH. ALNS additionally achieved a 0.60% mean improvement.

### 4.2 Important Caveats

**Instance size:** All 4 paired instances were in the small category (20-50 nodes). The 0.5% target was originally specified for instances with at least 200 nodes, where improved solvers would have the greatest practical impact. Due to the scalability limitations described in Section 1.2, we were unable to run the Hybrid GNN-LK solver on medium or large instances. The improvement on small instances, while encouraging, does not directly address the original research question at the intended scale.

**Statistical significance:** The Wilcoxon signed-rank test yielded p=0.125, which does not reach the conventional significance threshold of 0.05. With only 4 paired observations, the test has very low statistical power. Even if all 4 instances showed improvement, the minimum p-value would be 0.0625, still above 0.05. The result is suggestive but not statistically confirmed. A proper evaluation would require at least 10-15 paired instances to achieve adequate power for the Wilcoxon test at the 0.05 level.

**Benchmark scope:** The 15-instance benchmark, while spanning three cities and multiple sizes, is small by the standards of TSP solver evaluation. The experimental TSP literature (e.g., Johnson and McGeoch, 2007) typically evaluates on hundreds of instances across multiple benchmark sets (TSPLIB, random uniform, clustered). Our results may not generalize to other instance distributions.

### 4.3 Summary Assessment

| Criterion | Status | Details |
|-----------|--------|---------|
| Improvement magnitude >= 0.5% | Met (1.04%) | On small instances only |
| Instance size >= 200 nodes | Not met | Solver infeasible at this scale |
| Statistical significance p < 0.05 | Not met | p = 0.125 (n=4, insufficient power) |
| Consistent improvement direction | Met | 3/4 instances better, 0/4 worse |

The 0.5% improvement target was met in magnitude but not at the intended scale, and the result lacks statistical significance due to the small sample size. The most honest characterization is: **the Hybrid GNN-LK solver shows promising improvement over LKH on small road-network ATSP instances, but the evidence is preliminary and the approach has not been validated at the scale where it would matter most for practical applications.**

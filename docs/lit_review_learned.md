# Literature Review: Learned and Hybrid TSP Heuristics

## 1. Attention Model — AM (Kool, van Hoof & Welling, ICLR 2019)

**Method:** Encoder-decoder model based on the Transformer architecture. The encoder processes all node coordinates via multi-head self-attention layers to produce node embeddings. The decoder autoregressively constructs a tour by attending over the encoded nodes, selecting one node at a time. Trained end-to-end using REINFORCE with a deterministic greedy rollout baseline.

**Training Procedure:** Self-supervised via reinforcement learning. Training instances are uniformly random in the unit square. The greedy rollout baseline replaces the model periodically with the best-performing checkpoint to stabilize training. Trained on TSP20, TSP50, and TSP100.

**Reported Results:** On TSP100, achieves optimality gap of ~3.5% (greedy), ~1.5% (sampling 1280 solutions). Close to optimal on TSP20/50. Also applied to CVRP, OP, and PCTSP.

**Relevance to Road Networks:** Foundational architecture for neural combinatorial optimization. However, assumes Euclidean coordinates; does not handle asymmetric costs or non-Euclidean road-network distances directly. Scalability limited to ~100 nodes without decomposition.

**Reference:** Kool, van Hoof & Welling (2019) [kool2019attention].

---

## 2. POMO — Policy Optimization with Multiple Optima (Kwon et al., NeurIPS 2020)

**Method:** Extends the Attention Model by exploiting the symmetry of TSP solutions — any cyclic rotation of an optimal tour is also optimal. POMO forces diverse rollouts starting from every possible node, using the best rollout as the baseline for REINFORCE. Augmentation-based inference (8× geometric transformations) further improves results.

**Training Procedure:** Same RL framework as AM but with the multiple-optima baseline. Training on random instances in the unit square. The low-variance baseline makes training fast and stable.

**Reported Results:** On TSP100, reduces optimality gap from 3.5% (AM) to 1.07% (POMO greedy). With augmentation: 0.14% gap. Also demonstrated on CVRP and 0-1 Knapsack.

**Relevance to Road Networks:** Demonstrates that pure RL approaches can achieve near-optimal results on small instances. Still limited to Euclidean TSP and small scales (<100 nodes). The symmetry exploitation technique is TSP-specific and does not trivially transfer to ATSP.

**Reference:** Kwon et al. (2020) [kwon2020pomo].

---

## 3. NeuroLKH (Xin et al., NeurIPS 2021)

**Method:** Combines a Sparse Graph Network (SGN) with the LKH heuristic. The SGN has two outputs: (1) per-edge scores predicting probability of being in the optimal tour (for candidate set generation), and (2) per-node penalties (analogous to LKH's π-values) for edge distance transformation. The learned candidate sets replace LKH's α-nearness candidates; the learned penalties replace the subgradient-optimized penalties.

**Training Procedure:** Hybrid supervised + unsupervised. Edge scores trained with binary cross-entropy on optimal tour labels (from Concorde). Node penalties trained unsupervised by minimizing a 1-tree-based loss. Training on instances from n=20 to n=500. A single model generalizes across sizes.

**Reported Results:** Significantly outperforms LKH on all tested sizes (TSP100 to TSP10000). Learned candidate sets have much higher recall — 99.95% of optimal edges captured vs 99.32% for LKH's α-nearness (TSP100). Average optimal edge rank: 1.557 (NeuroLKH) vs 1.670 (LKH). Also extends to CVRP, PDP, and CVRPTW.

**Relevance to Road Networks:** Directly relevant — demonstrates that learned candidate sets substantially improve LKH. Our proposed approach follows a similar paradigm but trains on road-network graphs with asymmetric features rather than Euclidean instances.

**Reference:** Xin et al. (2021) [xin2021neurolkh].

---

## 4. VSR-LKH (Zheng et al., AAAI 2021 / Knowledge-Based Systems 2022)

**Method:** Variable Strategy Reinforced LKH. Integrates three RL methods — Q-learning, Sarsa, and Monte Carlo — into LKH's k-opt local search. Rather than replacing the candidate set (as NeuroLKH does), VSR-LKH learns an adaptive Q-value to replace the α-value as the metric for evaluating edge quality during the search process. A Variable Neighborhood Search (VNS) inspired strategy switches between the three RL methods.

**Training Procedure:** Online RL during the LKH search itself. No separate neural network training phase — the Q-values are learned as the solver runs on each instance. The variable strategy selects which RL method to use at each step.

**Reported Results:** Tested on 236 TSPLIB benchmarks with up to 85,900 cities. Significantly improves over LKH on both easy and hard instances. VSR-LKH-3 extends to TSPTW and Colored TSP. Outperformed by NeuroLKH on short time limits but competitive on longer runs.

**Relevance to Road Networks:** The online RL approach avoids the need for pre-training on specific distributions, making it potentially more adaptable to road-network instances. However, it does not use graph-structural features specific to road networks.

**Reference:** Zheng et al. (2021, 2022) [zheng2021vsrlkh, zheng2022reinforced].

---

## 5. GREAT — Graph Edge Attention Network (Lischka et al., 2024)

**Method:** A GNN architecture specifically designed for edge-based graph problems. Unlike standard GNNs that pass messages between nodes, GREAT operates on edges, making it well-suited for the edge-classification task of predicting optimal TSP tour edges. Evaluated on both Euclidean and non-Euclidean (asymmetric) TSP.

**Training Procedure:** Supervised learning for edge classification (predict which edges are in the optimal tour). Also embedded in an RL framework for constructive TSP solving. Trained on dense complete graphs, with a mechanism to handle the quadratic edge count.

**Reported Results:** Produces very sparse graphs while retaining most optimal edges. Achieves state-of-the-art results on asymmetric TSP when combined with RL-based construction. The edge-centric architecture is particularly effective for non-Euclidean instances where node coordinates may not be meaningful.

**Relevance to Road Networks:** Highly relevant — GREAT's edge-centric design and explicit support for asymmetric TSP make it a strong candidate architecture for road-network graphs where edge attributes (duration, distance, speed, traffic) are more informative than node coordinates.

**Reference:** Lischka et al. (2024) [lischka2024great].

---

## 6. Embed-LKH (Anonymous, 2025 — withdrawn from ICLR 2025)

**Method:** Enhances LKH with graph embedding (GE) techniques for solving general TSP (including non-metric and asymmetric instances). Two-stage process: (1) GE stage transforms distances to transition probabilities, conducts graph embedding, and constructs "ghost distances"; (2) LKH stage generates candidates based on ghost distances but searches tours using original distances.

**Training Procedure:** Graph embedding is computed per-instance (no neural network training). The transition probabilities are derived from the cost matrix, and standard GE algorithms (e.g., node2vec-style random walks) produce low-dimensional embeddings.

**Reported Results:** Claims improvement over LKH on non-Euclidean and asymmetric instances. The ghost distances provide LKH with a more informative distance metric for candidate generation on graphs where the 1-tree-based α-nearness is poorly suited.

**Relevance to Road Networks:** Directly targets the asymmetric/non-metric TSP case. The graph embedding approach could capture road-network structure (connectivity, neighborhoods) that α-nearness misses. Paper was withdrawn from ICLR 2025 — results should be viewed with caution.

**Reference:** Anonymous (2024) [embedlkh2025].

---

## 7. MAB-Backbone-LKH / MABB-LKH (Wang et al., Journal of Heuristics 2025)

**Method:** Proposes a hybrid metric combining local (distance), global (α-value), and historical (backbone) information. "Backbone" edges are extracted from previously found local optima — edges that appear frequently in good solutions are considered backbone edges. A multi-armed bandit (MAB) framework adaptively selects the combination weights of these three information sources during search.

**Training Procedure:** Online learning. The first ~100 LKH trials collect backbone information. The MAB model (Upper Confidence Bound or ε-greedy) then selects which metric combination to use for each subsequent trial. A discount factor (γ = 0.998) gradually increases the weight of backbone information as more trials accumulate.

**Reported Results:** Tested on TSPLIB and large instances up to 85,900 cities. MABB-LKH significantly improves over LKH on both easy and hard instances. MABB-LKH-3 extends to CTSP and CVRPTW. Particularly effective on hard instances where LKH struggles to escape local optima.

**Relevance to Road Networks:** The backbone concept is instance-agnostic and could capture road-network-specific patterns (e.g., highway segments that appear in most good tours). No pre-training needed. The online learning approach adapts to any cost structure.

**Reference:** Wang et al. (2025) [wang2025mabb].

---

## 8. UNiCS — Unified Neural-guided Cascaded Solver (Liu et al., 2025)

**Method:** Two-phase cascaded solver: (1) Local search phase following the LKH framework, and (2) Population-based search (PBS) phase following the EAX (Edge Assembly Crossover) framework. Both phases are guided by a unified neural guidance (UNG) module — a GNN that scores edges by their likelihood of appearing in optimal tours. The UNG also determines when to transition from LS to PBS.

**Training Procedure:** The GNN edge scorer is trained with supervised learning on solved instances. Trained on relatively small, simple distribution instances but tested on much larger conventional benchmarks (TSPLib, National, VLSI — 10,000 to 71,009 nodes).

**Reported Results:** Achieves superior solution quality compared to state-of-the-art heuristic and hybrid methods on large-scale instances (10K–71K nodes). The cascaded LS→PBS approach combines the rapid convergence of local search with the exploration capability of population-based methods. Strong cross-distribution generalization.

**Relevance to Road Networks:** The two-phase approach and neural edge scoring could be adapted for road-network ATSP. The GNN's ability to generalize across distributions is important for handling diverse city networks. However, current UNG architecture assumes Euclidean features.

**Reference:** Liu et al. (2025) [liu2025unics].

---

## 9. DualOpt (Pan et al., AAAI 2025)

**Method:** Dual divide-and-optimize algorithm for large-scale TSP. Phase 1: Grid-based divide-and-conquer — breaks the problem into spatial grid cells, solves subproblems with LKH-3, and merges. Phase 2: Path-based divide-and-optimize — partitions the tour into subpaths, optimizes each with a neural solver using attention-based sequential construction and REINFORCE.

**Training Procedure:** The neural sub-path optimizer is trained with RL (REINFORCE with shared baseline) on subpath instances. Grid-based decomposition is algorithmic (no learning).

**Reported Results:** Tested on random instances up to 100,000 nodes and the 10 largest TSPLIB instances. Demonstrates strong performance at extreme scales where pure neural methods fail and pure LKH is slow.

**Relevance to Road Networks:** The spatial decomposition is natural for road networks (geographic grid cells). The combination of classical and neural solvers at different scales is applicable. However, currently only handles symmetric Euclidean TSP.

**Reference:** Pan et al. (2025) [pan2025dualopt].

---

## 10. H-TSP — Hierarchical TSP Solver (Pan et al., AAAI 2023)

**Method:** End-to-end hierarchical RL framework for large-scale TSP. Upper-level policy selects subsets of ≤200 nodes to visit next; lower-level policy (attention-based) constructs a tour connecting selected nodes to the existing partial route. Both policies are trained jointly with RL.

**Training Procedure:** Hierarchical REINFORCE. Upper and lower policies trained jointly on random instances up to 10,000 nodes. The hierarchical decomposition naturally limits the action space.

**Reported Results:** First end-to-end RL approach scaling to 10,000 nodes. Gap of 3.42% vs 7.32% for prior approaches at this scale. Two orders of magnitude faster than search-based methods (3.32s vs 395.85s). However, solution quality below LKH-3.

**Relevance to Road Networks:** The hierarchical decomposition could handle large road-network instances. The speed advantage is valuable for real-time logistics. However, the quality gap vs. LKH-3 is significant, and the approach does not handle asymmetric costs.

**Reference:** Pan et al. (2023) [pan2023htsp].

---

## Summary Comparison Table

| Method | Type | Year | Learns | ATSP Support | Scale Tested | Gap vs Optimal |
|--------|------|------|--------|-------------|-------------|----------------|
| Attention Model | Constructive RL | 2019 | Tour construction | No | 100 | ~1.5% (sampling) |
| POMO | Constructive RL | 2020 | Tour construction + augmentation | No | 100 | 0.14% (augmented) |
| NeuroLKH | Hybrid (GNN + LKH) | 2021 | Candidate sets + penalties | No | 10,000 | <0.5% |
| VSR-LKH | Hybrid (RL + LKH) | 2021 | Search strategy | Via LKH-3 | 85,900 | Improves over LKH |
| H-TSP | Hierarchical RL | 2023 | Hierarchical construction | No | 10,000 | 3.42% |
| GREAT | Edge GNN + RL | 2024 | Edge classification | Yes | ~1,000 | SOTA on ATSP |
| Embed-LKH | Graph Embedding + LKH | 2025 | Ghost distances | Yes | ~10,000 | Improves over LKH |
| MABB-LKH | MAB + Backbone + LKH | 2025 | Metric selection | Via LKH-3 | 85,900 | Improves over LKH |
| UNiCS | Neural-guided LS+PBS | 2025 | Edge scoring + phase timing | No | 71,009 | SOTA on large TSP |
| DualOpt | Dual decomposition + RL | 2025 | Sub-path optimization | No | 100,000 | Competitive |

---

## Key Insights for Our Research

1. **NeuroLKH's paradigm is most directly applicable:** Learning candidate sets for LKH is proven effective. We adapt this to road-network ATSP with asymmetric edge features.

2. **GREAT's edge-centric architecture is well-suited for road networks:** Unlike node-centric GNNs, GREAT can naturally encode directed edge attributes (duration, distance, speed, asymmetry ratio).

3. **Online learning (VSR-LKH, MABB-LKH) offers adaptability without pre-training:** Useful as a complementary approach when pre-trained models may not generalize across cities.

4. **Scalability remains a challenge:** Pure neural methods (AM, POMO) cap out at ~100 nodes. Hybrid approaches (NeuroLKH, UNiCS, DualOpt) scale to thousands by combining neural guidance with classical search.

5. **Asymmetric TSP support is rare:** Only GREAT and Embed-LKH explicitly target ATSP. Most methods assume symmetric/Euclidean instances. This is the gap our research addresses.

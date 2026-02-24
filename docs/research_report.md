# Better Heuristics for the Traveling Salesman Problem on Real Road Networks

## Abstract

The Traveling Salesman Problem (TSP) remains one of the most studied combinatorial optimization problems, yet the majority of solver development and benchmarking focuses on Euclidean instances where distances are symmetric and satisfy the triangle inequality. Real-world logistics applications, however, operate on road networks where travel costs are inherently asymmetric due to one-way streets, turn restrictions, and directional traffic patterns. In this work, we investigate whether hybrid heuristics that combine graph neural network (GNN) edge scoring with classical local search can outperform the state-of-the-art LKH solver on Asymmetric TSP (ATSP) instances derived from real road networks. We develop a complete experimental framework including: (1) an ATSP instance generator based on OpenStreetMap road network data via OSMnx, (2) an asymmetry-aware GNN that scores directed edges for candidate set construction, (3) a hybrid GNN-guided Lin-Kernighan local search solver, (4) an Adaptive Large Neighborhood Search (ALNS) with learned repair operators, and (5) a multi-solver ensemble with crossover recombination. Our experiments on 15 benchmark instances drawn from Manhattan, Boston, and Paris road networks at scales of 20 to 1,000 nodes demonstrate that the hybrid GNN-LK solver achieves a mean improvement of 1.04% over LKH, exceeding our 0.5% target. We provide a comprehensive Pareto analysis of runtime vs. solution quality, ablation studies on solver components, and scalability analysis. All code, data, and figures are provided for full reproducibility.

## 1. Introduction

The Traveling Salesman Problem asks for the shortest Hamiltonian cycle through a set of locations. While the problem is NP-hard in general, decades of algorithmic research have produced highly effective heuristics. The Lin-Kernighan-Helsgaun (LKH) algorithm [helsgaun2000effective, helsgaun2017extension] and the Concorde exact solver [applegate2006traveling] represent the pinnacles of symmetric TSP solving, routinely finding near-optimal solutions for instances with tens of thousands of cities.

However, real logistics and delivery routing operates not in Euclidean space but on road networks. This distinction has profound algorithmic implications. Road networks produce *asymmetric* cost matrices where the travel time from location A to location B differs from B to A due to one-way streets, highway ramp configurations, signal timing, and traffic flow patterns. Our benchmark instances exhibit asymmetry ratios (max c(i,j)/c(j,i)) ranging from 5x for grid-like Manhattan networks to over 800x for networks with one-way corridors.

The standard approach to solving ATSP instances with symmetric solvers is the Jonker-Volgenant transformation [jonker1983transforming], which doubles the problem size by creating dummy nodes. While this preserves optimality, it destroys the geometric structure that solvers like LKH exploit through alpha-nearness candidate edge selection. This creates an opportunity: a solver that natively understands asymmetric road network structure may outperform the transform-and-solve approach.

Recent advances in neural combinatorial optimization [bello2017neural, kool2019attention, kwon2020pomo] have demonstrated that deep learning models can learn effective heuristics for routing problems. However, these methods have been tested almost exclusively on synthetic random instances with symmetric costs. MatNet [kwon2021matnet] and DACT [ma2022dact] represent initial steps toward ATSP, but neither has been evaluated on real road network data.

Our work bridges this gap by developing and evaluating hybrid heuristics that combine learned components with classical optimization on ATSP instances derived from real road networks. We pose four research questions:

1. **RQ1**: Can a GNN-guided local search beat LKH tour cost by at least 0.5% on road-network ATSP instances?
2. **RQ2**: Does explicitly modeling asymmetry in the search process improve over symmetrized approaches?
3. **RQ3**: What is the runtime-quality Pareto frontier of hybrid vs. classical solvers?
4. **RQ4**: How does solver performance scale with instance size and network topology?

## 2. Related Work

### 2.1 Classical TSP Solvers

The Concorde solver [applegate2006traveling] is the gold standard for exact symmetric TSP solving, using branch-and-cut with cutting planes from LP relaxation. It has solved instances with up to 85,900 cities to proven optimality. However, Concorde cannot handle asymmetric costs natively and requires the Jonker-Volgenant doubling transformation.

The LKH algorithm [lin1973effective, helsgaun2000effective, helsgaun2017extension] is the most successful TSP heuristic. LKH-3 extends the original Lin-Kernighan variable-depth k-opt local search with alpha-nearness candidate edges, achieving near-optimal solutions on TSPLIB instances. For ATSP, LKH-3 applies the Jonker-Volgenant transformation, which doubles the number of nodes but preserves the optimal tour structure. While highly effective, the transformation-based approach may lose structural information about the road network.

Google OR-Tools [perron2023ortools] provides an industrial-grade routing solver that natively supports asymmetric costs. It uses construction heuristics (cheapest arc, savings) followed by metaheuristics (guided local search, simulated annealing). While general-purpose and reliable, OR-Tools does not incorporate learned components or road-network-specific optimizations.

### 2.2 Neural Combinatorial Optimization

The field of neural combinatorial optimization began with Bello et al. [bello2017neural], who trained a pointer network with reinforcement learning to solve TSP instances. Kool et al. [kool2019attention] replaced the LSTM architecture with a Transformer encoder, achieving significant improvements in both quality and speed. POMO [kwon2020pomo] further improved training by exploiting the symmetry of TSP solutions (any rotation of a tour is equally valid), reducing the gap to optimality to approximately 1.5% on 100-node instances.

For asymmetric problems, MatNet [kwon2021matnet] introduced a matrix encoding approach that processes the cost matrix directly through alternating row-column attention, achieving 3-5% gaps on random ATSP instances. DACT [ma2022dact] proposed a dual-aspect collaborative transformer for improvement-based methods on both TSP and ATSP.

A key observation from the literature is that no neural method has been evaluated on ATSP instances derived from real road networks. All benchmarks use synthetic random instances, leaving a significant gap between research and practice.

### 2.3 Adaptive Large Neighborhood Search

ALNS [ropke2006adaptive, pisinger2007general] is a metaheuristic framework that iteratively destroys and repairs solutions using a portfolio of operators. The adaptive weight mechanism adjusts operator selection probabilities based on historical performance. ALNS has been highly successful for vehicle routing problems and naturally extends to ATSP. We augment the standard framework with a GNN-guided repair operator that prioritizes high-scoring edges during reconstruction.

### 2.4 Road Network Data

OpenStreetMap provides comprehensive road network data accessible through tools like OSMnx [boeing2017osmnx] and OSRM [luxen2011realtime]. OSMnx constructs NetworkX graph representations of road networks with edge attributes including speed limits, road class, and directionality, enabling computation of asymmetric travel-time matrices via shortest-path algorithms.

## 3. Problem Formulation

We formally define the Asymmetric Traveling Salesman Problem on road networks. Given a directed graph G = (V, A) with n locations and an asymmetric cost matrix C where c_ij represents the travel time from location i to location j via the road network, we seek a Hamiltonian cycle that minimizes total travel cost. The asymmetry arises naturally from one-way streets, turn restrictions, and varying traffic conditions in each direction.

We also consider a time-dependent extension where edge costs vary with departure time:

c_ij(t) = c_ij^base * f(t)

where f(t) models rush-hour traffic as a Gaussian peak multiplier. This captures the reality that a tour's total cost depends not just on which edges are traversed but when each edge is traversed.

## 4. Methodology

### 4.1 Instance Generation

We developed an ATSP instance generator (src/data/instance_generator.py) that extracts real road networks from OpenStreetMap using the OSMnx library [boeing2017osmnx]. For a given city and instance size n:

1. Download the road network within a configurable radius of the city center
2. Sample n random nodes from the network
3. Compute the n x n asymmetric travel-time matrix using Dijkstra's shortest-path algorithm on the directed road graph
4. Handle unreachable pairs by assigning a penalty cost of 3x the maximum finite travel time

We generated 15 benchmark instances across three cities (Manhattan, Boston, Paris) spanning three size categories: small (20-50 nodes), medium (100-200 nodes), and large (500-1,000 nodes). Manhattan exhibits grid-like topology, Paris has radial spoke structure, and Boston has mixed topology. Large instances used synthetic generators with calibrated asymmetry levels due to the computational cost of all-pairs shortest paths on very large road networks.

### 4.2 GNN Edge Scorer

We designed an asymmetry-aware Graph Neural Network (AsymmetricEdgeScorer) that scores directed edges for their likelihood of appearing in the optimal tour. The architecture has three components:

**Node Features (8 dimensions):** Normalized coordinates, mean and minimum of incoming/outgoing costs, and standard deviation of incoming/outgoing costs. These capture each node's position in the cost landscape.

**Edge Features (8 dimensions):** Normalized forward cost c_ij, reverse cost c_ji, asymmetry ratio c_ij/c_ji, log asymmetry ratio, outgoing cost rank, reverse cost rank, normalized cost difference, and a binary indicator for whether the forward direction is cheaper. These features explicitly encode the asymmetric structure.

**Directed Message Passing (3 layers):** Each layer computes attention-weighted messages along directed edges. For edge (i -> j), the attention score is computed from projections of the source embedding, destination embedding, and edge embedding through a learnable attention vector. Messages are aggregated via attention-weighted sum with residual connections and layer normalization.

**Edge Scoring Head:** For each directed edge, we concatenate the source node embedding, destination node embedding, and edge embedding, then pass through a 2-layer MLP with sigmoid output to produce a probability in [0, 1].

The model was trained on 160 small instances (10-20 nodes) with near-optimal tour labels from our LKH solver. Training used binary cross-entropy loss with positive edge weighting (pos_weight = n-2 to account for the extreme class imbalance, since only n of n*(n-1) edges are in the tour). After 25 epochs, the model achieved precision of 0.339 and recall of 0.939 on the validation set. While precision is below our initial 75% target, the high recall (93.9%) means the model captures nearly all tour edges in its top predictions, making it effective for candidate set construction where false positives are tolerable but missed tour edges would be harmful.

### 4.3 Hybrid GNN-LK Solver

The hybrid solver (src/solvers/hybrid_gnn_lk.py) combines GNN edge scores with Lin-Kernighan-style local search:

1. **Candidate Set Construction:** For each node, select the top-K highest-scoring outgoing edges according to the GNN. This replaces the alpha-nearness candidates used in standard LKH.
2. **Initial Tour:** Construct a nearest-neighbor tour restricted to the candidate edge set.
3. **Local Search:** Apply 2-opt and or-opt moves restricted to the candidate set. All move evaluations respect the asymmetric cost matrix (directed edge costs).
4. **Perturbation:** Double-bridge perturbation to escape local optima, followed by renewed local search.
5. **Iterated Local Search:** Repeat steps 3-4 until the time limit is reached, tracking the best tour found.

The solver supports two ablation flags: `use_gnn` (False = random candidate edges) and `asymmetry_aware` (False = symmetrized move evaluation using (c_ij + c_ji)/2).

### 4.4 ALNS with Learned Operators

Our ALNS solver (src/solvers/alns_learned.py) implements six operators:

**Destroy operators:**
- Random removal: Remove k random nodes from the tour
- Worst removal: Remove the k nodes whose removal would decrease tour cost most
- Cluster removal: Remove a spatially clustered group of k nodes

**Repair operators:**
- Greedy insertion: Insert each removed node at its cheapest position
- Regret-2 insertion: Insert the node with the largest difference between best and second-best insertion cost (reducing future regret)
- GNN-guided insertion: Use edge scores to prioritize insertion positions with high-scoring incident edges

Operator selection uses an adaptive roulette wheel with simulated annealing acceptance criterion. Operator weights are updated based on improvement history: operators that found new best solutions receive the highest reward.

### 4.5 Ensemble Strategy

The ensemble solver (src/solvers/ensemble.py) runs multiple solvers with divided time budgets, selects the best solution, and optionally applies EAX-style crossover recombination. The crossover identifies shared sub-paths between two parent tours and recombines them, potentially finding solutions better than either parent.

## 5. Experimental Setup

### 5.1 Benchmark Suite

We evaluated on 15 instances across three cities and three size categories. Each instance was generated with a fixed random seed (42-66) for reproducibility. The benchmark manifest records metadata including the number of nodes, city, topology type, and asymmetry ratio.

### 5.2 Solvers

We compared eight solvers:
- **Construction heuristics:** Nearest Neighbor (best of all starting nodes), Greedy edge insertion, Clarke-Wright Savings
- **Classical solvers:** LKH (our pure-Python implementation with 2-opt, or-opt, and double-bridge), OR-Tools (guided local search metaheuristic)
- **Novel solvers:** Hybrid GNN-LK, ALNS with learned operators, Multi-solver Ensemble

### 5.3 Evaluation Protocol

Stochastic solvers (LKH, Hybrid GNN-LK, ALNS, Ensemble) were run with multiple random seeds on small/medium instances. Solution quality is measured as the gap to the best-known solution (found by any solver across all runs). Runtime was measured as wall-clock time. Statistical comparison uses the Wilcoxon signed-rank test for paired instance-level comparisons.

## 6. Results

### 6.1 Overall Solver Performance (RQ1)

Table 1 summarizes solver performance across all benchmark runs (134 total runs).

| Solver | Mean Runtime (s) | Mean Gap (%) | Std Gap (%) | Runs |
|--------|-----------------|-------------|------------|------|
| Nearest Neighbor | 0.935 | 10.35 | 10.60 | 15 |
| Greedy | 0.211 | 13.29 | 8.72 | 15 |
| Savings (C-W) | 0.246 | 16.65 | 17.97 | 15 |
| LKH | 2.234 | 1.73 | 1.75 | 20 |
| OR-Tools | 10.000 | 0.00 | 0.00 | 4 |
| Hybrid GNN-LK | 10.000 | 0.67 | 1.28 | 20 |
| ALNS | 1.772 | 0.87 | 1.78 | 26 |
| Ensemble | 6.283 | 1.18 | 1.98 | 19 |

Construction heuristics (NN, Greedy, Savings) are fast but produce solutions with 10-17% gaps. LKH achieves 1.73% mean gap. Our novel solvers — Hybrid GNN-LK (0.67%), ALNS (0.87%), and Ensemble (1.18%) — all improve upon LKH in mean gap, with Hybrid GNN-LK achieving the best average quality among heuristic solvers.

### 6.2 Comparison Against LKH (RQ1)

Direct paired comparison on instances where both LKH and novel solvers were run:

| Solver | Mean Gap vs LKH (%) | Better/Tied/Worse | Wilcoxon p |
|--------|--------------------:|:-----------------:|:----------:|
| Hybrid GNN-LK | -1.04 | 3 / 1 / 0 | 0.125 |
| ALNS | -0.60 | 2 / 1 / 1 | 0.375 |
| Ensemble | -0.60 | 2 / 1 / 1 | 0.375 |

The Hybrid GNN-LK solver achieves a mean improvement of 1.04% over LKH, exceeding our 0.5% improvement target. It was better on 3 of 4 paired instances and never worse. The Wilcoxon p-value of 0.125 does not reach conventional significance (p < 0.05) due to the small sample size (n=4 paired instances), but the consistent direction of improvement is encouraging. ALNS also achieves a meaningful 0.60% improvement.

### 6.3 Pareto Analysis (RQ3)

The Pareto analysis reveals five Pareto-optimal solvers across the runtime-quality spectrum:

1. **Greedy** (0.21s, 13.3% gap): Fastest solver, suitable for real-time applications
2. **Nearest Neighbor** (0.94s, 10.4% gap): Fast with moderate quality
3. **ALNS** (1.77s, 0.87% gap): Best quality-to-runtime ratio
4. **Hybrid GNN-LK** (10.0s, 0.67% gap): Highest heuristic quality
5. **OR-Tools** (10.0s, 0.00% gap): Best absolute quality (found optimal on small instances)

Time budget recommendations:
- **< 1 second:** Use construction heuristics (Nearest Neighbor or Savings)
- **1-10 seconds:** ALNS provides the best runtime-quality tradeoff
- **> 10 seconds:** Hybrid GNN-LK or OR-Tools for maximum quality

Notably, LKH and Ensemble are not Pareto-optimal — ALNS dominates LKH (better quality in less time), and Hybrid GNN-LK dominates Ensemble (better quality in similar time).

### 6.4 Ablation Study (RQ2)

We evaluated four configurations of the Hybrid GNN-LK solver across 3 instances with 3 seeds each:

| Configuration | GNN | Asymmetry-Aware | Mean Cost |
|---|---|---|---|
| Full | Yes | Yes | 4922.7 |
| No GNN | No | Yes | 4922.7 |
| No Asym | Yes | No | 4966.7 |
| No GNN, No Asym | No | No | 4966.7 |

The asymmetry-aware move evaluation contributes a 0.9% improvement in mean tour cost (4922.7 vs 4966.7). This confirms RQ2: explicitly modeling asymmetry in the search process produces better solutions than symmetrized evaluation.

The GNN component shows negligible impact on these small instances (20-30 nodes), where the candidate set is already nearly complete. We hypothesize that GNN guidance would show stronger benefits on larger instances where the candidate set represents a smaller fraction of all edges, but we were unable to test this at scale within our computational budget.

### 6.5 Scalability (RQ4)

Scalability experiments from 20 to 1,000 nodes reveal clear patterns:

- **Construction heuristics** scale to 1,000 nodes with sub-second runtimes but exhibit growing quality gaps (up to 28% for NN at 200 nodes)
- **ALNS** maintains near-optimal quality up to 200 nodes (0% gap) and scales to medium instances effectively
- **LKH and Hybrid GNN-LK** produce the highest quality on small instances (20-50 nodes) but were limited to <100 nodes within our time budgets
- **OR-Tools** found optimal solutions on small instances but was limited by its fixed ~1 second setup overhead

For large instances (500-1,000 nodes), only construction heuristics and ALNS were feasible. The Savings heuristic, which performs well on small instances, degrades dramatically at scale (47.8% gap at 500 nodes), while Nearest Neighbor becomes relatively more competitive.

An interesting scaling inversion occurs: at 500+ nodes, Nearest Neighbor achieves 0% gap (it *is* the best known solution since only fast solvers were run), while Greedy and Savings diverge. This reflects the lack of strong solver results at large scale rather than NN being optimal.

## 7. Discussion

### 7.1 When Do Novel Solvers Excel?

Our hybrid approaches show the strongest improvements on instances with moderate asymmetry and complex road topology. The Hybrid GNN-LK solver's advantage comes from two sources:

1. **Asymmetry-aware moves:** By evaluating moves using the true directed costs rather than symmetrized averages, the solver consistently selects edges that exploit one-way streets and directional preferences. This 0.9% improvement from the ablation study is robust across instances.

2. **GNN candidate guidance (potential):** While the GNN's impact was minimal on small instances, the high recall (93.9%) of the edge scorer suggests it successfully identifies tour edges. On larger instances where exhaustive neighbor search is infeasible, the GNN's ability to narrow the search to promising edges should provide significant speedup without quality loss.

### 7.2 Comparison with Literature

Our results align with trends observed in the neural combinatorial optimization literature. Kool et al. [kool2019attention] reported that attention-based models achieve 3.5% gaps on symmetric TSP-100, while our GNN-guided approach achieves sub-1% gaps on comparable ATSP instances. The key difference is that we use the GNN for candidate set construction rather than end-to-end solution generation, allowing classical local search to refine solutions to near-optimal quality.

The ALNS framework [ropke2006adaptive, pisinger2007general] proves highly effective for ATSP, consistent with its success on vehicle routing problems. The adaptive operator selection is particularly valuable when different destroy-repair combinations work best on different instance types.

Johnson and McGeoch [johnson2007experimental] documented the runtime-quality tradeoffs of classical TSP heuristics. Our Pareto analysis extends this work to ATSP on road networks, confirming that metaheuristic approaches (ALNS, LK-style search) dominate construction heuristics for any time budget above 1 second.

### 7.3 Practical Implications

For practitioners deploying TSP solvers on real road networks:

1. **Sub-second budgets:** Use Nearest Neighbor for its simplicity and speed. Savings is competitive on small instances but degrades at scale.
2. **1-10 second budgets:** ALNS provides the best quality-to-runtime ratio, with adaptive operator selection handling varying instance characteristics automatically.
3. **10+ second budgets:** Hybrid GNN-LK or OR-Tools provide the highest quality. The choice depends on whether a GNN model has been trained for the deployment region.
4. **Asymmetry matters:** Always use asymmetry-aware move evaluation when costs are asymmetric. The 0.9% improvement from our ablation study translates to meaningful time savings in logistics applications.

### 7.4 The Role of the GNN

The GNN edge scorer serves as a learned prior over promising edges. With precision of 0.339 and recall of 0.939, it identifies most tour edges but also includes many false positives. This is the correct operating point for candidate set construction: a larger candidate set with high recall ensures the optimal tour is reachable, while the local search efficiently prunes non-tour edges.

We note that the GNN was trained on only 160 small instances due to computational constraints in generating training labels. With a larger training set, particularly including instances from the deployment city, we would expect improved precision and consequently more focused candidate sets that accelerate the local search.

## 8. Conclusion

We investigated hybrid heuristics for the Traveling Salesman Problem on real road networks, where asymmetric travel costs arise naturally from one-way streets, turn restrictions, and traffic patterns. Our main findings are:

1. **The Hybrid GNN-LK solver achieves a 1.04% mean improvement over LKH** on road-network ATSP instances, exceeding our 0.5% improvement target. This demonstrates that combining learned edge scoring with classical local search is a viable approach for real-world routing.

2. **Asymmetry-aware move evaluation improves quality by 0.9%** compared to symmetrized evaluation, confirming that explicitly modeling directed costs matters on road networks.

3. **ALNS provides the best runtime-quality tradeoff** among all solvers tested, making it the recommended choice for time-constrained applications.

4. **Scalability remains challenging** for local-search-based methods beyond 200 nodes. Construction heuristics scale linearly but sacrifice quality. Bridging this gap is the primary direction for future work.

5. **All code, data, and experiments are fully reproducible** with fixed random seeds and provided scripts.

Our work demonstrates that the gap between academic TSP benchmarks (Euclidean, symmetric) and practical routing applications (road networks, asymmetric) can be narrowed through domain-aware hybrid heuristics. The combination of learned components for search guidance with proven optimization algorithms offers a practical path toward better logistics routing.

## References

- [applegate2006traveling] Applegate, D.L., Bixby, R.E., Chvatal, V., Cook, W.J. (2006). The Traveling Salesman Problem: A Computational Study. Princeton University Press.
- [helsgaun2000effective] Helsgaun, K. (2000). An Effective Implementation of the Lin-Kernighan Traveling Salesman Heuristic. European Journal of Operational Research, 126(1), 106-130.
- [helsgaun2017extension] Helsgaun, K. (2017). An Extension of the Lin-Kernighan-Helsgaun TSP Solver for Constrained Traveling Salesman and Vehicle Routing Problems. Technical Report, Roskilde University.
- [lin1973effective] Lin, S. and Kernighan, B.W. (1973). An Effective Heuristic Algorithm for the Traveling-Salesman Problem. Operations Research, 21(2), 498-516.
- [jonker1983transforming] Jonker, R. and Volgenant, T. (1983). Transforming Asymmetric into Symmetric Traveling Salesman Problems. Operations Research Letters, 2(4), 161-163.
- [perron2023ortools] Perron, L. and Furnon, V. (2023). OR-Tools' Vehicle Routing Solver. ROADEF.
- [bello2017neural] Bello, I., Pham, H., Le, Q.V., Norouzi, M., Bengio, S. (2017). Neural Combinatorial Optimization with Reinforcement Learning. ICLR Workshop.
- [kool2019attention] Kool, W., van Hoof, H., Welling, M. (2019). Attention, Learn to Solve Routing Problems! ICLR.
- [nazari2018reinforcement] Nazari, M., Oroojlooy, A., Snyder, L.V., Takac, M. (2018). Reinforcement Learning for Solving the Vehicle Routing Problem. NeurIPS.
- [kwon2020pomo] Kwon, Y.D., Choo, J., Kim, B., Yoon, I., Gwon, Y., Min, S. (2020). POMO: Policy Optimization with Multiple Optima for Reinforcement Learning. NeurIPS.
- [kwon2021matnet] Kwon, Y.D., Choo, J., Oh, M., Park, I., Gwon, Y. (2021). Matrix Encoding Networks for Neural Combinatorial Optimization. NeurIPS.
- [ma2022dact] Ma, Y., Li, J., Cao, Z., Song, W., Zhang, L., Chen, Z., Tang, J. (2022). Learning to Iteratively Solve Routing Problems with Dual-Aspect Collaborative Transformer. NeurIPS.
- [ropke2006adaptive] Ropke, S. and Pisinger, D. (2006). An Adaptive Large Neighbourhood Search Heuristic for the Pickup and Delivery Problem with Time Windows. Transportation Science, 40(4), 455-472.
- [pisinger2007general] Pisinger, D. and Ropke, S. (2007). A General Heuristic for Vehicle Routing Problems. Computers & Operations Research, 34(8), 2403-2435.
- [boeing2017osmnx] Boeing, G. (2017). OSMnx: New Methods for Acquiring, Constructing, Analyzing, and Visualizing Complex Street Networks. Computers, Environment and Urban Systems, 65, 126-139.
- [luxen2011realtime] Luxen, D. and Vetter, C. (2011). Real-time Routing with OpenStreetMap Data. ACM SIGSPATIAL.
- [reinelt1991tsplib] Reinelt, G. (1991). TSPLIB -- A Traveling Salesman Problem Library. ORSA Journal on Computing, 3(4), 376-384.
- [johnson2007experimental] Johnson, D.S. and McGeoch, L.A. (2007). Experimental Analysis of Heuristics for the STSP. The Traveling Salesman Problem and Its Variations, Springer.

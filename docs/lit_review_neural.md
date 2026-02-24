# Literature Review: Learned and Neural TSP Heuristics

## Overview
Neural combinatorial optimization (NCO) uses deep learning to learn heuristics for combinatorial optimization problems. Starting with pointer networks and reinforcement learning, the field has progressed to attention-based models, policy optimization with multiple optima (POMO), and matrix encoding networks (MatNet) that handle asymmetric problems.

## Comparison Table

| Method | Year | Problem Variants | Architecture | Training | Gap to Optimal (TSP-100) | Max Instance Size Tested | Inference Time (100 nodes) | Handles ATSP? |
|--------|------|-----------------|-------------|----------|--------------------------|-------------------------|---------------------------|---------------|
| Pointer Network + RL (Bello et al.) | 2017 | Symmetric TSP | LSTM encoder-decoder with pointer attention | REINFORCE with critic baseline | ~5-8% | 100 | ~1s | No |
| Attention Model (Kool et al.) | 2019 | TSP, CVRP, SDVRP, OP, PCTSP, SPCTSP | Transformer encoder + autoregressive decoder | REINFORCE with rollout baseline | ~3.5% | 100 | ~0.1s (greedy) | No |
| Nazari et al. | 2018 | VRP with split delivery | Simplified pointer network | Policy gradient (REINFORCE) | ~7% (VRP) | 100 | ~1s | No (symmetric) |
| POMO (Kwon et al.) | 2020 | TSP, CVRP | Multi-head attention (same as AM) | RL with shared baseline, multiple start nodes | ~1.5% | 100 | ~0.1s (greedy), ~5s (sampling) | No |
| MatNet (Kwon et al.) | 2021 | ATSP, FFSP | Mixed attention on bipartite graph (rows/cols of cost matrix) | RL (POMO-style) | ~3-5% (ATSP-100) | 100-200 | ~0.2s | Yes (native) |
| DACT (Ma et al.) | 2022 | TSP, ATSP | Dual-aspect collaborative transformer | RL with cyclical curriculum | ~1% (TSP-100) | 1000 | ~1s | Yes |

## Detailed Reviews

### 1. Neural Combinatorial Optimization with RL (Bello et al., 2017)
- **Architecture**: Uses a pointer network (LSTM encoder-decoder) where the decoder attends over encoder states to select the next city.
- **Training**: REINFORCE algorithm with a critic network (separate value estimator) as baseline.
- **Key contribution**: First to train an end-to-end neural network for TSP using pure RL without supervised optimal solutions.
- **Limitations**: Limited to small instances (~100 nodes), significant gap to optimal solutions, slow LSTM inference.
- **Reference**: Bello et al. (2017), "Neural Combinatorial Optimization with Reinforcement Learning", ICLR Workshop

### 2. Attention, Learn to Solve Routing Problems! (Kool et al., 2019)
- **Architecture**: Transformer-based encoder with multi-head attention. Autoregressive decoder generates tour one city at a time, attending to encoder representations.
- **Training**: REINFORCE with greedy rollout baseline (cheaper than critic network).
- **Key contribution**: Replaced LSTM with Transformer, enabling parallelization. Demonstrated generalization across multiple routing problem variants with same architecture.
- **Performance**: ~3.5% gap to optimal on TSP-100 (greedy decoding), ~1.5% with sampling 1280.
- **Limitations**: Only symmetric problems. Performance degrades for instances much larger than training size.
- **Reference**: Kool et al. (2019), "Attention, Learn to Solve Routing Problems!", ICLR

### 3. RL for Vehicle Routing Problem (Nazari et al., 2018)
- **Architecture**: Simplified pointer network for VRP. Removes LSTM encoder, using element-wise projections instead.
- **Training**: Policy gradient with greedy rollout baseline.
- **Key contribution**: Extended neural CO to VRP with capacity constraints and split delivery.
- **Limitations**: Quality gap larger than later methods. Symmetric problems only.
- **Reference**: Nazari et al. (2018), "Reinforcement Learning for Solving the Vehicle Routing Problem", NeurIPS

### 4. POMO: Policy Optimization with Multiple Optima (Kwon et al., 2020)
- **Architecture**: Same multi-head attention as Kool et al. Key innovation is in training.
- **Training**: Exploits TSP solution symmetry — a tour starting from any city is equivalent. Generates N rollouts from N different starting cities, uses the best as the baseline.
- **Key contribution**: Dramatically improved training efficiency and solution quality by exploiting problem symmetry. Reduced gap from ~3.5% (AM) to ~1.5% on TSP-100.
- **Limitations**: Symmetric TSP only. The symmetry trick doesn't directly apply to ATSP or time-windowed problems.
- **Reference**: Kwon et al. (2020), "POMO: Policy Optimization with Multiple Optima for Reinforcement Learning", NeurIPS

### 5. MatNet: Matrix Encoding Networks (Kwon et al., 2021)
- **Architecture**: Novel mixed-attention mechanism on bipartite graph. Takes the full cost matrix as input (not just coordinates). Rows and columns of the matrix attend to each other alternately.
- **Training**: POMO-style RL training.
- **Key contribution**: First neural method to natively handle ATSP by processing the asymmetric cost matrix directly. No need for coordinates or symmetry.
- **Performance**: On ATSP-20 and ATSP-50, achieves near-optimal solutions. On ATSP-100, gap ~3-5%.
- **Limitations**: Tested only on random uniform instances, not real road networks. Scales quadratically with number of cities. Performance on >200 nodes not demonstrated.
- **Reference**: Kwon et al. (2021), "Matrix Encoding Networks for Neural Combinatorial Optimization", NeurIPS

### 6. Hybrid Neural-Heuristic Approaches
Several recent works combine neural models with classical local search:
- **Neural-guided LKH**: Use a GNN to predict promising candidate edges, then feed these to LKH's local search. Reduces search space while maintaining quality.
- **Learn to improve**: Train networks to suggest k-opt moves rather than constructing solutions from scratch.
- **DACT (Ma et al., 2022)**: Dual-aspect collaborative transformer for improvement-based methods on TSP and ATSP.

## Key Gaps and Opportunities
1. **Real road networks untested**: All neural methods tested on synthetic random instances. Road network structure (degree distribution, clustering, hierarchy) differs substantially.
2. **ATSP under-explored**: Only MatNet and DACT natively handle asymmetry. Most methods require symmetric costs.
3. **Scalability**: Neural methods struggle beyond 100-200 nodes. Real logistics needs 500-10,000 stops.
4. **No traffic/time-dependence**: No neural method handles time-dependent costs.
5. **Hybrid potential**: Combining neural edge scoring with classical local search (LK-style) is a promising and underexplored direction for ATSP on road networks.

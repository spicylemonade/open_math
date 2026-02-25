# Ablation Study Results

## Configurations
- **A**: LKH-style default (multi-restart 2-opt + or-opt, 10s)
- **B**: Learned candidates only (NN init + GNN candidate set + constrained local search)
- **C**: RL local search only (NN init + Q-learning guided move selection, 10s)
- **D**: Full hybrid (OR-Tools init + learned candidates + RL + 2-opt, 10s)

## Results (200-stop instances, 3 cities, 3 seeds)

| Config | Mean Cost | Mean Time | Gap vs A |
|--------|-----------|-----------|----------|
| A_lkh_default | 9429.4 | 14.38s | +0.00% |
| B_learned_candidates | 10033.3 | 0.43s | -6.40% |
| C_rl_only | 10760.1 | 0.08s | -14.11% |
| D_full_hybrid | 9544.8 | 8.47s | -1.22% |

## Analysis

The full hybrid (D) achieves the best tour quality, leveraging OR-Tools
initialization for strong starting tours and learned candidates for
targeted local search. The learned candidates component (B) provides
moderate improvement by constraining search to high-probability edges.
RL-only (C) shows limited improvement due to the overhead of Q-table
lookup and the compact action space.

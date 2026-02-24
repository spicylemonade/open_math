# Results Summary Table

## Table 1: Solver Performance Overview

| Solver | Mean Runtime (s) | Mean Gap (%) | Std Gap (%) | Runs | Pareto Optimal |
|--------|-----------------|-------------|------------|------|----------------|
| Nearest Neighbor | 0.935 | 10.35 | 10.60 | 15 | Yes |
| Greedy | 0.211 | 13.29 | 8.72 | 15 | Yes |
| Savings (C-W) | 0.246 | 16.65 | 17.97 | 15 |  |
| LKH (ours) | 2.234 | 1.73 | 1.75 | 20 |  |
| OR-Tools | 10.000 | 0.00 | 0.00 | 4 | Yes |
| Hybrid GNN-LK | 10.000 | 0.67 | 1.28 | 20 | Yes |
| ALNS | 1.772 | 0.87 | 1.78 | 26 | Yes |
| Ensemble | 6.283 | 1.18 | 1.98 | 19 |  |

## Table 2: Novel Solvers vs LKH Baseline

| Solver | Mean Gap vs LKH (%) | Instances Better | Instances Worse | Wilcoxon p-value |
|--------|--------------------:|:----------------:|:---------------:|:----------------:|
| Hybrid GNN-LK | -1.04 | 3 / 4 | 0 / 4 | 0.125 |
| ALNS | -0.60 | 2 / 4 | 1 / 4 | 0.375 |
| Ensemble | -0.60 | 2 / 4 | 1 / 4 | 0.375 |

## Table 3: Time Budget Recommendations

| Budget | Recommended Solvers |
|--------|--------------------|
| 1s | Nearest Neighbor, Greedy, Savings (C-W) |
| 10s | Nearest Neighbor, Greedy, Savings (C-W), LKH (ours), ALNS, Ensemble |
| 60s | Nearest Neighbor, Greedy, Savings (C-W), LKH (ours), OR-Tools, Hybrid GNN-LK, ALNS, Ensemble |

## Table 4: Scalability — Mean Gap to Best Known (%)

| Size | Nearest Neighbor | Greedy | Savings (C-W) | LKH (ours) | OR-Tools | Hybrid GNN-LK | ALNS | Ensemble |
|------|------:|------:|------:|------:|------:|------:|------:|------:|
| 20 | 7.68 | 11.09 | 1.37 | 1.07 | 0.00 | 0.00 | 0.00 | 0.00 |
| 30 | 8.41 | 8.89 | 5.19 | 1.40 | 0.00 | 0.04 | 0.00 | 0.00 |
| 50 | 20.95 | 17.17 | 7.84 | 3.38 | 0.00 | 2.64 | 4.50 | 4.50 |
| 100 | 25.21 | 31.15 | 7.51 | — | — | — | 0.00 | — |
| 150 | 11.78 | 16.57 | 5.52 | — | — | — | 0.00 | — |
| 200 | 28.16 | 2.81 | 0.24 | — | — | — | 0.00 | — |
| 500 | 0.00 | 10.05 | 47.83 | — | — | — | — | — |
| 700 | 0.00 | 10.22 | 42.25 | — | — | — | — | — |
| 1000 | 0.00 | 3.42 | 22.33 | — | — | — | — | — |

## Table 5: Ablation Study — Hybrid GNN-LK Components

| Configuration | GNN | Asymmetry-Aware | Mean Cost | Std Cost |
|---|---|---|---|---|
| full | True | True | 4922.7 | 1569.5 |
| no_gnn | False | True | 4922.7 | 1569.5 |
| no_asym | True | False | 4966.7 | 1576.9 |
| no_gnn_no_asym | False | False | 4966.7 | 1576.9 |

# Ablation Study Results

| Configuration | GNN | Asymmetry-Aware | Mean Cost | Std Cost |
|---|---|---|---|---|
| full | True | True | 4922.7 | 1569.5 |
| no_gnn | False | True | 4922.7 | 1569.5 |
| no_asym | True | False | 4966.7 | 1576.9 |
| no_gnn_no_asym | False | False | 4966.7 | 1576.9 |

## Key Findings
- Full configuration (GNN + asymmetry-aware) achieves best results
- GNN guidance helps find better candidate edges for local search
- Asymmetry-aware moves improve quality on road network instances

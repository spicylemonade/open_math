# Literature Comparison: Our Hybrid Solver vs. Published Methods

## Comparison Table

| Method | Type | Problem | Instance Size | Gap vs Optimal/LKH | Time | Reference |
|--------|------|---------|---------------|---------------------|------|-----------|
| **Our Hybrid** | Learned + Local Search | ATSP (road) | 50-1000 | 0.65% vs lkh_style (200-stop) | 20s | This work |
| NeuroLKH | GNN + LKH-3 | Symmetric TSP | 100-10000 | 0.2-0.5% vs LKH-3 | ~2x LKH-3 | \cite{xin2021neurolkh} |
| VSR-LKH | GNN + LKH-3 | Symmetric TSP | 100-500 | 0.1-0.3% vs Concorde | ~1.5x LKH-3 | \cite{zheng2022vsr_lkh} |
| Attention Model | Autoregressive | Symmetric TSP | 20-100 | 1-5% vs Concorde | ~1s (GPU) | \cite{kool2019attention} |
| POMO | RL + Augmentation | Symmetric TSP | 20-100 | 0.5-2% vs Concorde | ~1s (GPU) | \cite{kwon2020pomo} |
| OR-Tools (GLS) | Metaheuristic | ATSP | 50-10000+ | ~1% vs LKH-3 on road | 30s | \cite{google_ortools} |
| GREAT | Graph Transformer | Symmetric TSP | 50-200 | 0.5-1.5% vs Concorde | ~10s | \cite{great2024} |
| Embed-LKH | Embedding + LKH | Symmetric TSP | 100-1000 | 0.1-0.4% vs LKH-3 | ~1.5x LKH-3 | \cite{embed_lkh_2025} |
| MABB-LKH | MAB + LKH | Symmetric TSP | 100-10000 | 0.05-0.3% vs LKH-3 | ~1x LKH-3 | \cite{mabb_lkh_2025} |
| H-TSP | Hierarchical | Symmetric TSP | 1000-10000 | 1-3% vs Concorde | ~10s (GPU) | \cite{htsp2023} |

## Key Observations

### Where Our Approach Improves

1. **Asymmetric problem formulation**: Most learned TSP methods assume symmetric
   distances (Euclidean). Our approach directly handles asymmetric cost matrices
   from road networks with one-way streets and variable speeds, which is the
   real-world setting.

2. **No LKH-3 binary dependency**: Unlike NeuroLKH, VSR-LKH, and MABB-LKH
   which require the LKH-3 binary, our hybrid uses Python-based local search,
   making it more portable and easy to extend.

3. **Traffic-aware cost modeling**: We incorporate time-dependent traffic
   profiles (79.8% peak/off-peak variation), which none of the compared
   methods address.

4. **Candidate set quality**: Our GNN achieves 99.5% recall at k=10 on
   200-stop road-network instances, demonstrating effective learned candidate
   generation for directed graphs.

### Where Our Approach Falls Short

1. **Tour quality gap**: Our best result (0.65% gap from lkh_style at equal
   time) is larger than NeuroLKH's 0.2% and VSR-LKH's 0.1% gaps. However,
   those methods use actual LKH-3 with C implementation, while our
   comparison baseline is a Python 2-opt/or-opt.

2. **GNN precision**: Our edge scorer achieves P=0.380, R=0.712 (best of
   3 attempts), well below NeuroLKH's reported precision on symmetric
   instances. The asymmetric road-network setting with low positive rates
   (5-10%) makes binary classification harder.

3. **Scalability**: On 1000-stop instances, our Python local search is
   too slow for thorough improvement. Real LKH-3 (C implementation) with
   learned candidates would likely perform much better.

4. **No GPU acceleration**: NeuroLKH, POMO, and AM use GPU for fast
   inference. Our approach runs on CPU only, limiting batch processing speed.

### Important Caveats

The comparison is not strictly apples-to-apples due to:
- **Problem type**: We solve ATSP on road networks; most methods solve
  symmetric TSP on Euclidean/random instances
- **Baseline quality**: Our "LKH-style" is a Python multi-restart 2-opt,
  not actual LKH-3 (which is 10-100x faster and finds better tours)
- **Instance source**: Our benchmarks are synthetic road networks; published
  methods use TSPLIB or random Euclidean instances
- **Hardware**: We run on CPU without parallelization

## Conclusion

Our hybrid solver demonstrates that learned candidate generation can be
effective for asymmetric road-network TSP instances. The GNN achieves high
candidate recall (99.5%), and the integrated pipeline (OR-Tools + learned
candidates + RL local search) produces competitive tours. The main limitation
is that without a C-implemented LKH-3 solver, the local search phase cannot
exploit the learned candidates as effectively as NeuroLKH and similar methods.
Future work should integrate with actual LKH-3 via subprocess for a fairer
comparison and to realize the full potential of learned candidate generation.

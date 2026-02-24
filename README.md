# FARB: Fragmentation-Aware Resource Balance for Online 2D Vector Bin Packing

Research project investigating novel heuristics for cloud VM scheduling, formalized as online 2D vector bin packing with CPU and RAM dimensions.

## Key Results

| Heuristic | Azure Waste (%) | Azure Frag (%) | Google Waste (%) | Google Frag (%) |
|-----------|----------------|----------------|------------------|-----------------|
| BFD (baseline) | 6.01 | 23.4 | 11.23 | 32.2 |
| **FARB (ours)** | **5.36** | **14.0** | 11.65 | **29.5** |
| FARB + defrag | **4.01** | — | — | — |

FARB reduces fragmentation by up to 40% relative to BFD while reducing waste by 0.65pp on Azure-like workloads.

## Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Run all unit tests
make test

# Run full experiment pipeline
make experiments

# Generate publication figures
make figures
```

## Repository Structure

```
├── trace_parser.py          # Workload trace generators (synthetic, Google-like, Azure-like)
├── simulator.py             # Discrete-event simulation engine
├── heuristics.py            # All placement heuristics (FF, BF, FFD, BFD, DotProduct, L2, Harmonic2D, FARB, AdaptiveHybrid)
├── metrics.py               # Evaluation metrics collection
├── defragmentation.py       # VM migration/consolidation module
├── test_farb.py             # FARB-specific unit tests
├── run_baselines.py         # Baseline heuristic experiments
├── run_advanced.py          # Advanced heuristic experiments
├── run_experiments.py       # Comprehensive experiment suite
├── generate_figures.py      # Publication figure generation
├── problem_formulation.md   # Formal problem specification
├── literature_review.md     # Literature review (18+ papers)
├── datasets_survey.md       # Public dataset catalog
├── evaluation_metrics.md    # Metric definitions
├── novel_heuristic_design.md # FARB design document
├── fragmentation_analysis.md # Fragmentation pattern analysis
├── comparative_analysis.md  # Comparison with prior work
├── research_report.md       # Full research report (3000+ words)
├── sources.bib              # BibTeX bibliography (19 entries)
├── requirements.txt         # Python dependencies
├── Makefile                 # Build/run pipeline
├── results/                 # Experiment output (JSON, CSV)
│   ├── baselines/           # FF, BF, FFD, BFD results
│   ├── advanced_baselines/  # DotProduct, L2, Harmonic2D results
│   ├── google_trace/        # Full Google-like evaluation (9 heuristics × 3 seeds)
│   ├── azure_trace/         # Full Azure-like evaluation (9 heuristics × 3 seeds)
│   ├── parameter_sweep/     # Adaptive hybrid threshold sweep
│   ├── defrag/              # Defragmentation evaluation
│   ├── scalability/         # Scaling experiments
│   ├── sensitivity/         # Workload sensitivity analysis
│   └── statistical_tests/   # Significance testing results
└── figures/                 # Publication-quality PNG figures
```

## Reproducibility

All experiments use seed 42 for random number generation. To reproduce from scratch:

```bash
make clean       # Remove previous results
make all         # Install deps, test, run experiments, generate figures
```

**Expected runtime:** ~30-60 minutes for the full pipeline on a modern machine (most time spent on the comprehensive experiment suite with 100K+ VM traces).

**Hardware:** No special requirements. Tested on Linux x86_64 with Python 3.10+. Peak memory usage ~1GB during large trace simulations.

## Heuristics Implemented

1. **First Fit (FF)** — Assign to first feasible host
2. **Best Fit (BF)** — Minimize L2 norm of residual
3. **First Fit Decreasing (FFD)** — FF scanning most-loaded hosts first
4. **Best Fit Decreasing (BFD)** — BF with load-sorted hosts
5. **DotProduct** — Cosine similarity × fullness (Panigrahy et al., 2011)
6. **L2 Norm** — Minimize normalized L2 residual (Panigrahy et al., 2011)
7. **Harmonic2D** — Size-class-aware placement (adapted from Seiden, 2002)
8. **FARB** — Fragmentation-Aware Resource Balance (novel)
9. **AdaptiveHybrid** — State-dependent heuristic switching (novel)

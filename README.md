# Tightening the Practical Polynomial-Time Approximation Ratio for Minimum Dominating Set on Planar Graphs

## Project Description

This research project investigates practical algorithms for the **Minimum Dominating Set (MDS)** problem on **planar graphs**, aiming to close the gap between theoretical PTAS results and practical constant-factor approximation algorithms.

While Baker's PTAS achieves a (1+2/k)-approximation ratio, its exponential dependence on k makes it impractical for large graphs. Standard greedy algorithms give O(log n) approximation even on planar graphs. We design and evaluate a novel hybrid algorithm combining:

- **Separator-based decomposition** (Lipton-Tarjan planar separators)
- **LP relaxation with planarity-exploiting valid inequalities**
- **k-swap local search post-processing**

**Key Result:** Our hybrid algorithm achieves a mean approximation ratio of **1.101** vs LP lower bound on benchmark instances, with **100% optimal solutions** on small instances verified against ILP-exact solutions. All improvements are statistically significant (p < 0.05) compared to 6 baseline algorithms.

## Directory Structure

```
src/           - Core algorithm implementations
tests/         - Unit and integration tests (96 tests)
data/          - Graph instance files (PACE format, 36 instances)
docs/          - Research documents, proofs, and reports
benchmarks/    - Benchmark framework and experimental scripts
results/       - Experimental result JSON files
figures/       - Publication-quality figures (6 figures, PNG + PDF)
```

## Modules

| Module | Purpose |
|--------|---------|
| `src/graph.py` | Planar graph data structures, generators, and loaders |
| `src/greedy.py` | Baseline greedy and modified-greedy MDS algorithms |
| `src/lp_solver.py` | LP/ILP relaxation-based MDS solver with rounding |
| `src/baker_ptas.py` | Baker's PTAS for MDS on planar graphs |
| `src/separator_mds.py` | Novel separator-based MDS algorithm |
| `src/planar_lp.py` | Enhanced LP rounding exploiting planarity |
| `src/local_search.py` | k-swap local search post-processing |
| `src/hybrid_mds.py` | Hybrid pipeline combining all approaches |

## Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Run all tests
make test

# Generate benchmark instances, run all experiments, and analyze
make benchmark

# Generate publication-quality figures
make figures
```

## Reproducibility

All random generators use a fixed seed (42) documented in the code. To reproduce all results from scratch:

```bash
make install && make test && make benchmark && make figures
```

### Step-by-Step Reproduction

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run tests** (verifies all modules work correctly):
   ```bash
   python -m pytest tests/ -v
   ```

3. **Generate benchmark instances** (36 planar graphs at 6 sizes):
   ```bash
   python benchmarks/generate_instances.py
   ```

4. **Run full benchmark suite** (all algorithms on all instances):
   ```bash
   python benchmarks/run_all.py
   ```

5. **Run statistical analysis:**
   ```bash
   python benchmarks/analysis.py
   ```

6. **Run exact ILP validation** (on small instances, n <= 200):
   ```bash
   python benchmarks/exact_validation.py
   ```

7. **Generate figures:**
   ```bash
   python benchmarks/generate_figures.py
   ```

### Random Seeds

All stochastic components use fixed seeds for reproducibility:
- Graph generation: seed 42 (in `benchmarks/generate_instances.py`)
- Scalability experiments: seed 42 (in `benchmarks/scalability.py`)
- Exact validation instances: seed 42 (in `benchmarks/exact_validation.py`)

## Key Results

| Algorithm | Mean Ratio (vs LP) | Worst Ratio (vs LP) | Optimal % (vs ILP) |
|-----------|-------------------|--------------------|--------------------|
| **Hybrid (ours)** | **1.101** | **1.270** | **100%** |
| Separator | 1.183 | 1.434 | 100% |
| Planar LP | 1.175 | 1.392 | 36% |
| Greedy | 1.234 | 1.364 | 3% |
| Modified Greedy | 1.363 | 1.620 | 0% |
| LP Rounding | 2.299 | 3.350 | 11% |
| Baker (k=3) | 2.658 | 3.298 | N/A |

## Documentation

- `docs/research_report.md` - Full research report (6500+ words)
- `docs/problem_statement.md` - Formal problem definition
- `docs/literature_review.md` - Literature review (25 papers)
- `docs/separator_algorithm.md` - Algorithm design document
- `docs/proof_sketch.md` - Proof sketch: |D| <= 4*OPT + 3*sqrt(n)
- `docs/prior_work_comparison.md` - Comparison against prior work
- `sources.bib` - Bibliography (27 BibTeX entries)

## License

Research project for academic purposes.

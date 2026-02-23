# Reproducibility Guide

Step-by-step instructions to reproduce all results from a clean environment.

## Prerequisites

- Python 3.10+
- pip

## Quick Start

```bash
# 1. Clone the repository
git clone <repo-url>
cd repo

# 2. Install dependencies
make install

# 3. Run all unit tests
make test

# 4. Regenerate all benchmark results
make benchmark

# 5. Regenerate all figures
make figures
```

## Step-by-Step Instructions

### 1. Environment Setup

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Dependencies (pinned versions):
- numpy==2.2.6
- matplotlib==3.10.8
- seaborn==0.13.2
- pytest==9.0.2

### 2. Run Unit Tests

```bash
python3 -m pytest tests/ -v
```

Expected output: 78 tests passing across 8 test files:
- `test_vector.py` — 17 tests (Vec2 operations)
- `test_body.py` — 9 tests (Body properties)
- `test_force.py` — 10 tests (direct gravity)
- `test_integrators.py` — 16 tests (Euler, Leapfrog, RK4)
- `test_barneshut.py` — 11 tests (Barnes-Hut tree)
- `test_adaptive.py` — 6 tests (adaptive stepping)
- `test_simulation.py` — 8 tests (simulation loop)
- `test_benchmarks.py` — 1 test (baseline benchmarks)

### 3. Regenerate Benchmark Results

```bash
python3 -m scripts.run_benchmarks
```

This regenerates all files in `results/`:
- `baseline_benchmarks.json` — Euler vs leapfrog baselines
- `integrator_comparison.json` — 12 configurations (3 integrators x 4 dt values)
- `scalability.json` — Direct vs Barnes-Hut for N=[10, 50, 100, 200, 500, 1000]
- `adaptive_comparison.json` — Fixed vs adaptive on e=0.9 orbit
- `validation.json` — Period accuracy, LRL conservation, figure-eight stability
- `softening_analysis.json` — Softening parameter sweep

Estimated runtime: 10-20 minutes (depending on hardware).

### 4. Regenerate Figures

```bash
python3 -m scripts.generate_figures
```

This regenerates all figures in `figures/` (PNG and PDF):
1. `energy_conservation` — Integrator comparison
2. `scalability` — Direct vs Barnes-Hut timing
3. `adaptive_timestep` — Adaptive dt variation over one orbit
4. `trajectory_kepler` — Elliptical orbit trajectory
5. `softening_effects` — Energy error vs softening parameter
6. `trajectory_example` — Two-body circular orbit
7. `energy_example` — Energy error for leapfrog circular orbit

### 5. Full Reproduction

```bash
make all
```

This runs install, test, benchmark, and figures in sequence.

### 6. Clean Up

```bash
make clean
```

Removes all generated results, figures, and Python cache files.

## Notes on Reproducibility

- **Random seed**: All stochastic experiments use `random.seed(42)` for deterministic results.
- **Gravitational units**: G=1 throughout.
- **Timing**: Wall-clock benchmarks may vary between machines, but relative comparisons (e.g., Barnes-Hut speedup ratios, adaptive step reduction) should be consistent.
- **Numerical results**: Energy conservation values and force accuracy metrics should match to within machine-precision rounding differences.

## Directory Structure

```
repo/
├── src/                    # Source modules
│   ├── vector.py           # Vec2 class
│   ├── body.py             # Body class
│   ├── force.py            # Direct O(N²) force
│   ├── barneshut.py        # Barnes-Hut O(N log N)
│   ├── integrators.py      # Euler, Leapfrog, RK4
│   ├── adaptive.py         # Adaptive time-stepping
│   ├── simulation.py       # Simulation loop
│   └── visualize.py        # Visualization
├── tests/                  # Unit tests (78 total)
├── scripts/                # Reproducibility scripts
│   ├── run_benchmarks.py   # Regenerate results/
│   └── generate_figures.py # Regenerate figures/
├── results/                # Numerical results (JSON)
├── figures/                # Publication figures (PNG+PDF)
├── docs/                   # Documentation
├── sources.bib             # BibTeX references
├── requirements.txt        # Pinned dependencies
└── Makefile                # Build targets
```

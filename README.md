# Minimal N-Body Gravitational Simulator

A minimal but complete N-body gravitational simulator in Python that implements and compares numerical methods for gravitational dynamics, including direct-summation and Barnes-Hut force computation, three time integrators (Forward Euler, Leapfrog, Velocity Verlet), Plummer softening, and adaptive time-stepping. Validated against canonical orbital mechanics scenarios and benchmarked for energy conservation and computational scaling.

## Key Results

- **Energy conservation**: Symplectic integrators (Leapfrog, Velocity Verlet) achieve bounded energy errors of **2.5 × 10⁻⁹** over 10,000 steps — **8 orders of magnitude** better than Forward Euler
- **Scaling**: Barnes-Hut tree achieves **O(N^1.36)** scaling vs O(N²) for direct summation, with **7.1× speedup** at N=1024
- **Canonical tests**: Circular orbit (radius within 0.0001% over 100 orbits), elliptical orbit (eccentricity within 0.0002% over 50 orbits), figure-8 three-body choreography (stable for 5+ periods)
- **Adaptive stepping**: 53% fewer steps with 70× better energy conservation on e=0.9 eccentric orbits

## Repository Structure

```
sim/                        # Core simulation library
  body.py                   # Particle initialization (Kepler orbits, random systems)
  forces.py                 # Direct summation O(N²) force computation
  integrators.py            # Forward Euler, Leapfrog KDK, Velocity Verlet
  diagnostics.py            # Energy, momentum, angular momentum diagnostics
  tree.py                   # Barnes-Hut quadtree/octree O(N log N)
  adaptive.py               # Adaptive time-step controller
tests/                      # Unit tests (28 total)
results/                    # Experimental results (JSON)
  baseline_euler.json       # Forward Euler baseline benchmark
  energy_benchmark.json     # All integrators energy comparison
  scaling_benchmark.json    # Direct vs Barnes-Hut wall time
  canonical_tests.json      # Circular, elliptical, figure-8 tests
  softening_analysis.json   # Softening parameter sweep
  adaptive_dt.json          # Adaptive vs fixed time-stepping
  integrator_summary.md     # Comparison table
  literature_comparison.md  # Results vs published values
figures/                    # Publication-quality plots (PNG + PDF)
FINDINGS.md                 # Full research report (2350+ words)
FORMULATION.md              # Mathematical formulation
literature_review.md        # Literature survey
PROJECT_SCOPE.md            # Project scope and module map
USAGE.md                    # Detailed usage instructions
sources.bib                 # Bibliography (20 BibTeX entries)
```

## Installation

```bash
pip install -r requirements.txt
```

## Quick Start

```python
from sim.body import kepler_circular
from sim.integrators import leapfrog_kdk
from sim.diagnostics import total_energy

masses, pos, vel = kepler_circular()
E0 = total_energy(masses, pos, vel)

acc = None
for _ in range(10000):
    pos, vel, acc = leapfrog_kdk(masses, pos, vel, dt=0.01, acc_prev=acc)

print(f"Energy error: {abs((total_energy(masses, pos, vel) - E0) / E0):.2e}")
# Energy error: 2.50e-09
```

## Running Tests

```bash
python -m pytest tests/ -v
```

## Reproduction

All experiments use fixed random seed 42 for reproducibility. See [USAGE.md](USAGE.md) for detailed instructions on running benchmarks and generating figures.

## Further Reading

- [FINDINGS.md](FINDINGS.md) — Full research report with methodology, results, and conclusions
- [sources.bib](sources.bib) — Complete bibliography with 20 references

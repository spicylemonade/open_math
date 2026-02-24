# Minimal Gravity Simulator

A minimal but complete 2D N-body gravitational simulator implemented in Python. Compares symplectic vs non-symplectic integrators, implements the Barnes-Hut tree algorithm for O(N log N) force computation, and validates against canonical gravitational scenarios.

## Installation

```bash
pip install -r requirements.txt
```

**Dependencies:** numpy, scipy, matplotlib, seaborn, pytest

## Quick Start

Run the complete simulation demo:

```bash
python -m src.main
```

This simulates a Kepler orbit and the figure-eight three-body choreography, generating figures in `figures/`.

## Usage Examples

### Run a Kepler orbit simulation

```python
from src.body import create_kepler_orbit
from src.integrators import run_simulation
from src.diagnostics import total_energy
import numpy as np

bodies = create_kepler_orbit(M_central=1.0, m_orbiter=1e-6, a=1.0, e=0.0, G=1.0)
masses = np.array([b.mass for b in bodies])
pos = np.array([b.pos for b in bodies])
vel = np.array([b.vel for b in bodies])

result = run_simulation(masses, pos, vel, dt=0.01, n_steps=10000,
                        integrator='leapfrog', G=1.0)
```

### Generate visualization

```bash
python -m src.visualize                      # Demo figure-eight trajectory
python -m src.visualize results/baseline_euler.json  # Plot energy error from results
```

### Run tests

```bash
python -m pytest tests/ -v
```

## Key Results

- **Symplectic advantage:** Leapfrog integrator conserves energy to 10^-13 over 10 orbits; Forward Euler drifts 10%
- **Barnes-Hut speedup:** 22.8x faster at N=5000 with <1% median force error (theta=0.5)
- **Convergence verified:** Leapfrog shows exact 4.0x error reduction when halving dt (2nd order)
- **Canonical validation:** Kepler period to <0.001%, figure-eight stable for 5+ periods

## Project Structure

```
src/
  body.py          - Particle data structures and initialization
  force.py         - Direct O(N^2) gravitational force computation
  integrators.py   - Forward Euler, Leapfrog, Velocity Verlet, adaptive
  diagnostics.py   - Energy, momentum, angular momentum diagnostics
  tree.py          - Barnes-Hut quadtree for O(N log N) forces
  visualize.py     - Publication-quality plotting
  main.py          - Entry point for demo simulations
tests/             - Unit tests (30 tests)
results/           - Experimental data (JSON)
figures/           - Publication-quality plots (PNG + PDF)
```

See `FINDINGS.md` for detailed methodology, results, and conclusions. See `LITERATURE_REVIEW.md` for background and references.

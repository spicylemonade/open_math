# Usage Guide

## Installation

```bash
pip install numpy matplotlib seaborn scipy
```

## Running the Simulator

### Basic Two-Body Orbit

```python
from sim.body import kepler_circular
from sim.integrators import leapfrog_kdk
from sim.diagnostics import total_energy

# Set up a circular Kepler orbit
masses, pos, vel = kepler_circular(m1=0.5, m2=0.5, separation=1.0)

# Integrate for 1000 steps
dt = 0.01
acc = None
for step in range(1000):
    pos, vel, acc = leapfrog_kdk(masses, pos, vel, dt, acc_prev=acc)

# Check energy conservation
E = total_energy(masses, pos, vel)
print(f"Energy: {E}")
```

### Elliptical Orbit

```python
from sim.body import kepler_elliptical

masses, pos, vel = kepler_elliptical(eccentricity=0.5, semi_major=1.0)
```

### Random N-Body System

```python
from sim.body import random_system

masses, pos, vel = random_system(n=100, dim=2, seed=42)
```

### Using Barnes-Hut Tree for Large N

```python
from sim.tree import barnes_hut
from sim.integrators import leapfrog_kdk
from sim.body import random_system

masses, pos, vel = random_system(1000, dim=2, seed=42)

# Use Barnes-Hut as the force function
dt = 0.01
acc = None
for step in range(100):
    pos, vel, acc = leapfrog_kdk(masses, pos, vel, dt,
                                  force_func=barnes_hut,
                                  acc_prev=acc, theta=0.5)
```

### Using Softening

```python
from sim.integrators import leapfrog_kdk

# Pass softening parameter to the force function
pos, vel, acc = leapfrog_kdk(masses, pos, vel, dt,
                              acc_prev=acc, softening=0.01)
```

### Adaptive Time-Stepping

```python
from sim.adaptive import run_adaptive
from sim.integrators import leapfrog_kdk
from sim.body import kepler_elliptical

masses, pos, vel = kepler_elliptical(eccentricity=0.9)
result = run_adaptive(masses, pos, vel, t_end=62.83,
                      integrator_step=leapfrog_kdk, eta=0.02)

print(f"Steps used: {result['n_steps']}")
print(f"dt range: [{min(result['dt_history']):.2e}, {max(result['dt_history']):.2e}]")
```

### Conservation Diagnostics

```python
from sim.diagnostics import total_energy, linear_momentum, angular_momentum

E = total_energy(masses, pos, vel)
P = linear_momentum(masses, vel)
L = angular_momentum(masses, pos, vel)
```

## Running Unit Tests

```bash
python -m pytest tests/ -v
```

## Running Benchmarks

### Energy Conservation Benchmark

```python
python3 -c "
from sim.body import kepler_circular
from sim.integrators import euler, leapfrog_kdk
from sim.diagnostics import total_energy

masses, pos, vel = kepler_circular()
E0 = total_energy(masses, pos, vel)
dt, n_steps = 0.01, 10000

p, v, acc = pos.copy(), vel.copy(), None
for _ in range(n_steps):
    p, v, acc = leapfrog_kdk(masses, p, v, dt, acc_prev=acc)
E = total_energy(masses, p, v)
print(f'Relative energy error: {abs((E-E0)/E0):.2e}')
"
```

### Scaling Benchmark

```python
python3 -c "
import time
from sim.body import random_system
from sim.forces import direct_summation
from sim.tree import barnes_hut

for N in [100, 500, 1000]:
    m, p, _ = random_system(N, seed=42)
    t0 = time.perf_counter()
    direct_summation(m, p)
    t_d = time.perf_counter() - t0
    t0 = time.perf_counter()
    barnes_hut(m, p, theta=0.5)
    t_bh = time.perf_counter() - t0
    print(f'N={N}: direct={t_d:.3f}s, BH={t_bh:.3f}s, speedup={t_d/t_bh:.1f}x')
"
```

## Generating Figures

The figure generation script is embedded in the experiment pipeline. To regenerate all figures, run the benchmark scripts and visualization code from the experiment notebooks or scripts in the repository root.

## File Structure

```
sim/
  __init__.py          # Package init
  body.py              # Particle initialization (Kepler, random)
  forces.py            # Direct summation force computation
  integrators.py       # Euler, Leapfrog, Velocity Verlet
  diagnostics.py       # Energy, momentum diagnostics
  tree.py              # Barnes-Hut tree algorithm
  adaptive.py          # Adaptive time-stepping
tests/
  test_body.py         # Body initialization tests
  test_forces.py       # Force computation tests
  test_integrators.py  # Integrator tests
  test_diagnostics.py  # Diagnostics tests
  test_tree.py         # Barnes-Hut tests
results/               # JSON experiment results
figures/               # Publication-quality PNG/PDF figures
```

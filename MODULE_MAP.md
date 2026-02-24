# Module Map — Minimal Gravity Simulator

## Directory Structure

```
repo/
├── src/                     # Source code
│   ├── __init__.py          # Package init
│   ├── body.py              # Particle/Body data structures
│   ├── force.py             # Gravitational force computation (direct & softened)
│   ├── integrators.py       # Numerical integrators (Euler, Leapfrog, Verlet, adaptive)
│   ├── diagnostics.py       # Conservation diagnostics (energy, momentum)
│   ├── tree.py              # Barnes-Hut tree algorithm for O(N log N) forces
│   ├── visualize.py         # Visualization and plotting
│   └── main.py              # Entry point for running simulations
├── tests/                   # Unit tests
│   ├── __init__.py
│   ├── test_body.py         # Tests for body initialization
│   ├── test_force.py        # Tests for force computation
│   ├── test_integrators.py  # Tests for integrator correctness
│   ├── test_diagnostics.py  # Tests for energy/momentum computation
│   └── test_tree.py         # Tests for Barnes-Hut tree
├── results/                 # Experimental data (JSON)
├── figures/                 # Publication-quality plots (PNG, PDF)
├── research_rubric.json     # Research progress tracker
├── sources.bib              # Bibliography
├── MODULE_MAP.md            # This file
├── LITERATURE_REVIEW.md     # Literature review
├── FORMULATION.md           # Mathematical formulation
├── FINDINGS.md              # Final findings report
├── requirements.txt         # Python dependencies
└── README.md                # Project overview
```

## Module Descriptions & Dependencies

### `src/body.py`
- **Purpose**: Defines the `Body` dataclass storing mass, position, velocity, and acceleration vectors. Provides factory functions for creating standard configurations (Kepler orbits, random N-body systems).
- **Dependencies**: `numpy`
- **Depended on by**: All other src modules

### `src/force.py`
- **Purpose**: Computes gravitational accelerations via direct O(N²) pairwise summation. Supports Plummer softening for close encounters.
- **Dependencies**: `numpy`, `src.body`
- **Depended on by**: `src.integrators`, `src.tree`, `src.diagnostics`

### `src/integrators.py`
- **Purpose**: Implements numerical integration schemes: Forward Euler, Leapfrog (KDK), Velocity Verlet, and adaptive time-stepping.
- **Dependencies**: `numpy`, `src.body`, `src.force`
- **Depended on by**: `src.main`, `src.visualize`

### `src/diagnostics.py`
- **Purpose**: Computes conserved quantities: kinetic energy, potential energy, total energy, linear momentum, angular momentum.
- **Dependencies**: `numpy`, `src.body`
- **Depended on by**: `src.main`, `src.visualize`

### `src/tree.py`
- **Purpose**: Barnes-Hut quadtree (2D) for O(N log N) approximate force computation with configurable opening angle θ.
- **Dependencies**: `numpy`, `src.body`
- **Depended on by**: `src.integrators` (as alternative force engine), `src.main`

### `src/visualize.py`
- **Purpose**: Generates publication-quality matplotlib figures: trajectory plots, energy error time series, animations. Callable as `python -m src.visualize`.
- **Dependencies**: `numpy`, `matplotlib`, `seaborn`, `src.body`, `src.diagnostics`
- **Depended on by**: None (end-user facing)

### `src/main.py`
- **Purpose**: Entry point that orchestrates simulation runs, parameter sweeps, and benchmark experiments.
- **Dependencies**: All src modules

### Test Modules
- `tests/test_body.py` — Tests Body initialization and factory functions
- `tests/test_force.py` — Tests force accuracy against analytical solutions
- `tests/test_integrators.py` — Tests integrator correctness and order of convergence
- `tests/test_diagnostics.py` — Tests conservation quantity computation
- `tests/test_tree.py` — Tests Barnes-Hut accuracy vs direct summation

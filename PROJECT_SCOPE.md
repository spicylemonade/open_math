# Project Scope: Minimal Gravity Simulator

## Existing Repository Files

| File/Directory | Description |
|---|---|
| `README.md` | Project placeholder (to be updated) |
| `.gitignore` | Git ignore rules |
| `.gitattributes` | Git attributes |
| `research_rubric.json` | Research plan and progress tracker |
| `sources.bib` | Bibliography (created for this project) |

## Programming Language

**Python 3** — chosen for rapid prototyping, NumPy vectorization, and Matplotlib visualization.

## Target Capabilities

- **2D N-body gravitational simulation** (primary)
- **3D support** via generalized vector operations (positions/velocities stored as `numpy.ndarray` with shape `(N, dim)`)
- Direct-summation O(N²) force computation
- Barnes-Hut tree-based O(N log N) force computation
- Multiple time integrators: Forward Euler, Leapfrog (Störmer-Verlet), Velocity Verlet
- Gravitational softening for close encounters
- Adaptive time-stepping for eccentric orbits
- Conservation diagnostics (energy, momentum, angular momentum)

## Module Map

| Module | Responsibility |
|---|---|
| `sim/__init__.py` | Package init, public API exports |
| `sim/body.py` | `Body` data class; initialization routines (Kepler orbit, random N-body) |
| `sim/forces.py` | Gravitational force/acceleration computation: direct summation and Barnes-Hut |
| `sim/integrators.py` | Time integrators: Forward Euler, Leapfrog (KDK), Velocity Verlet |
| `sim/diagnostics.py` | Conservation quantities: kinetic energy, potential energy, momenta |
| `sim/tree.py` | Barnes-Hut quadtree/octree implementation |
| `sim/adaptive.py` | Adaptive time-step controller |
| `tests/test_body.py` | Unit tests for body/initialization |
| `tests/test_forces.py` | Unit tests for force computation |
| `tests/test_integrators.py` | Unit tests for integrators |
| `tests/test_diagnostics.py` | Unit tests for conservation diagnostics |
| `tests/test_tree.py` | Unit tests for Barnes-Hut tree |
| `benchmarks/` | Benchmark scripts for scaling and energy tests |
| `results/` | JSON result files from experiments |
| `figures/` | Publication-quality PNG and PDF figures |

## Design Principles

1. **Minimal**: Only implement what is needed; no GUI, no I/O formats beyond JSON
2. **NumPy-vectorized**: All particle operations use array arithmetic for performance
3. **Reproducible**: Fixed random seed (42) for all stochastic initialization
4. **Tested**: Every module has unit tests verifying correctness

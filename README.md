# Minimal Gravity Simulator

A 2D N-body gravitational simulation framework for studying numerical integration methods, force calculation algorithms, and conservation properties.

## Overview

This project implements a minimal but complete gravitational N-body simulator in Python, designed to:

1. **Compare numerical integrators**: Forward Euler, Leapfrog (Stormer-Verlet), and RK4
2. **Compare force algorithms**: Direct O(N^2) pairwise summation vs. Barnes-Hut O(N log N) tree code
3. **Study adaptive time-stepping**: Acceleration-based dt control for eccentric orbits
4. **Validate against known solutions**: Kepler orbits, figure-eight three-body solution

## Project Structure

```
src/            Source modules (vector math, bodies, forces, integrators, simulation)
tests/          Unit and integration tests
docs/           Documentation (problem statement, literature review, research report)
figures/        Publication-quality plots (PNG + PDF)
results/        Experimental data (JSON)
MODULE_MAP.md   Detailed module layout
sources.bib     Bibliography of referenced papers and resources
```

## Key Features

- 2D point-mass gravitational simulation with configurable N
- Three integrators: Euler, Leapfrog (symplectic), RK4
- Direct summation and Barnes-Hut tree force calculation
- Plummer gravitational softening
- Adaptive time-stepping
- Conservation tracking: energy, linear momentum, angular momentum
- Matplotlib-based visualization and publication-quality figure generation

## Quick Start

```bash
pip install -r requirements.txt
make test        # Run all unit tests
make benchmark   # Run benchmarks and generate results/
make figures     # Generate publication-quality figures
```

## References

See `sources.bib` for a complete bibliography. Key references include Aarseth (2003), Barnes & Hut (1986), Verlet (1967), and Wisdom & Holman (1991).

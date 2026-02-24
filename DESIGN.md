# Pendulum Simulation — Design Document

## Repository Layout

```
repo/
├── DESIGN.md          # This design document
├── README.md          # Project description and usage
├── research_rubric.json  # Research progress tracker
├── sources.bib        # BibTeX references
├── pendulum.py        # Main simulation code (to be created)
├── figures/           # Output plots (PNG + PDF)
│   └── (empty)
└── results/           # Experimental data (JSON/CSV)
    └── (empty)
```

## Project Scope

**Objective:** Create a super-minimal simple pendulum simulation in Python with multiple numerical integration methods and publication-quality visualization.

**Scope Statement:** A minimal-file (1–3 Python files, <500 lines total) simple pendulum simulation implementing four numerical integrators (forward Euler, symplectic Euler, RK4, Störmer–Verlet) with energy tracking, phase-space visualization, convergence analysis, and performance benchmarking. No external dependencies beyond NumPy, SciPy, and Matplotlib.

### Physics Model

The simple pendulum is governed by the nonlinear ODE:

    θ'' + (g/L) sin(θ) = 0

where:
- θ is the angular displacement from vertical
- g = 9.81 m/s² is gravitational acceleration
- L is the pendulum length (default 1.0 m)

State vector: **x** = [θ, ω] where ω = dθ/dt.

### Integrators to Implement

| Method           | Order | Symplectic | Cost/step |
|-----------------|-------|------------|-----------|
| Forward Euler    | 1     | No         | 1 eval    |
| Symplectic Euler | 1     | Yes        | 1 eval    |
| RK4              | 4     | No         | 4 evals   |
| Störmer–Verlet   | 2     | Yes        | 1–2 evals |

### Key Outputs

1. **Figures:** θ(t), E(t), phase space, convergence, stability, accuracy, performance
2. **Results:** JSON files with quantitative metrics for each experiment
3. **Analysis:** Markdown summary comparing methods with literature references

### Design Decisions

- Single main file `pendulum.py` with all integrators and experiment functions
- Separate experiment runner functions callable from CLI or imported
- Fixed random seed (42) for reproducibility where applicable
- Publication-quality figures using seaborn + matplotlib with custom rcParams

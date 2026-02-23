# Analysis: Minimal Gravity Simulation

## 1. Repository Structure

| Path | Purpose |
|------|---------|
| `README.md` | Project overview (currently minimal placeholder) |
| `.gitignore` | Git ignore rules (secrets, environment files, task logs) |
| `.gitattributes` | Git LFS and attribute configuration |
| `research_rubric.json` | Research plan with items, phases, and progress tracking |
| `sources.bib` | BibTeX bibliography for all consulted references |
| `results/` | Directory for experimental data output (JSON) |
| `figures/` | Directory for publication-quality plots (PNG, PDF) |
| `TASK_researcher_attempt_1.md` | Task description for the researcher agent |
| `.archivara/` | Orchestration logs (gitignored) |

## 2. Chosen Programming Language

**Python 3.10** is chosen for this project.

**Justification:**
- **NumPy vectorization**: Gravitational force computation on arrays of particles maps naturally to NumPy broadcasting, giving near-C performance for the O(N^2) inner loop without requiring compilation
- **Matplotlib/Seaborn**: Publication-quality figure generation is a core requirement; Python's plotting ecosystem is unmatched
- **Rapid prototyping**: The rubric calls for implementing and comparing multiple integrators (Euler, Verlet, Leapfrog, adaptive); Python allows fast iteration
- **Reproducibility**: `numpy.random.seed(42)` provides deterministic random initialization
- **Ecosystem**: SciPy, Astropy, and other scientific libraries are available if needed for validation
- **No compilation step**: Simplifies the "minimal" goal — single-file simulation with no build system

## 3. Definition of "Minimal" Scope

### Gravitational Physics
- **Newtonian point-mass gravity only** (no relativistic corrections, no tidal forces, no radiation pressure)
- Universal gravitational constant G treated as a parameter (default G=1 in natural units for simplicity; real-unit mode for solar system tests)
- **Gravitational softening** included to prevent singularities during close encounters: F ∝ 1/(r² + ε²)

### Target Particle Counts
- **Primary focus**: 2-body and 3-body systems for validation against analytical solutions
- **Benchmark range**: N = 10 to 1,000 particles for performance scaling measurements
- **Stretch goal**: Barnes-Hut tree approximation for O(N log N) scaling demonstration

### Spatial Dimensions
- **2D simulation** as the baseline (sufficient for orbital mechanics visualization)
- Data structures will use 2D vectors (x, y) for positions, velocities, and accelerations

### Integration Methods (to be implemented and compared)
1. Forward Euler (baseline, 1st order)
2. Velocity Verlet / Störmer-Verlet (2nd order, symplectic)
3. Leapfrog / kick-drift-kick (2nd order, symplectic)
4. Adaptive time-stepping variant

### Output Format
- **Simulation state**: NumPy arrays for positions, velocities, masses
- **Results**: JSON files in `results/` with energy traces, timing data, error metrics
- **Figures**: PNG (300 DPI) and PDF in `figures/` for all plots
- **No animation or real-time rendering** (out of scope for "minimal")

### What Is Explicitly Out of Scope
- GPU acceleration (CUDA/OpenCL)
- Particle mesh methods
- Relativistic corrections
- Collisions and mergers
- 3D rendering or interactive visualization
- Parallel/distributed computation

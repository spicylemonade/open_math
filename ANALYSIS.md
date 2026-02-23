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

## 4. Literature Review

### 4.1 N-body Gravitational Simulation Algorithms

The gravitational N-body problem requires computing the mutual gravitational interactions among N point masses and integrating their equations of motion forward in time. The fundamental challenge is computational cost: the direct pairwise force calculation scales as O(N²), which becomes prohibitive for large N.

**Key survey papers:**

1. **Dehnen & Read (2011)** — "N-body simulations of gravitational dynamics" (arXiv:1105.1082). Comprehensive review covering both collisional (star clusters) and collisionless (galaxies, large-scale structure) regimes. Describes state-of-the-art algorithms including tree codes, FMM, and particle-mesh methods. Identifies that direct N-body codes like NBODY6 are practical up to ~20,000 particles for Hubble-time integrations.

2. **Trenti & Hut (2008)** — "Gravitational N-body Simulations" (arXiv:0806.3950). Overview of N-body methods from few-body to cosmological scales. Emphasizes the importance of choosing appropriate force solvers and integrators for different physical regimes.

3. **Aarseth (2003)** — "Gravitational N-Body Simulations" (Cambridge University Press). The definitive monograph on direct N-body methods, written by the pioneer of the field. Covers regularization techniques for close encounters, Hermite integration, and the NBODY series of codes.

### 4.2 Symplectic Integrators for Orbital Mechanics

Symplectic integrators preserve the geometric structure of Hamiltonian systems — specifically, they conserve phase-space volume (Liouville's theorem). This makes them ideal for long-term orbital integrations where energy conservation over many orbits is critical.

**Key findings:**

4. **Velocity Verlet and Leapfrog are mathematically equivalent** — they are the same second-order symplectic method expressed in different forms (Verlet computes x, v at aligned time steps; Leapfrog staggers them by dt/2). Both are time-reversible and exactly conserve a shadow Hamiltonian close to the true Hamiltonian, resulting in bounded energy oscillations rather than secular drift.

5. **Yoshida (1990)** — "Construction of higher order symplectic integrators" (Physics Letters A). Showed how to compose leapfrog steps with specially chosen sub-step sizes to achieve 4th, 6th, and 8th order symplectic integrators. The 4th-order Yoshida integrator uses 3 leapfrog evaluations per step.

6. **Wisdom & Holman (1991)** — Developed the symplectic mapping method for planetary dynamics, enabling efficient long-term solar system integrations.

### 4.3 Efficient Force Computation Methods

**Barnes-Hut (1986):**
- Divides space into a hierarchical octree (3D) or quadtree (2D)
- Distant groups of particles approximated as single point masses at their center of mass
- Opening angle parameter θ controls accuracy vs. speed tradeoff
- Complexity: O(N log N)
- θ = 0 degenerates to exact direct summation; typical θ ≈ 0.5–0.7

7. **Barnes & Hut (1986)** — "A hierarchical O(N log N) force-calculation algorithm" (Nature, 324, 446-449). The foundational paper introducing the tree-code approximation.

**Fast Multipole Method (Greengard & Rokhlin, 1987):**
- Uses multipole expansions for cell-to-cell interactions
- Achieves O(N) complexity for uniform particle distributions
- More complex to implement but higher accuracy for given computational cost

8. **Greengard & Rokhlin (1987)** — "A fast algorithm for particle simulations" (Journal of Computational Physics). Introduced the FMM, achieving linear scaling for N-body force computation.

### 4.4 Key Papers Summary

| # | Authors | Year | Title | Key Contribution |
|---|---------|------|-------|-----------------|
| 1 | Dehnen & Read | 2011 | N-body simulations of gravitational dynamics | Comprehensive algorithm survey |
| 2 | Trenti & Hut | 2008 | Gravitational N-body Simulations | Astrophysical context overview |
| 3 | Aarseth | 2003 | Gravitational N-Body Simulations (book) | Direct N-body methods bible |
| 4 | Verlet | 1967 | Computer experiments on classical fluids | Velocity Verlet algorithm |
| 5 | Yoshida | 1990 | Construction of higher order symplectic integrators | Higher-order symplectic methods |
| 6 | Barnes & Hut | 1986 | A hierarchical O(N log N) force-calculation algorithm | Tree-code approximation |
| 7 | Greengard & Rokhlin | 1987 | A fast algorithm for particle simulations | Fast Multipole Method |
| 8 | Wisdom & Holman | 1991 | Symplectic maps for the N-body problem | Symplectic mapping for planets |

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

## 5. Survey of Open-Source N-body Simulation Codebases

### Comparison Table

| Code | Language | Integration Method | Force Algorithm | License | Best For |
|------|----------|-------------------|-----------------|---------|----------|
| **REBOUND** | C + Python | WHFast, IAS15, Leapfrog, SEI, MERCURIUS | Direct, Barnes-Hut tree | GPL-3.0 | Planetary dynamics, rings, high-precision orbits |
| **Gadget-2/4** | C | Leapfrog (KDK) | TreePM (tree + particle mesh) | GPL-2.0 | Cosmological N-body/SPH, galaxy formation |
| **NBODY6++GPU** | Fortran/C | 4th-order Hermite | Direct N-body + KS regularization | MIT | Star clusters, close encounters, million-body |
| **GravHopper** | Python + C | Leapfrog | Direct, Barnes-Hut tree | MIT | Educational, quick prototyping, galpy integration |
| **galpy** | Python + C | Orbit integration (RK, symplectic) | Analytic potentials, N-body snapshots | BSD-3 | Galactic dynamics, orbit computation |
| **pynbody** | Python | N/A (analysis only) | N/A | GPL-3.0 | Post-processing Gadget/PKDGRAV outputs |

### Detailed Notes

**REBOUND** (Rein & Liu, 2012): The most relevant comparison point for this project. It is a modular C library with a Python wrapper that provides multiple integrators and force solvers. Its IAS15 integrator achieves machine-precision accuracy with adaptive time-stepping. The leapfrog integrator in REBOUND uses the standard kick-drift-kick form. REBOUND's modularity (separate gravity modules, collision modules, integrator modules) is an excellent design pattern.

**Gadget-2** (Springel, 2005): The standard cosmological simulation code. Uses a TreePM algorithm combining a hierarchical multipole expansion for short-range forces with a particle mesh FFT for long-range forces. Optimized for large N (millions to billions) on distributed-memory clusters. Overkill for our minimal simulation but a good reference for Barnes-Hut tree implementation.

**NBODY6++GPU** (Wang et al., 2015): State-of-the-art direct N-body code for star clusters. Uses 4th-order Hermite integration with block time-steps and Ahmad-Cohen neighbor schemes. GPU acceleration provides ~33x speedup for regular force computation. Handles close encounters via Kustaanheimo-Stiefel regularization — far beyond our minimal scope.

**GravHopper** (Bailin, 2023): Closest in spirit to our project — a simple Python interface with C backend, supporting both direct summation and Barnes-Hut. Uses leapfrog integration and can generate equilibrium initial conditions (Plummer, Hernquist profiles). Good reference for Python/C hybrid design.

## 6. Mathematical Formulation of the Newtonian N-body Problem

### 6.1 Newton's Law of Universal Gravitation

The gravitational force between two point masses m_i and m_j separated by displacement vector **r**_ij = **r**_j - **r**_i is:

**F**_ij = G * m_i * m_j * **r**_ij / |**r**_ij|³

where G is Newton's gravitational constant (G ≈ 6.674 × 10⁻¹¹ m³ kg⁻¹ s⁻² in SI units).

### 6.2 Equations of Motion for N Point Masses

For a system of N point masses {m_1, m_2, ..., m_N} at positions {**r**_1, **r**_2, ..., **r**_N}, the acceleration of the i-th body is:

**a**_i = d²**r**_i/dt² = G * Σ_{j≠i} m_j * (**r**_j - **r**_i) / |**r**_j - **r**_i|³

This gives 2N second-order ODEs (or equivalently 4N first-order ODEs in 2D) that must be integrated simultaneously.

### 6.3 Gravitational Potential Energy

The total gravitational potential energy of the system is:

U = -G * Σ_{i<j} m_i * m_j / |**r**_i - **r**_j|

The sum runs over all unique pairs (i, j) with i < j to avoid double counting.

### 6.4 Kinetic Energy

The total kinetic energy is:

T = Σ_i (1/2) * m_i * |**v**_i|²

where **v**_i = d**r**_i/dt is the velocity of the i-th body.

### 6.5 Total Energy Conservation

The total mechanical energy E = T + U is a conserved quantity (constant of motion) for the exact solution of the Newtonian N-body problem. This follows from the conservative nature of the gravitational force (it can be derived from a potential).

In numerical simulation, the relative energy error |ΔE/E₀| = |E(t) - E(0)| / |E(0)| serves as the primary diagnostic for integration accuracy. For symplectic integrators, this error remains bounded; for non-symplectic integrators (e.g., Forward Euler), it exhibits secular growth.

### 6.6 Gravitational Softening

When two bodies approach closely, |**r**_ij| → 0, the force diverges as 1/|**r**_ij|². This singularity causes numerical problems (extremely large accelerations, tiny required time steps). The standard remedy is **gravitational softening** — replacing the distance with a softened distance:

|**r**_ij|² → |**r**_ij|² + ε²

where ε > 0 is the softening length. The softened acceleration becomes:

**a**_i = G * Σ_{j≠i} m_j * (**r**_j - **r**_i) / (|**r**_j - **r**_i|² + ε²)^(3/2)

**Properties of softening:**
- ε = 0 recovers exact Newtonian gravity
- For |**r**_ij| >> ε, the force is essentially Newtonian
- For |**r**_ij| << ε, the force is approximately linear (harmonic), preventing divergence
- The softened potential is: Φ_soft = -G * m_j / √(|**r**_ij|² + ε²)
- Softening introduces a systematic bias in the potential energy; the energy is no longer exactly conserved even analytically, but the softened system has its own conserved energy
- Choosing ε involves a tradeoff: too large suppresses real dynamics; too small allows near-singular behavior (Dehnen & Read 2011)

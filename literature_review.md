# Literature Review: N-Body Gravitational Simulation Methods

## 1. Direct-Summation Methods

The direct-summation (or brute-force) approach computes gravitational forces by evaluating all pairwise interactions between N particles, yielding O(N²) complexity per time step. This is the most accurate method but scales poorly for large N.

The dynamics requires that at every time step, gravitational forces are recomputed for every pair of objects. The largest direct-summation simulations are limited to N ≲ 10⁶; for example, a globular cluster simulation of ~500,000 particles by Heggie (2014) took nearly 3 years of computation (Aarseth, 2003).

Aarseth's NBODY6 is the state-of-the-art serial direct N-body integrator, using a fourth-order Hermite scheme with individual (adaptive) time steps and regularization of close encounters (Aarseth, 2003). Special-purpose hardware such as GRAPE boards has been developed to accelerate pairwise force computations, achieving teraflop performance (Makino & Taiji, 1998).

For our minimal simulator, direct summation is the natural baseline: simple to implement, exact (to numerical precision), and sufficient for N ≲ 1000 particles.

## 2. Symplectic Integrators (Leapfrog, Verlet)

Symplectic integrators preserve the symplectic structure of Hamiltonian systems, meaning they conserve phase-space volume and exhibit bounded energy errors over long integrations — in contrast to non-symplectic methods (like Forward Euler or RK4) which suffer secular energy drift.

### Störmer-Verlet / Leapfrog

The Störmer-Verlet method was first used by Delambre in 1791 and rediscovered by Størmer (1907), Verlet (1967), and others. It is a second-order, symplectic, time-reversible integrator. The "leapfrog" formulation staggers position and velocity updates by half a time step. Jacobs (2019) showed that the leapfrog and velocity Verlet methods are algebraically equivalent despite their different formulations.

The kick-drift-kick (KDK) variant:
1. **Kick**: v(t + dt/2) = v(t) + a(t) · dt/2
2. **Drift**: x(t + dt) = x(t) + v(t + dt/2) · dt
3. **Kick**: v(t + dt) = v(t + dt/2) + a(t + dt) · dt/2

This formulation requires only one force evaluation per step and is widely used in astrophysical simulations (Springel, 2005; Rein & Liu, 2012).

### Velocity Verlet

The velocity Verlet variant computes positions and velocities at the same time points:
1. x(t + dt) = x(t) + v(t)·dt + ½a(t)·dt²
2. Compute a(t + dt) from new positions
3. v(t + dt) = v(t) + ½[a(t) + a(t + dt)]·dt

This is mathematically equivalent to leapfrog/KDK and produces identical trajectories (Hairer, Lubich & Wanner, 2003).

### Wisdom-Holman Mapping

For planetary dynamics, Wisdom & Holman (1991) developed a symplectic mapping that splits the Hamiltonian into Keplerian and perturbation parts, allowing large time steps when perturbations are small. This has been implemented in REBOUND with higher-order extensions achieving up to six orders of magnitude better accuracy (Rein, Tamayo & Brown, 2019).

### Higher-Order Methods

Yoshida (1990) showed how to compose second-order symplectic integrators into higher-order ones by choosing specific sub-step sizes. Fourth-order Yoshida integrators require four force evaluations per step but achieve much higher accuracy for smooth problems. Chin (2005) developed forward symplectic integrators with only positive time steps, requiring force gradients but achieving accuracy comparable to RK4 at 5–10× larger step sizes.

## 3. Tree-Based Methods (Barnes-Hut)

Barnes & Hut (1986) introduced a hierarchical tree algorithm that reduces force computation from O(N²) to O(N log N). The key idea: group distant particles and approximate their collective gravitational effect using the center of mass of the group.

**Algorithm:**
1. Build a quadtree (2D) or octree (3D) by recursively subdividing space until each leaf contains at most one particle
2. Store total mass and center of mass at each internal node
3. For each particle, traverse the tree; if a node subtends an angle s/d < θ (the opening angle), treat it as a single pseudo-particle

With θ = 0.5, the method achieves ~1% force accuracy while reducing computation by 50% for N < 500 and 80–90% for N > 1000 (Barnes & Hut, 1986). The method can be parallelized on GPUs, achieving >50× speedup over serial CPU code for large N (Bédorf, Gaburov & Portegies Zwart, 2012).

More sophisticated tree codes use multipole expansions beyond monopole (Dehnen, 2002) and the Fast Multipole Method (FMM) achieves O(N) scaling (Greengard & Rokhlin, 1987).

## 4. Softening Techniques

Gravitational softening modifies the force law at small separations to avoid the 1/r singularity:

**Plummer softening** (Aarseth, 1963; Plummer, 1911):
F = -G·m₁·m₂·r / (r² + ε²)^(3/2)

This replaces point masses with Plummer spheres of scale radius ε. The softening length ε controls the trade-off between noise reduction (large ε) and force accuracy (small ε).

**Optimal softening**: Dehnen (2001) and Athanassoula et al. (2000) showed that optimal ε depends on both the mass distribution and particle number N, with higher N requiring smaller ε. Barnes (2012) reinterpreted softening as a smoothing operation, making the connection to kernel density estimation explicit.

**Alternatives**: Spline softening (Hernquist & Katz, 1989) and higher-power softening kernels provide better force representation than standard Plummer softening by partially compensating for the reduced forces at r < ε with enhanced forces at r ≈ ε (Dyer & Ip, 1993).

For our simulator, Plummer softening is the simplest and most widely used approach, with a configurable ε parameter.

## 5. Adaptive Time-Stepping

Fixed time-step integrators waste computation during slow orbital phases and may miss dynamics during close encounters. Adaptive schemes address this by varying dt based on local conditions.

### Aarseth's Individual Timesteps

Aarseth (1985, 2003) pioneered individual (per-particle) adaptive time steps using ratios of force derivatives. Combined with a fourth-order Hermite integrator, this allows each particle to evolve on its own dynamical timescale. Block time-stepping (Hayli, 1967; McMillan, 1986) quantizes time steps to powers of two for synchronization efficiency.

### Acceleration-Based Criteria

A common simple criterion:
dt = η · √(ε / |a|)

where η is a dimensionless accuracy parameter, ε is the softening length, and |a| is the acceleration magnitude. This reduces dt during close encounters when accelerations are large.

### Newer Approaches

- **Zemp et al. (2007)** proposed a dynamical-time criterion that adapts based on the true local dynamical time, eliminating dependence on artificial parameters like softening length
- **Hopkins (2020)** used the tidal tensor to estimate local dynamical timescales, providing a general-purpose criterion that respects the equivalence principle
- **Rein et al. (2024)** developed a derivative-based criterion using acceleration, jerk, and snap that is guaranteed to resolve orbital periods and pericenter passages for any two-body orbit

### Caveat

Adaptive time-stepping generally breaks symplecticity (Hairer, Lubich & Wanner, 2003). The integrated Hamiltonian changes when the step size changes, so adaptive symplectic integrators are no longer truly symplectic. However, for problems with large dynamical range (e.g., highly eccentric orbits), the gains in efficiency typically outweigh the loss of exact symplecticity.

## Summary of Method Selection

For our minimal gravity simulator, we select:
1. **Forward Euler** — as a baseline to demonstrate energy drift
2. **Leapfrog (KDK)** — the standard symplectic workhorse
3. **Velocity Verlet** — to demonstrate equivalence with leapfrog
4. **Barnes-Hut quadtree** — for O(N log N) scaling demonstration
5. **Plummer softening** — simplest and most common approach
6. **Acceleration-based adaptive dt** — simple and effective for eccentric orbits

## 6. Survey of Open-Source N-Body Codebases

| Code | Language | Integrators | Force Algorithm | License | Key Reference |
|------|----------|-------------|-----------------|---------|---------------|
| **REBOUND** | C core + Python API | IAS15 (15th-order adaptive), WHFast (Wisdom-Holman), Leapfrog, Mercurius (hybrid), SABA family | Direct summation, tree code | GPL v3 | Rein & Liu (2012) |
| **GADGET-2** | C (MPI parallel) | Leapfrog (KDK) with individual time steps | TreePM (tree + particle-mesh hybrid) | GPL v2 | Springel (2005) |
| **NBODY6** | Fortran | 4th-order Hermite with block time steps, KS regularization for binaries | Direct summation with neighbor scheme | Public domain | Aarseth (1999, 2003) |
| **GravHopper** | Python + C backend | Leapfrog | Barnes-Hut tree or direct summation | MIT | Bailin (2023) |
| **galpy** | Python + C extensions | Various orbit integrators (symplectic, DOP853, etc.) | Analytic potentials (not particle-based) | BSD 3-Clause | Bovy (2015) |
| **grav_sim** | C + Python API | Euler, RK4, Leapfrog, Yoshida, IAS15-like | Direct summation | MIT | Ng (2024) |

### REBOUND
The most feature-rich Python-accessible N-body code. Ships with >10 integrators including the 15th-order IAS15 (machine-precision accuracy with adaptive steps) and WHFast (fast Wisdom-Holman mapping). Supports collision detection, additional forces, and has extensive documentation. Our implementation draws design inspiration from REBOUND's modular integrator architecture.

### GADGET-2
The standard code for cosmological simulations. Uses a TreePM algorithm combining Barnes-Hut tree for short-range forces with a particle-mesh FFT for long-range forces. Massively parallel via MPI. Successor GADGET-4 is available but less widely used. Our Barnes-Hut implementation follows the same octree/quadtree approach used in GADGET's tree module.

### NBODY6
The gold standard for collisional stellar dynamics (star clusters). Uses direct summation with Ahmad-Cohen neighbor scheme, 4th-order Hermite integration, KS regularization for close binaries, and chain regularization for few-body subsystems. GPU-accelerated version (NBODY6++GPU) scales to million-body simulations.

### GravHopper
A pedagogical Python+C code that bridges galpy and pynbody ecosystems. Supports both direct summation and Barnes-Hut tree. Includes initial condition generators for Plummer, Hernquist, and exponential disk profiles. Its simplicity makes it a useful reference for our implementation.

### galpy
Focused on galactic dynamics in analytic potentials rather than particle-particle interactions. Provides orbit integration, distribution function sampling, and action-angle coordinate computation. Relevant as a comparison point for orbit integration accuracy.

## References

1. Aarseth, S.J. (2003). *Gravitational N-Body Simulations*. Cambridge University Press.
2. Verlet, L. (1967). "Computer experiments on classical fluids. I." *Physical Review*, 159, 98–103.
3. Barnes, J. & Hut, P. (1986). "A hierarchical O(N log N) force-calculation algorithm." *Nature*, 324, 446–449.
4. Wisdom, J. & Holman, M. (1991). "Symplectic maps for the N-body problem." *Astronomical Journal*, 102, 1528–1538.
5. Springel, V. (2005). "The cosmological simulation code GADGET-2." *MNRAS*, 364, 1105–1134.
6. Rein, H. & Liu, S.-F. (2012). "REBOUND: an open-source multi-purpose N-body code." *Astronomy & Astrophysics*, 537, A128.
7. Yoshida, H. (1990). "Construction of higher order symplectic integrators." *Physics Letters A*, 150, 262–268.
8. Hairer, E., Lubich, C. & Wanner, G. (2003). "Geometric numerical integration illustrated by the Störmer-Verlet method." *Acta Numerica*, 12, 399–450.
9. Dehnen, W. (2001). "Towards optimal softening in 3D N-body codes." *MNRAS*, 324, 273–291.
10. Barnes, J.E. (2012). "Gravitational softening as a smoothing operation." *MNRAS*, 425, 1104–1120.
11. Chin, S.A. (2005). "Forward symplectic integrators for solving gravitational few-body problems." *Celestial Mechanics and Dynamical Astronomy*, 91, 301–322.
12. Rein, H., Tamayo, D. & Brown, G. (2019). "High-order symplectic integrators for planetary dynamics and their implementation in REBOUND." *MNRAS*, 489, 4632–4640.
13. Greengard, L. & Rokhlin, V. (1987). "A fast algorithm for particle simulations." *Journal of Computational Physics*, 73, 325–348.
14. Hernandez, D.M. & Bertschinger, E. (2015). "Symplectic integration for the collisional gravitational N-body problem." *MNRAS*, 452, 1934–1944.
15. Plummer, H.C. (1911). "On the problem of distribution in globular star clusters." *MNRAS*, 71, 460–470.

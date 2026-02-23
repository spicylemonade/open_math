# Findings: Minimal N-Body Gravitational Simulator

## 1. Introduction and Problem Statement

The gravitational N-body problem — computing the trajectories of N massive particles under mutual gravitational attraction — is one of the oldest and most fundamental problems in computational physics. First formulated by Newton over 350 years ago, it remains a central challenge in astrophysics, celestial mechanics, and computational science.

This project implements a minimal but complete N-body gravitational simulator in Python, designed to explore and compare numerical methods for gravitational dynamics. The goal is not to compete with production codes like REBOUND (Rein & Liu, 2012) or GADGET-2 (Springel, 2005), but to provide a clear, well-tested implementation that demonstrates the key concepts: force computation algorithms, time integration methods, conservation properties, and scaling behavior.

Specifically, we address the following questions:

1. **How do different time integrators compare for gravitational dynamics?** We implement and benchmark Forward Euler (1st order, non-symplectic), Leapfrog/Störmer-Verlet (2nd order, symplectic), and Velocity Verlet (2nd order, symplectic) to quantify the importance of symplecticity for long-term orbital evolution.

2. **How does the Barnes-Hut tree algorithm compare to direct summation?** We implement both O(N²) direct summation and O(N log N) Barnes-Hut approximation to characterize the accuracy-performance trade-off.

3. **How do softening and adaptive time-stepping improve robustness?** We investigate Plummer softening for close encounters and acceleration-based adaptive time-stepping for eccentric orbits.

4. **Can our simulator reproduce canonical gravitational scenarios?** We validate against circular orbits, elliptical orbits, and the Chenciner-Montgomery figure-8 three-body choreography.

## 2. Methods

### 2.1 Force Computation

#### Direct Summation

The gravitational acceleration on particle *i* is computed by summing pairwise interactions with all other particles (Aarseth, 2003):

**a**_i = -G Σ_{j≠i} m_j (**r**_i - **r**_j) / |**r**_i - **r**_j|³

This has O(N²) complexity and serves as the exact reference. Our implementation uses a simple double loop over particles with NumPy vector arithmetic for each pair. While not the most optimized approach (a fully vectorized implementation using broadcasting would be faster), it is clear and correct, providing the foundation for all experiments.

#### Barnes-Hut Tree Algorithm

Following Barnes & Hut (1986), we implement a hierarchical tree algorithm that reduces force computation to O(N log N). The algorithm:

1. Builds a quadtree (2D) or octree (3D) by recursively subdividing space
2. Stores total mass and center of mass at each node
3. Uses the multipole acceptance criterion (MAC): if a node subtends an angle s/d < θ (the opening angle), approximate all particles in that subtree as a single pseudo-particle at the center of mass

With θ = 0.5, the standard choice in practice, we achieve median force errors of 0.75% compared to direct summation, with the 90th percentile error below 3%. This is consistent with the original Barnes & Hut (1986) analysis showing ~1% typical force errors for θ = 0.5.

### 2.2 Time Integrators

#### Forward Euler (1st Order)

The simplest explicit method:

**r**(t + dt) = **r**(t) + **v**(t) · dt
**v**(t + dt) = **v**(t) + **a**(t) · dt

Forward Euler is not symplectic and not time-reversible, leading to secular energy drift — the total energy of the system monotonically increases (or decreases, depending on sign convention) over time. We include it solely as a negative baseline.

#### Leapfrog / Störmer-Verlet (KDK, 2nd Order)

The kick-drift-kick formulation of the leapfrog method (Verlet, 1967; Hairer et al., 2003):

1. **Kick**: **v**(t + dt/2) = **v**(t) + **a**(t) · dt/2
2. **Drift**: **r**(t + dt) = **r**(t) + **v**(t + dt/2) · dt
3. **Kick**: **v**(t + dt) = **v**(t + dt/2) + **a**(t + dt) · dt/2

This is a symplectic integrator, meaning it preserves the symplectic 2-form of the Hamiltonian phase space (Yoshida, 1990). Consequently, it conserves a modified Hamiltonian H̃ = H + O(dt²), leading to bounded, oscillating energy errors with no secular drift. It requires only one force evaluation per step (the kicks at the end of one step and the beginning of the next can be combined).

#### Velocity Verlet (2nd Order)

An equivalent formulation that keeps positions and velocities synchronized:

1. **r**(t + dt) = **r**(t) + **v**(t) · dt + ½**a**(t) · dt²
2. Compute **a**(t + dt)
3. **v**(t + dt) = **v**(t) + ½[**a**(t) + **a**(t + dt)] · dt

As proven by Jacobs (2019) and discussed in Hairer et al. (2003), Velocity Verlet and Leapfrog KDK produce identical trajectories to machine precision. We verify this equivalence numerically.

### 2.3 Gravitational Softening

To prevent numerical singularities during close encounters, we use Plummer softening (Plummer, 1911; Aarseth, 2003):

**a**_i = -G Σ_{j≠i} m_j (**r**_i - **r**_j) / (|**r**_i - **r**_j|² + ε²)^{3/2}

The softening parameter ε replaces point masses with extended Plummer spheres of scale radius ε. This trades force accuracy at small separations (r < ε) for numerical stability. Following Dehnen (2001) and Barnes (2012), we interpret softening as a smoothing operation on the mass distribution.

### 2.4 Adaptive Time-Stepping

For eccentric orbits where the orbital velocity varies dramatically between pericenter and apocenter, fixed time-stepping is inefficient. We implement an acceleration-based adaptive scheme:

dt = η · √(r_min / a_max)

where η is a dimensionless accuracy parameter, r_min is the minimum inter-particle distance, and a_max is the maximum acceleration magnitude. This reduces dt during close approaches (large accelerations) and increases dt during slow orbital phases. The approach is inspired by Aarseth's (2003) individual time-step methodology, simplified to a shared time step.

**Caveat**: Adaptive time-stepping breaks strict symplecticity because the integrated Hamiltonian changes when dt changes (Hairer et al., 2003). However, the gains in efficiency typically outweigh this drawback for problems with large dynamical range.

## 3. Results

### 3.1 Energy Conservation Benchmark

We ran all three integrators on a circular two-body Kepler orbit for 10,000 steps with dt = 0.01 (approximately 16 orbital periods). Key results (see `figures/energy_error_comparison.png`):

| Integrator | Max |dE/E| | Behavior |
|---|---|---|
| Forward Euler | 4.78 × 10⁻¹ | Secular drift (energy grows monotonically) |
| Leapfrog KDK | 2.50 × 10⁻⁹ | Bounded oscillation (no secular drift) |
| Velocity Verlet | 2.50 × 10⁻⁹ | Bounded oscillation (identical to Leapfrog) |

The symplectic integrators outperform Forward Euler by **8 orders of magnitude** in energy conservation. This dramatic difference illustrates the fundamental importance of symplecticity for Hamiltonian systems — the symplectic methods preserve a modified Hamiltonian that oscillates around the true value, while non-symplectic methods allow energy to drift without bound.

These results are consistent with the theoretical analysis of Hairer et al. (2003), who show that Störmer-Verlet preserves a modified Hamiltonian H̃ = H + O(dt²). With dt = 0.01, we expect energy oscillations of order dt² ≈ 10⁻⁴ in the modified Hamiltonian; the much smaller actual error (10⁻⁹) reflects the favorable geometry of the circular orbit.

### 3.2 Performance Scaling

We measured wall-clock time for a single force evaluation at N = 64, 128, 256, 512, and 1024 particles (see `figures/scaling_benchmark.png`). Power-law fitting:

| Method | Scaling Exponent | Expected |
|---|---|---|
| Direct Summation | N^2.00 | N^2 |
| Barnes-Hut (θ = 0.5) | N^1.36 | N log N ≈ N^1.1-1.3 |

Direct summation scales exactly as O(N²), confirming the pairwise nature of the force computation. Barnes-Hut achieves sub-quadratic scaling with exponent 1.36, close to the theoretical O(N log N). At N = 1024, Barnes-Hut is 7.1× faster than direct summation.

The fitted exponent of 1.36 for Barnes-Hut is slightly above the theoretical O(N log N) due to Python overhead in the recursive tree traversal. A C implementation would likely achieve an exponent closer to 1.1-1.2, as reported in the original Barnes & Hut (1986) paper and in the GADGET-2 code (Springel, 2005).

### 3.3 Canonical Gravitational Scenarios

All three canonical scenarios pass their acceptance criteria (see `results/canonical_tests.json`):

**Circular orbit (100 orbits)**: The orbital radius is maintained to within 0.0001% over 100 complete orbits, with maximum energy error 2.50 × 10⁻⁹. This demonstrates that the Leapfrog integrator is capable of extremely long-term stable integration for well-resolved circular orbits.

**Elliptical orbit (e = 0.5, 50 orbits)**: The eccentricity is preserved to within 0.0002% over 50 orbits, with maximum energy error 6.79 × 10⁻⁵. The larger energy error compared to the circular case reflects the need to resolve the faster pericenter passage with a fixed time step.

**Figure-8 three-body choreography (5 periods)**: The Chenciner-Montgomery (2000) solution remains stable for 5 full periods with position drift of only 7.4 × 10⁻⁴ and energy error 5.89 × 10⁻⁷. This is a stringent test because the three-body problem is chaotic — any integration error could cause the choreographic solution to diverge. The stability of our integration confirms the accuracy of the Leapfrog method for this problem at dt = 0.001.

### 3.4 Softening Analysis

We tested Plummer softening on a 3-body near-collision scenario with four values of ε (see `results/softening_analysis.json`):

| ε | Max |dE/E| |
|---|---|
| 0 (none) | 587 |
| 0.01 | 85 |
| 0.05 | 0.10 |
| 0.1 | 0.006 |

Without softening, the close encounter causes energy errors of 587× the initial energy — effectively numerical explosion. Softening dramatically improves stability: ε = 0.1 keeps energy errors below 0.6%. The trade-off is that softening reduces force accuracy at separations r < ε, effectively smoothing out the physics of close encounters (Barnes, 2012).

### 3.5 Adaptive Time-Stepping

On a highly eccentric (e = 0.9) elliptical orbit over 10 orbital periods:

| Method | Steps | Final |dE/E| |
|---|---|---|
| Fixed dt = 0.01 | 6,283 | 2.59 × 10⁻¹ |
| Adaptive (η = 0.02) | 2,975 | 3.67 × 10⁻³ |

Adaptive time-stepping uses **53% fewer steps** while achieving **70× better energy conservation**. It automatically reduces dt during pericenter passages (where accelerations are large) and increases dt during the slow apocenter phase. The minimum dt used was 1.88 × 10⁻⁴ (during pericenter), while the maximum was 7.42 × 10⁻² (during apocenter), spanning a factor of ~400 in step size.

## 4. Discussion

### Comparison with Prior Work

Our results are quantitatively consistent with published literature:

1. **Energy conservation**: The Leapfrog energy error of ~10⁻⁹ for a circular orbit at dt = 0.01 matches the performance of REBOUND's Leapfrog integrator (Rein & Liu, 2012) and is consistent with the theoretical O(dt²) bound from Hairer et al. (2003).

2. **Barnes-Hut accuracy**: Our median force error of 0.75% for θ = 0.5 is consistent with the ~1% accuracy reported by Barnes & Hut (1986) and used in production codes like GADGET-2 (Springel, 2005).

3. **Figure-8 stability**: The Chenciner-Montgomery (2000) three-body choreography is known to be linearly stable. Our successful 5-period integration confirms that the Leapfrog method with dt = 0.001 adequately resolves the dynamics of this choreographic solution.

### Limitations

1. **Python performance**: Our pure-Python implementation is orders of magnitude slower than C/Fortran codes like REBOUND, GADGET, or NBODY6. The O(N²) force loop in Python becomes prohibitive for N > 1000. The Barnes-Hut tree implementation is particularly affected by Python's overhead for recursive function calls.

2. **Monopole approximation**: Our Barnes-Hut implementation uses only the monopole (center-of-mass) approximation. Production codes use quadrupole or higher-order multipole expansions for better accuracy at the same opening angle (Dehnen, 2002; Springel, 2005).

3. **Fixed shared time steps**: Our adaptive scheme uses a shared (global) time step, whereas production codes like NBODY6 (Aarseth, 2003) use individual per-particle time steps with block-step synchronization. Individual time steps are essential for large dynamical range in particle-rich systems (e.g., star clusters).

4. **No regularization**: We do not implement KS regularization (Kustaanheimo-Stiefel) or chain regularization for close binary interactions, which are critical for accurate evolution of bound pairs in dense stellar systems.

### Future Directions

- **Vectorization**: Replace Python loops with NumPy vectorized operations for O(N²) forces, or use Numba JIT compilation
- **Higher-order integrators**: Implement Yoshida (1990) 4th-order composites or the IAS15 adaptive integrator from REBOUND
- **Multipole expansion**: Extend Barnes-Hut to include quadrupole terms for better accuracy
- **GPU acceleration**: The direct-summation force loop is embarrassingly parallel and well-suited for GPU computation
- **3D visualization**: Add real-time visualization using OpenGL or a web-based renderer

## 5. Conclusions

We have implemented and validated a minimal N-body gravitational simulator that demonstrates the core concepts of computational gravitational dynamics:

1. **Symplectic integrators are essential** for gravitational dynamics. The Leapfrog method provides 8 orders of magnitude better energy conservation than Forward Euler at negligible additional cost. This is not merely a numerical convenience — it reflects the fundamental structure of Hamiltonian mechanics.

2. **The Barnes-Hut tree algorithm** successfully reduces force computation from O(N²) to O(N^1.36) with median force errors below 1% at the standard opening angle θ = 0.5. This enables efficient simulation of larger particle systems.

3. **Plummer softening** is effective at preventing numerical singularities during close encounters, with ε = 0.1 reducing energy errors by 5 orders of magnitude compared to unsoftened interactions.

4. **Adaptive time-stepping** provides substantial efficiency gains for eccentric orbits (53% fewer steps with 70× better energy conservation), making it indispensable for problems with large dynamical range.

5. **Canonical test cases** — circular orbit, elliptical orbit, and figure-8 three-body choreography — all pass quantitative validation criteria, with results consistent with published literature values from Hairer et al. (2003), Rein & Liu (2012), and Chenciner & Montgomery (2000).

The complete codebase, with all source files, unit tests, benchmark scripts, and publication-quality figures, is available in this repository. All experiments are reproducible using fixed random seed 42.

## References

All references are available in `sources.bib`. Key citations:

- Aarseth, S.J. (2003). *Gravitational N-Body Simulations*. Cambridge University Press.
- Barnes, J. & Hut, P. (1986). Nature, 324, 446–449.
- Barnes, J.E. (2012). MNRAS, 425, 1104–1120.
- Chenciner, A. & Montgomery, R. (2000). Annals of Mathematics, 152, 881–901.
- Dehnen, W. (2001). MNRAS, 324, 273–291.
- Hairer, E., Lubich, C. & Wanner, G. (2003). Acta Numerica, 12, 399–450.
- Plummer, H.C. (1911). MNRAS, 71, 460–470.
- Rein, H. & Liu, S.-F. (2012). A&A, 537, A128.
- Rein, H., Tamayo, D. & Brown, G. (2019). MNRAS, 489, 4632–4640.
- Springel, V. (2005). MNRAS, 364, 1105–1134.
- Verlet, L. (1967). Physical Review, 159, 98–103.
- Wisdom, J. & Holman, M. (1991). AJ, 102, 1528–1538.
- Yoshida, H. (1990). Physics Letters A, 150, 262–268.

# Literature Review: N-Body Gravitational Simulation Methods

## 1. The N-Body Problem

The gravitational N-body problem involves integrating the equations of motion for N particles interacting through Newtonian gravity. It is among the oldest and most fundamental problems in computational physics, dating back to Newton's *Principia* (1687) and continuing to drive advances in numerical methods and high-performance computing (Aarseth, 2003; Dehnen & Read, 2011).

**Key finding:** The problem is simple in principle — merely integrating 6N ordinary differential equations — but the O(N²) pairwise force computation and the need for long-term accuracy make it computationally and numerically challenging.

## 2. Direct Summation Methods

The most straightforward approach computes gravitational forces by direct pairwise summation over all N(N-1)/2 particle pairs. This O(N²) method is exact (to machine precision) but computationally expensive for large N.

**Key finding:** Direct summation remains the gold standard for collisional systems (e.g., star clusters) where close encounters matter. Aarseth's NBODY6 code is the state-of-the-art serial direct N-body integrator, employing adaptive time-stepping, Ahmad-Cohen neighbour schemes, and KS regularization for close encounters (Aarseth, 2003). Practical limits are approximately N ≈ 20,000 particles for Hubble-time integrations on serial hardware.

## 3. Hierarchical Tree Methods (Barnes-Hut)

Barnes & Hut (1986) introduced a revolutionary O(N log N) algorithm that groups distant particles using a hierarchical tree (octree in 3D, quadtree in 2D). Distant groups are approximated as single bodies using their center of mass.

**Key finding:** The opening angle parameter θ controls the accuracy-speed tradeoff. At θ = 0.5 (commonly used), force errors are typically < 1% relative to direct summation. The crossover point where Barnes-Hut becomes faster than direct summation is around N ≈ 50–100. For N > 1000, Barnes-Hut provides 80–90% speedup over direct summation.

## 4. Symplectic Integrators

Symplectic integrators preserve the geometric (symplectic) structure of Hamiltonian phase space, leading to bounded energy errors over long integrations rather than secular drift.

### 4.1 Leapfrog / Störmer-Verlet

The leapfrog method (also known as Störmer-Verlet or velocity Verlet) is a second-order symplectic integrator that has been the workhorse of N-body simulations since Størmer (1907) and Verlet (1967). It exists in two equivalent forms:

- **Kick-Drift-Kick (KDK):** Half-kick velocities, full-drift positions, half-kick velocities
- **Drift-Kick-Drift (DKD):** Half-drift positions, full-kick velocities, half-drift positions

**Key finding:** Leapfrog/Verlet is time-reversible, symplectic, and second-order accurate, requiring only one force evaluation per step (same as forward Euler). The energy error oscillates around the true value rather than drifting secularly. For a circular Kepler orbit, energy errors remain bounded at O(dt²) indefinitely (Wisdom & Holman, 1991; Hernandez & Bertschinger, 2015).

### 4.2 Velocity Verlet

Velocity Verlet is algebraically identical to the KDK leapfrog but provides synchronized positions and velocities at each full timestep, which is convenient for diagnostics. The position and velocity updates are:

1. v(t + dt/2) = v(t) + a(t) · dt/2
2. x(t + dt) = x(t) + v(t + dt/2) · dt
3. Compute a(t + dt)
4. v(t + dt) = v(t + dt/2) + a(t + dt) · dt/2

**Key finding:** Velocity Verlet and KDK leapfrog produce identical trajectories to machine precision when given identical initial conditions.

### 4.3 Higher-Order Symplectic Methods (Yoshida)

Yoshida (1990) showed how to construct higher-order symplectic integrators by composing leapfrog steps with specific coefficients. The 4th-order Yoshida integrator uses three leapfrog sub-steps with carefully chosen time increments.

**Key finding:** Higher-order methods reduce truncation error per step but at the cost of additional force evaluations. For smooth problems, the 4th-order Yoshida method provides ~4th-order convergence while remaining symplectic. However, the negative sub-step coefficients can cause stability issues for stiff problems.

## 5. Non-Symplectic Integrators

### 5.1 Forward Euler

The simplest integrator: x(t+dt) = x(t) + v(t)·dt, v(t+dt) = v(t) + a(t)·dt. First-order accurate, neither symplectic nor time-reversible.

**Key finding:** Forward Euler systematically *adds* energy to orbital systems, causing orbits to spiral outward. Energy drift is linear in time and proportional to dt. For a Kepler orbit, energy errors typically exceed 10% within 10 orbital periods at dt = 0.001 (normalized units). It serves as a useful baseline to demonstrate why symplectic integrators are necessary.

### 5.2 Runge-Kutta 4th Order (RK4)

A classic 4th-order explicit method requiring 4 force evaluations per step.

**Key finding:** RK4 has excellent local accuracy (O(dt⁵) local error) but is not symplectic, leading to secular energy drift over long integrations. For short simulations, RK4 outperforms leapfrog in accuracy per step. For long-term orbit integrations (> 100 periods), symplectic methods are preferred because they maintain bounded energy errors. RK4 is also more expensive (4 force evaluations per step vs. 1 for leapfrog).

## 6. Gravitational Softening

Softening modifies the gravitational potential to remove the 1/r singularity at r = 0. The most common form is Plummer softening:

Φ = -Gm / sqrt(r² + ε²)

**Key finding:** The softening parameter ε represents a trade-off between bias (oversmoothing at small separations) and noise (force spikes from close encounters). Optimal ε depends on N and the mass distribution (Dehnen, 2001; Athanassoula et al., 2000). For collisionless simulations, ε should be chosen to minimize the total mean-square force error. Plummer softening was introduced by Aarseth (1963) and remains the most common choice due to its simplicity and the fact that it corresponds to treating particles as Plummer density profiles.

## 7. Adaptive Time-Stepping

Fixed time-stepping is wasteful because the required resolution varies dramatically — close encounters need tiny dt while distant interactions evolve slowly.

**Key finding:** Common criteria for adaptive stepping include:
- **Acceleration-based:** dt ∝ (ε/|a|)^(1/2) where ε is a tolerance
- **Jerk-based:** dt ∝ |a|/|ȧ| (ratio of acceleration to its time derivative)
- **Tidal tensor-based:** Uses eigenvalues of the gravitational tidal tensor for a general-purpose criterion

A fundamental challenge: adaptive time-stepping generally *breaks* symplecticity. Time-reversible integrators offer a practical alternative that preserves many of the benefits of symplectic methods while allowing variable step sizes (Huang & Leimkuhler, 1997).

## 8. Conservation Laws as Diagnostics

For an isolated gravitational system, the following quantities are exactly conserved:
- Total energy E = T + V (kinetic + potential)
- Total linear momentum P = Σ mᵢvᵢ
- Total angular momentum L = Σ mᵢ(rᵢ × vᵢ)

**Key finding:** Monitoring these conservation laws is the primary diagnostic for assessing numerical accuracy. Symplectic integrators show bounded oscillations in |ΔE/E₀|, while non-symplectic methods show secular growth. Angular momentum conservation provides an independent check that is particularly sensitive to force symmetry violations.

## 9. Canonical Test Problems

### 9.1 Kepler Problem (Two-Body)

The two-body problem has an exact analytical solution (conic sections). It is the standard benchmark for integrator validation.

**Key finding:** Circular orbits (e = 0) test energy conservation stability. Eccentric orbits (e > 0) test the integrator's ability to handle varying timescales within a single orbit. At e = 0.9, the pericenter velocity is ~19× the apocenter velocity, severely stressing fixed-timestep integrators.

### 9.2 Figure-Eight Three-Body Choreography

Discovered numerically by Moore (1993) and proven to exist by Chenciner & Montgomery (2000), this remarkable periodic solution has three equal masses tracing a figure-eight curve.

**Key finding:** Initial conditions (Simó):
- Body 1: x = (-0.97000436, 0.24308753), v = (0.4662036850, 0.4323657300)
- Body 2: x = (0.97000436, -0.24308753), v = (0.4662036850, 0.4323657300)
- Body 3: x = (0, 0), v = (-0.93240737, -0.86473146)
- G = 1, m₁ = m₂ = m₃ = 1, Period T ≈ 6.3259

This solution is linearly stable (Kapela & Simó, 2007) and provides an excellent test of integrator accuracy for multi-body systems.

## 10. Survey of Open-Source N-Body Codebases

### 10.1 REBOUND (Python/C)
- **Language:** C core with Python bindings
- **Algorithms:** Leapfrog, SEI, Wisdom-Holman (WHFast), IAS15 (15th-order), MERCURIUS (hybrid)
- **Design:** Highly modular, supports collisions, open/periodic boundaries, Barnes-Hut tree
- **Reference:** Rein & Liu (2012), A&A 537, A128

### 10.2 GADGET-2 (C)
- **Language:** C with MPI parallelization
- **Algorithms:** TreePM (Barnes-Hut tree + particle-mesh), SPH for gas
- **Design:** Massively parallel cosmological code, block time-stepping, space-filling curve domain decomposition
- **Reference:** Springel (2005), MNRAS 364, 1105

### 10.3 NBODY6 (Fortran)
- **Language:** Fortran
- **Algorithms:** Direct summation with Ahmad-Cohen neighbour scheme, KS regularization, chain regularization
- **Design:** Specialized for collisional stellar dynamics, adaptive individual time-steps
- **Reference:** Aarseth (2003), Cambridge University Press

### 10.4 PyNbody (Python)
- **Language:** Pure Python with NumPy
- **Algorithms:** Direct summation, basic integrators
- **Design:** Educational, easy to read and modify
- **Notable:** Good reference implementation for learning

### 10.5 AMUSE (Python/Multiple)
- **Language:** Python framework coupling multiple codes
- **Algorithms:** Bridges multiple specialized codes (NBODY6, Gadget, etc.)
- **Design:** Community framework for multi-physics astrophysical simulations
- **Notable:** Provides uniform Python interface to diverse simulation codes

### 10.6 Brutus (C++)
- **Language:** C++
- **Algorithms:** Direct summation with arbitrary-precision arithmetic (MPFR)
- **Design:** Designed for converged N-body solutions, can achieve machine-independent results
- **Notable:** Used to establish "ground truth" solutions for chaotic N-body problems

## 11. Integration Method Comparison and Selection

### Comparison Table

| Method | Order | Symplectic | Time-Reversible | Force Evals/Step | Energy Drift Behavior |
|--------|-------|-----------|-----------------|-------------------|----------------------|
| Forward Euler | 1st | No | No | 1 | Linear growth (secular) — E increases monotonically |
| Symplectic Euler | 1st | Yes | No | 1 | Bounded oscillation around true E |
| Leapfrog/Verlet (KDK) | 2nd | Yes | Yes | 1 | Bounded oscillation, O(dt²) amplitude |
| RK4 (Runge-Kutta 4th) | 4th | No | No | 4 | Slow secular drift — better short-term, worse long-term |
| Yoshida 4th-order | 4th | Yes | Yes | 3 | Bounded oscillation, O(dt⁴) amplitude |

### Selected Methods for Implementation

We select **4 integrators** for implementation, justified as follows:

1. **Forward Euler** — Baseline. Demonstrates why naive integration fails for Hamiltonian systems. Shows linear energy drift serving as motivation for symplectic methods. [verlet1967, dehnen2011]

2. **Leapfrog (KDK)** — Workhorse symplectic integrator. Second-order accurate, time-reversible, requires only 1 force evaluation per step. The standard choice for N-body simulations across astrophysics. [wisdom1991, hernandez2015]

3. **Velocity Verlet** — Mathematically equivalent to KDK leapfrog but provides synchronized positions and velocities at each step. Verification of equivalence validates our implementation. [verlet1967]

4. **Adaptive time-stepping** (acceleration-based with leapfrog core) — Addresses the key practical limitation of fixed-step methods for eccentric orbits. Uses dt ∝ sqrt(ε/|a|) criterion. [huang1997, aarseth2003]

### Rationale for Omissions

- **Symplectic Euler**: Omitted because leapfrog is strictly superior (same cost, higher order, time-reversible).
- **RK4**: Omitted from core implementation because it is not symplectic and the project focuses on long-term orbital dynamics where symplecticity matters. RK4's strength (high-order local accuracy) is less relevant than its weakness (secular energy drift) for our benchmarks.
- **Yoshida 4th-order**: Omitted for simplicity. While it offers 4th-order symplectic integration, the negative sub-step coefficients can cause stability issues, and for our benchmark problems the 2nd-order leapfrog suffices.

## References

All sources are cited in `sources.bib`. Key references include:
- Aarseth (2003) — Gravitational N-Body Simulations (textbook)
- Barnes & Hut (1986) — Hierarchical O(N log N) force calculation
- Verlet (1967) — Computer experiments on classical fluids
- Wisdom & Holman (1991) — Symplectic maps for the N-body problem
- Yoshida (1990) — Construction of higher order symplectic integrators
- Dehnen & Read (2011) — N-body simulations review
- Springel (2005) — GADGET-2 cosmological simulation code
- Rein & Liu (2012) — REBOUND N-body code
- Chenciner & Montgomery (2000) — Figure-eight three-body choreography
- Hernandez & Bertschinger (2015) — Symplectic integration for collisional N-body

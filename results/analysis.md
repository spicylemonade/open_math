# Summary Analysis: Numerical Integrators for Simple Pendulum Simulation

## 1. Integrator Properties

| Method | Order | Symplectic | Cost/Step (evals) | Energy Behavior |
|--------|-------|------------|-------------------|-----------------|
| Forward Euler | 1 | No | 1 | Monotonic drift |
| Symplectic Euler | 1 | Yes | 1 | Bounded oscillation |
| Störmer–Verlet | 2 | Yes | 2 | Bounded oscillation |
| RK4 | 4 | No | 4 | Slow drift |

## 2. Convergence Results

Our convergence study (see `figures/convergence.png`) measured energy drift across five timestep sizes (dt = 0.1, 0.05, 0.01, 0.005, 0.001) over 50 seconds with theta_0 = pi/3:

- **Forward Euler** shows O(dt) energy drift scaling, consistent with its first-order accuracy. Energy grows monotonically, reaching 9090% drift over 1000 s (see `figures/long_time_energy.png`).
- **Symplectic Euler** shows O(dt) energy drift *magnitude* but the error remains **bounded** rather than growing secularly. Over 1000 s, drift stays at 1.3% — confirming the symplectic property described by Hairer et al. [hairer_geometric].
- **Störmer–Verlet** exhibits O(dt^2) convergence, with energy drift bounded at 0.02% over 1000 s. This is the best-performing symplectic method, as expected for a second-order scheme [wikipedia_verlet].
- **RK4** achieves O(dt^4) convergence, with energy drift as low as 1.8e-15 J at dt=0.001. However, being non-symplectic, it exhibits slow secular drift over very long timescales [wikipedia_rk].

## 3. Accuracy vs Analytical Solution

At small angles (theta_0 = 0.05 rad), we compared all methods against the linearized analytical solution theta(t) = theta_0 * cos(sqrt(g/L) * t):

- RK4 and Verlet at small dt converge to a floor of ~1e-4 RMS error, which is the **linearization error** (sin(theta) ≈ theta approximation), not numerical error.
- At theta_0 = 1e-4, RK4 achieves normalized error 2.6e-7, confirming true 4th-order accuracy.
- Forward Euler requires dt < 0.001 to achieve RMS error below 1e-3.

See `results/accuracy.json` for the full comparison table.

## 4. Large-Angle Verification

At theta_0 = 3.0 rad (near inverted), RK4 with dt=0.001 reproduces the exact elliptic-integral period T = 4*sqrt(L/g)*K(sin(theta_0/2)) to within **0.001%** relative error (see `results/large_angle.json`). The period T = 5.158 s is 2.57x the small-angle period T_0 = 2.006 s, clearly demonstrating the nonlinear period-amplitude dependence described in [herman_elliptic_period].

The non-sinusoidal waveform is clearly visible in `figures/large_angle.png`.

## 5. Performance Tradeoffs

From `results/performance.csv` and `figures/perf_accuracy.png`:

| Scenario | Recommended Method | Rationale |
|----------|--------------------|-----------|
| **Real-time / interactive** | Symplectic Euler | Cheapest per step (1 eval), bounded energy, adequate accuracy |
| **Long-time simulation** | Störmer–Verlet | 2nd-order with symplectic energy preservation; 0.02% drift over 1000 s |
| **High-accuracy / reference** | RK4 | 4th-order convergence, lowest numerical error, but ~4x cost and non-symplectic |
| **Never use** | Forward Euler | Monotonic energy growth makes it unsuitable for any production use |

## 6. Key Findings

1. **Symplectic methods are essential for long-time integration.** Forward Euler's energy diverges exponentially, while symplectic Euler and Verlet maintain bounded energy oscillation indefinitely [hairer_geometric, wikipedia_symplectic].

2. **Verlet offers the best overall tradeoff** between accuracy, computational cost, and energy conservation for Hamiltonian systems [hairer_symplectic_lecture].

3. **RK4 is the accuracy champion** but should be used with caution for long simulations without energy correction, as its non-symplectic nature leads to secular drift.

4. **The nonlinear pendulum period** matches the exact elliptic-integral formula to high precision, confirming correct implementation of the equations of motion [herman_elliptic_period].

## References

- [hairer_geometric] Hairer, Lubich, Wanner. *Geometric Numerical Integration*, 2nd ed. Springer, 2006.
- [hairer_symplectic_lecture] Hairer. *Lecture 2: Symplectic Integrators*. University of Geneva, 2010.
- [wikipedia_symplectic] Wikipedia. *Symplectic integrator*. 2025.
- [wikipedia_verlet] Wikipedia. *Verlet integration*. 2025.
- [wikipedia_rk] Wikipedia. *Runge–Kutta methods*. 2025.
- [herman_elliptic_period] Herman. *The Period of the Nonlinear Pendulum*. LibreTexts, 2023.

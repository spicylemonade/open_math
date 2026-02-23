# Integrator Comparison Summary

All measurements from a two-body circular Kepler orbit benchmark (dt = 0.01, 10,000 steps).

| Integrator | Order | Symplectic | Max \|dE/E\| at 10k steps | Wall Time per Step | Recommended Use Case |
|---|---|---|---|---|---|
| **Forward Euler** | 1st | No | 4.78 × 10⁻¹ | 13.5 μs | Educational / debugging only. Unsuitable for production simulations due to secular energy drift. |
| **Leapfrog (KDK)** | 2nd | Yes | 2.50 × 10⁻⁹ | 14.7 μs | **General-purpose gravitational dynamics.** Best balance of accuracy, symplecticity, and speed. Standard in GADGET, REBOUND, and most N-body codes. |
| **Velocity Verlet** | 2nd | Yes | 2.50 × 10⁻⁹ | 17.3 μs | Equivalent to Leapfrog. Preferred when synchronized position-velocity output is needed (e.g., for diagnostics). Slightly slower due to extra array operations. |

## Key Findings

1. **Symplecticity matters**: Leapfrog and Velocity Verlet maintain bounded energy errors (~10⁻⁹), while Forward Euler drifts to ~50% error — a difference of **8 orders of magnitude**.

2. **Leapfrog ≡ Velocity Verlet**: Both produce identical trajectories to machine precision, confirming the mathematical equivalence proven by Jacobs (2019) and Hairer et al. (2003).

3. **Negligible cost difference**: All three integrators have comparable wall time per step (~13–17 μs for a 2-body system), since the dominant cost is the O(N²) force evaluation. For larger N, integrator overhead becomes irrelevant.

4. **Recommendation**: Use **Leapfrog (KDK)** as the default integrator. It is the simplest symplectic option, requires only one force evaluation per step, and integrates naturally with adaptive time-stepping schemes.

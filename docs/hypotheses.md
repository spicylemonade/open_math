# Research Hypotheses and Success Metrics

## Overview

This document defines three falsifiable hypotheses with quantitative targets for evaluating the minimal gravity simulator. Each hypothesis is grounded in the theoretical expectations from the literature review and targets measurable outcomes.

---

## H1: Symplectic Energy Conservation

**Hypothesis:** Symplectic integrators (leapfrog/Stormer-Verlet) will conserve energy to within 1e-6 relative error over 1000 orbital periods for the two-body Kepler problem (e=0.5), while forward Euler will exhibit secular energy drift.

### Theoretical Basis

Backward error analysis (Hairer, Lubich & Wanner 2006) shows that symplectic integrators preserve a modified Hamiltonian close to the true Hamiltonian, with the difference being O(dt^p) where p is the order of the method. For the leapfrog (p=2), the energy error oscillates but does not grow secularly. In contrast, non-symplectic methods like forward Euler introduce systematic dissipation, causing monotonic energy drift.

### Quantitative Predictions

| Integrator | dt     | Expected |dE/E| after 1000 periods | Error behavior |
|------------|--------|----------------------------------------|----------------|
| Euler      | 0.001  | > 1e-2 (secular growth)                | Monotonic drift |
| Leapfrog   | 0.001  | < 1e-6 (bounded oscillation)           | Oscillating     |
| RK4        | 0.001  | 1e-8 to 1e-4 (slow secular drift)      | Slow drift      |

### Falsification Criteria

- **CONFIRMED** if leapfrog |dE/E| < 1e-6 at t = 1000T AND Euler |dE/E| > 100x leapfrog |dE/E|
- **FALSIFIED** if leapfrog shows secular drift comparable to Euler, or if Euler conserves energy as well as leapfrog

### Test Configuration

- Two bodies: m1 = m2 = 0.5, semi-major axis a = 1, eccentricity e = 0.5
- G = 1, period T = 2*pi
- dt = 0.001, total time = 1000 * T
- Softening = 0 (exact Kepler problem)

---

## H2: Barnes-Hut Scalability Advantage

**Hypothesis:** The Barnes-Hut tree algorithm with theta=0.5 will outperform direct O(N^2) summation in wall-clock time for N > 100 particles, while maintaining force accuracy within 1% RMS relative error compared to direct summation.

### Theoretical Basis

Barnes & Hut (1986) showed that tree-based force computation scales as O(N log N) compared to O(N^2) for direct summation. The crossover point depends on implementation overhead, but typically occurs at N ~ 50-200. The opening angle theta controls accuracy: smaller theta gives more accurate but slower results. For theta=0.5, the force error is typically well below 1% (Dehnen & Read 2011).

### Quantitative Predictions

| N    | Direct time (relative) | Barnes-Hut time (relative) | BH faster? |
|------|----------------------|---------------------------|------------|
| 10   | 1.0                  | ~2.0                      | No         |
| 50   | 1.0                  | ~1.0                      | ~Equal     |
| 100  | 1.0                  | ~0.5                      | Yes        |
| 500  | 1.0                  | ~0.15                     | Yes        |
| 1000 | 1.0                  | ~0.08                     | Yes        |

### Falsification Criteria

- **CONFIRMED** if: (a) Barnes-Hut is faster than direct for N >= 200, AND (b) RMS force error < 1% for all tested N
- **FALSIFIED** if: Barnes-Hut is slower than direct for N > 500, OR force error exceeds 5% with theta=0.5

### Test Configuration

- Random N-body cluster: positions uniform in [-10, 10]^2, masses uniform in [0.5, 1.5]
- Fixed random seed = 42
- Force computation timed over 10 repetitions (median reported)
- N in [10, 50, 100, 200, 500, 1000]

---

## H3: Adaptive Time-Stepping Efficiency

**Hypothesis:** Adaptive time-stepping (dt proportional to 1/sqrt(max|a|)) will reduce the total number of integration steps by more than 50% compared to fixed time-stepping on a highly eccentric two-body orbit (e=0.9), while achieving comparable or better energy conservation.

### Theoretical Basis

Eccentric orbits have vastly different dynamical timescales at perihelion (fast, strong forces) vs. aphelion (slow, weak forces). Fixed time-stepping must use the smallest dt needed at perihelion everywhere, wasting computation during the slow aphelion passage. Adaptive methods concentrate steps near perihelion and use large steps near aphelion. Quinn et al. (1997) and Rein & Spiegel (2015) demonstrate significant efficiency gains from adaptive stepping.

### Quantitative Predictions

- For e = 0.9, the velocity ratio between perihelion and aphelion is sqrt((1+e)/(1-e)) = sqrt(19) ~ 4.36
- Fixed dt must resolve the fastest timescale everywhere: ~10,000 steps/period
- Adaptive dt can use large steps during ~80% of the orbit: expected ~3,000-4,000 steps/period
- Step reduction: > 50%

### Falsification Criteria

- **CONFIRMED** if adaptive uses < 50% of fixed-step count AND |dE/E| is within 2x of fixed-step result
- **FALSIFIED** if adaptive uses > 70% of fixed-step count, OR energy error is > 10x worse

### Test Configuration

- Two bodies: m1 = m2 = 0.5, semi-major axis a = 1, eccentricity e = 0.9
- G = 1, period T = 2*pi
- Fixed: dt = 0.001
- Adaptive: dt_base = 0.01, eta = 0.01 (safety factor), dt = eta / sqrt(max|a|)
- Total time: 100 periods
- Softening = 0

---

## Summary of Predictions

| Hypothesis | Key Prediction | Quantitative Target | Test |
|------------|---------------|---------------------|------|
| H1 | Leapfrog conserves energy, Euler drifts | Leapfrog |dE/E| < 1e-6 over 1000T | item_017 |
| H2 | Barnes-Hut faster for N > 100 | BH faster for N >= 200, force error < 1% | item_018 |
| H3 | Adaptive stepping saves > 50% steps | Step count < 50% of fixed, energy ~ same | item_019 |

All predictions are falsifiable with clear quantitative thresholds and will be tested in Phase 4 experiments.

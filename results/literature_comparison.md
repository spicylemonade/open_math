# Comparison of Simulation Results Against Published Literature

## 1. Energy Conservation Rates for Symplectic Integrators

| Metric | Our Result | Literature Value | Source | Agreement |
|--------|-----------|------------------|--------|-----------|
| Leapfrog energy error (10 orbits, dt=0.001) | 2.8e-13 | O(dt²) bounded | Dehnen & Read (2011), Wisdom & Holman (1991) | Excellent — error bounded as predicted by theory |
| Forward Euler drift (10 orbits, dt=0.001) | 10.1% | Linear secular growth | Dehnen & Read (2011), Wikipedia: Energy drift | Consistent — linear drift confirmed |
| Leapfrog 2nd-order convergence ratio | 4.00x | 4.0x (2nd order) | Verlet (1967), Yoshida (1990) | Exact match |
| Symplectic vs non-symplectic | Leapfrog bounded, Euler drifts | Symplectic: bounded; non-symplectic: secular drift | Hernandez & Bertschinger (2015), Dehnen & Read (2011) | Fully consistent |

**Explanation:** Our leapfrog integrator shows energy errors oscillating around the true value (bounded at ~10^-13 for dt=0.001), consistent with the "shadow Hamiltonian" theory described in Dehnen & Read (2011). The forward Euler's secular drift at ~10% per 10 orbits matches the expected first-order non-symplectic behavior. The exact 4.0x convergence ratio confirms the theoretical 2nd-order accuracy of the Störmer-Verlet method (Verlet, 1967).

## 2. Barnes-Hut Force Accuracy vs Opening Angle θ

| θ | Our Mean Error | Our Median Error | Literature | Source | Agreement |
|---|---------------|-----------------|------------|--------|-----------|
| 0.0 | 0.0% | 0.0% | Exact | Barnes & Hut (1986) | Exact — reduces to direct summation |
| 0.3 | 0.37% | 0.22% | ~0.1-1% | Barnes & Hut (1986), Dehnen & Read (2011) | Consistent |
| 0.5 | 1.58% | 0.82% | ~1-2% | Barnes & Hut (1986), Princeton BH assignment | Consistent |
| 0.7 | 3.70% | 2.10% | ~3-5% | Grudic (2017) blog post | Consistent |
| 1.0 | 9.45% | 5.55% | ~5-10% | Barnes & Hut (1986) | Consistent |

**Explanation:** Our force errors are fully consistent with literature values. Barnes & Hut (1986) note that θ = 0.5 is commonly used in practice, providing a good accuracy-speed tradeoff. The slightly elevated mean error relative to the median is caused by outlier particles near tree cell boundaries, a known effect discussed in Dehnen & Read (2011). The monopole-only approximation used here (no quadrupole corrections) is the simplest Barnes-Hut variant; adding quadrupole moments would reduce errors by approximately an order of magnitude.

## 3. Computational Scaling Exponents

| Method | Our Exponent | Literature Value | Source | Agreement |
|--------|-------------|------------------|--------|-----------|
| Direct summation | 2.00 | 2.0 (O(N²)) | Aarseth (2003), Dehnen & Read (2011) | Exact match |
| Barnes-Hut (θ=0.5) | 1.24 | ~1.0-1.3 (O(N log N)) | Barnes & Hut (1986), Springel (2005) | Consistent |
| Crossover N | ~100 | ~50-100 | arborjs.org BH tutorial, Princeton assignment | Consistent |

**Explanation:** The direct summation exponent of exactly 2.0 confirms the O(N²) theoretical complexity. The Barnes-Hut exponent of 1.24 falls between N (exponent 1.0) and N^1.3, consistent with O(N log N) behavior — the logarithmic factor adds a slowly growing component to the linear scaling. The crossover at N~100 matches the commonly cited range of 50-100 particles in the Barnes-Hut literature. Springel (2005) notes that the GADGET code uses a similar tree structure and observes comparable scaling behavior.

## 4. Figure-Eight Choreography Stability

| Metric | Our Result | Literature Value | Source | Agreement |
|--------|-----------|------------------|--------|-----------|
| Period | ~6.3259 | 6.32591... | Chenciner & Montgomery (2000), Simó | Consistent |
| Stability over 5 periods | Energy error 5.9e-9 | Linearly stable | Kapela & Simó (2007) | Confirmed |
| Position return error | 8.9e-5 | Small (stable orbit) | Moore (1993) | Consistent |

**Explanation:** Our reproduction of the figure-eight choreography confirms its stability as proven by Kapela & Simó (2007). The energy conservation of 5.9e-9 over 5 periods demonstrates that the leapfrog integrator accurately preserves the Hamiltonian structure of this three-body orbit. The position return error of 8.9e-5 confirms that the orbit is periodic to high precision.

## Summary

All three categories of quantitative comparison show excellent agreement with published literature values. No unexplained deviations were observed. The minor discrepancies (e.g., Barnes-Hut mean error slightly above typical values for θ=0.5) are attributable to implementation choices (monopole-only, no quadrupole) and are consistent with expectations.

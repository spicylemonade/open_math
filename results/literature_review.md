# Literature Review: Kissing Number Problem in Dimension 5

## 1. Problem Statement

The kissing number τ(n) is the maximum number of non-overlapping unit spheres in ℝⁿ that can simultaneously touch a central unit sphere. Equivalently, it is the maximum number of points on the unit sphere S^{n-1} such that any two points have angular separation at least 60° (inner product ≤ 1/2).

**Status for n=5:** 40 ≤ τ₅ ≤ 44. The exact value remains open.

## 2. Known Exact Kissing Numbers

| Dimension | τ(n)    | Proved by                | Year |
|-----------|---------|--------------------------|------|
| 1         | 2       | Trivial                  | —    |
| 2         | 6       | Trivial                  | —    |
| 3         | 12      | Schütte & van der Waerden | 1953 |
| 4         | 24      | Musin                    | 2003/2008 |
| 8         | 240     | Odlyzko & Sloane (LP)    | 1979 |
| 24        | 196,560 | Odlyzko & Sloane (LP)    | 1979 |

## 3. Key Methods and Papers

### 3.1 Delsarte Linear Programming Method

**Delsarte (1973)** introduced the linear programming method for bounding sizes of codes. Extended to spherical codes by **Delsarte, Goethals, and Seidel (1977)**. The method uses Gegenbauer polynomials: if f(t) = Σ fₖ Cₖ^λ(t) satisfies f̂(k) ≥ 0 for all k and f(t) ≤ 0 for t ∈ [-1, 1/2], then τ(n) ≤ f(1).

For n=5 with λ = 3/2, the LP bound gives τ₅ ≤ ~46.3 (Odlyzko-Sloane, 1979).

### 3.2 Kabatyansky-Levenshtein Bound

**Kabatyansky and Levenshtein (1978)** derived asymptotic bounds for spherical codes. Their methods provide the best known asymptotic upper bounds: τ(n) ≤ 2^{0.401n(1+o(1))} as n → ∞.

### 3.3 Odlyzko-Sloane (1979)

**Odlyzko and Sloane** applied the Delsarte LP method systematically. They proved τ₈ = 240 and τ₂₄ = 196,560 exactly (the LP bound is tight). For n=5 they obtained τ₅ ≤ 46.

### 3.4 Musin's Proof for n=4 (2003/2008)

**Musin (2008)** proved τ₄ = 24 by combining the Delsarte LP method with geometric arguments about contact graphs. The Delsarte LP alone gives τ₄ ≤ 25.56, so additional geometric reasoning was needed. Published in *Annals of Mathematics*.

### 3.5 Bachoc-Vallentin SDP Bounds (2008)

**Bachoc and Vallentin (2008)** introduced semidefinite programming (SDP) bounds that extend the Delsarte LP. Using three-point correlations (not just pairwise), they proved τ₅ ≤ 45, improving from 46. Their method also re-proved τ₃ = 12, τ₄ = 24, τ₈ = 240, τ₂₄ = 196,560. Published in *JAMS*. Won the SIAG/OPT prize.

### 3.6 Mittelmann-Vallentin High-Accuracy SDP (2010)

**Mittelmann and Vallentin (2010)** performed high-accuracy numerical computations of the Bachoc-Vallentin SDP bound. For n=5 they obtained τ₅ ≤ 44.998, which gives the integer bound τ₅ ≤ 44. This is the current best upper bound.

### 3.7 Pfender-Ziegler Survey (2004)

**Pfender and Ziegler (2004)** wrote an accessible survey of kissing numbers and sphere packings, covering the history from Newton-Gregory to modern LP bounds. Published in *Notices of the AMS*. **Pfender (2007)** also improved Delsarte bounds for small dimensions.

### 3.8 Cohn-Kumar Universal Optimality (2007)

**Cohn and Kumar (2007)** introduced the concept of universally optimal spherical codes and proved optimality for "sharp" configurations. The D₅ minimal vectors form a spherical code but are NOT universally optimal (this was the "belief" later refuted by Szöllősi). Published in *JAMS*.

### 3.9 Boyvalenkov-Dodunekov-Musin Survey (2012/2015)

**Boyvalenkov, Dodunekov, and Musin** wrote comprehensive surveys covering old and recent results on kissing numbers. They unified the various LP/SDP approaches and documented bounds across all dimensions up to 128.

### 3.10 Szöllősi's New 5D Arrangement (2023)

**Szöllősi (2023)** discovered a third non-isometric kissing arrangement Q₅ of 40 vectors in ℝ⁵, distinct from D₅ and L₅ (Leech-type). This refuted a "belief" of Cohn-Jiao-Kumar-Torquato about uniqueness. Published in *Mathematical Research Letters*.

### 3.11 Cohn-Rajagopal Variations (2024)

**Cohn and Rajagopal (2024)** analyzed Szöllősi's construction and produced a fourth non-isometric kissing configuration in 5D. They also constructed five-dimensional sphere packings from these configurations.

### 3.12 Cohn-Elkies Sphere Packing Bounds (2003)

**Cohn and Elkies (2003)** extended LP bounds to sphere packing densities. Their approach laid groundwork for Viazovska's solution in dimension 8.

### 3.13 Viazovska (2017)

**Viazovska (2017)** proved the E₈ lattice is the densest sphere packing in ℝ⁸. Uses modular forms as the "magic function" for the Cohn-Elkies LP bound. Published in *Annals of Mathematics*.

## 4. Summary of Bounds History for n=5

| Year | Authors               | Method        | Upper Bound |
|------|-----------------------|---------------|-------------|
| 1963 | Coxeter               | Geometric     | 48          |
| 1979 | Odlyzko-Sloane        | Delsarte LP   | ~46         |
| 2008 | Bachoc-Vallentin      | SDP           | 45          |
| 2010 | Mittelmann-Vallentin  | High-acc. SDP | 44          |

Lower bound: 40 (D₅ lattice, confirmed by 3+ distinct constructions).

## 5. Gap Analysis

The gap 40–44 persists because:

1. **LP/SDP bounds plateau**: The Delsarte LP gives ~46, 3-point SDP gives 44. Higher-order correlations (4-point, 5-point) are computationally intractable.
2. **Constructions plateau**: Despite finding 3+ non-isometric 40-point arrangements, no one has found a 41-point arrangement. However, this doesn't prove none exists.
3. **The gap between methods**: LP/SDP bounds use global polynomial conditions. Construction methods are local (start from a configuration and try to add points). Neither approach has enough resolution to close the gap.

## 6. Opportunities for Dimensional Analysis Approach

Based on this review, the dimensional analysis framework could contribute in two ways:

1. **Constraining Gegenbauer coefficients**: The volume recurrence V_n = (2π/n)R²V_{n-2} creates relationships between cap areas in different dimensions that could add constraints to the Delsarte LP.

2. **Ruling out contact graph structures**: The dimensional volume argument V_n = S_{n-1}·R/n constrains how many caps of a given size can fit on S^{n-1}, potentially eliminating certain contact graph topologies for hypothetical 41-44 point configurations.

## References

All papers cited above are recorded in `sources.bib` in the repository root.

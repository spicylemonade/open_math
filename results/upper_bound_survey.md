# Survey of Upper Bound Techniques for τ₅

## 1. Delsarte Linear Programming Bound

**Reference:** Delsarte (1973) \cite{delsarte1973algebraic}, Delsarte-Goethals-Seidel (1977) \cite{delsarte1977spherical}

The Delsarte LP bound for the kissing number in dimension n uses Gegenbauer polynomials C_k^λ(t) with λ = (n-2)/2. The bound is:

**τ_n ≤ max f(1)** subject to:
- f(t) = Σ_{k=0}^{d} f_k C_k^λ(t)
- f̂(k) = f_k ≥ 0 for all k ≥ 1
- f(t) ≤ 0 for all t ∈ [-1, 1/2]
- f(0) = 1 (normalization, equivalent form)

For n=5 (λ = 3/2), the LP bound gives τ₅ ≤ ~46.3 \cite{odlyzko1979kissing}. The polynomial degree needs to be sufficiently large; with degree d ≥ 8, the bound converges.

**Why it's not tight for n=5:** The LP bound is tight only for n = 8 and n = 24, where special "magic" polynomials exist. For other dimensions, the LP constraint f(t) ≤ 0 on [-1, 1/2] is too permissive—it doesn't capture the geometric constraints from three or more vectors simultaneously.

## 2. Bachoc-Vallentin SDP Bound (Three-Point Bound)

**Reference:** Bachoc & Vallentin (2008) \cite{bachoc2008new}

Extends Delsarte LP by incorporating three-point correlations. Instead of just constraining pairwise inner products, the SDP considers the positive semidefiniteness of a matrix involving triples of points on the sphere.

For n=5, this improves the bound from 46 to 45 \cite{bachoc2008new}.

The method represents the angular distribution as a sum of "zonal" and "non-zonal" terms, each constrained by SDP conditions. The resulting optimization problem is:

**τ_n ≤ max 1 + f(1)** subject to:
- A certain matrix-valued function M(t₁, t₂, t₃) being positive semidefinite
- f(t) ≤ 0 for t ∈ [-1, 1/2]
- Additional SDP constraints from three-point geometry

## 3. Mittelmann-Vallentin High-Accuracy SDP

**Reference:** Mittelmann & Vallentin (2010) \cite{mittelmann2010high}

Performed high-accuracy numerical computation of the Bachoc-Vallentin SDP, obtaining τ₅ ≤ 44.998, which gives the integer bound **τ₅ ≤ 44**.

This is the current best upper bound. The computation used sophisticated SDP solvers with careful numerical analysis to ensure the bound is rigorous.

## 3. Why the Gap 40–44 Persists

### Upper bound side:
1. **LP/SDP hierarchy saturation:** The Delsarte LP (1-point bound) gives ~46. The 3-point SDP gives ~45. Higher-order k-point bounds are computationally intractable for k ≥ 4.
2. **No "magic function":** Unlike dimensions 8 and 24, there is no known polynomial that simultaneously satisfies f(1/2) = 0 and has a root structure matching the inner product spectrum of an optimal code.

### Lower bound side:
1. **D5 lattice gives 40:** The minimal vectors of D5 form a 40-point kissing configuration with inner product spectrum {-1, -1/2, 0, +1/2}.
2. **Multiple non-isometric 40-point configs:** Szöllősi (2023) \cite{szollosi2023five} found a third configuration Q₅; Cohn-Rajagopal (2024) \cite{cohn2024variations} found a fourth. This suggests 40 may be optimal, as multiple constructions hitting the same value typically indicates optimality.
3. **No 41-point config found:** Despite extensive search, no valid 41-point kissing configuration in ℝ⁵ has been discovered.

### The fundamental difficulty:
The gap between 40 and 44 exists because current polynomial/SDP methods cannot distinguish between "approximately feasible" and "exactly feasible" configurations at the boundary. The LP/SDP dual certificates provide upper bounds, but they leave a residual gap that seems to require fundamentally new techniques to close.

## 4. Opportunities for Dimensional Analysis Approach

### Opportunity 1: Constraining Gegenbauer Coefficients via Volume Identities

The volume recurrence V_n = (2π/n)R²V_{n-2} links the geometry of S⁴ to that of S² and S³. Specifically:

- The integral of a Gegenbauer polynomial over a spherical cap can be expressed in terms of cap areas in lower dimensions
- The recurrence V₅ = (2π/5)·V₃ means the "volumetric content" of spherical caps on S⁴ is constrained by cap geometry on S²
- This creates additional linear constraints on the Gegenbauer coefficients f_k that can be added to the Delsarte LP

**Potential impact:** If the volume-based constraints are linearly independent from the existing LP constraints, they could tighten the bound below 44.

### Opportunity 2: Ruling Out Contact Graph Structures

The D5 kissing configuration has a 12-regular contact graph (each point touches exactly 12 neighbors at angle 60°). A hypothetical 41-point configuration would need a different graph structure.

Using dimensional volume arguments:
- Each vertex in the contact graph has degree ≤ τ₄ = 24 (since the neighbors lie on a great 3-sphere S³)
- The 1/n factor in V_n = S_{n-1}·R/n constrains the "volume overhead" per contact
- If a hypothetical 41-point graph requires certain subconfigurations that violate these dimensional constraints, it can be ruled out

**Potential impact:** This could eliminate τ₅ = 44 or 43 by showing no graph with the required properties can be realized on S⁴.

### Opportunity 3: Cross-Dimensional Density Constraints

The cap density ρ_n = τ_n · A_cap(n, π/6) / S_{n-1} measures how efficiently the sphere is packed with caps. The dimensional recurrence creates constraints:

- ρ₃ = 12 · A_cap(3, π/6) / S₂ (known exactly)
- ρ₅ must be "compatible" with ρ₃ through the recurrence

This is explored further in Phase 3 (cross-dimensional consistency check).

## 5. Summary Table

| Method | Year | Authors | τ₅ Upper Bound | Key Innovation |
|--------|------|---------|----------------|----------------|
| Simple cap packing | — | Folklore | 77 | Area ratio |
| Coxeter bound | 1963 | Coxeter | 48 | Geometric |
| Delsarte LP | 1979 | Odlyzko-Sloane | ~46 | Gegenbauer polynomials |
| 3-point SDP | 2008 | Bachoc-Vallentin | 45 | Semidefinite programming |
| High-acc. SDP | 2010 | Mittelmann-Vallentin | **44** | Numerical precision |
| Dimensional analysis | 2026 | This work | TBD | Volume recurrence constraints |

## References

\cite{delsarte1973algebraic, delsarte1977spherical, odlyzko1979kissing, bachoc2008new, mittelmann2010high, szollosi2023five, cohn2024variations, pfender2004kissing, musin2008kissing}

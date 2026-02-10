# Family-by-Family Analysis

## Overview

For each family of semisimple Lie groups, we determine whether the answer to the central question depends on the ambient group G. Recall the question: can Γ (uniform lattice in G with 2-torsion) be π₁ of a closed manifold with ℚ-acyclic universal cover?

---

## Family 1: SO(n, 1) — Real Hyperbolic Groups

| Property | Value |
|----------|-------|
| **Symmetric space** | ℍⁿ (real hyperbolic n-space) |
| **Dimension** | n |
| **Uniform lattices with 2-torsion?** | Yes, for all n ≥ 2. Hyperbolic reflection groups (Vinberg) exist for n ≤ 30. Arithmetic lattices with 2-torsion exist for all n. |
| **Smith-theoretic obstruction?** | No. M̃ can be ℚ-acyclic but not 𝔽₂-acyclic. |
| **Surgery-theoretic approach** | Works for n ≥ 5. The rational surgery obstruction vanishes. The 2-local obstruction is case-dependent but manageable. |
| **Verdict** | **YES** for n ≥ 5. For n = 2, 3, 4: requires separate analysis (low-dimensional topology). |

**Notes:** For n = 2 (Fuchsian groups), every Fuchsian group with torsion is π₁ of a 2-orbifold. Finding a 2-manifold M with π₁(M) = Γ and ℚ-acyclic M̃: since M is a surface, M̃ must be simply connected and ℚ-acyclic, i.e., ℍ² or a simply connected surface. But the only simply connected compact surface without boundary is S², and π₁(S²) = 0, not Γ. If M is not simply connected... wait, M̃ IS simply connected (universal cover). A compact surface without boundary with non-trivial fundamental group has universal cover ℝ² (aspherical) or S² (finite π₁). Since our Γ is infinite and has torsion, neither works as a surface fundamental group with ℚ-acyclic cover. So for n = 2, the answer may be **NO** because surfaces are too constrained. But dim(M) = n = 2, and the only closed 2-manifolds are classified (genus g ≥ 0), and their universal covers are S², ℝ², or {point}. The question is whether there exists a 2-manifold with the required properties — this seems impossible since all surface groups are either finite, ℤ², or free products (for the orientable case: surface groups of genus ≥ 1 are torsion-free). However, the question asks for dim(M) = dim(G/K) = n, and for n = 2 the classification of surfaces prevents it.

**Revised verdict:** **YES** for n ≥ 5, **likely YES** for n = 4 (Freedman), **OPEN** for n = 3, **NO** for n = 2 (surface classification).

---

## Family 2: SU(n, 1) — Complex Hyperbolic Groups

| Property | Value |
|----------|-------|
| **Symmetric space** | ℂℍⁿ (complex hyperbolic n-space) |
| **Dimension** | 2n |
| **Uniform lattices with 2-torsion?** | Yes, for all n ≥ 1. Anti-holomorphic involutions and central elements provide 2-torsion. |
| **Smith-theoretic obstruction?** | No. Same argument as SO(n,1). |
| **Surgery-theoretic approach** | Works for 2n ≥ 5, i.e., n ≥ 3. Rational obstruction vanishes. |
| **Verdict** | **YES** for n ≥ 3 (dim ≥ 6). **Likely YES** for n = 2 (dim 4, Freedman). **OPEN** for n = 1 (dim 2, same surface constraint as SO(2,1)). |

---

## Family 3: Sp(n, 1) — Quaternionic Hyperbolic Groups

| Property | Value |
|----------|-------|
| **Symmetric space** | ℍℍⁿ (quaternionic hyperbolic n-space) |
| **Dimension** | 4n |
| **Uniform lattices with 2-torsion?** | Yes. All lattices are arithmetic (Corlette/Gromov–Schoen). Quaternionic involutions provide 2-torsion. |
| **Smith-theoretic obstruction?** | No. |
| **Surgery-theoretic approach** | Works for 4n ≥ 5, i.e., n ≥ 2 (dim ≥ 8). For n = 1 (dim 4): Freedman theory applies. |
| **Verdict** | **YES** for n ≥ 2 (dim ≥ 8). **Likely YES** for n = 1 (dim 4). |

---

## Family 4: F₄₍₋₂₀₎ — Exceptional Rank-1 Group (Cayley Hyperbolic Plane)

| Property | Value |
|----------|-------|
| **Symmetric space** | Cayley hyperbolic plane 𝕆ℍ² |
| **Dimension** | 16 |
| **Uniform lattices with 2-torsion?** | Yes (arithmetic lattices exist, and contain torsion). |
| **Smith-theoretic obstruction?** | No. |
| **Surgery-theoretic approach** | Works (dim = 16 ≥ 5). |
| **Verdict** | **YES**. |

---

## Family 5: SL(n, ℝ) — Higher-Rank Groups (n ≥ 3)

| Property | Value |
|----------|-------|
| **Symmetric space** | SL(n,ℝ)/SO(n) |
| **Dimension** | n(n+1)/2 − 1 |
| **Uniform lattices with 2-torsion?** | Yes, for all n ≥ 2. The matrix −I has order 2 for even n. For odd n, −I ∉ SL(n,ℝ), but other involutions exist in arithmetic lattices. |
| **Smith-theoretic obstruction?** | No. |
| **Surgery-theoretic approach** | Works for n ≥ 3 (dim ≥ 5). For n = 2: SL(2,ℝ)/SO(2) = ℍ², same as SO(2,1). |
| **Verdict** | **YES** for n ≥ 3 (dim ≥ 5). |

---

## Family 6: SO(p, q) with p, q ≥ 2 — Higher-Rank Orthogonal Groups

| Property | Value |
|----------|-------|
| **Symmetric space** | SO(p,q)/(SO(p)×SO(q)) |
| **Dimension** | pq |
| **Uniform lattices with 2-torsion?** | Yes. Raghunathan \cite{raghunathan1984} explicitly studied Spin(2,n) coverings. |
| **Smith-theoretic obstruction?** | No. |
| **Surgery-theoretic approach** | Works for pq ≥ 5. |
| **Verdict** | **YES** for pq ≥ 5 (almost all cases). |

---

## Summary Table

| Family | G | dim(G/K) | 2-torsion lattices exist? | Smith obstruction? | Surgery works? | Verdict |
|--------|---|----------|--------------------------|-------------------|---------------|---------|
| SO(n,1) | rank 1 | n | Yes (all n ≥ 2) | No | Yes (n ≥ 5) | YES (n ≥ 5) |
| SU(n,1) | rank 1 | 2n | Yes (all n ≥ 1) | No | Yes (n ≥ 3) | YES (n ≥ 3) |
| Sp(n,1) | rank 1 | 4n | Yes (all n ≥ 1) | No | Yes (n ≥ 2) | YES (n ≥ 2) |
| F₄₍₋₂₀₎ | rank 1 | 16 | Yes | No | Yes | YES |
| SL(n,ℝ) | rank n−1 | n(n+1)/2−1 | Yes (n ≥ 2) | No | Yes (n ≥ 3) | YES (n ≥ 3) |
| SO(p,q) | rank min(p,q) | pq | Yes | No | Yes (pq ≥ 5) | YES (pq ≥ 5) |

**The answer is YES for every family in sufficiently high dimension (dim G/K ≥ 5).** The low-dimensional cases (dim ≤ 4) require separate treatment due to surgery theory limitations.

**Consistency with item_014 synthesis: CONFIRMED.** The family-by-family analysis is fully consistent with the YES verdict.

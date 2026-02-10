# Open Questions and Future Directions

The following open questions emerge from our analysis of whether uniform lattices with 2-torsion can be fundamental groups of closed manifolds with rationally acyclic universal covers.

---

## Question 1: Explicit 2-Local Surgery Obstruction Computation

**Formal Statement.** Let Γ be a cocompact lattice in SO(5,1) containing an element of order 2, and let X be a finite Poincaré complex with π₁(X) ≅ Γ and H̃_*(X̃; ℚ) = 0. Does the surgery obstruction σ(f, b) ∈ L₅(ℤ[Γ]) vanish for some choice of normal map (f, b): M → X?

**Why it is interesting.** Our analysis establishes that the *rational* surgery obstruction vanishes and that the 2-local obstruction lies in a finite group. However, we have not computed this 2-local obstruction explicitly for any specific lattice. An explicit computation would either confirm the YES answer constructively or reveal unexpected obstructions at the prime 2.

**Applicable techniques.** The Farrell–Jones conjecture (verified for such Γ \cite{luck2005}) reduces the computation to the family of finite subgroups of Γ. For lattices with only ℤ/2 torsion, this reduces to computing L₅(ℤ[ℤ/2]), which is known (Wall \cite{wall1965}), but the assembly map contribution requires careful analysis.

**Related conjectures.** This is related to the general problem of computing structure sets S^{TOP}(X) for Poincaré complexes with infinite fundamental group, which connects to the Borel and Novikov conjectures \cite{ranicki1992}.

---

## Question 2: Low-Dimensional Cases (dim G/K ≤ 4)

**Formal Statement.** Let Γ be a cocompact Fuchsian group with 2-torsion (e.g., the triangle group Δ(2,3,7)). Does there exist a closed 3-manifold or 4-manifold M with π₁(M) ≅ Γ and H̃_*(M̃; ℚ) = 0?

**Why it is interesting.** Our main result requires dim(G/K) ≥ 5 due to surgery theory limitations. The 2-dimensional case is impossible (surface classification), and the 3- and 4-dimensional cases remain open. In dimension 3, Thurston's geometrization and Perelman's theorem provide powerful tools but are not directly applicable. In dimension 4, Freedman's theory might provide additional flexibility.

**Applicable techniques.** For dimension 4: Freedman's classification of simply connected closed 4-manifolds \cite{davis1983}, combined with equivariant techniques. For dimension 3: the orbifold theorem (Boileau–Leeb–Porti) characterizes 3-orbifolds, but producing a manifold (not orbifold) with the required π₁ is different.

**Related conjectures.** This connects to the question of which orbifold groups can be realized as fundamental groups of manifolds in one dimension higher than the orbifold dimension.

---

## Question 3: Optimal Homological Conditions

**Formal Statement.** For a fixed uniform lattice Γ with 2-torsion, what is the minimal amount of integral homology that the universal cover M̃ must carry? Specifically, define:

T(Γ) = min{ rank_ℤ H_*(M̃; ℤ/2) : M closed, π₁(M) ≅ Γ, H̃_*(M̃; ℚ) = 0 }

where the minimum is over all closed manifolds M satisfying the stated conditions. Is T(Γ) computable?

**Why it is interesting.** Our construction produces an M̃ that is ℚ-acyclic but has non-trivial 2-torsion in its integral homology. Understanding how much torsion is *necessary* would quantify the gap between ℚ-acyclicity and contractibility and could lead to a finer classification of manifolds by the homological complexity of their universal covers.

**Applicable techniques.** Smith theory \cite{smith1941} provides lower bounds: the fixed-point set of a ℤ/2-action constrains the mod-2 Betti numbers. Oliver's characterization \cite{oliver1975} of fixed-point sets could give sharper bounds. The Borel construction and equivariant cohomology spectral sequences are the natural computational tools.

**Related conjectures.** This is related to Dranishnikov's work on cohomological dimension and rational acyclicity in dimension theory, and to the general study of "how far from contractible" a universal cover can be while still allowing manifold structure.

---

## Question 4: Extension to p-Torsion for Odd Primes

**Formal Statement.** Let p be an odd prime, and let Γ be a uniform lattice in a semisimple Lie group G with an element of order p. Does there exist a closed manifold M with π₁(M) ≅ Γ and H̃_*(M̃; ℚ) = 0?

**Why it is interesting.** Our analysis focuses on 2-torsion, which is the most delicate case because the surgery obstruction groups L_*(ℤ[ℤ/p]) have the richest structure when p = 2. For odd p, Smith theory gives slightly different constraints (using 𝔽_p instead of 𝔽₂), and the L-theoretic obstructions are simpler (odd-primary L-theory is well-understood). The edge case analysis (results/edge_cases.md) predicts YES, but a complete proof has not been given.

**Applicable techniques.** For odd p, the key simplification is that L_*(ℤ[ℤ/p]) ⊗ ℤ[1/2] is computable via the Rothenberg sequence, and the 2-local complications that arise for p = 2 do not occur. The Davis–Lück manifold models \cite{davisluck2023} already handle the case where Γ/Γ' has odd order, providing a strong starting point.

**Related conjectures.** Davis–Lück conjecture that manifold models for E̲Γ exist when Γ/Γ' has odd order. Our question is the ℚ-acyclic relaxation of this conjecture extended to even order.

---

## Question 5: Smooth vs. Topological Category

**Formal Statement.** In the main result, the manifold M is constructed in the topological category (TOP). Does M admit a smooth structure? That is, can one find a *smooth* closed manifold M with π₁(M) ≅ Γ and H̃_*(M̃; ℚ) = 0?

**Why it is interesting.** The surgery exact sequence differs in the smooth (DIFF) and topological (TOP) categories. In the TOP category, the surgery obstruction groups are the L-groups of ℤ[Γ], while in the DIFF category there is an additional contribution from the exotic spheres group Θ_n. For n ≥ 5, the difference between S^{TOP}(X) and S^{DIFF}(X) is controlled by the homotopy groups of TOP/O. In many cases (e.g., n ≠ 4), TOP manifolds can be smoothed, but the smoothing obstruction could interact non-trivially with the 2-local structure.

**Applicable techniques.** Kirby–Siebenmann invariant for smoothability of TOP manifolds. The smoothing obstruction lies in H^4(M; ℤ/2), which depends on the specific manifold produced by our construction. For hyperbolic manifolds (G = SO(n,1)), the standard quotient Γ'\ℍⁿ is smooth, and the equivariant surgery could potentially be performed in the smooth category.

**Related conjectures.** For n = 4, this connects to the famous open problem of whether all closed topological 4-manifolds admit smooth structures (they don't in general — Donaldson/Freedman), and whether the specific manifolds produced by our construction are smoothable.

---

## Question 6: Characterization of All Realizable Groups

**Formal Statement.** Characterize the class of finitely presented groups Γ that can appear as π₁(M) for some closed manifold M with H̃_*(M̃; ℚ) = 0. Is this class strictly larger than the class of groups that can appear as π₁ of aspherical manifolds (i.e., torsion-free groups of type F)?

**Why it is interesting.** Our result shows that uniform lattices with torsion belong to this class, but the full characterization is unknown. The class of torsion-free groups of type F is well-studied (these are precisely the groups that can be π₁ of aspherical closed manifolds, in high dimensions). Our work shows the class for ℚ-acyclic covers is strictly larger: it contains groups with torsion.

**Applicable techniques.** The necessary conditions include: Γ must be of type FP over ℚ, must satisfy rational Poincaré duality in some dimension d, and the Wall finiteness obstruction in K̃₀(ℤ[Γ]) must vanish. The Bestvina–Brady construction \cite{bestvinabrady1997} shows that groups of type FP (over ℤ) need not be finitely presented; the analogous question over ℚ is whether rational FP implies the manifold realization.

**Related conjectures.** This is related to the general realization problem in geometric group theory: which groups are fundamental groups of closed manifolds? The combination of Poincaré duality and finite presentability constraints is classical (Wall), but the ℚ-acyclicity condition adds a new dimension to the problem.

---

## Summary

| # | Question | Difficulty | Most Promising Approach |
|---|----------|-----------|------------------------|
| 1 | Explicit 2-local obstruction | Medium | Farrell–Jones + assembly map computation |
| 2 | Low dimensions (≤ 4) | Hard | Freedman (dim 4), geometrization (dim 3) |
| 3 | Optimal torsion in M̃ | Medium | Smith theory + equivariant cohomology |
| 4 | Odd prime torsion | Medium-Easy | Davis–Lück + odd-primary L-theory |
| 5 | Smooth vs. topological | Medium | Kirby–Siebenmann + smoothing theory |
| 6 | Full characterization | Hard | General surgery theory + group theory |

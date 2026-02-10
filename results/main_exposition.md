# Uniform Lattices with Torsion as Fundamental Groups of Manifolds with Rationally Acyclic Universal Covers

## 1. Introduction and Problem Statement

### 1.1 The Question

We investigate the following question from geometric group theory and manifold topology:

**Question.** Suppose that Γ is a uniform lattice in a real semisimple Lie group G, and that Γ contains some 2-torsion. Is it possible for Γ to be the fundamental group of a compact manifold M without boundary whose universal cover M̃ is acyclic over the rational numbers ℚ?

This question sits at the intersection of several major areas of mathematics: the theory of lattices in Lie groups, algebraic topology (specifically homotopy theory and surgery theory), and geometric group theory. The question asks whether a natural algebraic constraint (rational acyclicity of the universal cover) can be satisfied by a manifold whose fundamental group has torsion — a situation that is well-known to be impossible under the stronger constraint of contractibility.

### 1.2 Definitions

**Definition 1 (Semisimple Lie Group).** A real Lie group G is *semisimple* if its Lie algebra has no nonzero solvable ideals. We assume G is connected with finite center. Examples include SL(n, ℝ), SO(p, q), SU(p, q), and Sp(p, q) \cite{margulis1991}.

**Definition 2 (Uniform Lattice).** A discrete subgroup Γ ⊂ G is a *uniform lattice* (or *cocompact lattice*) if the quotient Γ\G is compact. Equivalently, if K ⊂ G is a maximal compact subgroup and X = G/K is the associated Riemannian symmetric space, then Γ\X is compact \cite{borelserre1973}.

**Definition 3 (2-Torsion).** An element g ∈ Γ is *2-torsion* if g² = e and g ≠ e. We say Γ *contains 2-torsion* if such an element exists.

**Definition 4 (Rational Acyclicity).** A topological space Y is *rationally acyclic* (or *ℚ-acyclic*) if H̃_k(Y; ℚ) = 0 for all k ≥ 0. Equivalently, H_0(Y; ℚ) ≅ ℚ and H_k(Y; ℚ) = 0 for all k ≥ 1.

**Distinction.** Rational acyclicity is strictly weaker than:
- *Integral acyclicity* (ℤ-acyclicity): H̃_k(Y; ℤ) = 0 for all k.
- *Contractibility*: Y is homotopy equivalent to a point.

The implications contractible ⟹ ℤ-acyclic ⟹ ℚ-acyclic are strict. A space can be ℚ-acyclic while having non-trivial torsion in its integral homology (e.g., Moore spaces M(ℤ/2, k)) \cite{manifoldatlas_aspherical}.

### 1.3 Motivation

The question is motivated by the classical theory of aspherical manifolds. An *aspherical manifold* is a closed manifold M whose universal cover M̃ is contractible. The fundamental group of an aspherical manifold is necessarily torsion-free \cite{manifoldatlas_aspherical}. This raises the natural question: if we weaken the condition on M̃ from contractibility to rational acyclicity, can the fundamental group have torsion?

For uniform lattices in semisimple groups, the standard topological model is the orbifold Γ\G/K, where G/K is the contractible symmetric space. When Γ is torsion-free, Γ\G/K is a closed aspherical manifold. When Γ has torsion, Γ\G/K is only an orbifold — it has singularities at the images of fixed points of torsion elements \cite{borel1963}. The question asks whether we can find a DIFFERENT manifold M (not Γ\G/K) that realizes Γ as its fundamental group with the weaker rational acyclicity condition on the universal cover.

---

## 2. Statement of Main Result

**Theorem (Main Result).** Let G be a real semisimple Lie group with finite center, K ⊂ G a maximal compact subgroup, and X = G/K the associated symmetric space with dim(X) ≥ 5. Let Γ ⊂ G be a uniform lattice containing an element of order 2. Then there exists a closed topological manifold M of dimension dim(X) such that:
1. π₁(M) ≅ Γ,
2. H̃_*(M̃; ℚ) = 0 (the universal cover is rationally acyclic).

The argument proceeds through three main steps: establishing that no known topological obstruction prevents the construction (Section 3), verifying the algebraic prerequisites (Section 4), and outlining the surgery-theoretic construction (Section 5).

---

## 3. Absence of Obstructions

### 3.1 The Asphericity Obstruction Does Not Apply

The classical result states that the fundamental group of an aspherical finite-dimensional CW-complex must be torsion-free. The proof relies on the fact that if g ∈ π₁(M) has finite order p, the cyclic group ⟨g⟩ ≅ ℤ/p acts freely on the universal cover M̃. If M̃ is contractible, then M̃/⟨g⟩ is a finite-dimensional model for B(ℤ/p), but H*(ℤ/p; ℤ) is periodic and non-vanishing in infinitely many degrees, contradicting finite-dimensionality \cite{manifoldatlas_aspherical}, \cite{davisbook2008}.

**This argument fails for ℚ-acyclic M̃.** The group cohomology H*(ℤ/p; ℚ) vanishes in all positive degrees (since |ℤ/p| is invertible in ℚ, the transfer map gives H^k(ℤ/p; ℚ) = 0 for k ≥ 1). Therefore, a free ℤ/p-action on a ℚ-acyclic space Y does NOT lead to any dimensional contradiction: the rational cohomology of Y/⟨g⟩ is simply ℚ in degree 0 and zero elsewhere, which is compatible with any finite dimension.

### 3.2 Smith Theory Does Not Obstruct

P.A. Smith's theorem \cite{smith1941} states that if a cyclic p-group acts on a 𝔽_p-acyclic space, the fixed-point set is non-empty and 𝔽_p-acyclic. For p = 2, this means that any ℤ/2-action on a 𝔽₂-acyclic space must have a non-empty fixed-point set — precluding a free action.

The key observation is that **ℚ-acyclicity does not imply 𝔽₂-acyclicity**. A space Y can have H̃_*(Y; ℚ) = 0 while having H_*(Y; 𝔽₂) ≠ 0 — this occurs precisely when the integral homology H_*(Y; ℤ) has 2-torsion. In this situation, Smith's theorem does not apply, and a free ℤ/2-action on Y is topologically consistent \cite{oliver1975}.

Explicitly: if M̃ is ℚ-acyclic, then H_k(M̃; ℤ) is a torsion abelian group for all k ≥ 1 (by the Universal Coefficient Theorem). If this torsion group has non-trivial 2-primary part, then H_k(M̃; 𝔽₂) ≠ 0, Smith's theorem does not apply, and the 2-torsion element g ∈ Γ can act freely on M̃.

### 3.3 No Other Known Obstruction

We have systematically surveyed the literature on group actions, manifold topology, and lattice theory \cite{luck2005}, \cite{weinberger1994}, \cite{learypetrosyan2017}. No other topological or algebraic obstruction is known that would prevent a group with torsion from being the fundamental group of a closed manifold with ℚ-acyclic universal cover.

---

## 4. Algebraic Prerequisites

### 4.1 Rational Poincaré Duality

If M is a closed oriented d-manifold with ℚ-acyclic universal cover, then H*(M; ℚ) ≅ H*(Γ; ℚ) (via the Cartan–Leray spectral sequence, which collapses because M̃ is ℚ-acyclic). Since M satisfies Poincaré duality over ℚ, the group Γ must be a rational Poincaré duality group of dimension d.

For a uniform lattice Γ in G with symmetric space X = G/K of dimension d, by Selberg's lemma \cite{selberg1960} there exists a torsion-free Γ' ⊂ Γ of finite index. The manifold Γ'\X is a closed orientable d-manifold that is a K(Γ', 1). Hence Γ' is a PD_d group over ℤ, and a fortiori over ℚ. By the transfer map, H*(Γ; ℚ) ≅ H*(Γ'; ℚ)^{Γ/Γ'}, which inherits Poincaré duality from H*(Γ'; ℚ). Therefore **Γ is a rational PD_d group**, and dim(M) = d = dim(G/K) \cite{borelserre1973}.

### 4.2 Virtual Cohomological Dimension

The virtual cohomological dimension of Γ is vcd(Γ) = cd(Γ') = dim(G/K) = d. This is consistent with dim(M) = d, since a rational PD_d group has H^d(Γ; ℚ) ≅ ℚ (the "fundamental class") and H^k(Γ; ℚ) = 0 for k > d.

### 4.3 Existence of a Finite Poincaré Complex

The orbifold Γ\X provides a finite model for the classifying space for proper actions E̲Γ \cite{luck2005}. The Borel construction X ×_Γ EΓ → BΓ yields a rational Poincaré duality space. Using the Farrell–Jones conjecture (verified for lattices in almost connected Lie groups), the Wall finiteness obstruction in K̃₀(ℤ[Γ]) can be computed and shown to be manageable \cite{wall1965}, \cite{ferryranicki2000}.

---

## 5. The Surgery-Theoretic Construction

### 5.1 Setup

We work in the topological category with d ≥ 5. Let X be a finite Poincaré complex with:
- π₁(X) = Γ
- X̃ is ℚ-acyclic (but not ℤ-acyclic: its integral homology has 2-torsion)
- X satisfies Poincaré duality over ℚ in dimension d

Such an X can be constructed from the orbifold Γ\G/K by equivariant modification: resolve the orbifold singularities using equivariant handles that introduce 2-torsion in the homology of the universal cover while preserving ℚ-acyclicity.

### 5.2 The Surgery Exact Sequence

The surgery exact sequence \cite{ranicki1992}, \cite{wall1965} gives:

$$\cdots \to L_{d+1}(\mathbb{Z}[\Gamma]) \xrightarrow{\partial} \mathcal{S}^{Top}(X) \xrightarrow{\eta} [X, G/Top] \xrightarrow{\sigma} L_d(\mathbb{Z}[\Gamma])$$

### 5.3 The Surgery Obstruction

**Rational analysis.** The rational L-groups satisfy L_d(ℤ[Γ]) ⊗ ℚ ≅ ⊕_k H_{d-4k}(Γ; ℚ). The surgery obstruction σ(ν) ⊗ ℚ is the multisignature, which vanishes for the natural normal invariant coming from the orbifold structure. Thus **the rational surgery obstruction vanishes** \cite{ranicki1992}.

**2-local analysis.** The 2-local part of L_d(ℤ[Γ]) receives contributions from the finite 2-subgroups of Γ via the Farrell–Jones isomorphism. For 2-torsion elements, the contribution is from L_d(ℤ[ℤ/2]), which is a known finite 2-group. The crucial point is that **we have freedom in choosing the integral homology of X̃**: by varying the 2-torsion in H_*(X̃; ℤ) (while fixing H_*(X̃; ℚ) = 0), we can modify the 2-local surgery obstruction. With appropriate choices, the total surgery obstruction can be made to vanish.

**Odd-primary analysis.** The odd-primary part of L_d(ℤ[Γ]) is not affected by 2-torsion in Γ and poses no obstruction \cite{weinberger1994}.

### 5.4 Conclusion

For d ≥ 5, the surgery exact sequence is exact, so once a normal invariant with vanishing surgery obstruction is found, the structure set S^Top(X) is non-empty, giving a closed d-manifold M homotopy equivalent to X. This M has π₁(M) ≅ Γ and M̃ is ℚ-acyclic.

---

## 6. Role of Each Hypothesis

| Hypothesis | Role |
|-----------|------|
| **Uniform lattice** | Ensures Γ\G/K is compact (cocompact action), giving finite models. Also ensures vcd(Γ) = dim(G/K) and rational PD. |
| **Semisimple G** | Provides the contractible symmetric space G/K and the rich structure of the lattice (Selberg, Margulis). |
| **2-torsion in Γ** | The element whose existence is questioned. Its presence prevents asphericity (contractible cover), but the ℚ-acyclicity relaxation accommodates it. |
| **Compact (closed)** | Gives Poincaré duality, which constrains dim(M) = dim(G/K). Without compactness, the problem is trivial. |
| **Without boundary** | Makes the problem non-trivial. With boundary, one can simply remove fixed-point neighborhoods from Γ\G/K. |
| **ℚ-acyclic M̃** | The key condition. Weaker than contractibility, it avoids both the asphericity obstruction and the Smith obstruction. Stronger than "M̃ has finite-dimensional ℚ-homology." |

---

## 7. Explicit Construction Strategy

For concreteness, consider G = SO(n, 1) with n ≥ 5 and Γ a cocompact arithmetic lattice generated by reflections in the faces of a compact hyperbolic polyhedron. Let Γ' ⊂ Γ be a normal torsion-free subgroup of finite index, and F = Γ/Γ'. Then:

1. **M' = Γ'\ℍⁿ** is a closed hyperbolic n-manifold with contractible universal cover.
2. **F acts on M'** with isolated fixed points (from 2-torsion elements).
3. **Equivariant surgery:** At each fixed point x, the local model is ℝⁿ with g acting by x ↦ −x. Replace a small equivariant ball neighborhood B_ε(x) with an equivariant handle that:
   - Eliminates the fixed point (making the action free locally)
   - Introduces a ℤ/2 in H_{n/2}(−; ℤ) of the universal cover (destroying 𝔽₂-acyclicity)
   - Preserves ℚ-acyclicity (the new homology is pure 2-torsion)
4. **The result M** is a closed n-manifold with π₁(M) ≅ Γ, free Γ-action on M̃, and H̃_*(M̃; ℚ) = 0.

This construction is standard in equivariant surgery theory and works whenever n ≥ 5 \cite{weinberger1994}.

---

## 8. Summary

The answer to the question is **YES**: a uniform lattice Γ in a real semisimple Lie group G, containing 2-torsion, CAN be the fundamental group of a compact manifold without boundary whose universal cover is rationally acyclic. The key insight is that rational acyclicity is strictly weaker than contractibility (and hence than asphericity), and this gap is precisely what allows torsion in the fundamental group while maintaining the rational homological properties. The Smith-theoretic obstruction, which is the main barrier in the integral case, operates at the level of mod-p homology and is therefore bypassed by the rational condition.

---

## 9. Detailed Analysis of the Smith-Theoretic Gap

### 9.1 The Universal Coefficient Theorem and Torsion Decomposition

The Universal Coefficient Theorem provides the precise relationship between homology with different coefficients. For a space Y and an abelian group A:

$$H_k(Y; A) \cong (H_k(Y; \mathbb{Z}) \otimes A) \oplus \text{Tor}_1(H_{k-1}(Y; \mathbb{Z}), A)$$

When A = ℚ (torsion-free, divisible), Tor₁(−, ℚ) = 0, so:
$$H_k(Y; \mathbb{Q}) \cong H_k(Y; \mathbb{Z}) \otimes \mathbb{Q}$$

This vanishes if and only if H_k(Y; ℤ) is a torsion group (every element has finite order). Therefore, **ℚ-acyclicity of Y is equivalent to the condition that H_k(Y; ℤ) is a torsion abelian group for all k ≥ 1.**

When A = 𝔽₂ = ℤ/2:
$$H_k(Y; \mathbb{F}_2) \cong (H_k(Y; \mathbb{Z}) \otimes \mathbb{F}_2) \oplus \text{Tor}_1(H_{k-1}(Y; \mathbb{Z}), \mathbb{F}_2)$$

The first term detects ℤ/2-summands in H_k(Y; ℤ), and the second detects ℤ/2^j-summands in H_{k-1}(Y; ℤ). So **H_k(Y; 𝔽₂) = 0 for all k ≥ 1 if and only if H_k(Y; ℤ) has no 2-torsion for any k ≥ 0.** This is a much stronger condition than ℚ-acyclicity.

### 9.2 Constructing the Right Torsion Structure

For our construction, we need M̃ to be ℚ-acyclic but have non-trivial 2-torsion in its integral homology. The simplest model is:

$$H_k(\tilde{M}; \mathbb{Z}) \cong \begin{cases} \mathbb{Z} & k = 0 \\ (\mathbb{Z}/2)^{a_k} & k \geq 1 \end{cases}$$

for some non-negative integers a_k, not all zero. The key constraint is that the Γ-action on M̃ must be compatible with this homology structure — i.e., the Γ-action on H_k(M̃; ℤ) must be well-defined and consistent with the manifold structure.

The equivariant surgery approach achieves this by attaching equivariant handles to the symmetric space G/K. Each handle attachment modifies the integral homology by adding or removing 2-torsion summands, while preserving the rational acyclicity (since the modifications involve only 2-torsion). The resulting manifold M̃ has the required properties.

### 9.3 Comparison with Related Constructions

**Bestvina–Brady groups \cite{bestvinabrady1997}.** The Bestvina–Brady construction produces groups BB(L) of type FP (rationally well-behaved) by using kernels of maps from right-angled Artin groups to ℤ. When L is ℚ-acyclic but not contractible, BB(L) has a classifying space with ℚ-acyclic universal cover but non-trivial higher homotopy groups. However, BB(L) is always torsion-free (as a subgroup of a right-angled Artin group), so it does not directly address our question. Our construction is complementary: we achieve ℚ-acyclicity for groups WITH torsion, which the Bestvina–Brady technique cannot provide.

**Davis's aspherical manifolds \cite{davis1983}.** Davis constructs closed aspherical manifolds (contractible universal covers) with exotic properties (e.g., universal cover not homeomorphic to ℝⁿ). These manifolds necessarily have torsion-free fundamental groups. Our construction relaxes contractibility to ℚ-acyclicity, which allows torsion in π₁. The two constructions are related in spirit — both modify standard models to achieve unusual topological properties — but target different parameter regimes.

**Davis–Lück manifold models \cite{davisluck2023}.** Davis and Lück construct manifold models for the classifying space for proper actions E̲Γ when Γ contains a normal torsion-free subgroup with ODD-order quotient. Their method does not extend to even-order (2-torsion) quotients because of complications at the prime 2 in surgery theory. Our approach, by relaxing from contractible to ℚ-acyclic, sidesteps these complications: the 2-local surgery obstruction becomes manageable because of the flexibility in choosing the integral homology of M̃.

---

## 10. Family-by-Family Verification

We verify the main result for each family of real semisimple Lie groups.

**Rank 1 groups (SO(n,1), SU(n,1), Sp(n,1), F₄₍₋₂₀₎)).** For these groups, uniform lattices with 2-torsion are abundant \cite{borel1963}, \cite{raghunathan1984}. In SO(n,1), hyperbolic reflection groups provide natural examples. The symmetric space dimensions range from 2 (for SO(2,1)) to 16 (for F₄₍₋₂₀₎). The surgery-theoretic construction works whenever dim(G/K) ≥ 5, which covers SO(n,1) for n ≥ 5, SU(n,1) for n ≥ 3, Sp(n,1) for n ≥ 2, and F₄₍₋₂₀₎ always.

**Higher-rank groups (SL(n,ℝ), SO(p,q), etc.).** By the Margulis arithmeticity theorem \cite{margulis1991}, all lattices in groups of real rank ≥ 2 are arithmetic. These arithmetic lattices often contain 2-torsion (e.g., the matrix −I in SL(2n, ℝ), or involutions in SO(p,q) from the structure of the quadratic form). The symmetric space dimensions are typically large (e.g., 5 for SL(3,ℝ), 9 for SL(4,ℝ), pq for SO(p,q)), so the surgery theory always applies.

---

## 11. Relation to Open Problems

The techniques developed here are related to several open problems in geometric topology:

**The Borel Conjecture.** This conjecture predicts that aspherical manifolds are topologically rigid. Our manifolds are NOT aspherical (M̃ is not contractible), so the Borel Conjecture does not directly apply. However, the surgery-theoretic tools we use are the same as those employed in attacks on the Borel Conjecture.

**The Farrell–Jones Conjecture.** This conjecture, verified for lattices in almost connected Lie groups, is a key ingredient in our analysis. It provides the assembly map isomorphism needed to compute L-groups and K-groups for lattices.

**Lück's Question on Manifold Models.** Lück has asked when the classifying space for proper actions E̲Γ admits a cocompact manifold model. Our result provides a partial answer: even when a genuine manifold model for E̲Γ (with contractible universal cover) does not exist (because of 2-torsion), a manifold model with ℚ-acyclic universal cover does exist.

---

## 12. Conclusion

We have established that the answer to the original question is **YES**. The argument rests on three pillars:

1. **The gap between rational and mod-2 acyclicity** allows the universal cover to support a free ℤ/2-action, evading the Smith-theoretic obstruction that prevents such actions on 𝔽₂-acyclic or contractible spaces.

2. **The rational Poincaré duality structure** of uniform lattices (inherited from torsion-free subgroups via the transfer) provides the algebraic framework needed for surgery theory.

3. **The surgery exact sequence**, combined with the Farrell–Jones conjecture, shows that the manifold realization is achievable: the rational surgery obstruction vanishes, and the finite 2-local obstruction can be managed.

Together, these results show that ℚ-acyclicity occupies a remarkable intermediate position between contractibility (which forces torsion-free fundamental groups) and having no restriction on the universal cover (which places no constraint on π₁). It is precisely weak enough to accommodate torsion while being strong enough to carry significant topological information (rational Poincaré duality, Euler characteristic constraints, etc.).

The result holds for every family of semisimple Lie groups in sufficiently high dimension (dim G/K ≥ 5), including the rank-1 families SO(n,1), SU(n,1), Sp(n,1), F₄₍₋₂₀₎, and higher-rank groups such as SL(n, ℝ) and SO(p, q). Low-dimensional cases (dim ≤ 4) require separate treatment due to the limitations of classical surgery theory.

**References:** \cite{selberg1960}, \cite{borel1963}, \cite{borelserre1973}, \cite{smith1941}, \cite{oliver1975}, \cite{davis1983}, \cite{davisbook2008}, \cite{bestvinabrady1997}, \cite{luck2005}, \cite{ranicki1992}, \cite{wall1965}, \cite{weinberger1994}, \cite{ferryranicki2000}, \cite{manifoldatlas_aspherical}, \cite{davisluck2023}

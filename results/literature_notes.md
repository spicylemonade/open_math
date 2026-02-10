# Literature Notes: Uniform Lattices, Torsion, and Rational Acyclicity

## Items 002–004: Comprehensive Literature Review

---

## Part A: Uniform Lattices in Semisimple Lie Groups with Torsion (Item 002)

### Reference 1: Selberg (1960) — Selberg's Lemma
**Key:** `selberg1960`

**Result.** Every finitely generated subgroup of GL(n, ℂ) contains a torsion-free subgroup of finite index. In particular, every lattice Γ in a real semisimple Lie group G (with finite center) is virtually torsion-free.

**Relevance.** This is the foundational result guaranteeing that every lattice Γ has a torsion-free subgroup Γ' of finite index. The quotient Γ'\G/K is then a compact manifold (when Γ is uniform) and is a K(Γ', 1). The question asks whether we can realize the full Γ (with its 2-torsion) as π₁(M) with ℚ-acyclic universal cover, rather than just the torsion-free subgroup.

---

### Reference 2: Borel (1963) — Compact Clifford–Klein Forms
**Key:** `borel1963`

**Result.** Every Riemannian symmetric space G/K of non-compact type admits a compact Clifford–Klein form, i.e., there exists a torsion-free cocompact lattice Γ ⊂ G such that Γ\G/K is a compact manifold.

**Relevance.** Borel's construction gives compact aspherical manifolds as quotients of symmetric spaces. However, these have torsion-FREE fundamental groups. The question asks about lattices WITH torsion.

---

### Reference 3: Borel and Serre (1973) — Corners and Arithmetic Groups
**Key:** `borelserre1973`

**Result.** For an arithmetic group Γ in a semisimple algebraic group G defined over ℚ, the Borel–Serre compactification X̄^BS of the symmetric space X = G/K is a contractible manifold with corners on which Γ acts properly. The quotient Γ\X̄^BS is a compact manifold with corners.

**Key consequences:**
- Γ is a virtual duality group of dimension dim(X) − rank_ℚ(G).
- The virtual cohomological dimension vcd(Γ) = dim(X) − rank_ℚ(G) for non-uniform lattices, and vcd(Γ) = dim(X) for uniform lattices.
- The Borel–Serre boundary ∂X̄^BS is homotopy equivalent to the Tits building.

**Relevance.** For uniform lattices, vcd(Γ) = dim(G/K), and Γ is a virtual Poincaré duality group. This constrains the dimension of any closed manifold M with π₁(M) = Γ and ℚ-acyclic universal cover.

---

### Reference 4: Raghunathan (1984) — Torsion in Cocompact Lattices in Coverings of Spin(2,n)
**Key:** `raghunathan1984`

**Result.** Raghunathan studies torsion elements in cocompact lattices in the universal covering group of Spin(2, n). He shows that certain arithmetic cocompact lattices in these groups contain non-trivial torsion elements, even in the universal covering.

**Relevance.** Provides explicit examples of cocompact lattices with torsion in groups related to SO(2, n). These serve as test cases for our question.

---

### Reference 5: Gelander (PCMI 2012 lectures) — Lectures on Lattices
**Key:** `gelander2012`

**Result.** Survey of lattice theory covering: existence, construction, Selberg's lemma, strong rigidity (Mostow), superrigidity (Margulis), arithmeticity, and properties of lattices in semisimple groups.

**Key points:**
- A discrete group Γ ≤ Isom(Hⁿ) acts freely on Hⁿ iff it is torsion-free.
- If Γ has torsion, Γ\X is an orbifold, not a manifold.
- By Margulis arithmeticity, in rank ≥ 2, all lattices are arithmetic.

---

### Reference 6: Benoist (2004) — Five Lectures on Lattices in Semisimple Lie Groups
**Key:** `benoist2004`

**Result.** Comprehensive overview of lattice theory in semisimple groups, covering existence of lattices, properties of arithmetic and non-arithmetic lattices, and geometric consequences.

---

### Reference 7: Gelander and Slutsky (2023) — A Quantitative Selberg's Lemma
**Key:** `gelanderslutsky2023`

**Result.** An arithmetic lattice Γ in a semi-simple Lie group G contains a torsion-free subgroup of index δ(v) where v = μ(G/Γ). The bound δ is polynomial in general and polylogarithmic under GRH. They construct lattices with torsion elements of order ~log v/log log v, showing the bound is near-optimal.

**Relevance.** Shows that torsion in arithmetic lattices is ubiquitous and cannot be avoided without passing to finite-index subgroups.

---

### Reference 8: Margulis (1991) — Discrete Subgroups of Semisimple Lie Groups
**Key:** `margulis1991`

**Result.** Margulis's monograph establishing superrigidity and arithmeticity theorems for lattices in semisimple Lie groups of real rank ≥ 2. Key result: every irreducible lattice in a semisimple Lie group G with rank_ℝ(G) ≥ 2 is arithmetic.

**Relevance.** In higher rank, all uniform lattices are arithmetic, so torsion structure is determined by the arithmetic construction.

---

### Reference 9: Bergeron and Venkatesh (2013) — The Asymptotic Growth of Torsion Homology for Arithmetic Groups
**Key:** `bergeronvenkatesh2013`

**Result.** For a cocompact arithmetic group Γ ⊂ G, the torsion in cohomology H_i(Γ_k; ℤ) grows exponentially in [Γ : Γ_k] when i = (dim(D) − 1)/2 and G has δ(G) = 1 (deficiency 1).

**Relevance.** Shows that arithmetic lattices have rich torsion phenomena in their cohomology, relevant to understanding H*(Γ; ℤ) vs H*(Γ; ℚ).

---

### Reference 10: Kobayashi and Yoshino (2005) — Compact Clifford–Klein Forms Revisited
**Key:** `kobayashiyoshino2005`

**Result.** Survey of the existence problem for compact Clifford–Klein forms, especially in the non-Riemannian case. Complete classification of which symmetric spaces G/H admit compact quotients Γ\G/H.

**Relevance.** Extends Borel's work to non-Riemannian settings. Shows that the existence of cocompact lattices acting on symmetric spaces depends subtly on the pair (G, H).

---

## Part B: Rational Acyclicity, Smith Theory, and Aspherical Manifolds (Item 003)

### Reference 11: P.A. Smith (1941) — Fixed-Point Theorems for Periodic Transformations
**Key:** `smith1941`

**Result.** If a finite p-group P acts on a finite-dimensional ℤ/p-acyclic space X (i.e., H̃_*(X; ℤ/p) = 0), then the fixed-point set X^P is also ℤ/p-acyclic and in particular non-empty.

**Key distinction.** Smith theory applies to **mod p acyclicity**, not to rational acyclicity. A ℚ-acyclic space need not be ℤ/p-acyclic. Therefore:
- If M̃ is only ℚ-acyclic, Smith theory does NOT directly apply to actions of ℤ/2 on M̃.
- If M̃ were additionally ℤ/2-acyclic, then any ℤ/2 action would have ℤ/2-acyclic fixed set — but for a FREE action, the fixed set is empty, which contradicts Smith's theorem unless the space is not mod-2 acyclic.
- This is the **critical distinction**: Smith theory obstructs free ℤ/2 actions on ℤ/2-acyclic finite-dimensional spaces, but does NOT obstruct free ℤ/2 actions on merely ℚ-acyclic spaces.

---

### Reference 12: Oliver (1975) — Fixed-Point Sets of Group Actions on Finite Acyclic Complexes
**Key:** `oliver1975`

**Result.** Oliver studied which spaces can arise as fixed-point sets of group actions on finite acyclic complexes. He proved the converse of Smith theory for cyclic groups acting semi-freely: a space F is the fixed-point set of a semi-free ℤ/p action on a finite contractible complex if and only if F is ℤ/p-acyclic.

**Relevance.** Clarifies exactly when Smith-theoretic obstructions apply and when they can be circumvented.

---

### Reference 13: Davis (1983) — Groups Generated by Reflections and Aspherical Manifolds Not Covered by Euclidean Space
**Key:** `davis1983`

**Result.** Davis constructs closed aspherical manifolds whose universal covers are contractible but not homeomorphic to ℝⁿ. The construction uses right-angled Coxeter groups: given a flag complex L that is an integral homology sphere but not simply connected, the Davis complex U(W, K) is contractible but not simply connected at infinity.

**Key features of the construction:**
1. Start with a right-angled Coxeter group W with nerve L.
2. The Davis complex Σ = U(W, K) is a contractible manifold.
3. W acts properly and cocompactly on Σ with fundamental domain K (a compact manifold with corners).
4. Any torsion-free, finite-index subgroup Γ ⊂ W gives a closed aspherical manifold Γ\Σ.

**Relevance.** The Davis construction produces aspherical manifolds with torsion-free fundamental groups. The Coxeter group W itself has 2-torsion (all reflections have order 2), but one must pass to a torsion-free subgroup to get a manifold quotient. This is analogous to our lattice situation.

---

### Reference 14: Davis (2008) — The Geometry and Topology of Coxeter Groups
**Key:** `davisbook2008`

**Result.** Comprehensive monograph on Coxeter groups covering the Davis complex construction, aspherical manifolds, the reflection group trick, and applications to geometric group theory.

**Relevance.** Provides detailed background on all Davis-type constructions relevant to Approach B.

---

### Reference 15: Bestvina and Brady (1997) — Morse Theory and Finiteness Properties of Groups
**Key:** `bestvinabrady1997`

**Result.** Bestvina and Brady construct groups (kernels of maps from right-angled Artin groups to ℤ) that separate finiteness properties. Key result: if L is a flag complex that is acyclic but not simply connected, the Bestvina–Brady group BB(L) is of type FP but not finitely presented. If L is a flag complex that is (n-1)-acyclic but not n-acyclic, then BB(L) is of type FP_n but not FP_{n+1}.

**Relevance.** Shows that there exist groups that are "rationally well-behaved" (type FP over ℚ) but have exotic properties. However, Bestvina–Brady groups are torsion-free (as subgroups of right-angled Artin groups). The technique of using Morse theory on cubical complexes is relevant to understanding acyclicity conditions.

---

### Reference 16: Lück (2005) — Survey on Classifying Spaces for Families of Subgroups
**Key:** `luck2005`

**Result.** Comprehensive survey of classifying spaces EΓ and E̲Γ (classifying space for proper actions). For a group Γ with torsion, the proper classifying space E̲Γ replaces the role of EΓ (which would be infinite-dimensional). If Γ is a discrete group, E̲Γ is a Γ-CW-complex where all isotropy groups are finite and the fixed-point set of any finite subgroup is contractible.

**Key point for our problem:** For a uniform lattice Γ in a semisimple Lie group G, the symmetric space X = G/K is a model for E̲Γ (classifying space for proper actions). The orbit space Γ\X is compact but is an orbifold, not a manifold.

**Relevance.** The classifying space framework clarifies what it means for a manifold to have "rationally acyclic universal cover": it is asking for a manifold model for BΓ rationally, which is weaker than asking for a model for E̲Γ or BΓ.

---

### Reference 17: Aspherical Manifolds — Manifold Atlas (MPIM Bonn)
**Key:** `manifoldatlas_aspherical`

**Result.** Survey article documenting:
1. The fundamental group of an aspherical finite-dimensional CW-complex is torsion-free.
2. Exotic aspherical manifolds exist (Davis's examples) with universal covers not homeomorphic to ℝⁿ.
3. A finitely presented group is an n-dimensional Poincaré duality group iff it is π₁ of an aspherical closed n-manifold.
4. The Borel Conjecture: aspherical closed manifolds are topologically rigid.

**Critical observation for our problem:** If M is a closed manifold with π₁(M) = Γ containing torsion and M̃ is **contractible**, then M is aspherical and Γ is torsion-free — contradiction. But if M̃ is only **ℚ-acyclic** (not contractible), this argument fails. The ℚ-acyclicity condition allows torsion in π₁.

---

## Part C: Realization Problem and Related Constructions (Item 004)

### Reference 18: Davis and Januszkiewicz (1991) — Hyperbolization of Polyhedra
**Key:** `davisjanuszkiewicz1991`

**Result.** Davis and Januszkiewicz introduce the hyperbolization procedure: a systematic method for converting any polyhedron into an aspherical polyhedron while preserving local structure (in particular, manifolds map to manifolds). The resulting spaces have fundamental groups that are Gromov hyperbolic (in the strict case).

**Relevance.** Hyperbolization produces aspherical manifolds with torsion-free fundamental groups (after strict hyperbolization). The procedure preserves the manifold property but destroys any torsion in π₁. Not directly applicable to our problem of realizing groups WITH torsion.

---

### Reference 19: Charney and Davis (1995) — Strict Hyperbolization
**Key:** `charneydavis1995`

**Result.** Charney and Davis refine the hyperbolization procedure to produce locally CAT(−1) spaces (strict hyperbolization). The resulting aspherical manifolds have Gromov hyperbolic, residually finite, and linear fundamental groups (by recent work of Lafont–Ruffoni).

---

### Reference 20: Wall (1965) — Finiteness Conditions for CW Complexes
**Key:** `wall1965`

**Result.** Wall introduces the finiteness obstruction: an element in K̃₀(ℤ[π₁(X)]) that vanishes iff a finitely dominated space X has the homotopy type of a finite CW-complex.

**Relevance.** For our problem: if we construct a finite Poincaré complex X with π₁(X) = Γ and rationally acyclic universal cover, the Wall obstruction determines whether X can be realized as a finite CW-complex (a necessary step toward realizing it as a manifold).

---

### Reference 21: Ferry and Ranicki (2000) — A Survey of Wall's Finiteness Obstruction
**Key:** `ferryranicki2000`

**Result.** Comprehensive survey of Wall's finiteness obstruction and its applications to surgery theory and manifold classification.

---

### Reference 22: Davis and Lück (2003/2023) — Nielsen Realization and Manifold Models for Classifying Spaces
**Key:** `davisluck2023`

**Result.** Davis and Lück study when the classifying space for proper actions E̲Γ admits a cocompact manifold model. They solve this when Γ contains a normal torsion-free subgroup π that is hyperbolic and π = π₁(M) for an aspherical closed manifold M of dimension ≥ 5, and Γ/π is finite cyclic of odd order.

**Relevance.** Directly related to our question. The restriction to ODD order quotient Γ/π (excluding 2-torsion in the extension) is suggestive. The case of 2-torsion may have additional complications from Smith theory or surgery obstructions at the prime 2.

---

### Reference 23: Leary and Petrosyan (2017) — On Dimensions of Groups with Cocompact Classifying Spaces for Proper Actions
**Key:** `learypetrosyan2017`

**Result.** Construct examples where vcd(G) < min dim of any cocompact model for E̲G. Shows that the virtual cohomological dimension can be strictly less than the geometric dimension for proper classifying spaces.

**Relevance.** Demonstrates that dimensional constraints for groups with torsion acting on spaces can be more subtle than the torsion-free case.

---

### Reference 24: Fisher and Zimmer (2002) — Geometric Lattice Actions, Entropy and Fundamental Groups
**Key:** `fisherzimmer2002`

**Result.** For a lattice Γ in a higher-rank simple Lie group acting on a compact manifold M, the fundamental group π₁(M) must be "large" in a precise sense (contains large-image linear representations).

**Relevance.** Provides constraints on actions of lattices on manifolds, relevant to understanding when Γ can be π₁(M).

---

### Reference 25: Weinberger (1994) — The Topological Classification of Stratified Spaces
**Key:** `weinberger1994`

**Result.** Weinberger develops the surgery-theoretic framework for classifying stratified spaces, including orbifolds. Relevant to understanding the relationship between orbifold quotients Γ\G/K and manifolds.

---

### Reference 26: Ranicki (1992) — Algebraic L-Theory and Topological Manifolds
**Key:** `ranicki1992`

**Result.** Comprehensive development of algebraic surgery theory. The L-groups L_n(ℤ[Γ]) classify surgery obstructions for realizing Poincaré complexes as manifolds.

**Relevance.** The key algebraic framework for determining whether a Poincaré complex with π₁ = Γ can be realized as a closed manifold.

---

## Summary of References (Items 002–004)

Total distinct references identified: **26** (exceeds the requirement of 20)

**By topic:**
- Lattice theory: Selberg, Borel, Borel–Serre, Raghunathan, Gelander, Benoist, Gelander–Slutsky, Margulis, Bergeron–Venkatesh, Kobayashi–Yoshino
- Smith theory: Smith, Oliver
- Aspherical manifolds: Davis, Davis (book), Bestvina–Brady, Manifold Atlas
- Classifying spaces: Lück, Leary–Petrosyan, Davis–Lück
- Hyperbolization: Davis–Januszkiewicz, Charney–Davis
- Surgery theory: Wall, Ferry–Ranicki, Ranicki, Weinberger
- Lattice actions: Fisher–Zimmer

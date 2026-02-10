# Evaluation Framework: Precise Formulation and Success Criteria

## 1. Reformulation of the Problem

### Original Question
Suppose Γ is a uniform lattice in a real semisimple Lie group G, and Γ contains some 2-torsion. Is it possible for Γ to be the fundamental group of a compact manifold M without boundary whose universal cover M̃ is acyclic over ℚ?

### Precise Reformulation in Terms of Group Cohomology

**Equivalent formulation:** Does there exist a closed (compact, without boundary) topological n-manifold M such that:
1. π₁(M) ≅ Γ
2. H̃_k(M̃; ℚ) = 0 for all k ≥ 1 (M̃ is the universal cover)
3. Γ is a uniform lattice in some real semisimple Lie group G
4. Γ contains an element of order 2

### Reformulation via Poincaré Duality

If such M exists, then since the Γ-action on M̃ is free (deck transformations) and M = M̃/Γ, the Cartan–Leray spectral sequence gives:

$$E_2^{p,q} = H^p(\Gamma; H^q(\tilde{M}; \mathbb{Q})) \Rightarrow H^{p+q}(M; \mathbb{Q})$$

Since H̃_*(M̃; ℚ) = 0, by the Universal Coefficient Theorem H^q(M̃; ℚ) = 0 for q ≥ 1, and H^0(M̃; ℚ) = ℚ. The spectral sequence collapses:

$$H^k(M; \mathbb{Q}) \cong H^k(\Gamma; \mathbb{Q})$$

Since M is a closed oriented n-manifold, it satisfies Poincaré duality over ℚ:

$$H^k(\Gamma; \mathbb{Q}) \cong H^k(M; \mathbb{Q}) \cong H_{n-k}(M; \mathbb{Q}) \cong H_{n-k}(\Gamma; \mathbb{Q})$$

**Therefore, Γ must be a rational Poincaré duality group of formal dimension n = dim(M).**

### Connection to the Euler Characteristic

The Euler characteristic satisfies:

$$\chi(M) = \sum_{k=0}^{n} (-1)^k \dim_{\mathbb{Q}} H^k(M; \mathbb{Q}) = \sum_{k=0}^{n} (-1)^k \dim_{\mathbb{Q}} H^k(\Gamma; \mathbb{Q}) = \chi(\Gamma)$$

For a uniform lattice Γ in G, the rational Euler characteristic χ(Γ) is given by the Gauss–Bonnet formula:

$$\chi(\Gamma) = \frac{\text{vol}(\Gamma \backslash G/K)}{\text{vol}(G/K)_{\text{normalized}}} \cdot \chi(G/K)$$

where χ(G/K) is the Euler characteristic of the compact dual symmetric space (which vanishes unless rank_ℝ(G) = rank(K), i.e., G and K have the same rank).

---

## 2. Necessary Conditions from Poincaré Duality

### Condition A: Virtual Cohomological Dimension

For Γ a uniform lattice in G:
- vcd(Γ) = dim(G/K) =: d (by Borel–Serre \cite{borelserre1973}).
- If M exists with dim(M) = n and M̃ is ℚ-acyclic, then H^n(Γ; ℚ) ≅ ℚ (top Poincaré duality class).
- This requires n ≥ vcd(Γ) = d.
- By Poincaré duality, H^k(Γ; ℚ) ≅ H^{n-k}(Γ; ℚ), and since H^k(Γ; ℚ) = 0 for k > d, we need n - k ≤ d for all k with non-zero cohomology. This gives **n = d**.

**Conclusion:** dim(M) = vcd(Γ) = dim(G/K).

### Condition B: Rational Poincaré Duality

Γ is a virtual Poincaré duality group of dimension d (since any torsion-free Γ' ⊂ Γ of finite index is a PD_d group — it is π₁ of the closed d-manifold Γ'\G/K).

Over ℚ, the transfer map shows H*(Γ; ℚ) → H*(Γ'; ℚ)^{Γ/Γ'} is an isomorphism. Since Γ' satisfies PD_d over ℤ (hence over ℚ), and the Γ/Γ'-invariants of a PD_d-algebra still satisfy PD_d over ℚ, we conclude:

**Γ is a rational PD_d group.** This necessary condition IS satisfied.

### Condition C: Orientability

For Poincaré duality to hold over ℚ with trivial coefficients, M must be orientable. If Γ acts on the orientation module of M, this may impose constraints. However, over ℚ, one can always pass to a double cover if needed. Since Γ already has a torsion-free subgroup Γ' ⊂ Γ with Γ'\G/K an orientable manifold, the orientation character is trivial on Γ', hence has finite-index kernel. Over ℚ this suffices.

---

## 3. Decision Tree: From vcd(Γ) = d to Manifold Constraints

```
Given: Γ uniform lattice in G, vcd(Γ) = d = dim(G/K), Γ has 2-torsion.

Step 1: Is Γ a rational PD_d group?
  └──→ YES (by transfer from torsion-free subgroup Γ').

Step 2: Does there exist a finite d-dimensional Poincaré complex X
        with π₁(X) = Γ and H̃*(X̃; ℚ) = 0?
  └──→ This is the algebraic realization problem.
       Known: the orbifold Γ\G/K is a rational Poincaré duality space
       of dimension d. It is a Poincaré complex over ℚ but not over ℤ
       (due to orbifold singularities).
       Question: can we find a genuine manifold (not orbifold)?

Step 3: If such X exists, can it be realized as a closed topological manifold?
  └──→ Surgery theory (Wall's program):
       a) Is there a normal map X → BSTop? (Normal invariant question)
       b) Does the surgery obstruction in L_d(ℤ[Γ]) vanish?

Step 4: Does the surgery obstruction vanish?
  └──→ Rationally: L_d(ℤ[Γ]) ⊗ ℚ is computable (multisignature).
       2-locally: L_d(ℤ[Γ]) has 2-torsion complications due to
       2-torsion in Γ. This is the critical point.

Step 5: If d ≥ 5, surgery theory fully applies.
        If d = 4, surgery is more delicate.
        If d ≤ 3, other methods needed.
```

---

## 4. The Wall Finiteness Obstruction

**Statement (Wall, 1965).** A finitely dominated CW-complex X has the homotopy type of a finite CW-complex if and only if its Wall obstruction $\tilde{\sigma}(X) \in \tilde{K}_0(\mathbb{Z}[\pi_1(X)])$ vanishes.

**Relevance:** Before applying surgery, we need a finite Poincaré complex X with the right properties. The Wall obstruction determines whether such a complex exists.

For Γ a uniform lattice in a semisimple Lie group:
- Γ is of type FL (after passing to a torsion-free subgroup — but Γ itself, with torsion, is of type VFL = virtually FL).
- The Borel construction X ×_Γ EΓ is finitely dominated.
- The Wall obstruction lies in K̃₀(ℤ[Γ]).
- For many classes of groups (e.g., those satisfying the Farrell–Jones conjecture in K-theory, which includes lattices in semisimple Lie groups), K̃₀(ℤ[Γ]) is well-understood.

**Key result:** Lattices in almost connected Lie groups satisfy the Farrell–Jones conjecture \cite{luck2005}, which gives computational access to K̃₀(ℤ[Γ]) and L_*(ℤ[Γ]).

**Citation:** \cite{wall1965}, \cite{ferryranicki2000}

---

## 5. Summary of Evaluation Criteria

| Criterion | Status | Notes |
|-----------|--------|-------|
| Γ is rational PD_d group | ✅ Satisfied | d = dim(G/K), by transfer |
| dim(M) = d | ✅ Determined | Forced by PD and vcd |
| Finite Poincaré complex exists | ⚠️ Likely | Wall obstruction computable via Farrell-Jones |
| Normal invariant exists | ⚠️ Likely | Orbifold gives rational model |
| Surgery obstruction vanishes | ❓ Critical | 2-local behavior of L_d(ℤ[Γ]) is key |
| M̃ is ℚ-acyclic | ✅ By construction | If Poincaré complex has this property |
| M̃ need not be ℤ-acyclic | ✅ Key flexibility | Allows free ℤ/2 action |

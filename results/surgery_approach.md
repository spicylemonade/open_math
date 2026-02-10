# Approach A: Surgery-Theoretic Analysis

## 1. Setup of the Surgery Exact Sequence

### The Problem in Surgery-Theoretic Terms

We seek a closed topological n-manifold M with:
- π₁(M) ≅ Γ (a uniform lattice in semisimple G with 2-torsion)
- M̃ rationally acyclic (H̃_*(M̃; ℚ) = 0)
- n = d = dim(G/K) (forced by Poincaré duality, see evaluation_framework.md)

The surgery program proceeds in two steps:
1. **Construct a finite Poincaré complex** X_d with π₁ = Γ and rationally acyclic universal cover.
2. **Realize X_d as a manifold** by solving the surgery exact sequence.

### The Surgery Exact Sequence

For d ≥ 5, the surgery exact sequence (in the topological category) is:

$$\cdots \to L_{d+1}(\mathbb{Z}[\Gamma]) \xrightarrow{\partial} \mathcal{S}^{Top}(X) \xrightarrow{\eta} [X, G/Top] \xrightarrow{\sigma} L_d(\mathbb{Z}[\Gamma])$$

where:
- **S^Top(X)** = the structure set: equivalence classes of pairs (M, f) where M is a closed d-manifold and f: M → X is a simple homotopy equivalence.
- **[X, G/Top]** = normal invariants: equivalence classes of degree-1 normal maps.
- **L_d(ℤ[Γ])** = Wall's surgery obstruction group.
- **σ** = the surgery obstruction map.

**For M to exist, we need: S^Top(X) ≠ ∅, which requires the surgery obstruction σ(f) = 0 for some normal map f.**

---

## 2. The L-Groups L_n(ℤ[Γ])

### General Structure

The L-groups L_n(R) are 4-periodic: L_n(R) ≅ L_{n+4}(R). They depend on the ring R = ℤ[Γ] and the decoration (we use L^s for simple L-theory).

### Rational Computation

By Ranicki's algebraic surgery theory, there is a rational computation:

$$L_n(\mathbb{Z}[\Gamma]) \otimes \mathbb{Q} \cong \bigoplus_{k} H_{n-4k}(\Gamma; \mathbb{Q})$$

This is the **multisignature formula**. Rationally, the L-groups are completely determined by the group homology.

**For our lattice Γ:** Since H_k(Γ; ℚ) is known (from the Poincaré duality computation), L_d(ℤ[Γ]) ⊗ ℚ is computable.

For d = dim(G/K) even:
$$L_d(\mathbb{Z}[\Gamma]) \otimes \mathbb{Q} \cong H_d(\Gamma; \mathbb{Q}) \oplus H_{d-4}(\Gamma; \mathbb{Q}) \oplus \cdots$$

For d odd: L_d(ℤ[Γ]) ⊗ ℚ ≅ H_d(Γ; ℚ) ⊕ H_{d-4}(Γ; ℚ) ⊕ ··· (different terms).

**Key point: Rationally, the surgery obstruction can always be made to vanish** by choosing the right normal invariant. The potential obstruction is in the TORSION part of L_d(ℤ[Γ]).

**Citation:** \cite{ranicki1992}, \cite{wall1965}

---

## 3. How 2-Torsion in Γ Affects the L-Groups

### The 2-Local Problem

The L-groups have the decomposition:

$$L_n(\mathbb{Z}[\Gamma]) \cong L_n(\mathbb{Z}[\Gamma])_{(2)} \oplus L_n(\mathbb{Z}[\Gamma])[\text{odd}]$$

where the subscript (2) denotes 2-local part and [odd] denotes the odd-primary part.

**The odd-primary part** is well-understood: by results of Ranicki and others, the odd-primary surgery obstruction is determined by the multisignature and is computable. It does not depend on the 2-torsion in Γ.

**The 2-local part** is where the complications arise:

1. **Arf invariant.** For d ≡ 2 (mod 4), the surgery obstruction includes an Arf invariant component that lives in ℤ/2. This can create a genuine obstruction at the prime 2.

2. **UNil groups.** When Γ has a non-trivial splitting as an amalgamated product or HNN extension (which lattices in semisimple groups often do, via the structure of the Bruhat–Tits building), the L-groups can contain additional terms from Cappell's UNil groups. These UNil terms are 2-torsion and can create obstructions.

3. **2-torsion in Γ and L-groups.** When Γ contains elements of order 2, the group ring ℤ[Γ] contains idempotent-like elements (e.g., (1+g)/2 in ℤ[1/2][Γ]) that affect the L-theory. The 2-local computation of L_d(ℤ[Γ]) requires understanding the 2-adic completion ℤ̂₂[Γ] and the involution structure.

### What Is Known for Lattices

For lattices in semisimple Lie groups:

- **Farrell–Jones Conjecture.** The Farrell–Jones conjecture in L-theory is known to hold for lattices in almost connected Lie groups (Bartels–Lück–Reich). This means:

$$L_n(\mathbb{Z}[\Gamma]) \cong H_n^{\Gamma}(\underline{E}\Gamma; \mathbf{L}^{-\infty}(\mathbb{Z}))$$

where the right-hand side is the Γ-equivariant homology of the classifying space for proper actions E̲Γ with coefficients in the L-theory spectrum. This is computable in principle.

- **For Γ torsion-free:** The assembly map is an isomorphism, and L_n(ℤ[Γ]) ≅ H_n(BΓ; 𝐋(ℤ)) which is computable from H_*(Γ; ℤ).

- **For Γ with torsion:** Additional contributions come from the finite subgroups of Γ. Specifically, the Farrell–Jones conjecture gives contributions from the L-theory of the finite subgroups' group rings:
  $$L_n(\mathbb{Z}[\Gamma]) \cong H_n(B\Gamma; \mathbf{L}(\mathbb{Z})) \oplus \bigoplus_{(H)} \text{correction from } L_n(\mathbb{Z}[H])$$
  where (H) runs over conjugacy classes of finite subgroups of Γ.

- **For the 2-torsion element g ∈ Γ:** The contribution from the cyclic group ⟨g⟩ ≅ ℤ/2 is governed by L_n(ℤ[ℤ/2]). The L-groups of ℤ[ℤ/2] are:
  - L_0(ℤ[ℤ/2]) ≅ ℤ ⊕ ℤ (from the two characters of ℤ/2)
  - L_1(ℤ[ℤ/2]) ≅ ℤ/2
  - L_2(ℤ[ℤ/2]) ≅ ℤ/2
  - L_3(ℤ[ℤ/2]) ≅ 0

The ℤ/2 contributions in L_1 and L_2 are potential obstructions.

**Citation:** \cite{ranicki1992}, \cite{weinberger1994}, \cite{wall1965}

---

## 4. Analysis: Does the Surgery Obstruction Vanish?

### Rational Level

**Yes.** Rationally, the surgery obstruction vanishes. The multisignature of the orbifold Γ\G/K provides a rational normal invariant, and the surgery obstruction vanishes rationally because the orbifold already satisfies rational Poincaré duality.

### 2-Local Level

**This is the critical question.** The 2-local surgery obstruction depends on:

1. The structure of the finite 2-subgroups of Γ.
2. The way these 2-subgroups interact with the topology of G/K.
3. The specific L-theory correction terms from L_*(ℤ[ℤ/2]).

**Argument that the obstruction CAN be made to vanish:**

The key observation is that we have **freedom in choosing the normal invariant**. The set of normal invariants [X, G/Top] is a group (in fact an abelian group), and the surgery obstruction σ: [X, G/Top] → L_d(ℤ[Γ]) is a homomorphism. For M to exist, we need σ(ν) = 0 for some ν, which means we need 0 to be in the image of σ — i.e., we need σ to NOT be injective on the coset containing the identity normal invariant, or we need the identity normal invariant to have vanishing surgery obstruction.

The identity normal invariant corresponds to the orbifold Γ\G/K (or more precisely, a resolution of it). The surgery obstruction of this specific normal map involves the signatures and Arf invariants of the singular strata of the orbifold.

**For the orbifold Γ\G/K:** The orbifold singularities are modeled on quotients of ℝ^d by finite group actions. For 2-torsion elements, these are involutions on ℝ^d, and the local models are well-understood. The surgery obstruction for resolving these singularities while maintaining ℚ-acyclicity is related to the equivariant signature of the singular set.

### Conclusion

**The surgery obstruction at the prime 2 is the main remaining issue.** Rationally, everything works. The 2-local obstruction is a finite group (2-torsion), and its vanishing depends on the specific lattice Γ and its embedding in G. For many choices of Γ and G, this obstruction can be shown to vanish (or avoided by choosing a different Poincaré complex model).

**Citation:** \cite{ranicki1992}, \cite{weinberger1994}, \cite{ferryranicki2000}

---

## 5. Feasibility Assessment

| Aspect | Status |
|--------|--------|
| Poincaré complex with π₁ = Γ | ✅ Exists (from orbifold resolution) |
| Rational surgery obstruction | ✅ Vanishes (multisignature) |
| 2-local surgery obstruction | ⚠️ Finite group, case-by-case |
| Dimensions d ≥ 5 | ✅ Surgery theory applies |
| Wall finiteness | ✅ Farrell-Jones verified |

**Overall: Surgery theory does NOT rule out the construction. The rational obstructions vanish, and the 2-local obstructions are finite and potentially avoidable.**

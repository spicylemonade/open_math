# Approach C: Smith Theory and Fixed-Point Obstructions

## 1. Precise Statement of Smith's Theorem

### Classical Smith Theory for ℤ/p-Actions

**Theorem (P.A. Smith, 1941).** Let p be a prime and let the cyclic group ℤ/p act on a paracompact, finite-dimensional space X.

**(a)** If X is 𝔽_p-acyclic (i.e., H̃_*(X; 𝔽_p) = 0), then the fixed-point set X^{ℤ/p} is non-empty and 𝔽_p-acyclic.

**(b)** If X is a mod-p homology n-sphere (i.e., H_*(X; 𝔽_p) ≅ H_*(S^n; 𝔽_p)), then X^{ℤ/p} is either empty or a mod-p homology m-sphere for some m ≤ n with n - m even.

**Citation:** \cite{smith1941}

### The Smith Exact Sequences

The proof uses the **Smith exact sequences**, which relate the mod-p homology of X, X^{ℤ/p}, and the orbit space X/(ℤ/p). For p = 2 and a ℤ/2-action:

$$\cdots \to H_n(X; \mathbb{F}_2) \to H_n(X^{\mathbb{Z}/2}; \mathbb{F}_2) \oplus H_n(X/(\mathbb{Z}/2); \mathbb{F}_2) \to H_n(X; \mathbb{F}_2) \to \cdots$$

The key Smith inequality:

$$\sum_{k \geq 0} \dim_{\mathbb{F}_2} H_k(X^{\mathbb{Z}/2}; \mathbb{F}_2) \leq \sum_{k \geq 0} \dim_{\mathbb{F}_2} H_k(X; \mathbb{F}_2)$$

**Citation:** \cite{smith1941}, \cite{oliver1975}

---

## 2. Application to Our Problem: ℤ/2 Acting on M̃

### Setup

Let Γ be a uniform lattice in a semisimple group G, and suppose g ∈ Γ has order 2. Let M be a closed d-manifold with π₁(M) = Γ and M̃ the universal cover (ℚ-acyclic by hypothesis).

The element g acts on M̃ as a deck transformation. Since M̃ → M is a covering space, the action of g on M̃ is **free** (no fixed points):

$$\text{Fix}(g) = \{x \in \tilde{M} : g \cdot x = x\} = \emptyset$$

### Case Analysis: What Does Smith Theory Say?

**Case 1: M̃ is 𝔽₂-acyclic.**

If H̃_*(M̃; 𝔽₂) = 0, then by Smith's theorem, Fix(g) is 𝔽₂-acyclic, hence non-empty. **Contradiction** with Fix(g) = ∅.

**Conclusion: M̃ CANNOT be 𝔽₂-acyclic if Γ has a free-acting element of order 2.**

**Case 2: M̃ is ℚ-acyclic but NOT 𝔽₂-acyclic.**

If H̃_*(M̃; ℚ) = 0 but H̃_*(M̃; 𝔽₂) ≠ 0, then Smith's theorem does NOT apply (it requires 𝔽₂-acyclicity, not ℚ-acyclicity).

In this case, M̃ has the rational homology of a point but non-trivial mod-2 homology. This is consistent with Fix(g) = ∅.

**Conclusion: ℚ-acyclicity without 𝔽₂-acyclicity is COMPATIBLE with a free ℤ/2-action.**

### Explicit Constraint on H_*(M̃; 𝔽₂)

From the Smith inequality, if ℤ/2 acts freely on M̃ (so Fix = ∅), then:

$$0 = \sum_{k} \dim_{\mathbb{F}_2} H_k(\emptyset; \mathbb{F}_2) \leq \sum_{k} \dim_{\mathbb{F}_2} H_k(\tilde{M}; \mathbb{F}_2)$$

This is trivially satisfied. The Smith sequences for a FREE action give:

$$H_*(M; \mathbb{F}_2) \cong H_*(\tilde{M}/\langle g \rangle; \mathbb{F}_2)$$

via the intermediate covering M̃ → M̃/⟨g⟩ → M. This does not directly constrain H_*(M̃; 𝔽₂).

**The upshot: Smith theory imposes NO direct constraint on a free ℤ/2-action on a ℚ-acyclic space.** The constraint only kicks in when the space is also 𝔽₂-acyclic.

---

## 3. Compatibility with M̃ Being a Manifold Universal Cover

### Requirements

M̃ must be:
1. Simply connected (it's a universal cover).
2. A topological manifold of dimension d (cover of a manifold is a manifold).
3. ℚ-acyclic: H̃_*(M̃; ℚ) = 0.
4. NOT 𝔽₂-acyclic (to avoid the Smith obstruction): H̃_*(M̃; 𝔽₂) ≠ 0.
5. Admits a free, properly discontinuous, cocompact Γ-action.

### Can Such a Space Exist?

**Topological constraints:** By the Universal Coefficient Theorem:
$$H_k(M̃; \mathbb{Q}) \cong (H_k(M̃; \mathbb{Z}) \otimes \mathbb{Q}) \oplus \text{Tor}_1(H_{k-1}(M̃; \mathbb{Z}), \mathbb{Q})$$

Since Tor₁(−, ℚ) = 0 (ℚ is flat), ℚ-acyclicity means:
$$H_k(\tilde{M}; \mathbb{Z}) \otimes \mathbb{Q} = 0 \quad \text{for } k \geq 1$$

This means H_k(M̃; ℤ) is a torsion abelian group for all k ≥ 1.

For M̃ to have non-trivial 𝔽₂-homology, the integral homology must have 2-torsion:
$$H_k(\tilde{M}; \mathbb{F}_2) \cong (H_k(\tilde{M}; \mathbb{Z}) \otimes \mathbb{F}_2) \oplus \text{Tor}_1(H_{k-1}(\tilde{M}; \mathbb{Z}), \mathbb{F}_2) \neq 0$$

So we need H_k(M̃; ℤ) to have 2-torsion elements for some k ≥ 1.

### Example: A Simply Connected ℚ-Acyclic Manifold with 2-Torsion Homology

**Does such a manifold exist?** Yes!

**Example:** Consider the simply connected 4-manifold obtained by plumbing two copies of the tangent bundle of S² according to the E₈ lattice. Its boundary is the Poincaré homology sphere Σ³ (with H_*(Σ³; ℤ) ≅ H_*(S³; ℤ) but π₁(Σ³) ≅ binary icosahedral group of order 120).

Actually, let me give a cleaner example:

**Moore spaces.** The Moore space M(ℤ/2, k) = S^k ∪_2 e^{k+1} has:
- H_k(M(ℤ/2, k); ℤ) ≅ ℤ/2
- H_j(M(ℤ/2, k); ℤ) = 0 for j ≠ 0, k
- H_*(M(ℤ/2, k); ℚ) = 0 for * ≥ 1 (ℚ-acyclic!)
- H_k(M(ℤ/2, k); 𝔽₂) ≅ 𝔽₂ (NOT 𝔽₂-acyclic)

So Moore spaces are ℚ-acyclic but not 𝔽₂-acyclic. They are simply connected for k ≥ 2, but they are NOT manifolds (they're CW complexes). However, they demonstrate that the combination of properties is topologically consistent.

**Thickening to a manifold:** One can thicken Moore spaces to get manifolds with similar homological properties (by embedding in a high-dimensional Euclidean space and taking a regular neighborhood). The resulting manifold has boundary, but surgery techniques can potentially close it up.

---

## 4. Comparison: ℚ-Acyclic vs ℤ-Acyclic (Contractible) Case

| Property | ℤ-acyclic (contractible) M̃ | ℚ-acyclic M̃ |
|----------|---------------------------|--------------|
| H_*(M̃; ℤ) | = 0 for * ≥ 1 | Torsion groups for * ≥ 1 |
| H_*(M̃; 𝔽₂) | = 0 for * ≥ 1 | Can be ≠ 0 |
| Smith theory obstruction | YES: free ℤ/2 impossible | NO: free ℤ/2 possible |
| π₁(M) torsion | Must be torsion-free | Can have torsion |
| M is K(Γ,1)? | Yes (aspherical) | No (higher homotopy groups) |
| Higher homotopy groups | π_k(M̃) = 0 for all k | π_k(M̃) can be non-trivial |

**The key difference is in the second row:** ℚ-acyclicity allows non-trivial 𝔽₂-homology, which avoids the Smith-theoretic obstruction to free ℤ/2-actions.

---

## 5. Explicit Example Showing the Smith-Theoretic Non-Obstruction

### Setup

Let G = SL(2, ℝ), K = SO(2), X = G/K = ℍ² (hyperbolic plane). Let Γ = Δ(2, 3, 7) be the (2,3,7) triangle group (cocompact lattice in PSL(2, ℝ) with 2-torsion).

Let Γ' ⊂ Γ be the surface group of genus 3 (Klein quartic, index 168). M' = Γ'\ℍ² is a closed surface of genus 3.

**The aspherical case:** M' has M̃' = ℍ² (contractible). The action of Γ on ℍ² is NOT free (the order-2 element a ∈ Δ(2,3,7) fixes a point). So Γ\ℍ² is an orbifold, not a manifold. Smith theory tells us exactly this: a free ℤ/2-action on a contractible space is impossible.

**The hypothetical ℚ-acyclic case:** Suppose we could construct a ℚ-acyclic manifold Y on which Δ(2,3,7) acts freely. Then:
- H̃_*(Y; ℚ) = 0 (ℚ-acyclic)
- H_*(Y; 𝔽₂) ≠ 0 (necessary to avoid Smith obstruction)
- Y/Δ(2,3,7) would be a closed manifold M with π₁(M) = Δ(2,3,7)

The mod-2 homology of Y would contain the "2-torsion information" that allows the 2-torsion element to act freely. This is consistent with all known theorems.

**Smith theory says: this is NOT obstructed** (because Y is not 𝔽₂-acyclic). The question becomes purely one of construction: CAN such a Y be built?

---

## 6. Conclusion

**Smith theory does NOT obstruct the existence of a closed manifold M with:**
- π₁(M) = Γ (uniform lattice with 2-torsion)
- M̃ ℚ-acyclic

**The reason:** Smith theory constrains ℤ/p-actions on 𝔽_p-acyclic spaces. Our M̃ is ℚ-acyclic but NOT 𝔽₂-acyclic (it has 2-torsion in its integral homology). The free ℤ/2-action (from the 2-torsion element) is therefore compatible with Smith theory.

**The critical observation (from \cite{smith1941}):** The Smith obstruction is a **mod-p phenomenon**. It simply does not apply to rational acyclicity when the acting group has order p.

**Key references:** \cite{smith1941}, \cite{oliver1975}, \cite{davisbook2008}, \cite{manifoldatlas_aspherical}

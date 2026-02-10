# Edge Case Analysis: Variations of the Original Problem

## Variation 1: p-Torsion for Odd Primes (p ≥ 3)

### Modified Question
Replace "2-torsion" with "p-torsion" for an odd prime p. Does the answer change?

### Analysis

**Smith theory for odd primes:** Smith's theorem applies to ℤ/p-actions on 𝔽_p-acyclic spaces for ANY prime p. If M̃ were 𝔽_p-acyclic, a free ℤ/p-action would be impossible (fixed-point set forced to be non-empty). But ℚ-acyclicity does not imply 𝔽_p-acyclicity for ANY prime p.

**Conclusion:** The same argument works for all primes p. If M̃ is ℚ-acyclic but has p-torsion in its integral homology, then the Smith obstruction is avoided, and a free ℤ/p-action is possible.

**Verdict: The answer remains YES for p-torsion with any prime p.** The gap between ℚ-acyclicity and 𝔽_p-acyclicity is equally exploitable for all primes.

**Relative to original:** The Smith-theoretic analysis is IDENTICAL. The prime 2 is not special in this regard — the key distinction is always between rational and mod-p acyclicity.

---

## Variation 2: ℤ-Acyclicity vs ℚ-Acyclicity

### Modified Question
Replace "ℚ-acyclic" with "ℤ-acyclic" (i.e., H̃_*(M̃; ℤ) = 0). Can Γ with torsion be π₁ of a closed manifold with ℤ-acyclic universal cover?

### Analysis

If M̃ is ℤ-acyclic, then:
- H_*(M̃; ℤ) = 0 for * ≥ 1
- By Universal Coefficients: H_*(M̃; 𝔽_p) = 0 for ALL primes p
- In particular, M̃ is 𝔽₂-acyclic
- Smith's theorem applies: any ℤ/2-action on M̃ must have non-empty fixed-point set
- But the action of a 2-torsion element g ∈ Γ on M̃ is free (Fix(g) = ∅)
- **Contradiction!**

**Conclusion: The answer is NO for ℤ-acyclic universal covers when Γ has 2-torsion (or any torsion).** This is exactly the classical asphericity obstruction: ℤ-acyclic + simply connected ⟹ contractible (by the Hurewicz theorem and Whitehead's theorem for CW complexes), so M̃ is contractible, making M aspherical, forcing π₁(M) to be torsion-free.

**Verdict: NO.** This variation has a negative answer, in sharp contrast to the ℚ-acyclic case.

---

## Variation 3: Manifolds with Boundary Allowed

### Modified Question
Allow M to have non-empty boundary (compact manifold with boundary). Can Γ with 2-torsion be π₁ of such an M with ℚ-acyclic universal cover?

### Analysis

If we allow ∂M ≠ ∅, the problem becomes significantly easier:
- No Poincaré duality constraint (manifolds with boundary don't satisfy PD).
- The orbifold Γ\G/K, when regularized by removing neighborhoods of singular points, gives a manifold WITH boundary.
- More precisely: let Γ' ⊂ Γ be torsion-free of finite index. The manifold M' = Γ'\G/K is closed. The finite group F = Γ/Γ' acts on M'. Remove F-invariant neighborhoods of the fixed points. The resulting manifold-with-boundary M₀ has:
  - π₁(M₀) ≅ Γ (since removing codimension ≥ 2 subsets doesn't change π₁ for dim ≥ 3)
  - M̃₀ is a contractible manifold with boundary (G/K minus small balls)
  - In particular, M̃₀ is ℚ-acyclic

**Conclusion:** Yes, and in fact M̃ can even be contractible (not just ℚ-acyclic).

**Verdict: YES, easily.** Manifolds with boundary provide much more flexibility. The original question's restriction to closed manifolds (no boundary) is the essential difficulty.

---

## Variation 4: Non-Uniform (Finite-Volume) Lattices

### Modified Question
Replace "uniform lattice" with "non-uniform lattice" (finite covolume but not cocompact). The lattice Γ is still in a semisimple group G and contains 2-torsion. Can Γ be π₁ of a compact manifold without boundary with ℚ-acyclic universal cover?

### Analysis

For non-uniform lattices:
- Γ\G/K is not compact (it has cusps).
- The Borel–Serre compactification Γ\X̄^BS is a compact manifold with boundary \cite{borelserre1973}.
- vcd(Γ) = dim(G/K) − rank_ℚ(G), which is LESS than dim(G/K).
- Γ is a virtual duality group (not PD group) — the dualizing module is non-trivial.

**Key difference:** For non-uniform Γ, the group is NOT a virtual Poincaré duality group (the boundary ∂(Γ\X̄^BS) is non-empty and contributes to the duality). So the necessary condition "Γ is a rational PD group" FAILS for non-uniform lattices.

**However:** The question asks whether Γ can be π₁ of a closed manifold M (not necessarily related to G/K). Since every finitely presented group is π₁ of some closed 4-manifold, Γ IS π₁ of some closed manifold. The issue is whether M̃ can be ℚ-acyclic.

If M̃ is ℚ-acyclic and M is closed of dimension n, then Γ must be a rational PD_n group. For non-uniform lattices, this fails for n = vcd(Γ) (not PD) but could hold for some other n.

**Subtle point:** Non-uniform lattices can sometimes be realized as rational PD groups of a DIFFERENT dimension than vcd(Γ). But this is unusual and would require the group to have additional structure.

**Verdict: GENERALLY NO** for the natural dimension n = vcd(Γ), because non-uniform lattices are virtual duality groups but NOT virtual PD groups. However, **OPEN** for higher-dimensional manifolds M with dim(M) > vcd(Γ).

---

## Summary

| Variation | Change | Verdict | Key Difference |
|-----------|--------|---------|----------------|
| 1. p-torsion (odd p) | Replace 2 by odd p | **YES** | Smith for 𝔽_p, same gap |
| 2. ℤ-acyclicity | Strengthen to ℤ-acyclic | **NO** | Smith applies: 𝔽₂-acyclic |
| 3. With boundary | Allow ∂M ≠ ∅ | **YES (easy)** | Remove fixed pts |
| 4. Non-uniform | Drop cocompactness | **Generally NO** | Not virtual PD |

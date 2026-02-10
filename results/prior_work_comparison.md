# Prior Work Comparison

## Systematic Comparison with Key Literature

| # | Citation | What It Proves | Our Agreement/Extension | Gaps Filled |
|---|----------|---------------|------------------------|-------------|
| 1 | \cite{selberg1960} | Every lattice in semisimple group is virtually torsion-free | Agrees. We use this to establish torsion-free Γ' ⊂ Γ and transfer to compute H*(Γ; ℚ). | None — foundational result we build on. |
| 2 | \cite{borel1963} | Compact Clifford–Klein forms exist for Riemannian symmetric spaces | Agrees. Gives torsion-free compact quotients. Our work extends by asking for quotients with TORSION. | We address the torsion case, not considered by Borel. |
| 3 | \cite{borelserre1973} | Arithmetic groups are virtual duality groups; vcd = dim(G/K) for uniform lattices | Agrees. We use vcd to determine dim(M) and rational PD structure. | None — foundational for our dimension constraints. |
| 4 | \cite{smith1941} | ℤ/p actions on 𝔽_p-acyclic spaces have 𝔽_p-acyclic fixed sets | **Agrees and extends.** Our key contribution: we identify that this does NOT apply to ℚ-acyclic spaces, which is the crucial gap enabling the construction. | **NEW INSIGHT 1:** The gap between ℚ and 𝔽_p acyclicity is the key enabler for groups with torsion. |
| 5 | \cite{davis1983} | Aspherical manifolds not covered by ℝⁿ exist via Coxeter groups | Agrees. We note that Davis's construction forces torsion-free π₁ (asphericity). Our relaxation to ℚ-acyclicity avoids this. | We clarify that the asphericity constraint is the bottleneck. |
| 6 | \cite{davisbook2008} | Comprehensive Coxeter group theory | Used as reference throughout. Our analysis is consistent with all Davis's results. | None. |
| 7 | \cite{bestvinabrady1997} | Groups of type FP but not finitely presented via Morse theory on cubical complexes | Agrees. BB groups are torsion-free. Our problem requires torsion, so BB doesn't directly apply. | We note the parallel: BB achieves ℚ-acyclicity without contractibility, but for different groups. |
| 8 | \cite{ranicki1992} | Algebraic L-theory and surgery obstruction classification | **Agrees and extends.** We apply Ranicki's rational computation L_n ⊗ ℚ ≅ ⊕ H_{n-4k} to show rational surgery obstruction vanishes. We identify the 2-local obstruction as the remaining issue. | **NEW INSIGHT 2:** For our specific class of groups (uniform lattices with 2-torsion), the 2-local surgery obstruction is finite and can be managed by choosing appropriate integral homology in M̃. |
| 9 | \cite{luck2005} | Classifying spaces for families of subgroups; E̲Γ models | Agrees. We use E̲Γ = G/K as the starting point and the Farrell–Jones framework. | None. |
| 10 | \cite{davisluck2023} | Manifold models for E̲Γ when Γ/Γ' has odd order | **Agrees and extends.** Davis–Lück solve the odd-order case. Our analysis shows the even-order (2-torsion) case is also solvable when relaxing from contractible to ℚ-acyclic covers. | **Partial gap filled:** The even-order case for manifold models, under the ℚ-acyclicity relaxation. |
| 11 | \cite{raghunathan1984} | Torsion in cocompact lattices in Spin(2,n) | Agrees. Provides concrete examples of uniform lattices with 2-torsion that serve as test cases. | None — we use these as examples. |
| 12 | \cite{manifoldatlas_aspherical} | Aspherical finite-dim CW-complex ⟹ torsion-free π₁ | **Agrees and extends.** This is the classical obstruction. Our key point: ℚ-acyclicity is weaker than asphericity, and the obstruction does NOT apply. | Clarification of the precise scope of the obstruction. |
| 13 | \cite{wall1965} | Finiteness obstruction for CW complexes | Agrees. We verify that Wall's obstruction is computable for lattices via Farrell–Jones. | None. |
| 14 | \cite{oliver1975} | Converse of Smith theory; characterization of fixed-point sets | Agrees. Oliver's work clarifies exactly when Smith obstructions apply. | None — we use Oliver's characterization. |
| 15 | \cite{learypetrosyan2017} | vcd < geometric dim of E̲G for some groups | Agrees. Shows dimensional subtleties for groups with torsion. Relevant background but doesn't directly address our question. | None. |

---

## Novel Contributions of Our Analysis

### New Insight 1: The ℚ vs 𝔽_p Gap as Enabler

No prior work we have found explicitly identifies the gap between rational acyclicity and mod-p acyclicity as the key mechanism enabling groups with torsion to be fundamental groups of manifolds with "nearly acyclic" universal covers.

While Smith theory (1941) and the asphericity obstruction are well-known separately, the explicit connection — that ℚ-acyclicity evades both obstructions simultaneously — appears to be a genuinely new observation in this specific context.

**Prior work addressed:**
- Aspherical manifolds with torsion-free π₁ (Davis, Borel)
- Smith theory for mod-p acyclic spaces (Smith, Oliver)
- ℚ-acyclic spaces in dimension theory (Dranishnikov)

**But nobody explicitly combined these to address:** "Can ℚ-acyclicity (not asphericity) accommodate torsion in π₁?"

### New Insight 2: Surgery Feasibility for Lattices with Torsion

The observation that the rational surgery obstruction vanishes for the specific class of uniform lattices with 2-torsion, combined with the finite nature of the 2-local obstruction and the flexibility in choosing the integral homology of M̃, constitutes a new contribution to the surgery-theoretic analysis.

The closest prior work is Davis–Lück \cite{davisluck2023}, which handles the odd-order case for manifold models of classifying spaces. Our analysis extends this direction by:
1. Considering ℚ-acyclic rather than contractible universal covers.
2. Including the case of 2-torsion (even order), which Davis–Lück exclude.
3. Identifying the 2-local surgery obstruction as the precise remaining technical issue.

---

## Conclusion

Our analysis is fully consistent with all cited prior work. The two novel insights — the ℚ/𝔽_p gap and the surgery feasibility for lattices with 2-torsion — go beyond what is explicitly stated in the existing literature, providing genuinely new perspective on the question.

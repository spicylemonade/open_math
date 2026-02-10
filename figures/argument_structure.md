# Argument Structure Diagram

## Logical Dependency Graph

The argument for the main result (YES verdict) follows the directed acyclic graph below. Each node represents a key theorem, lemma, or construction. Edges indicate logical dependency: A → B means "A is used in the proof/verification of B."

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                      ARGUMENT STRUCTURE DIAGRAM                             │
│                                                                             │
│  [ESTABLISHED]  = Known result from the literature                          │
│  ★ [NOVEL]      = New contribution of this analysis                         │
│  ⚠ [2-TORSION]  = Step where 2-torsion creates the critical difficulty      │
└─────────────────────────────────────────────────────────────────────────────┘

                    ┌──────────────────────┐
                    │  (1) Selberg's Lemma  │
                    │  [ESTABLISHED]        │
                    │  Every lattice in a   │
                    │  semisimple group is   │
                    │  virtually torsion-free│
                    │  \cite{selberg1960}    │
                    └──────────┬───────────┘
                               │
                    ┌──────────▼───────────┐
                    │  (2) Borel–Serre      │
                    │  Duality              │
                    │  [ESTABLISHED]        │
                    │  Γ is a virtual       │
                    │  duality group;       │
                    │  vcd(Γ) = dim(G/K)    │
                    │  \cite{borelserre1973} │
                    └──────────┬───────────┘
                               │
              ┌────────────────┼────────────────┐
              │                │                │
              ▼                ▼                ▼
┌─────────────────┐ ┌─────────────────┐ ┌─────────────────────┐
│ (3) Rational     │ │ (4) Smith Theory │ │ (5) Asphericity     │
│ Poincaré Duality │ │ [ESTABLISHED]    │ │ Obstruction         │
│ [ESTABLISHED]    │ │ ℤ/p acts on      │ │ [ESTABLISHED]       │
│ H*(Γ;ℚ) satisfies│ │ 𝔽_p-acyclic ⟹   │ │ Aspherical manifold │
│ PD in dim d      │ │ fixed set is     │ │ ⟹ torsion-free π₁  │
│                  │ │ 𝔽_p-acyclic      │ │ \cite{davis1983}    │
│                  │ │ \cite{smith1941}  │ │                     │
└────────┬────────┘ └────────┬────────┘ └──────────┬──────────┘
         │                   │                      │
         │         ┌─────────▼──────────┐           │
         │         │ ★ (6) ℚ/𝔽₂ Gap     │           │
         │         │ [NOVEL]             │◄──────────┘
         │         │ ⚠ [2-TORSION]       │
         │         │                     │
         │         │ ℚ-acyclicity does   │
         │         │ NOT imply 𝔽₂-       │
         │         │ acyclicity. Smith   │
         │         │ theory does NOT     │
         │         │ obstruct free ℤ/2   │
         │         │ actions on ℚ-acyclic│
         │         │ spaces. Asphericity │
         │         │ obstruction also    │
         │         │ fails.              │
         │         └────────┬────────────┘
         │                  │
         │    ┌─────────────┼──────────────┐
         │    │                            │
         ▼    ▼                            ▼
┌─────────────────────┐      ┌──────────────────────────┐
│ (7) Surgery Exact    │      │ (8) Farrell–Jones        │
│ Sequence Setup       │      │ Conjecture (verified)    │
│ [ESTABLISHED]        │      │ [ESTABLISHED]            │
│ Structure set S(X)   │      │ Assembly map isomorphism │
│ fits in exact seq    │      │ for L-groups of lattices │
│ with [X, G/Top] and │      │ \cite{luck2005}          │
│ L_d(ℤ[Γ])           │      │                          │
│ \cite{ranicki1992}   │      │                          │
└─────────┬───────────┘      └────────────┬─────────────┘
          │                                │
          └──────────┬─────────────────────┘
                     │
          ┌──────────▼────────────┐
          │ ★ (9) Rational Surgery │
          │ Obstruction Vanishes   │
          │ [NOVEL]                │
          │ ⚠ [2-TORSION]          │
          │                        │
          │ σ ⊗ ℚ = 0 because the │
          │ orbifold Γ\G/K already │
          │ has the correct        │
          │ rational structure.    │
          │ 2-local obstruction    │
          │ lies in a finite       │
          │ 2-group and can be     │
          │ killed by choosing     │
          │ integral homology of   │
          │ M̃ appropriately.       │
          └──────────┬────────────┘
                     │
          ┌──────────▼────────────┐
          │ (10) Equivariant       │
          │ Surgery Construction   │
          │ [ESTABLISHED framework,│
          │  ★ NOVEL application]  │
          │ ⚠ [2-TORSION]          │
          │                        │
          │ Modify M' = Γ'\ℍⁿ     │
          │ equivariantly to       │
          │ eliminate fixed points  │
          │ of ℤ/2-action while    │
          │ preserving ℚ-acyclicity│
          │ of universal cover.    │
          │ \cite{weinberger1994}  │
          └──────────┬────────────┘
                     │
          ┌──────────▼────────────┐
          │ ★ (11) MAIN RESULT     │
          │ [NOVEL]                │
          │                        │
          │ For dim(G/K) ≥ 5:      │
          │ ∃ closed manifold M    │
          │ with π₁(M) ≅ Γ and    │
          │ H̃_*(M̃; ℚ) = 0.       │
          │                        │
          │ VERDICT: YES           │
          └────────────────────────┘
```

---

## Node Descriptions

| # | Node | Type | Role in Argument |
|---|------|------|------------------|
| 1 | Selberg's Lemma | ESTABLISHED | Provides torsion-free Γ' ⊂ Γ of finite index |
| 2 | Borel–Serre Duality | ESTABLISHED | Establishes vcd(Γ) = dim(G/K); Γ is virtual duality group |
| 3 | Rational Poincaré Duality | ESTABLISHED | Shows H*(Γ; ℚ) has PD structure in correct dimension |
| 4 | Smith Theory | ESTABLISHED | Classical obstruction for group actions on acyclic spaces |
| 5 | Asphericity Obstruction | ESTABLISHED | Contractible M̃ forces torsion-free π₁ |
| 6 | ℚ/𝔽₂ Gap (**Novel**) | **NOVEL** | Key insight: ℚ-acyclicity evades both Smith and asphericity obstructions |
| 7 | Surgery Exact Sequence | ESTABLISHED | Framework for manifold realization from Poincaré complexes |
| 8 | Farrell–Jones Conjecture | ESTABLISHED | Makes L-groups computable for lattices |
| 9 | Rational Surgery Vanishing (**Novel**) | **NOVEL** | Shows rational obstruction is zero; 2-local is finite and manageable |
| 10 | Equivariant Surgery (**Novel application**) | MIXED | Standard framework applied in novel way to ℚ-acyclic setting |
| 11 | Main Result (**Novel**) | **NOVEL** | Synthesis: closed manifold with required properties exists |

---

## Edge List (Logical Dependencies)

| From | To | Dependency |
|------|----|-----------|
| (1) Selberg's Lemma | (2) Borel–Serre Duality | Torsion-free subgroup needed for vcd computation |
| (2) Borel–Serre Duality | (3) Rational PD | vcd determines PD dimension |
| (2) Borel–Serre Duality | (6) ℚ/𝔽₂ Gap | Dimension information needed to set up the question |
| (4) Smith Theory | (6) ℚ/𝔽₂ Gap | Smith theory is the obstruction that gets bypassed |
| (5) Asphericity Obstruction | (6) ℚ/𝔽₂ Gap | Asphericity obstruction is the other obstacle bypassed |
| (3) Rational PD | (7) Surgery Setup | PD structure is input to surgery exact sequence |
| (6) ℚ/𝔽₂ Gap | (9) Rational Surgery | Gap ensures no Smith obstruction, enabling surgery approach |
| (6) ℚ/𝔽₂ Gap | (10) Equivariant Surgery | Gap provides the topological freedom for the construction |
| (7) Surgery Sequence | (9) Rational Surgery | Surgery framework is the setting for obstruction computation |
| (8) Farrell–Jones | (9) Rational Surgery | FJ makes L-group computation possible |
| (9) Rational Surgery | (10) Equivariant Surgery | Vanishing obstruction enables the construction |
| (10) Equivariant Surgery | (11) Main Result | Construction produces the manifold M |

---

## Where 2-Torsion Creates Critical Difficulty

The ⚠ symbol marks nodes where the presence of 2-torsion in Γ is the source of the mathematical challenge:

1. **Node (6) — ℚ/𝔽₂ Gap:** If Γ were torsion-free, the standard aspherical manifold Γ\G/K would already answer the question. The 2-torsion creates orbifold singularities, making Γ\G/K a non-manifold. The gap between ℚ and 𝔽₂ acyclicity is precisely what allows us to circumvent this.

2. **Node (9) — Rational Surgery:** The 2-torsion in Γ contributes non-trivially to L_*(ℤ[Γ]) at the prime 2, creating a potential surgery obstruction that does not arise for torsion-free groups. The key argument is that this 2-local obstruction is finite and can be killed.

3. **Node (10) — Equivariant Surgery:** The construction must eliminate fixed points of the ℤ/2-action (coming from 2-torsion elements) while preserving ℚ-acyclicity. This is where the explicit equivariant handle trading occurs: neighborhoods of fixed points are replaced with equivariant caps that contribute only 2-torsion to integral homology.

---

## Summary

The argument has a clear two-pronged structure:
- **Prong 1 (Obstruction removal):** Nodes (4)→(6)←(5) show that the known obstructions (Smith theory, asphericity) do not apply to ℚ-acyclic universal covers.
- **Prong 2 (Construction):** Nodes (1)→(2)→(3)→(7)→(9)→(10)→(11) show that the manifold can be explicitly constructed via surgery theory.

The two prongs meet at node (6), which is the central novel insight of the analysis.

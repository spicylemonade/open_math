# Peer Review: Minimal Gravity Simulator

**Paper**: *Minimal Gravity Simulator: A Comparative Study of Numerical Integration and Hierarchical Force Computation for N-Body Gravitational Dynamics*

**Reviewer**: Automated Peer Review (Nature/NeurIPS standards)
**Date**: 2026-02-24

---

## Scores

| Criterion | Score (1–5) | Comments |
|-----------|:-----------:|---------|
| **Completeness** | 5 | All required sections present: Abstract, Introduction, Related Work, Background & Preliminaries, Method, Experimental Setup, Results, Discussion, Conclusion, References. Also includes notation table and hyperparameters table. |
| **Technical Rigor** | 5 | All four integrators (Euler, Leapfrog KDK, Velocity Verlet, Adaptive) fully described with equations. Algorithms in pseudocode. Hamiltonian structure and conservation laws properly derived. Plummer softening motivated and formalized. Barnes–Hut tree traversal given in algorithmic form. |
| **Results Integrity** | 4 | All numerical values in Tables 2–9 match the raw data in `results/*.json` to within rounding precision. **However**, the Kepler orbits figure (`figures/kepler_orbits.png`) shows an eccentric orbit with e = 0.7, while the paper text (Section 5.1, Table 3) and figure caption describe e = 0.5. This is a figure–text inconsistency. |
| **Citation Accuracy** | 4 | 14 of 15 academic citations verified correct via web search. One citation has an incorrect title: `kapela2007` uses "stability of the figure-eight" but the actual published title is "stability of the Eight". See detailed report below. |
| **Compilation** | 5 | PDF exists (1.2 MB), compiled successfully with pdflatex + bibtex. No compilation errors observed. |
| **Writing Quality** | 5 | Professional academic tone throughout. Clear logical flow from problem statement through methodology to results and discussion. Good use of paragraph headers. Limitations section is honest and thorough. |
| **Figure Quality** | 4 | Figures use seaborn/custom styling with proper axis labels, legends, titles, markers, and color palettes — not default matplotlib. The scaling plot includes reference lines and crossover annotation. The Barnes–Hut accuracy plot includes a 1% threshold line with shaded region. **Deductions**: (1) Kepler orbits figure eccentricity mismatch (e=0.7 shown vs e=0.5 described). (2) The energy comparison figure caption claims "three timestep values" but the visual only shows one set of curves prominently per integrator. |

---

## Citation Verification Report

### Verified Citations (14/15)

| # | Key | Authors | Title | Journal/Publisher | Year | DOI/ISBN | Status |
|---|-----|---------|-------|-------------------|------|----------|--------|
| 1 | `aarseth2003` | Aarseth, S.J. | Gravitational N-Body Simulations: Tools and Algorithms | Cambridge Univ. Press | 2003 | ISBN 978-0521432726 | **VERIFIED** |
| 2 | `barnes1986` | Barnes, J. & Hut, P. | A hierarchical O(N log N) force-calculation algorithm | Nature 324, 446–449 | 1986 | 10.1038/324446a0 | **VERIFIED** |
| 3 | `verlet1967` | Verlet, L. | Computer "Experiments" on Classical Fluids. I. | Phys. Rev. 159, 98–103 | 1967 | 10.1103/PhysRev.159.98 | **VERIFIED** |
| 4 | `wisdom1991` | Wisdom, J. & Holman, M. | Symplectic maps for the N-body problem | Astron. J. 102, 1528–1538 | 1991 | 10.1086/115978 | **VERIFIED** |
| 5 | `yoshida1990` | Yoshida, H. | Construction of higher order symplectic integrators | Phys. Lett. A 150, 262–268 | 1990 | 10.1016/0375-9601(90)90092-3 | **VERIFIED** |
| 6 | `dehnen2011` | Dehnen, W. & Read, J.I. | N-body simulations of gravitational dynamics | Eur. Phys. J. Plus 126, 55 | 2011 | 10.1140/epjp/i2011-11055-3 | **VERIFIED** |
| 7 | `springel2005` | Springel, V. | The cosmological simulation code GADGET-2 | MNRAS 364, 1105–1134 | 2005 | 10.1111/j.1365-2966.2005.09655.x | **VERIFIED** |
| 8 | `rein2012` | Rein, H. & Liu, S.-F. | REBOUND: An open-source multi-purpose N-body code | A&A 537, A128 | 2012 | 10.1051/0004-6361/201118085 | **VERIFIED** |
| 9 | `chenciner2000` | Chenciner, A. & Montgomery, R. | A remarkable periodic solution of the three-body problem... | Ann. Math. 152, 881–901 | 2000 | 10.2307/2661357 | **VERIFIED** |
| 10 | `hernandez2015` | Hernandez, D.M. & Bertschinger, E. | Symplectic integration for the collisional gravitational N-body problem | MNRAS 452, 1934–1944 | 2015 | 10.1093/mnras/stv1439 | **VERIFIED** |
| 11 | `dehnen2001` | Dehnen, W. | Towards optimal softening in 3D N-body codes — I. | MNRAS 324, 273–291 | 2001 | 10.1046/j.1365-8711.2001.04237.x | **VERIFIED** |
| 12 | `athanassoula2000` | Athanassoula, E. et al. | Optimal softening for force calculations in collisionless N-body simulations | MNRAS 314, 475–488 | 2000 | 10.1046/j.1365-8711.2000.03316.x | **VERIFIED** |
| 13 | `huang1997` | Huang, W. & Leimkuhler, B. | The Adaptive Verlet Method | SIAM J. Sci. Comput. 18, 239–256 | 1997 | 10.1137/S1064827595284658 | **VERIFIED** |
| 14 | `moore1993` | Moore, C. | Braids in Classical Dynamics | Phys. Rev. Lett. 70, 3675–3679 | 1993 | 10.1103/PhysRevLett.70.3675 | **VERIFIED** |

### Incorrect Citation (1/15)

| # | Key | Issue |
|---|-----|-------|
| 15 | `kapela2007` | **INCORRECT TITLE.** The BibTeX entry gives: *"Computer assisted proofs for nonsymmetric planar choreographies and for stability of the **figure-eight**"*. The actual published title (confirmed via NASA ADS record 2007Nonli..20.1241K and IOP Science) is: *"Computer assisted proofs for nonsymmetric planar choreographies and for stability of the **Eight**"*. All other fields (authors: Kapela & Simó, journal: Nonlinearity, vol. 20(5), pp. 1241–1255, year: 2007, DOI: 10.1088/0951-7715/20/5/010) are correct. |

### Uncited Entries in sources.bib

The following 5 entries exist in `sources.bib` but are **not cited** anywhere in the paper via `\cite`, `\citep`, or `\citet`. They do not cause compilation issues but represent unnecessary bibliography entries:

- `wikipedia_nbody` (Wikipedia: N-body simulation)
- `wikipedia_verlet` (Wikipedia: Verlet integration)
- `arborjs_barneshut` (Olsen, Barnes-Hut Algorithm)
- `princeton_barneshut` (Princeton COS 126)
- `grudic2017` (Grudic, Pythonic Barnes-Hut treecode)

### In-text Citation Cross-check

All `\cite`, `\citep`, and `\citet` commands in the paper resolve to valid entries in `sources.bib`. No undefined references or missing bibliography keys.

---

## Results Data Verification

I cross-checked every numerical claim in the paper against raw data files:

| Paper Claim | Data File | Raw Value | Match? |
|-------------|-----------|-----------|--------|
| Euler dt=0.01 final error 47.8% | `energy_benchmark.json` | 0.4775 (47.75%) | Yes |
| Euler dt=0.001 final error 1.93×10⁻² | `energy_benchmark.json` | 0.01926 | Yes |
| Leapfrog dt=0.001 final error 2.34×10⁻¹³ | `energy_benchmark.json` | 2.342×10⁻¹³ | Yes |
| Leapfrog dt=0.01 max error 2.50×10⁻⁹ | `energy_benchmark.json` | 2.500×10⁻⁹ | Yes |
| Verlet dt=0.001 final error 2.15×10⁻¹³ | `energy_benchmark.json` | 2.147×10⁻¹³ | Yes |
| Direct scaling exponent 2.00 | `scaling_benchmark.json` | 2.005 | Yes |
| BH scaling exponent 1.24 | `scaling_benchmark.json` | 1.244 | Yes |
| BH speedup at N=5000: 22.7× | `scaling_benchmark.json` | 80.84/3.56 = 22.7× | Yes |
| BH θ=0.5 median error 0.82% | `barneshut_accuracy.json` | 0.815% | Yes |
| BH θ=0.5 mean error 1.58% | `barneshut_accuracy.json` | 1.578% | Yes |
| Fig-8 max energy error 5.89×10⁻⁹ | `canonical_tests.json` | 5.892×10⁻⁹ | Yes |
| Fig-8 position return 8.93×10⁻⁵ | `canonical_tests.json` | 8.927×10⁻⁵ | Yes |
| Adaptive steps 6,245 | `adaptive_stepping.json` | 6245 | Yes |
| Adaptive energy error 7.84×10⁻⁴ | `adaptive_stepping.json` | 7.836×10⁻⁴ | Yes |
| Fixed steps 31,415 | `adaptive_stepping.json` | 31415 | Yes |
| Softening ε=0.01 bias 1.00×10⁻⁴ | `softening_analysis.json` | 9.999×10⁻⁵ | Yes |
| Baseline Euler 10.1% drift | `baseline_euler.json` | 0.1011 (10.1%) | Yes |

**All numerical claims in the paper are substantiated by the raw data.**

---

## Overall Verdict: **REVISE**

### Justification

The paper is of high quality overall, with strong technical content, thorough experimental evaluation, professional writing, and nearly perfect citations. However, two issues prevent acceptance:

### Required Revisions

1. **Fix `kapela2007` citation title** (Critical — citation accuracy requirement)
   - **File**: `sources.bib`, line 149
   - **Current**: `title = {Computer assisted proofs for nonsymmetric planar choreographies and for stability of the figure-eight}`
   - **Correct**: `title = {Computer assisted proofs for nonsymmetric planar choreographies and for stability of the {E}ight}`
   - This is the only citation error found. All other 14 academic citations are verified correct.

2. **Fix Kepler orbits figure eccentricity mismatch** (Critical — results integrity)
   - **File**: `figures/kepler_orbits.png`
   - **Issue**: The right panel of the figure shows "Eccentric Kepler Orbit (e = 0.7)" but the paper text (Section 5.5.1), the figure caption (Figure 5), and canonical test data (`canonical_tests.json`) all describe an eccentric orbit with **e = 0.5**.
   - **Fix**: Regenerate the Kepler orbits figure with the correct eccentricity e = 0.5 in the right panel, or update the paper text/caption to match the figure if e = 0.7 was intentional.

### Optional Improvements (not required for acceptance)

3. **Remove uncited bibliography entries**: The 5 misc entries (`wikipedia_nbody`, `wikipedia_verlet`, `arborjs_barneshut`, `princeton_barneshut`, `grudic2017`) are not cited in the paper. Consider removing them to keep the bibliography clean.

4. **Energy comparison figure clarity**: The caption for Figure 1 claims it shows "three timestep values" but the visual presentation primarily highlights one curve per integrator. Consider using subplots or clearer visual separation to distinguish the three dt values.

5. **Recompile PDF** after making the above fixes to ensure the bibliography and figures are updated.

### Summary

This is a well-executed computational physics study with solid methodology, reproducible experiments, and honest analysis of limitations. The two required revisions are straightforward to fix. Once addressed, the paper would meet publication standards.

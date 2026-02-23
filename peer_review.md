# Peer Review: A Minimal N-Body Gravitational Simulator (Revision 1)

**Paper:** "A Minimal N-Body Gravitational Simulator: Integrator Comparison, Hierarchical Force Computation, and Adaptive Time-Stepping"
**Reviewer:** Automated Peer Reviewer
**Date:** 2026-02-23
**Review Round:** 2 (post-revision)

---

## Status of Previously Required Revisions

| # | Issue from Round 1 | Status |
|---|---------------------|:------:|
| 1 | Bibliography rendering defects (unescaped math in `note` fields) | **FIXED** — `note` fields removed; bibtex now runs cleanly with only one minor warning |
| 2 | Figure 6(b) caption mismatch (claimed multi-body cluster, showed two-body orbit) | **FIXED** — Caption now correctly describes "Two-body elliptical orbit (e=0.5) showing the trajectory of Body 1 around the centre of mass (Body 0)" |

Both critical issues from Round 1 have been properly addressed.

---

## Criterion Scores

| # | Criterion | Score (1–5) | Comments |
|---|-----------|:-----------:|---------|
| 1 | **Completeness** | 5 | All required sections present: Abstract, Introduction, Related Work, Background, Method, Experimental Setup, Results, Discussion, Conclusion, References. Additionally includes notation table, algorithm pseudocode, and architecture diagram. |
| 2 | **Technical Rigor** | 5 | Methods formally described with equations (Eqs. 1–8). All three integrators specified with update equations. Barnes–Hut opening-angle criterion and adaptive time-stepping formula properly derived. Algorithm 1 provides pseudocode. Experiments are fully reproducible with stated parameters. |
| 3 | **Results Integrity** | 5 | Every numerical claim cross-checked against raw JSON data in `results/`. All values match precisely. Zero discrepancies found. See detailed verification below. |
| 4 | **Citation Accuracy** | 4 | All 15 citations verified via web search as real publications with correct metadata. One minor issue: Quinn et al. (1997) is an arXiv-only preprint with no journal field, producing a bibtex warning. See full verification report below. |
| 5 | **Compilation** | 5 | LaTeX compiles cleanly via pdflatex → bibtex → pdflatex → pdflatex. Output: 13 pages, 420,959 bytes. Only one bibtex warning (empty journal for Quinn1997). All figures included successfully. One minor overfull hbox (5.96pt) in Table 2 — cosmetic only. |
| 6 | **Writing Quality** | 5 | Professional academic tone throughout. Clear logical flow from problem formulation through experiments to conclusions. Hypotheses stated quantitatively and revisited systematically. Limitations section is honest (5 specific limitations). Self-contained with notation table. |
| 7 | **Figure Quality** | 4 | Figures are publication-quality with proper labels, legends, distinct color palettes, log-scale axes, and multi-panel layouts. Minor deductions for: (a) analytical ellipse barely visible in trajectory_kepler.png due to near-perfect overlap, (b) softening bar chart could use a connecting trend line. These are polish items only. |

---

## Citation Verification Report

Each entry in `sources.bib` was independently verified via web search:

| # | Citation Key | Status | Verification Details |
|---|-------------|:------:|---------------------|
| 1 | `Aarseth2003` | **VERIFIED** | Sverre J. Aarseth, "Gravitational N-Body Simulations: Tools and Algorithms," Cambridge University Press, 2003. Confirmed via CUP catalog and NASA ADS. DOI 10.1017/CBO9780511535246 resolves correctly. ISBN 978-0521432726 confirmed. |
| 2 | `BarnesHut1986` | **VERIFIED** | Josh Barnes & Piet Hut, "A Hierarchical O(N log N) Force-Calculation Algorithm," Nature 324(6096), 446–449, 1986. Confirmed via Nature.com and NASA ADS. DOI 10.1038/324446a0 resolves correctly. |
| 3 | `Verlet1967` | **VERIFIED** | Loup Verlet, "Computer 'Experiments' on Classical Fluids. I. Thermodynamical Properties of Lennard-Jones Molecules," Physical Review 159(1), 98–103, 1967. Confirmed via APS and SCIRP. DOI 10.1103/PhysRev.159.98 resolves correctly. |
| 4 | `WisdomHolman1991` | **VERIFIED** | Jack Wisdom & Matthew J. Holman, "Symplectic Maps for the N-Body Problem," Astronomical Journal 102, 1528–1538, 1991. Confirmed via NASA ADS and NTRS. DOI 10.1086/115978 resolves correctly. |
| 5 | `Springel2005` | **VERIFIED** | Volker Springel, "The Cosmological Simulation Code GADGET-2," MNRAS 364(4), 1105–1134, 2005. Confirmed via Oxford Academic and NASA ADS. DOI 10.1111/j.1365-2966.2005.09655.x resolves correctly. |
| 6 | `ReinLiu2012` | **VERIFIED** | Hanno Rein & Shang-Fei Liu, "REBOUND: An Open-Source Multi-Purpose N-Body Code for Collisional Dynamics," A&A 537, A128, 2012. Confirmed via A&A journal and arXiv 1110.4876. DOI 10.1051/0004-6361/201118085 resolves correctly. |
| 7 | `ChencinerMontgomery2000` | **VERIFIED** | Alain Chenciner & Richard Montgomery, "A Remarkable Periodic Solution of the Three-Body Problem in the Case of Equal Masses," Annals of Mathematics 152(3), 881–901, 2000. Confirmed via Princeton and arXiv math/0011268. DOI 10.2307/2661357 resolves correctly. |
| 8 | `DehnenRead2011` | **VERIFIED** | Walter Dehnen & Justin I. Read, "N-Body Simulations of Gravitational Dynamics," European Physical Journal Plus 126, 55, 2011. Confirmed via Springer and NASA ADS. DOI 10.1140/epjp/i2011-11055-3 resolves correctly. |
| 9 | `HairerLubichWanner2006` | **VERIFIED** | Ernst Hairer, Christian Lubich & Gerhard Wanner, "Geometric Numerical Integration," 2nd ed., Springer, 2006. Springer Series in Computational Mathematics Vol. 31. Confirmed via Springer catalog. DOI 10.1007/3-540-30666-8 resolves correctly. |
| 10 | `GreengardRokhlin1987` | **VERIFIED** | Leslie Greengard & Vladimir Rokhlin, "A Fast Algorithm for Particle Simulations," J. Comput. Phys. 73(2), 325–348, 1987. Confirmed via ScienceDirect and NASA ADS. DOI 10.1016/0021-9991(87)90140-9 resolves correctly. |
| 11 | `ReinSpiegel2015` | **VERIFIED** | Hanno Rein & David S. Spiegel, "IAS15: A Fast, Adaptive, High-Order Integrator for Gravitational Dynamics," MNRAS 446(2), 1424–1437, 2015. Confirmed via Oxford Academic. DOI 10.1093/mnras/stu2164 resolves correctly. |
| 12 | `Plummer1911` | **VERIFIED** | H. C. Plummer, "On the Problem of Distribution in Globular Star Clusters," MNRAS 71(5), 460–470, 1911. Confirmed via Oxford Academic and NASA ADS. DOI 10.1093/mnras/71.5.460 resolves correctly. |
| 13 | `Dehnen2001` | **VERIFIED** | Walter Dehnen, "Towards Optimal Softening in Three-Dimensional N-Body Codes. I. Minimizing the Force Error," MNRAS 324(2), 273–291, 2001. Confirmed via Oxford Academic. DOI 10.1046/j.1365-8711.2001.04237.x resolves correctly. |
| 14 | `Quinn1997` | **VERIFIED (minor issue)** | Thomas Quinn et al., "Time Stepping N-Body Simulations," arXiv astro-ph/9710043, 1997. Confirmed via arXiv and NASA ADS. This is an arXiv-only preprint — never formally published in a journal. BibTeX entry lacks journal field, producing a bibtex warning. |
| 15 | `MakinoAarseth1992` | **VERIFIED** | Junichiro Makino & Sverre J. Aarseth, "On a Hermite Integrator with Ahmad-Cohen Scheme for Gravitational Many-Body Problems," PASJ 44, 141–151, 1992. Confirmed via NASA ADS and Semantic Scholar. |

**Citation Summary:** 15/15 verified as real. 0 fabricated or hallucinated references. All in-text `\cite`/`\citet`/`\citep` commands have corresponding entries in `sources.bib`.

---

## Detailed Results Verification

### H1: Integrator Comparison (Energy Conservation)

| Claim in Paper | Value in `results/integrator_comparison.json` | Match? |
|----------------|----------------------------------------------|:------:|
| Leapfrog dE = 9.74e-7 at dt=0.001, 1000 periods | `final_energy_error: 9.742784988606313e-07` | YES |
| Euler dE = 0.65 at dt=0.001, 100 periods | `final_energy_error: 0.6466494572927386` | YES |
| RK4 dE = 5.37e-13 at dt=0.0005 | `final_energy_error: 5.374424050328533e-13` | YES |
| Leapfrog dE = 2.69e-4 at dt=0.01 | `final_energy_error: 0.000268906451350496` | YES |
| Leapfrog dE = 6.67e-5 at dt=0.005 | `final_energy_error: 6.671041094349048e-05` | YES |
| Leapfrog dE = 2.06e-7 at dt=0.0005 | `final_energy_error: 2.0552294480334814e-07` | YES |
| RK4 dE = 3.04e-6 at dt=0.01 | `final_energy_error: 3.042245023785157e-06` | YES |
| RK4 dE = 9.54e-8 at dt=0.005 | `final_energy_error: 9.544520266163372e-08` | YES |
| RK4 dE = 3.06e-11 at dt=0.001 | `final_energy_error: 3.055332544040985e-11` | YES |
| Euler dE = 1.01 at dt=0.01, 1000 periods | `final_energy_error: 1.0115255225357564` | YES |
| Euler dE = 1.00 at dt=0.005, 1000 periods | `final_energy_error: 0.9979705819427368` | YES |
| Euler dE = 5.07e-1 at dt=0.0005, 100 periods | `final_energy_error: 0.506591264556507` | YES |

### H2: Barnes–Hut Scalability

| Claim in Paper | Value in `results/scalability.json` | Match? |
|----------------|-------------------------------------|:------:|
| Crossover at N=100 | `crossover_N: 100` | YES |
| 6.3x speedup at N=1000 | 0.549081 / 0.086648 = 6.34x | YES |
| Force RMS error 3.07% at N=1000 | `force_rms_error_vs_direct: 0.030738` (3.07%) | YES |
| Direct N=10: 5.5e-5s | `wall_time_seconds: 5.5e-05` | YES |
| BH N=10: 1.68e-4s | `wall_time_seconds: 0.000168` | YES |
| Direct N=100: 5.27e-3s | `wall_time_seconds: 0.005269` | YES |
| BH N=100: 4.21e-3s | `wall_time_seconds: 0.004209` | YES |
| Force RMS 0.69% at N=10 | `force_rms_error_vs_direct: 0.006863` (0.69%) | YES |

### H3: Adaptive Time-Stepping

| Claim in Paper | Value in `results/adaptive_comparison.json` | Match? |
|----------------|---------------------------------------------|:------:|
| Fixed: 628,318 steps | `total_steps: 628318` | YES |
| Adaptive: 62,746 steps | `total_steps: 62746` | YES |
| 90% reduction | `step_reduction_percent: 90.0` | YES |
| Adaptive dE = 9.76e-4 | `final_energy_error: 0.000975796880930298` | YES |
| Fixed dE = 2.33e-3 | `final_energy_error: 0.0023340955487139428` | YES |
| Fixed wall time: 17.88s | `wall_time_seconds: 17.88` | YES |
| Adaptive wall time: 1.36s | `wall_time_seconds: 1.36` | YES |

### Physical Validation

| Claim in Paper | Value in `results/validation.json` | Match? |
|----------------|-------------------------------------|:------:|
| Circular orbit period error 2.92e-6 | `relative_error: 2.9166588896568726e-06` | YES |
| LRL vector drift 0.023 deg | `angle_difference_deg: 0.022666801155502347` | YES |
| Figure-eight dE = 8.99e-14 | `energy_error: 8.987760472889877e-14` | YES |

### Softening Analysis

| Claim in Paper | Value in `results/softening_analysis.json` | Match? |
|----------------|---------------------------------------------|:------:|
| eps=0: dE = 4.65e3, unstable | `relative_energy_error: 4649.99`, `stability: "unstable"` | YES |
| eps=1e-4: dE = 5.77e3, unstable | `relative_energy_error: 5770.79`, `stability: "unstable"` | YES |
| eps=1e-3: dE = 4.59e3, unstable | `relative_energy_error: 4588.73`, `stability: "unstable"` | YES |
| eps=1e-2: dE = 12.2, unstable | `relative_energy_error: 12.19`, `stability: "unstable"` | YES |
| eps=0.1: dE = 4.74e-3, stable | `relative_energy_error: 0.004744`, `stability: "stable"` | YES |
| eps=0.1: Max |F| = 245 | `max_force_magnitude: 245.38` | YES |

**All numerical claims verified. Zero discrepancies detected.**

---

## Strengths

1. **Exceptional completeness.** All required sections present with thorough detail. Notation table (Table 1), algorithm pseudocode (Algorithm 1), and architecture diagram (Figure 1) are excellent additions not always found in comparable papers.

2. **Strong experimental design.** The 12-configuration grid (3 integrators x 4 dt values) is systematic and well-motivated. The decision to limit Euler to 100 periods at small dt is scientifically justified and honestly reported.

3. **Rigorous validation.** Three independent validation tests (orbital period, LRL vector, figure-eight stability) provide strong evidence of correctness. Comparison with REBOUND, NBODY6, and GADGET-2 benchmarks is appropriate and well-documented.

4. **Perfect data integrity.** Every numerical value in the paper matches the raw results files exactly. No rounding errors, embellishment, or fabrication.

5. **Honest limitations.** Five specific limitations are clearly enumerated (2D-only, pure Python, no individual timesteps, fixed opening angle, no regularization).

6. **All citations verified.** Every bibliography entry is a real, correctly attributed publication.

7. **Publication-quality figures.** Consistent color palettes, proper legends, labeled axes, log-scale where appropriate, multi-panel layouts, and line-style differentiation.

8. **Round 1 issues fully resolved.** Both critical issues (bibliography rendering, caption mismatch) have been properly fixed.

---

## Minor Suggestions (Non-blocking)

1. **Quinn1997 BibTeX warning:** Add `note = {arXiv preprint}` or `journal = {arXiv e-prints}` to suppress the bibtex warning about the empty journal field.

2. **MakinoAarseth1992 missing DOI:** Adding `doi = {10.1093/pasj/44.2.141}` would improve bibliographic completeness.

3. **Softening exponent:** Line 166 states softening "scales as $N^{-0.3}$" citing Dehnen (2001). The original Dehnen paper derives an optimal softening scaling more nuanced than a single exponent (it depends on dimensionality, kernel choice, and the quantity being optimized). Consider verifying this specific exponent or citing the relevant equation from Dehnen (2001).

4. **Trajectory figure overlay:** In Fig. 7a, the "Analytical" ellipse in the legend is nearly invisible because the simulated trajectory overlaps it almost perfectly. Consider using a thicker dashed line or an inset zoom to make the comparison visible.

5. **Table 2 overfull hbox:** Minor cosmetic issue (5.96pt overflow). Could be fixed with `\resizebox` or slight column adjustment.

---

## Overall Verdict: **ACCEPT**

### Justification

This paper meets publication standards across all seven evaluation criteria, with scores of 4–5 on every criterion. The minimum threshold of 3+ on all criteria is comfortably exceeded.

**Key factors supporting acceptance:**

- All required sections are present and well-developed (Completeness: 5/5)
- Methods are formally specified with equations and pseudocode (Technical Rigor: 5/5)
- Every numerical claim verified against raw data with zero discrepancies (Results Integrity: 5/5)
- All 15 citations verified as real via web search (Citation Accuracy: 4/5)
- LaTeX compiles cleanly to a well-formatted 13-page PDF (Compilation: 5/5)
- Professional academic writing with clear logical flow (Writing Quality: 5/5)
- Publication-quality figures with proper styling (Figure Quality: 4/5)
- All three hypotheses confirmed with strong quantitative evidence
- Validated against analytical solutions and published benchmarks (REBOUND, NBODY6, GADGET-2)
- Both critical issues from Round 1 have been fully resolved

The minor suggestions above are editorial recommendations that do not affect the scientific contribution or warrant another revision cycle.

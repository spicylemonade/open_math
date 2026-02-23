# Peer Review: A Minimal N-Body Gravitational Simulator

**Reviewer:** Automated Peer Reviewer (Nature/NeurIPS standard)
**Date:** 2026-02-23
**Paper:** "A Minimal N-Body Gravitational Simulator: Comparative Analysis of Integrators, Tree Algorithms, and Adaptive Methods"

---

## Scores

| Criterion | Score (1–5) |
|---|---|
| 1. Completeness | 5 |
| 2. Technical Rigor | 5 |
| 3. Results Integrity | 5 |
| 4. Citation Accuracy | 4 |
| 5. Compilation | 5 |
| 6. Writing Quality | 5 |
| 7. Figure Quality | 4 |

---

## 1. Completeness (5/5)

All required sections are present and well-developed:

- **Abstract**: Concise, quantitative summary of all key results.
- **Introduction** (Sec. 1): Clear problem motivation, gap identification, five enumerated contributions.
- **Related Work** (Sec. 2): Covers integrators, N-body codes, tree algorithms, softening, and canonical test problems with appropriate depth.
- **Background and Preliminaries** (Sec. 3): Formal mathematical setup with notation table, equations of motion, Hamiltonian structure, and conserved quantities.
- **Method** (Sec. 4): Detailed descriptions of all algorithms with equations and pseudocode.
- **Experimental Setup** (Sec. 5): Four experiment classes, baselines/metrics, hyperparameter table.
- **Results** (Sec. 6): Six subsections covering all experiments with tables and figures.
- **Discussion** (Sec. 7): Implications, literature comparison table, and four enumerated limitations.
- **Conclusion** (Sec. 8): Five key findings, future work, reproducibility statement.
- **References**: 17 cited works, all present in `sources.bib`.

No sections are missing or perfunctory.

---

## 2. Technical Rigor (5/5)

- All three integrators are defined with explicit equations (Eqs. 4–7) and the Leapfrog has formal pseudocode (Algorithm 1).
- The Hamiltonian structure (Eq. 3) and its separability are stated to motivate symplectic splitting.
- The Barnes–Hut opening angle criterion is formally defined.
- Plummer softening is given as a modified force law (Eq. 6).
- The adaptive time-stepping formula (Eq. 8) is clearly stated with physical motivation.
- The architecture diagram (Fig. 1, TikZ) effectively illustrates the simulator pipeline.
- All hyperparameters are documented in Table 2, and reproducibility is supported by a fixed random seed.

---

## 3. Results Integrity (5/5)

Every numerical claim in the paper was cross-checked against the raw data files in `results/`. All claims match:

| Claim in Paper | Data File Value | Match? |
|---|---|---|
| Euler max \|dE/E\| = 4.78e-1 | 0.47754 (energy_benchmark.json) | Yes |
| Leapfrog max \|dE/E\| = 2.50e-9 | 2.4996e-9 | Yes |
| Velocity Verlet max \|dE/E\| = 2.50e-9 | 2.4996e-9 | Yes |
| Direct scaling exponent = 2.00 | 1.9954 (scaling_benchmark.json) | Yes |
| Barnes–Hut scaling exponent = 1.36 | 1.3585 | Yes |
| BH speedup at N=1024 = 7.1x | 3951.4/555.4 = 7.11 | Yes |
| Circular orbit radius change < 0.0001% | 0.0% (canonical_tests.json) | Yes |
| Elliptical eccentricity change 0.0002% | 2e-6 | Yes |
| Figure-8 position drift = 7.4e-4 | 0.000743 | Yes |
| Figure-8 max \|dE/E\| = 5.89e-7 | 5.8918e-7 | Yes |
| Softening eps=0: 5.87e2 | 586.975 (softening_analysis.json) | Yes |
| Softening eps=0.1: 6.22e-3 | 0.00622 | Yes |
| Adaptive steps = 2975, dE = 3.67e-3 | 2975, 0.00367 (adaptive_dt.json) | Yes |
| Fixed steps = 6283, dE = 2.59e-1 | 6283, 0.2592 | Yes |
| 53% fewer steps | (6283-2975)/6283 = 52.7% | Yes |
| 70x improvement | 0.259/0.00367 = 70.6 | Yes |

No fabricated or inconsistent results found.

---

## 4. Citation Accuracy (4/5)

### Citation Verification Report

All 17 in-text citations were individually verified via web search. Results below:

| BibTeX Key | Cited in Paper? | Title Correct? | Authors Correct? | Year/Venue/DOI Correct? | Verdict |
|---|---|---|---|---|---|
| `aarseth2003` | Yes | Yes | Yes | Yes — Cambridge Univ. Press, 2003, DOI 10.1017/CBO9780511535246 | **VERIFIED** |
| `verlet1967` | Yes | Yes | Yes | Yes — Phys. Rev. 159(1), 98–103, 1967, DOI 10.1103/PhysRev.159.98 | **VERIFIED** |
| `barnes1986` | Yes | Yes | Yes | Yes — Nature 324, 446–449, 1986, DOI 10.1038/324446a0 | **VERIFIED** |
| `wisdom1991` | Yes | Yes | Yes | Yes — Astron. J. 102, 1528–1538, 1991, DOI 10.1086/115978 | **VERIFIED** |
| `springel2005` | Yes | Yes | Yes | Yes — MNRAS 364(4), 1105–1134, 2005, DOI 10.1111/j.1365-2966.2005.09655.x | **VERIFIED** |
| `rein2012` | Yes | Yes | Yes | Yes — A&A 537, A128, 2012, DOI 10.1051/0004-6361/201118085 | **VERIFIED** |
| `yoshida1990` | Yes | Yes | Yes | Yes — Phys. Lett. A 150(5–7), 262–268, 1990, DOI 10.1016/0375-9601(90)90092-3 | **VERIFIED** |
| `hairer2003` | Yes | Yes | Yes | Yes — Acta Numerica 12, 399–450, 2003, DOI 10.1017/S0962492902000144 | **VERIFIED** |
| `dehnen2001` | Yes | Yes | Yes | Yes — MNRAS 324(2), 273–291, 2001, DOI 10.1046/j.1365-8711.2001.04237.x | **VERIFIED** |
| `barnes2012` | Yes | Yes | Yes | Yes — MNRAS 425(2), 1104–1120, 2012, DOI 10.1111/j.1365-2966.2012.21462.x | **VERIFIED** |
| `chin2005` | Yes | Yes | **INCOMPLETE** — Missing co-author C.R. Chen. Actual authors: Chin, S.A. **and Chen, C.R.** | Yes — Celest. Mech. Dyn. Astron. 91, 301–322, 2005, DOI 10.1007/s10569-004-4622-z | **MINOR ERROR** |
| `rein2019` | Yes | Yes | Yes | Yes — MNRAS 489(4), 4632–4640, 2019, DOI 10.1093/mnras/stz2503 | **VERIFIED** |
| `greengard1987` | Yes | Yes | Yes | Yes — J. Comput. Phys. 73(2), 325–348, 1987, DOI 10.1016/0021-9991(87)90140-9 | **VERIFIED** |
| `hernandez2015` | Yes | Yes | Yes | Yes — MNRAS 452(2), 1934–1944, 2015, DOI 10.1093/mnras/stv1439 | **VERIFIED** |
| `plummer1911` | Yes | Yes | Yes | Yes — MNRAS 71, 460–470, 1911, DOI 10.1093/mnras/71.5.460 | **VERIFIED** |
| `chenciner2000` | Yes | Yes | Yes | Yes — Ann. Math. 152(3), 881–901, 2000, DOI 10.2307/2661357 | **VERIFIED** |
| `wang2015` | Yes | Yes | Yes | Yes — MNRAS 450(4), 4070–4080, 2015, DOI 10.1093/mnras/stv817 | **VERIFIED** |

#### Uncited entries in `sources.bib`:

| BibTeX Key | Cited in Paper? | Status |
|---|---|---|
| `bovy2015` | No | Verified correct but unused |
| `scholarpedia_nbody` | No | **INCORRECT** — Lists authors as "Spurzem, Rainer and Berczik, Peter" (2014). Actual authors are **Trenti, Michele and Hut, Piet** (2008). Not cited in paper. |
| `jacobs2019` | No | Verified correct but unused |

### Summary

- **16 of 17 cited references**: Fully verified with matching title, authors, year, venue, and DOI.
- **1 cited reference** (`chin2005`): Missing co-author C.R. Chen. All other fields correct.
- **1 uncited entry** (`scholarpedia_nbody`): Incorrect authors and year (not used in paper).
- **No fabricated or hallucinated citations.**

### Additional text-level note

In Section 2 (Related Work), the paper states "\citet{rein2019} extended REBOUND with optimised high-order symplectic integrators (WHFast)." The Rein et al. (2019) paper actually introduces the SABA family of high-order integrators. WHFast was introduced in an earlier paper (Rein & Tamayo 2015). The parenthetical "(WHFast)" is a slight misattribution.

---

## 5. Compilation (5/5)

- `research_paper.pdf` exists (384 KB) and was compiled successfully.
- The paper uses `natbib`, `pgfplots`, `tikz`, `booktabs`, `algorithm`, `subcaption`, and other standard packages.
- The TikZ architecture diagram compiles correctly within the document.
- All `\includegraphics` references resolve to existing PDF figures in `figures/`.
- Tables are properly formatted with `booktabs` rules.

---

## 6. Writing Quality (5/5)

- Professional academic tone throughout, consistent with a computational physics venue.
- Clear logical flow: problem statement → background → methods → experiments → results → discussion → conclusion.
- Equations are well-numbered and cross-referenced.
- Tables are well-captioned with bold formatting for key results.
- The Discussion section provides honest limitations (4 enumerated items) and a useful literature comparison table.
- Notation is defined in a dedicated table (Table 1) and used consistently.
- No grammatical errors or colloquialisms detected.

---

## 7. Figure Quality (4/5)

Four publication-quality figures are provided (both PNG at 300 DPI and PDF):

1. **Energy error comparison** (`energy_error_comparison.pdf`): Two-panel layout (signed + log-scale absolute). Distinct markers (squares, circles, triangles), distinct colors, proper legends. Clearly shows the 8-order-of-magnitude difference. **Good.**

2. **Scaling benchmark** (`scaling_benchmark.pdf`): Log-log plot with distinct line styles (dashed, dash-dot), annotated power-law exponents in legend, O(N^2) reference line. Proper axis labels. **Good.**

3. **Two-body orbit** (`two_body_orbit.pdf`): Clean circular orbit with center-of-mass marker. Both bodies labeled with masses in legend. **Adequate** — Body 1's trajectory is largely hidden behind Body 2's (equal-mass circular orbit). Could show both trajectories more distinctly, e.g., with partial transparency or offset markers.

4. **Figure-8 trajectory** (`figure_8_trajectory.pdf`): Classic figure-8 shape clearly visible. Three bodies at distinct positions. Proper axis labels. **Good.**

All figures use non-default styling with custom color palettes, proper axis labels, legends, and titles. No plain/default matplotlib bars or basic colors. The minor deduction is for the two-body orbit where equal-mass trajectories overlap, making it hard to distinguish both bodies' paths.

---

## Overall Verdict: **ACCEPT**

### Justification

This paper is a well-executed computational study that meets publication standards across all criteria:

1. **All sections are present and complete** (score 5/5).
2. **Technical methods are rigorously defined** with equations, pseudocode, and a clear architecture diagram (score 5/5).
3. **Every numerical claim was verified** against the raw data — no fabricated or inconsistent results (score 5/5).
4. **All 17 in-text citations are real, verified papers** with correct titles, venues, years, and DOIs. One minor bibliographic error (missing co-author on `chin2005`). No fabricated references (score 4/5).
5. **PDF compiles cleanly** with proper formatting (score 5/5).
6. **Writing is professional and well-structured** (score 5/5).
7. **Figures are publication-quality** with proper labels, legends, and non-default styling (score 4/5).

All criteria score 3 or above. The paper provides a genuine, transparent contribution — a minimal N-body simulator with systematic benchmarks that are reproducible and consistent with published literature.

---

## Minor Revisions Recommended (non-blocking)

While the paper meets acceptance threshold, the following minor corrections would strengthen it:

1. **Fix `chin2005` author field in `sources.bib`**: Add missing co-author. Change `author = {Chin, Siu A.}` to `author = {Chin, Siu A. and Chen, C. R.}`.

2. **Fix or remove `scholarpedia_nbody` entry in `sources.bib`**: The listed authors (Spurzem & Berczik, 2014) are incorrect. The actual authors are Trenti & Hut (2008). Since this entry is not cited in the paper, it should either be corrected or removed.

3. **Correct WHFast attribution** (Sec. 2, line on `rein2019`): Change "(WHFast)" to "(SABA family)" or similar. WHFast was introduced in Rein & Tamayo (2015), not the 2019 paper.

4. **Two-body orbit figure**: Consider making both bodies' trajectories visually distinct (e.g., different line widths, partial transparency, or dashed vs. solid lines) so that Body 1's path is not completely hidden behind Body 2's.

5. **Remove unused bib entries**: `bovy2015`, `scholarpedia_nbody`, and `jacobs2019` are defined in `sources.bib` but never cited in the paper. Consider removing them to keep the bibliography clean.

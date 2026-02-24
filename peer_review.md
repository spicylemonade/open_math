# Peer Review: Comparative Analysis of Numerical Integration Methods for Simple Pendulum Dynamics

**Reviewer:** Automated Peer Review Agent
**Date:** 2026-02-24
**Paper:** "Comparative Analysis of Numerical Integration Methods for Simple Pendulum Dynamics: Symplecticity, Convergence, and Long-Time Stability"

---

## Criterion Scores

| # | Criterion | Score (1-5) | Comments |
|---|-----------|:-----------:|---------|
| 1 | **Completeness** | 5 | All required sections present: Abstract, Introduction, Related Work, Background & Preliminaries, Method, Experimental Setup, Results, Discussion, Conclusion, References. The paper also includes a notation table, algorithm pseudocode, and a system architecture diagram. |
| 2 | **Technical Rigor** | 5 | All four integrators are presented with full mathematical formulations (Eqs. 3-12). RK4 is given as a formal algorithm. The Hamiltonian structure is properly derived. Experimental protocols are clearly specified with exact parameter values. Five distinct experimental protocols ensure comprehensive evaluation. |
| 3 | **Results Integrity** | 5 | Every numerical claim in the paper was cross-checked against the raw data in `results/`. All values match. See detailed verification below. |
| 4 | **Citation Accuracy** | 4 | All 19 references are real, verifiable works. No fabricated citations. However, 2 entries have incorrect publication years, 2 have approximate years, and 2 bib entries are unused. See detailed citation report below. |
| 5 | **Compilation** | 5 | LaTeX compiles without errors. Output: 14 pages, 1.57 MB PDF. Only minor underfull hbox warnings from long URLs in the bibliography. |
| 6 | **Writing Quality** | 5 | Professional academic tone throughout. Clear logical flow from background through experiments to conclusions. Effective use of paragraph headings. Limitations section is honest and thorough. Future work is well-motivated. |
| 7 | **Figure Quality** | 4 | Most figures are publication-quality: distinct markers/linestyles, colorblind-safe palette, proper axis labels with units, legends, and bold titles. The convergence log-log plot and phase portrait are excellent. The `theta_time_euler` and `energy_time_euler` subfigures are adequate but slightly simpler in styling compared to the others. |

**Composite Score: 33/35**

---

## Results Integrity Verification

All numerical claims were verified against raw data files:

### Convergence Study (`results/convergence.json` vs Table 3)
- Forward Euler dt=0.1: paper `2.01e2`, data `201.18` -- **Match**
- RK4 dt=0.001: paper `3.14e-12`, data `3.14e-12` -- **Match**
- Verlet dt=0.01: paper `1.10e-3`, data `1.10e-3` -- **Match**
- Verlet dt=0.005: paper `2.76e-4`, data `2.76e-4` -- **Match**
- Verlet ratio claim (3.99 ~ 4.0): `1.10e-3 / 2.76e-4 = 3.99` -- **Match**

### Long-Time Stability (`results/stability.json` vs Table 4)
- Euler drift: paper `9,090%`, data `9089.88%` -- **Match**
- Euler final energy: paper `475.7 J`, data `475.69 J` -- **Match**
- Symplectic Euler drift: paper `1.27%`, data `1.27%` -- **Match**
- Verlet drift: paper `0.019%`, data `0.019%` -- **Match**
- Initial energy: paper `-5.300 J`, data `-5.300 J` -- **Match**

### Large-Angle Validation (`results/large_angle.json` vs Table 6)
- T_exact: paper `5.1581 s`, data `5.1581 s` -- **Match**
- T_numerical: paper `5.1580 s`, data `5.1580 s` -- **Match**
- Relative error: paper `0.001%`, data `0.00129%` -- **Match** (rounded)
- Elliptic modulus k: paper `0.9975`, data `0.9975` -- **Match**

### Accuracy Study (`results/accuracy.json` vs Table 5)
- RK4 dt=0.01: paper `1.00e-4`, data `1.002e-4` -- **Match**
- Verlet dt=0.01: paper `7.40e-5`, data `7.40e-5` -- **Match**
- Euler dt=0.01: paper `1.21e-2`, data `1.21e-2` -- **Match**

### Performance (`results/performance.csv` vs Table 7)
- Euler dt=0.01 wall time: paper `1.80 ms`, data `1.80 ms` -- **Match**
- RK4 dt=0.01 wall time: paper `5.89 ms`, data `5.89 ms` -- **Match**
- Verlet dt=0.01 wall time: paper `2.87 ms`, data `2.87 ms` -- **Match**

**Conclusion: Zero discrepancies found between paper claims and raw data.**

---

## Citation Verification Report

All 19 entries in `sources.bib` were verified via web search. Each entry was checked for title, authors, year, venue/publisher, and URL/DOI correctness.

### Verified (15/19)

| # | Key | Title | Status |
|---|-----|-------|--------|
| 1 | `wikipedia_pendulum` | Pendulum (mechanics) | **VERIFIED** -- Wikipedia article exists at stated URL |
| 2 | `tedrake_underactuated` | Underactuated Robotics: Ch. 2 -- The Simple Pendulum | **VERIFIED** -- Russ Tedrake, MIT, URL confirmed |
| 3 | `landau_mechanics` | Mechanics (3rd ed.) | **VERIFIED** -- L.D. Landau & E.M. Lifshitz, 1976, Butterworth-Heinemann, Vol. 1 |
| 4 | `wikipedia_symplectic` | Symplectic integrator | **VERIFIED** -- Wikipedia article exists at stated URL |
| 5 | `wikipedia_verlet` | Verlet integration | **VERIFIED** -- Wikipedia article exists at stated URL |
| 6 | `wikipedia_semi_implicit_euler` | Semi-implicit Euler method | **VERIFIED** -- Wikipedia article exists at stated URL |
| 7 | `wikipedia_rk` | Runge--Kutta methods | **VERIFIED** -- Wikipedia article exists at stated URL |
| 8 | `hairer_geometric` | Geometric Numerical Integration (2nd ed.) | **VERIFIED** -- Hairer, Lubich & Wanner, 2006, Springer, DOI: 10.1007/3-540-30666-8 resolves correctly |
| 9 | `hairer_symplectic_lecture` | Lecture 2: Symplectic Integrators | **VERIFIED** -- Ernst Hairer, University of Geneva, URL confirmed |
| 10 | `wikipedia_leapfrog` | Leapfrog integration | **VERIFIED** -- Wikipedia article exists at stated URL |
| 11 | `kencx_pendulum` | pendulum: Simulations of simple and double pendulums | **VERIFIED** -- GitHub repo exists, user kencx confirmed |
| 12 | `scientific_python_pendulum` | Tutorial 1: The simple pendulum | **VERIFIED** -- readthedocs page exists at stated URL |
| 13 | `matplotlib_double_pendulum` | The double pendulum problem | **VERIFIED** -- Official matplotlib gallery example, URL confirmed |
| 14 | `tayo_pendulum_ode` | Simple Pendulum ODESolver using Python | **VERIFIED** -- Benjamin Obi Tayo, Medium, Feb 2019, URL confirmed |
| 15 | `phaseportrait_pkg` | phaseportrait: A simple way to do 2D and 3D phase portraits | **VERIFIED** -- GitHub repo exists, title matches |

### Issues Found (4/19)

| # | Key | Issue | Severity |
|---|-----|-------|----------|
| 1 | `fitzpatrick_classical` | **Year incorrect**: listed as 2012, but the book was originally published in 2005 (Lulu.com) with the online PDF last modified in 2011. No 2012 edition exists. Should be `year = {2011}` or `year = {2005}`. | **Moderate** |
| 2 | `cumming_symplectic` | **Year incorrect**: listed as 2024, but the course notes and copyright notice state Winter 2023 and "(c) Copyright 2023, CC BY SA 4.0". Should be `year = {2023}`. | **Moderate** |
| 3 | `herman_nonlinear_pendulum` | **Year approximate**: listed as 2023, but the LibreTexts compilation date is 02/01/2024 and the author's PDF carries a 2025 copyright. The year is not precisely 2023. | **Minor** |
| 4 | `herman_elliptic_period` | **Year approximate**: listed as 2023, but the original copyright is 2018 with the LibreTexts version dating to ~2022. | **Minor** |

### Unused Entries (2/19)

The following bib entries exist in `sources.bib` but are never cited via `\cite` in the paper:
- `wikipedia_pendulum`
- `wikipedia_leapfrog`

### In-Text Citation Consistency

All 17 `\cite`/`\citep`/`\citet` keys in the paper have corresponding entries in `sources.bib`. **Zero broken citations.**

---

## Figure Quality Assessment

| Figure | File | Quality | Notes |
|--------|------|---------|-------|
| Fig. 1 (Architecture) | TikZ in LaTeX | Excellent | Clean modular diagram with color-coded layers |
| Fig. 2 (Convergence) | `convergence.png` | Excellent | Log-log plot with 4 methods, distinct markers/linestyles, reference slopes, proper legend |
| Fig. 3 (Long-time energy) | `long_time_energy.png` | Excellent | Clear demonstration of energy divergence vs conservation, proper legend |
| Fig. 4a (Theta vs time) | `theta_time_euler.png` | Good | Shows growing amplitude; adequate as subfigure but simpler styling than other plots |
| Fig. 4b (Energy vs time) | `energy_time_euler.png` | Good | Shows monotonic drift; adequate as subfigure but simpler styling |
| Fig. 5 (Phase space) | `phase_space.png` | Excellent | Clean phase portrait with 3 ICs, Greek letter labels, clear closed orbits |
| Fig. 6 (Large angle) | `large_angle.png` | Excellent | Non-sinusoidal waveform with exact period markers and small-angle comparison |
| Fig. 7 (Perf vs accuracy) | `perf_accuracy.png` | Excellent | Log-log Pareto plot with distinct markers per method |

All figures use seaborn/professional styling, 300 DPI, colorblind-safe palette, labeled axes with units, and proper legends.

---

## Overall Verdict: **REVISE** (Minor Revisions)

### Justification

This is a well-written, technically rigorous paper with excellent experimental methodology, fully reproducible results, and no data fabrication. All numerical claims are verified against raw data files. The paper would be publishable with minor corrections.

However, per review policy, the citation year inaccuracies in `fitzpatrick_classical` (2012 should be 2005 or 2011) and `cumming_symplectic` (2024 should be 2023) constitute incorrect citation metadata that must be corrected before acceptance.

### Required Revisions (Mandatory)

1. **Fix `fitzpatrick_classical` year**: Change `year = {2012}` to `year = {2011}` (online PDF last modification date) or `year = {2005}` (original publication).

2. **Fix `cumming_symplectic` year**: Change `year = {2024}` to `year = {2023}` to match the course notes copyright.

3. **Fix `herman_nonlinear_pendulum` year**: Consider changing `year = {2023}` to `year = {2024}` to match the LibreTexts compilation date, or add explicit access date.

4. **Fix `herman_elliptic_period` year**: Consider changing `year = {2023}` to `year = {2018}` (original copyright) or adding an explicit access date.

5. **Remove or cite unused bib entries**: Either cite `wikipedia_pendulum` and `wikipedia_leapfrog` in the paper or remove them from `sources.bib`.

### Suggested Improvements (Optional)

6. **Euler baseline subfigures (Figs. 4a-4b)**: Consider adding grid lines and matching the richer styling of the other figures (marker differentiation, more annotations) for visual consistency.

7. **Theta_time_euler initial conditions**: The figure caption says the baseline uses `theta_0 = 0.05` rad for the accuracy comparison, but the theta_time_euler figure visually shows oscillations around 0.5 rad amplitude. This appears to be from `results/euler_baseline.json` where the theta plot was generated from a different initial condition than the accuracy comparison. Consider clarifying which initial condition is shown, or regenerating with consistent parameters.

8. **Recompile after bib fixes**: After correcting sources.bib, run the full `pdflatex -> bibtex -> pdflatex -> pdflatex` cycle to update the references in the compiled PDF.

---

## Summary

| Criterion | Score |
|-----------|:-----:|
| Completeness | 5/5 |
| Technical Rigor | 5/5 |
| Results Integrity | 5/5 |
| Citation Accuracy | 4/5 |
| Compilation | 5/5 |
| Writing Quality | 5/5 |
| Figure Quality | 4/5 |
| **Total** | **33/35** |

**Verdict: REVISE (Minor Revisions)** -- Fix 4 citation year inaccuracies and remove/cite 2 unused bib entries. No structural or content changes needed. The paper is otherwise ready for acceptance.

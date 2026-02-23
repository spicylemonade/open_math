# Peer Review: Tightening the Practical Polynomial-Time Approximation Ratio for Minimum Dominating Set on Planar Graphs

**Reviewer:** Automated Peer Reviewer (Nature/NeurIPS standard)
**Date:** 2026-02-23
**Paper:** `research_paper.tex` / `research_paper.pdf`

---

## Criterion Scores

| # | Criterion | Score (1-5) |
|---|-----------|:-----------:|
| 1 | Completeness | **5** |
| 2 | Technical Rigor | **3** |
| 3 | Results Integrity | **4** |
| 4 | Citation Accuracy | **2** |
| 5 | Compilation | **5** |
| 6 | Writing Quality | **4** |
| 7 | Figure Quality | **4** |

---

## Overall Verdict: **REVISE**

The paper presents a well-structured and promising contribution combining separator decomposition, LP rounding, and local search for Minimum Dominating Set on planar graphs. The experimental methodology is sound, figures are publication-quality, and the writing is professional. However, **multiple citation errors** (including a fabricated author name) and **technical issues in the proof** require revision before the paper can be accepted. Specific, actionable feedback follows below.

---

## 1. Completeness (Score: 5/5)

All required sections are present and well-organized:

- **Abstract**: Concise, states contributions and key results.
- **Introduction** (Section 1): Clearly motivates the problem and lists four contributions.
- **Related Work** (Section 2): Comprehensive survey across 5 subsections covering PTAS variants, greedy approaches, LP methods, distributed algorithms, and FPT/practical solvers.
- **Background** (Section 3): Formal definitions, notation table, and LP relaxation.
- **Method** (Section 4): Four strategies with pseudocode (Algorithms 1-3), theoretical analysis with theorem/lemmas/proofs, and architecture diagram.
- **Experimental Setup** (Section 5): Benchmarks, algorithms, metrics, hardware, hyperparameters, and statistical methods.
- **Results** (Section 6): Ratio comparison, distribution, exact validation, statistical significance, scalability, and prior work comparison.
- **Discussion** (Section 7): Implications, 5 limitations, and comparisons with Baker's PTAS and distributed algorithms.
- **Conclusion** (Section 8): Summary and 5 future work directions.
- **References**: 23 cited entries from sources.bib.

No missing sections. The paper follows a clear, logical structure.

---

## 2. Technical Rigor (Score: 3/5)

**Strengths:**
- Three algorithms presented with full pseudocode (Algorithms 1-3).
- LP formulation clearly specified with decision variables, objective, and constraints.
- Theorem 1 provides a formal worst-case bound: |D| <= 4*OPT + 3*sqrt(n).
- Statistical analysis uses appropriate non-parametric tests (Wilcoxon signed-rank).
- Experimental design with fixed seeds and controlled hyperparameters.

**Issues requiring revision:**

1. **Misattribution of the Planar Separator Theorem (Line 263):** The paper cites `\cite{GareyJohnson1979}` for the planar separator theorem ("every n-vertex planar graph has a separator S of size at most 2*sqrt(2n)"). This result is from **Lipton and Tarjan (1979)**, *"A Separator Theorem for Planar Graphs"*, SIAM J. Appl. Math. Garey and Johnson's book discusses NP-completeness but does not prove the separator theorem. A new bibliography entry for Lipton & Tarjan must be added and cited here.

2. **Sloppy reasoning in Theorem 1 proof (Lines 475-479):** The argument for the multiplicative ratio <= 5 when OPT >= 9 is poorly justified:
   - "4 + 3*sqrt(n)/OPT <= 4 + 3*sqrt(n)/9 <= 5 whenever n <= 9" -- This is trivially true but then the argument for n > 9 claims "OPT >= n/6 (Euler's formula on connected planar graphs with bounded degree)", which is not generally true. A planar graph can have a star with OPT = 1 and n arbitrary. The lower bound OPT >= n/(Delta+1) requires Delta to be bounded. The proof needs a cleaner case analysis or additional assumptions stated explicitly.

3. **Lemma 2 proof gap:** The claim "sum_i OPT(C_i) <= OPT" requires that the restriction of an optimal solution for G to each C_i dominates C_i. This is not immediate because vertices in C_i may be dominated by vertices in S in the global solution but not in the subproblem. The proof sketch acknowledges S is in the solution but does not formally argue that OPT restricted to C_i is a valid dominating set of C_i (some vertices in C_i near the boundary may only be dominated by S-vertices in the global optimum).

4. **Table 4 inconsistency:** The paper claims "36 instances where exact ILP-optimal solutions were computable (n <= 200)" and reports "36/36 (100%)" optimality for Hybrid MDS. However, the benchmark suite (Table 2) includes instances with n up to 10,000. The exact validation appears to be on all 36 instances (including small ones where ILP threshold T=200 applies), but this should be clarified -- are all 36 benchmark instances small enough for ILP, or only a subset?

---

## 3. Results Integrity (Score: 4/5)

**Verified claims:**
- The bar chart (ratio_comparison.png) values match Table 3: Hybrid = 1.101, Separator = 1.183, Planar LP = 1.175, Greedy = 1.234, etc.
- The scalability data in `results/scalability.json` is consistent with Table 6 (runtime 28.38s at n=1K, 36.10s at n=5K, 60.27s at n=10K for Hybrid).
- Baseline results in `results/baseline_results.json` show valid dominating sets (all `"valid": true`).
- Full results in `results/full_results.json` show consistent solution sizes and runtimes.
- Exact validation figure shows Hybrid and Separator both at 1.000 mean ratio.
- Statistical significance claims (6/6 Wilcoxon tests) are supported by Table 5 data.

**Minor concerns:**
- The paper claims "222 data points across 9 algorithms and 36 instances" (Section 5.3). Since 9 * 36 = 324, this implies not all algorithms were run on all instances (e.g., LP-based methods were skipped for large instances, Baker PTAS variants not run on all sizes). This is reasonable but should be stated more transparently.
- The scalability analysis (Table 6, Figure 4) references instances up to n=100,000, but the benchmark suite only goes to n=10,000. The scalability experiments appear to be separate from the main benchmark. This separation should be made explicit.

---

## 4. Citation Accuracy (Score: 2/5) -- CRITICAL

### Citation Verification Report

**Total entries in sources.bib: 27**
**Entries cited in paper: 23**
**Entries not cited (unused): 4** (WilliamsonShmoys2011, BonamyCookGroenlandWesolek2021, FominLokshtanovSaurabhThilikos2010, FominLokshtanovSaurabhThilikos2018)

#### Verified Citations (19/23 cited entries correct):

| # | BibTeX Key | Status | Notes |
|---|-----------|--------|-------|
| 1 | Baker1994 | VERIFIED | Title, authors, JACM vol 41(1), pp 153-180, DOI all correct |
| 2 | DemaineHajiaghayi2005 | VERIFIED | Title, authors, SODA 2005, pp 590-601 all correct |
| 3 | FominLokshtanovRamanSaurabh2011 | VERIFIED | arXiv:1005.5449, authors correct. Minor: arXiv posted 2010, SODA proceedings 2011 |
| 4 | MarzbanGu2013 | VERIFIED | Algorithms vol 6(1), pp 43-59, DOI 10.3390/a6010043 all correct |
| 5 | Dvorak2013 | VERIFIED | EJC vol 34(5), pp 833-840, DOI correct |
| 6 | Dvorak2019 | VERIFIED | J. Graph Theory vol 91(2), pp 162-173, DOI correct |
| 7 | BansalUmboh2017 | VERIFIED | IPL vol 122, pp 21-24, DOI correct |
| 8 | MorganSolomonWein2021 | VERIFIED | DISC 2021, LIPIcs vol 209, pp 33:1-33:19, DOI correct |
| 9 | LenzenOswaldWattenhofer2008 | VERIFIED | SPAA 2008, pp 46-54, DOI correct |
| 10 | LenzenPignoletWattenhofer2013 | VERIFIED | Distributed Computing vol 26, pp 119-137, DOI correct |
| 11 | CzygrinowHanckowiak2008 | VERIFIED | DISC 2008, LNCS 5218, pp 78-92, DOI correct |
| 12 | HilkeLenzenSuomela2014 | VERIFIED | PODC 2014, pp 344-346, DOI correct |
| 13 | HeydtKublenzOdMSiebertzVigny2025 | VERIFIED | EJC vol 123, article 103773, DOI correct |
| 14 | AlberBodlaenderFernauKloksNiedermeier2002 | VERIFIED | Algorithmica vol 33, pp 461-493, DOI correct |
| 15 | AlberFellowsNiedermeier2004 | VERIFIED | JACM vol 51(3), pp 363-384, DOI correct |
| 16 | FominThilikos2004 | VERIFIED | ICALP 2004, LNCS 3142, pp 581-592, DOI correct |
| 17 | GareyJohnson1979 | VERIFIED | Classic textbook, W. H. Freeman, 1979 |
| 18 | Vazirani2001 | VERIFIED | Springer textbook, DOI correct |
| 19 | PACE2025UzL | VERIFIED | IPEC 2025, LIPIcs vol 358, pp 39:1-39:4, DOI correct |

#### Incorrect Citations (4/23 cited entries with errors):

| # | BibTeX Key | Status | Error Details |
|---|-----------|--------|---------------|
| 20 | **Sun2021** | **INCORRECT** | **FABRICATED AUTHOR NAME.** The bib entry lists author as "Kevin Sun" -- the actual author is **Hao Sun** (University of Waterloo). Additionally: LNCS volume should be **12982** (not 13059); pages should be **39-47** (not 39-53). The DOI (10.1007/978-3-030-92702-8_3) itself resolves correctly. Verified via SpringerLink and DBLP. |
| 21 | **Siebertz2019** | **INCORRECT** | **WRONG DOI.** The DOI `10.1016/j.ipl.2019.01.001` resolves to a completely different paper ("On the VC-dimension of unique round-trip shortest path systems"). The correct DOI is **10.1016/j.ipl.2019.01.006**. Title, author, journal, volume, pages, and year are all correct. |
| 22 | **PACE2025report** | **INCORRECT** | Page range error: bib says `32:1--32:22`, actual publication on Dagstuhl DROPS is **32:1--32:17**. All other fields correct. |
| 23 | **PACE2025BadDSMaker** | **INCORRECT** | Page range error: bib says `35:1--35:4`, actual publication on Dagstuhl DROPS is **35:1--35:5**. All other fields correct. |

#### Unused Bib Entries (not cited in paper):

| # | BibTeX Key | Status | Notes |
|---|-----------|--------|-------|
| 24 | WilliamsonShmoys2011 | VERIFIED | Correct but unused in paper |
| 25 | **BonamyCookGroenlandWesolek2021** | **INCORRECT** | **FABRICATED AUTHORS.** Bib lists 5 authors including "Josse van den Heuvel" and "Jirka Matoušek" -- the actual paper has 4 authors: Marthe Bonamy, Linda Cook, **Carla Groenland**, and Alexandra Wesolek. Not cited in the paper but still an error in sources.bib. |
| 26 | FominLokshtanovSaurabhThilikos2010 | VERIFIED | Correct but unused |
| 27 | FominLokshtanovSaurabhThilikos2018 | VERIFIED | Correct but unused |

#### Additional Citation Issue:

- **Missing citation:** The Planar Separator Theorem (Section 3, line 263) is cited as `\cite{GareyJohnson1979}`. The correct citation is **Lipton, R.J. and Tarjan, R.E. (1979), "A Separator Theorem for Planar Graphs", SIAM J. Appl. Math., 36(2), pp 177-189**. This reference is entirely missing from sources.bib.

**Summary:** 4 of 23 cited entries contain errors; 1 has a fabricated author name (Sun2021); 1 unused entry has fabricated authors (BonamyCookGroenlandWesolek2021); 1 critical citation is missing entirely (Lipton-Tarjan). This is below publication standards.

---

## 5. Compilation (Score: 5/5)

- `research_paper.pdf` exists (1.65 MB), compiled successfully.
- All LaTeX packages load correctly.
- TikZ architecture diagram (Figure 1) renders properly.
- All 5 external figures (`ratio_comparison.png`, `ratio_distribution.png`, `scalability.png`, `ratio_vs_size.png`, `exact_validation.png`) are included and display correctly.
- Tables are well-formatted with `booktabs` styling.
- Algorithm environments render correctly.
- Theorem/Lemma/Proof environments display properly.
- No compilation warnings visible in output.

---

## 6. Writing Quality (Score: 4/5)

**Strengths:**
- Professional academic tone throughout.
- Clear, logical flow from motivation through method, experiments, and discussion.
- Effective use of `\paragraph{}` for sub-section organization.
- Limitations section is honest and thorough (5 specific limitations).
- Good use of theorem environments for formal claims.
- Consistent notation (established in Table 1 and used throughout).

**Minor issues:**
- The phrase "factor-of-40 gap" in Section 7.3 (line 907) should be "factor-of-4 gap" (theory ratio ~4 vs empirical 1.101, not a factor of 40).
- Some sentences are overly long, particularly in the Introduction.
- The paper would benefit from a brief comparison of the additive vs. multiplicative approximation guarantee (the additive 3*sqrt(n) term makes the bound incomparable to pure multiplicative bounds for small OPT).

---

## 7. Figure Quality (Score: 4/5)

All figures demonstrate publication-quality standards:

- **Figure 2 (ratio_comparison.png):** Bar chart with distinct colors per algorithm, error bars, value annotations above bars, dashed optimality baseline at 1.0. Well-designed.
- **Figure 3 (ratio_distribution.png):** Violin plots with mean/median markers, individual data points overlaid, legend. Effective visualization of distributional differences.
- **Figure 4 (scalability.png):** Dual-panel log-log plot (runtime + memory) with reference lines for O(n) and O(n^2), distinct markers per algorithm. Clear and informative.
- **Figure 5 (ratio_vs_size.png):** Scatter plot with log-scale x-axis, distinct marker shapes and colors per algorithm. Good for showing trends across sizes.
- **Figure 6 (exact_validation.png):** Dual-panel with hatched bars for worst case, optimality rate bar chart. Professional presentation.
- **Figure 1 (TikZ architecture):** Clean algorithmic pipeline diagram with color-coded stages.

**Minor suggestions:**
- The algorithm_pipeline.png figure (generated separately) is not included in the paper -- the TikZ version (Figure 1) is used instead. Consider removing the unused PNG or referencing it in supplementary material.
- Figure 5 (ratio_vs_size) could benefit from slightly larger marker sizes for the Hybrid algorithm to make it more visually prominent.

---

## Required Revisions (Actionable)

### Critical (must fix):

1. **Fix Sun2021 citation:** Change author from "Kevin Sun" to "Hao Sun". Change LNCS volume from 13059 to 12982. Change pages from 39-53 to 39-47.

2. **Fix Siebertz2019 DOI:** Change from `10.1016/j.ipl.2019.01.001` to `10.1016/j.ipl.2019.01.006`.

3. **Fix PACE2025report pages:** Change from `32:1--32:22` to `32:1--32:17`.

4. **Fix PACE2025BadDSMaker pages:** Change from `35:1--35:4` to `35:1--35:5`.

5. **Fix BonamyCookGroenlandWesolek2021 authors:** Replace `Marthe Bonamy and Linda Cook and Josse van den Heuvel and Jirka Matou\v{s}ek and Alexandra Wesolek` with `Marthe Bonamy and Linda Cook and Carla Groenland and Alexandra Wesolek`.

6. **Add missing Lipton-Tarjan citation:** Add a new bib entry for Lipton, R.J. and Tarjan, R.E. (1979), "A Separator Theorem for Planar Graphs", SIAM J. Appl. Math., 36(2), pp 177-189, DOI: 10.1137/0136016. Replace `\cite{GareyJohnson1979}` on line 263 with the new Lipton-Tarjan key.

7. **Fix Theorem 1 proof:** The argument on lines 475-479 for the multiplicative ratio <= 5 when OPT >= 9 relies on the unjustified claim OPT >= n/6. Either:
   - State the bound as purely additive: |D| <= 4*OPT + 3*sqrt(n), without claiming multiplicative ratio 5.
   - Or provide a rigorous case analysis for when OPT >= 9 implies the ratio <= 5 (accounting for graphs with small OPT but large n, like sparse planar graphs).

### Recommended (should fix):

8. **Clarify data point count:** Explain why 222 (not 324) data points were collected -- which algorithms were omitted on which instance sizes.

9. **Fix "factor-of-40" typo** in Section 7.3 (line 907): Should be "factor-of-4" or "gap of approximately 4x".

10. **Clarify exact validation scope:** State explicitly which 36 instances were used for ILP-optimal comparison (presumably the 12 smallest instances at n=50 and n=100 across 3 families x 2 trials = 12... but the paper says 36/36).

11. **Recompile PDF** after all citation fixes to ensure bibliography renders correctly.

---

## Summary

This paper makes a meaningful practical contribution by combining established algorithmic techniques (separator decomposition, LP rounding, local search) into a hybrid algorithm for MDS on planar graphs that achieves strong empirical performance. The experimental methodology is sound, the benchmark design is reasonable, and the figures are publication-quality. However, the citation errors -- particularly the fabricated author name in Sun2021 and the misattribution of the Planar Separator Theorem -- are serious issues that must be corrected. The theoretical proof also needs tightening. After these revisions, the paper would be suitable for acceptance.

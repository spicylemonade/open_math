# Peer Review: Learned Heuristics for the Asymmetric Traveling Salesman Problem on Real Road Networks

**Reviewer:** Automated Peer Review (Nature/NeurIPS standard)
**Date:** 2026-02-25
**Paper:** `research_paper.tex` / `research_paper.pdf`

---

## Overall Verdict: REVISE

The paper addresses a genuinely important gap—applying learned TSP heuristics to asymmetric road-network settings—and is well-written with a professional structure. However, **critical issues** in citation accuracy (one citation has entirely fabricated authors), benchmark integrity (the "three city" benchmarks are scaled copies of the same data), and figure quality (no error bars, basic matplotlib styling) prevent acceptance. Specific, actionable feedback is provided below.

---

## Criterion Scores

| # | Criterion | Score (1–5) | Summary |
|---|-----------|:-----------:|---------|
| 1 | Completeness | **4** | All required sections present and substantive |
| 2 | Technical Rigor | **3** | Methods well-described with equations, but experimental design has critical flaws |
| 3 | Results Integrity | **2** | Paper numbers match CSV data, but "three city" benchmarks are scaled copies of one matrix |
| 4 | Citation Accuracy | **2** | One citation has completely wrong authors; multiple others have missing co-authors or wrong first author |
| 5 | Compilation | **4** | PDF compiles and is well-formatted (600 KB, proper typesetting) |
| 6 | Writing Quality | **4** | Professional academic tone, clear structure, excellent use of LaTeX |
| 7 | Figure Quality | **2** | Missing error bars, basic matplotlib styling, scaling curve has only 2 data points |

**Aggregate: 3.0 — Below threshold for ACCEPT (requires 3+ on ALL criteria)**

---

## Detailed Evaluation

### 1. Completeness (4/5)

All required sections are present: Abstract, Introduction (§1), Related Work (§2), Problem Formulation (§3), Method (§4), Experimental Setup (§5), Results (§6), Discussion (§7), Conclusion (§8), and References. The paper also includes a notation table, four hypotheses, two algorithms in pseudocode, and a comprehensive literature comparison table. The TikZ architecture diagram (Figure 1) and GNN layer diagram (Figure 2) are well-crafted.

**Minor gap:** No dedicated "Future Work" section (briefly addressed in Conclusion paragraph).

### 2. Technical Rigor (3/5)

**Strengths:**
- The directed GNN architecture is properly formalized with attention equations (Eq. 4–5), gated updates, and edge update rules.
- The RL local search design (state/action/reward) is clearly specified with a compact 75-action Q-table.
- The hybrid pipeline is formalized as Algorithm 2 with clear stage descriptions and time allocation.
- The training progression (Table 3) honestly reports failure to meet the precision target (0.38 vs 0.85).

**Weaknesses:**
- The "LKH-style" baseline is a Python multi-restart 2-opt + or-opt implementation, **not** the actual LKH-3 binary. This makes all comparisons against "LKH-style" fundamentally uninformative about how the hybrid would perform against LKH-3, which is ~100× faster. The paper acknowledges this (§7.3) but the framing throughout still implies comparison with LKH-3.
- Only 3 random seeds were used (42, 43, 44) instead of the planned 10, severely limiting statistical power.
- The hybrid at T=1s simply returns the nearest-neighbor solution (identical costs in CSV), meaning the learned components provide zero value under tight time budgets.
- The statistical test for the key comparison (hybrid vs LKH at 30s) yields p=0.051, which is NOT significant at α=0.05.

### 3. Results Integrity (2/5)

**Data consistency verified:** All numbers reported in Tables 4–8 of the paper match the corresponding CSV files (`full_comparison.csv`, `ablation_results.csv`, `scalability_results.csv`, `statistical_tests.md`). The mean costs, gaps, and statistical test values are reproducible from the raw data.

**CRITICAL ISSUE — Benchmark Integrity:** The "three city" benchmarks (Manhattan, London, Berlin) are **scaled copies of the same cost matrix**, not genuinely distinct road networks:

| Solver (200-stop, 30s, seed 42) | Manhattan | London | Berlin | London/Manhattan | Berlin/Manhattan |
|---|---|---|---|---|---|
| Nearest Neighbor | 8,334.44 | 11,112.58 | 13,890.73 | **1.333333** (=4/3) | **1.666666** (=5/3) |
| LKH-style | 7,075.00 | 9,433.33 | 11,791.66 | **1.333333** (=4/3) | **1.666666** (=5/3) |
| Farthest Insertion | 7,504.61 | 9,994.93 | 12,493.66 | 1.3318 (≈4/3) | 1.6648 (≈5/3) |

The exact 4/3 and 5/3 ratios across deterministic solvers (NN, LKH-style) conclusively demonstrate that the London and Berlin matrices are the Manhattan matrix multiplied by a constant. The paper claims benchmarks "spanning three major cities" and instances "drawn from at least 3 distinct metro areas" but this is a single topology scaled. This means:
- The 9 "paired comparisons" in the Wilcoxon tests are really only 3 independent observations × 3 seeds.
- All cross-city generalization claims are vacuous.
- The benchmark suite has effectively only one city's topology, not three.

**Additional concern:** The ablation study (Table 6) shows the full hybrid (D, mean cost 9,545) is **worse** than the LKH-style baseline (A, mean cost 9,429). The hybrid only "beats" LKH-style at 30s (Table 4) because OR-Tools (a C++ solver) does the heavy lifting, not the learned components. The paper's positive framing obscures this.

### 4. Citation Accuracy (2/5)

26 entries in `sources.bib` were verified via web search. 22 in-text citation keys were cross-referenced against the bibliography. All in-text `\cite` keys have matching bib entries.

#### Citation Verification Report

| # | Citation Key | Status | Details |
|---|---|---|---|
| 1 | `applegate2006traveling` | **VERIFIED** | Book exists. Authors, title, publisher, year all correct. |
| 2 | `helsgaun2000effective` | **VERIFIED** | EJOR 2000, vol 126(1), pp 106–130. All details correct. |
| 3 | `helsgaun2009general` | **VERIFIED** | Math. Prog. Comp. 2009, vol 1(2–3), pp 119–163. All correct. |
| 4 | `helsgaun2017extension` | **VERIFIED** | Roskilde University tech report, 2017. All correct. |
| 5 | `perron2023ortools` | **ISSUES** | Paper exists but lists only 2 of 6 authors (missing Cuvelier, Didier, Gay, Mohajeri). Venue is ROADEF 2023, not "Google Research." |
| 6 | `coupey2018vroom` | **ISSUES** | Conference listing credits only Julien Coupey as presenter. Co-authors Nicola and Vidal could not be verified for this specific 2018 SotM talk. |
| 7 | `vroom_github` | **VERIFIED** | GitHub repository. Not cited in paper (unused bib entry). |
| 8 | `cook2025korea` | **VERIFIED** | Project web page. Authors, title, URL all correct. |
| 9 | `christofides1976worst` | **VERIFIED** | CMU Report 388, 1976. Not cited in paper (unused bib entry). |
| 10 | `held1962dynamic` | **VERIFIED** | J. SIAM 1962, vol 10(1), pp 196–210. Bib entry has correct full journal name. Not cited in paper. |
| 11 | `luxen2011realtime` | **VERIFIED** | ACM SIGSPATIAL 2011, pp 513–516. All correct. |
| 12 | `osrm_github` | **VERIFIED** | GitHub repository. Not cited in paper (unused bib entry). |
| 13 | `kool2019attention` | **VERIFIED** | ICLR 2019. Authors, title, venue all correct. |
| 14 | `kwon2020pomo` | **VERIFIED** | NeurIPS 2020. All 6 authors and details correct. |
| 15 | `xin2021neurolkh` | **VERIFIED** | NeurIPS 2021. All 4 authors and details correct. |
| 16 | `zheng2021vsrlkh` | **VERIFIED** | AAAI 2021, pp 12445–12452. All details correct. |
| 17 | `zheng2022reinforced` | **MINOR ISSUE** | Paper exists. Year listed as 2022 but volume 260 published January 2023. DOI correct. |
| 18 | `lischka2024great` | **ISSUES** | Paper exists on arXiv (2408.16717). Missing co-author **Filip Rydin** (5 authors, not 4). |
| 19 | `embedlkh2025` | **MINOR ISSUE** | Paper exists on OpenReview. Listed as "Anonymous" but actual authors (Xiong, Pan, Huang, Xia, Yan) are now publicly visible. |
| 20 | `wang2025mabb` | **MINOR ISSUE** | Paper exists. DOI assigned 2025 but journal volume officially published 2026. |
| 21 | `liu2025unics` | **ISSUES** | Paper exists (arXiv 2501.14285). **Wrong first author**: Liu Shengcai is 4th author, not 1st. First author is **Haoze Lv**. Missing authors: Wenjie Chen, Zhiyuan Wang, Ke Tang. |
| 22 | `pan2025dualopt` | **FABRICATED AUTHORS** | Paper exists (arXiv 2501.08565, AAAI 2025). **Entire author list is wrong.** Listed: Pan, Xuanhao; Jin, Yan; Ding, Yuandong; Feng, Mingxiao; Zhao, Li; Song, Lei; Bian, Jiang. **Actual authors: Zhou, Shipei; Ding, Yuandong; Zhang, Chi; Cao, Zhiguang; Jin, Yan.** The author list was apparently copied from `pan2023htsp` (H-TSP). Pan Xuanhao is NOT an author of DualOpt. |
| 23 | `reinelt1991tsplib` | **VERIFIED** | ORSA J. Computing 1991, vol 3(4), pp 376–384. All correct. |
| 24 | `ascheuer2001solving` | **VERIFIED** | Math. Programming 2001, vol 90(3), pp 475–506. All correct. |
| 25 | `boeing2017osmnx` | **VERIFIED** | CEUS 2017, vol 65, pp 126–139. All correct. |
| 26 | `pan2023htsp` | **VERIFIED** | AAAI 2023. All 7 authors and details correct. |

**Summary:** 17 fully verified, 3 minor issues, 4 significant issues (missing/wrong authors), **1 citation with fabricated author list** (`pan2025dualopt`).

### 5. Compilation (4/5)

The PDF (600 KB) exists and is properly formatted. The LaTeX source uses appropriate packages (natbib, booktabs, algorithm, pgfplots, tikz) and compiles without apparent errors. TikZ diagrams for the architecture and GNN layer are rendered inline. Figures are included as external PNGs.

**Minor:** No PDF versions of figures for vector-quality printing.

### 6. Writing Quality (4/5)

The paper is well-written with professional academic tone. The logical flow from problem motivation through method to results is clear. Equations are properly numbered and referenced. Tables are well-formatted with booktabs. The notation table (Table 1) aids readability. The hypothesis-driven structure provides clear evaluation criteria.

**Minor issues:**
- The paper uses "LKH-style" throughout, which could mislead readers into thinking this is LKH-3 rather than a Python reimplementation.
- Some claims in the abstract ("outperforming a multi-restart LKH-style baseline") are technically true but practically misleading given the baseline is ~100× slower than actual LKH-3.

### 7. Figure Quality (2/5)

**Issues requiring revision:**

1. **No error bars or confidence intervals** on any bar chart (Figures 1, 4, 6). With 3 seeds per condition, error bars are essential to show variance. This is below publication standard.

2. **Scaling curve (Figure 2) has only 2 data points** per solver line (50 and 200 stops). Two points cannot characterize scaling behavior. The scalability CSV has data for 50, 200, 500, 1000, 2000—all of these should be plotted.

3. **Basic matplotlib styling:** Figures use standard seaborn-paper style with no professional refinements. Specifically:
   - Default bar widths and spacing
   - No hatching or patterns for print accessibility
   - 150 DPI raster PNGs (should be vector PDF or 300+ DPI)
   - No grid lines for reading precise values

4. **Gap histogram (Figure 3):** Bin edges produce misleading visual impression. Several bins at 0.5–0.8% gap are not immediately apparent.

5. **Traffic impact (Figure 6):** Color coding (blue=off-peak, red=peak) is used but not explained in the figure itself. No y-axis unit label ("seconds" vs generic "Tour Cost").

---

## Specific Revision Requirements

### Must Fix (blocking acceptance)

1. **Fix `pan2025dualopt` citation:** Replace fabricated author list with correct authors: Zhou, Shipei; Ding, Yuandong; Zhang, Chi; Cao, Zhiguang; Jin, Yan.

2. **Fix other citation errors:**
   - `liu2025unics`: Correct first author to Lv, Haoze; add all 5 authors.
   - `lischka2024great`: Add missing co-author Filip Rydin.
   - `perron2023ortools`: Add 4 missing co-authors; fix venue to ROADEF 2023.
   - `coupey2018vroom`: Verify co-authors or list only Coupey.

3. **Disclose benchmark homogeneity:** Either (a) generate genuinely distinct city benchmarks with different topologies, or (b) clearly state that London and Berlin are scaled versions of Manhattan and adjust all claims accordingly. Remove language like "three major cities" and "cross-city" if using scaled copies. Recompute statistical tests with correct effective sample size.

4. **Add error bars to all bar charts** (Figures 1, 4, 6) showing standard deviation or 95% CI across seeds.

5. **Regenerate scaling curve (Figure 2)** using all available data points (50, 200, 500, 1000, 2000 stops) from `scalability_results.csv`.

### Should Fix (strengthening the paper)

6. **Increase random seeds** to at least 5 (preferably 10) to improve statistical power. The key comparison (hybrid vs LKH at 30s) has p=0.051, which is borderline. More seeds could resolve this.

7. **Clarify hybrid T=1s behavior:** The hybrid returns exact NN cost at T=1s across all instances. Either fix the fallback mechanism or explicitly acknowledge this limitation in the Results section (not buried in Discussion).

8. **Temper claims about "outperforming LKH":** The ablation shows full hybrid (D=9,545) is worse than LKH-style (A=9,429). The 30s advantage comes from OR-Tools initialization, not learned components. The paper should clearly attribute the improvement to OR-Tools + learned refinement, not imply the learned components independently beat LKH.

9. **Generate vector figures:** Replace 150 DPI PNGs with PDF vector figures or at minimum 300 DPI PNGs.

10. **Remove unused bib entries:** `vroom_github`, `osrm_github`, `christofides1976worst`, `held1962dynamic` are defined in `sources.bib` but never cited in the paper.

### Optional Improvements

11. Add a TSPLIB-ATSP comparison (e.g., ftv44, ftv70) alongside the synthetic benchmarks to provide a point of contact with published results.

12. Discuss what happens when the hybrid's GNN is trained on one genuine city and tested on another (transfer learning experiment).

13. The RL agent's 75-action Q-table is interesting but underexplored. A learning curve or Q-value heatmap would strengthen the RL contribution.

---

## Summary

This paper makes a legitimate contribution by adapting GNN-guided candidate generation to asymmetric road-network TSP—an underexplored and practically important setting. The writing is strong, the method is clearly described, and the hypothesis-driven evaluation is commendable. However, the fabricated author list on `pan2025dualopt`, multiple other citation inaccuracies, the discovery that "three city" benchmarks are scaled copies of one matrix, and the absence of error bars on figures collectively fall below the publication threshold. A revision addressing these issues—particularly genuine multi-city benchmarks, corrected citations, and professional figure quality—would substantially strengthen the submission.

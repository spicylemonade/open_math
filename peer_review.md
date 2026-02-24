# Peer Review: Better Heuristics for the Traveling Salesman Problem on Real Road Networks

**Reviewer:** Automated Peer Review (Nature/NeurIPS Standard)
**Date:** 2026-02-24
**Paper:** "Better Heuristics for the Traveling Salesman Problem on Real Road Networks: A Hybrid GNN-Guided Approach"

---

## Criterion Scores

| # | Criterion | Score (1-5) | Summary |
|---|-----------|:-----------:|---------|
| 1 | Completeness | **5** | All required sections present and well-structured |
| 2 | Technical Rigor | **4** | Solid methodology with honest limitations; underpowered statistical tests |
| 3 | Results Integrity | **4** | Data matches claims; minor figure-caption mismatches |
| 4 | Citation Accuracy | **2** | 3 citations with serious errors including fabricated author names |
| 5 | Compilation | **5** | PDF compiles cleanly, well-formatted with TikZ diagrams |
| 6 | Writing Quality | **4** | Professional tone, clear arguments, logical flow |
| 7 | Figure Quality | **3** | Functional figures with proper labels but several issues |

---

## Overall Verdict: REVISE

The paper presents a well-motivated and methodologically sound investigation into hybrid heuristics for ATSP on real road networks. The experimental framework is comprehensive and the results are honest about their limitations. However, the paper **cannot be accepted** due to: (1) **three citations with serious metadata errors**, including fabricated author names; (2) **figure-caption mismatches**; and (3) **a figure mislabeled as a heatmap** that is actually a bar chart. These issues are fixable and the underlying work is strong.

---

## Detailed Review

### 1. Completeness (5/5)

All required sections are present and well-organized:
- **Abstract:** Concise, states the problem, methods, and key result (1.04% improvement over LKH).
- **Introduction:** Motivates the Euclidean-vs-road-network gap clearly, states 5 contributions.
- **Related Work:** Covers classical solvers, neural CO, ALNS, and road network tools (4 subsections).
- **Background/Preliminaries:** Formal ATSP definition with ILP formulation (Eqs. 1-5), notation table.
- **Method:** Four components described in detail with pseudocode (Algorithm 1) and TikZ architecture diagram.
- **Experimental Setup:** Benchmark suite, solver list, evaluation protocol, hyperparameters.
- **Results:** Organized around 4 research questions with 6 tables and 7 figures.
- **Discussion:** Includes comparison with prior work, 5 limitations, practical recommendations.
- **Conclusion:** Summarizes 4 findings and 5 future directions.
- **References:** 18 entries in sources.bib.

The paper structure follows standard ML/OR conference format and is comprehensive.

### 2. Technical Rigor (4/5)

**Strengths:**
- The ATSP formulation (Eqs. 1-5) is correct with proper MTZ subtour elimination.
- The GNN architecture (Eqs. 6-8) is clearly specified: directed message passing with attention, edge scoring head.
- Algorithm 1 provides complete pseudocode for the hybrid solver.
- The ablation study isolates the contributions of GNN guidance vs. asymmetry-aware evaluation.
- The Wilcoxon signed-rank test is appropriate for paired comparisons, and the authors correctly note that n=4 pairs is insufficient for significance (minimum achievable p=0.0625).
- The paper honestly reports that GNN precision (0.339) falls below the 0.75 target.

**Weaknesses:**
- Only 4 paired instances for the LKH comparison severely limits statistical power. The paper acknowledges this but it remains a fundamental limitation.
- The GNN was trained on only 160 instances (vs. the planned 1,000), creating a chicken-and-egg bottleneck the paper correctly identifies.
- The time-dependent extension (Eq. 3) uses a synthetic Gaussian traffic model not validated against real traffic data.
- The "LKH baseline" is a pure-Python reimplementation, not the actual LKH-3 binary. This is a critical distinction — the 1.04% improvement is over the authors' own LKH-style solver, not Helsgaun's optimized C implementation. This should be stated more prominently.

### 3. Results Integrity (4/5)

**Verified claims against `results/` data:**

| Claim in Paper | Value in Data | Match? |
|---|---|---|
| 134 benchmark runs | 134 rows in full_benchmark.csv | Yes |
| Hybrid GNN-LK mean gap: 0.67% | pareto_analysis.json: 0.669% | Yes |
| ALNS mean gap: 0.87% | pareto_analysis.json: 0.866% | Yes |
| LKH mean gap: 1.73% | pareto_analysis.json: 1.732% | Yes |
| NN mean gap: 10.35% | pareto_analysis.json: 10.352% | Yes |
| Hybrid GNN-LK vs LKH: -1.04% | lkh_comparison.json: -1.041% | Yes |
| Wilcoxon p=0.125 | lkh_comparison.json: 0.125 | Yes |
| Ablation: Full=4922.7, No Asym=4966.7 | ablation_study.csv: computed means match | Yes |
| Scalability table values (Table 5) | scalability.csv: all values match | Yes |

All quantitative claims in the paper are consistent with the underlying data files. No fabricated results detected.

**Issues found:**
- **Figure 6 caption mismatch:** The caption refers to an "Ablation heatmap" but the actual figure (`ablation_heatmap.png`) is a grouped bar chart, not a heatmap. The caption should be corrected or the figure regenerated as an actual heatmap.
- **Figure 8 caption mismatch:** The caption states "LKH (bottom)" but the figure actually shows "Hybrid LK" tours. The Hybrid LK solver is compared against Nearest Neighbor, not LKH.
- **Benchmark comparison figure** (Figure 9) only shows "Small" and "Medium" categories but omits "Large" — likely because metaheuristic solvers weren't run at large scale, but this should be noted.

### 4. Citation Accuracy (2/5) — CRITICAL

**Methodology:** Each of the 18 entries in `sources.bib` was verified via web search against authoritative sources (publisher websites, arXiv, DBLP, ACM DL, Semantic Scholar).

#### Citation Verification Report

| # | BibTeX Key | Verdict | Details |
|---|---|---|---|
| 1 | `applegate2006traveling` | **VERIFIED** | All fields correct. Confirmed via Princeton University Press, Amazon, JSTOR. |
| 2 | `helsgaun2017extension` | **VERIFIED** | Technical report from Roskilde University. All fields correct. Minor: `@techreport` would be more appropriate than `@article`. |
| 3 | `helsgaun2000effective` | **VERIFIED** | European J. of Operational Research, Vol. 126(1), pp. 106-130, 2000. DOI confirmed. |
| 4 | `lin1973effective` | **VERIFIED** | Operations Research, Vol. 21(2), pp. 498-516, 1973. DOI confirmed via INFORMS. |
| 5 | `jonker1983transforming` | **VERIFIED** | Operations Research Letters, Vol. 2(4), pp. 161-163, 1983. DOI confirmed via ScienceDirect. |
| 6 | `perron2023ortools` | **INCORRECT** | **Missing authors.** The BibTeX lists only Perron and Furnon, but the actual paper (per HAL hal-04015496) has 6 authors: Cuvelier, Didier, Furnon, Gay, Mohajeri, and Perron. Four co-authors are omitted. |
| 7 | `bello2017neural` | **VERIFIED** | ICLR 2017 Workshop. arXiv:1611.09940. All author names confirmed via DBLP. |
| 8 | `kool2019attention` | **VERIFIED** | ICLR 2019. arXiv:1803.08475. Confirmed via OpenReview and DBLP. |
| 9 | `nazari2018reinforcement` | **VERIFIED** | NeurIPS 2018 (Vol. 31). arXiv:1802.04240. All fields correct. *Note: not cited in the paper text.* |
| 10 | `kwon2020pomo` | **VERIFIED** | NeurIPS 2020 (Vol. 33). arXiv:2010.16011. All 6 authors confirmed. |
| 11 | `kwon2021matnet` | **INCORRECT** | **Fabricated author names.** The BibTeX lists authors as "Kwon, Choo, Oh Munsang, Park Inwoo, Gwon" but the actual authors (per NeurIPS 2021 proceedings, arXiv:2106.11113) are **Kwon, Choo, Yoon Iljoo, Park Minah, Park Duwon, Gwon**. "Oh Munsang" and "Park Inwoo" do not appear on this paper. Three real authors (Yoon, M. Park, D. Park) are missing. |
| 12 | `ma2022dact` | **INCORRECT** | **Three errors:** (1) Year is wrong: should be **2021**, not 2022 (NeurIPS 2021). (2) Volume is wrong: should be **34**, not 35. (3) Last author name is wrong: should be "Tang, **Jing**", not "Tang, **Jian**" (different researchers). Confirmed via NeurIPS 2021 proceedings and OpenReview. |
| 13 | `luxen2011realtime` | **VERIFIED** | ACM SIGSPATIAL 2011. DOI confirmed via ACM Digital Library. |
| 14 | `boeing2017osmnx` | **VERIFIED** | Computers, Environment and Urban Systems, Vol. 65, pp. 126-139. DOI confirmed. |
| 15 | `valhalla2024` | **VERIFIED** | GitHub repository. Software citation is appropriate. *Note: not cited in the paper text.* |
| 16 | `ropke2006adaptive` | **VERIFIED** | Transportation Science, Vol. 40(4), pp. 455-472. DOI confirmed via INFORMS. |
| 17 | `pisinger2007general` | **VERIFIED** | Computers & Operations Research, Vol. 34(8), pp. 2403-2435. DOI confirmed. |
| 18 | `reinelt1991tsplib` | **VERIFIED** | ORSA Journal on Computing, Vol. 3(4), pp. 376-384. DOI confirmed. |

**Additional note on `johnson2007experimental`:** The listed year of 2007 reflects Springer's digitization/reissue after acquiring Kluwer. The original book chapter was published in **2002** by Kluwer Academic Publishers. Most scholars cite 2002 as the publication year. This is a minor inaccuracy.

**Summary:** 14 of 18 citations fully verified. **3 citations have serious errors** (fabricated author names in `kwon2021matnet`, wrong year/volume/author in `ma2022dact`, missing authors in `perron2023ortools`). 1 citation has a minor year discrepancy (`johnson2007experimental`). 2 entries are in `sources.bib` but not cited in the paper text (`nazari2018reinforcement`, `valhalla2024`).

### 5. Compilation (5/5)

- The PDF (`research_paper.pdf`, 2.1 MB) exists and is well-formatted.
- LaTeX compiles with proper packages: `geometry`, `amsmath`, `algorithm`, `booktabs`, `natbib`, `pgfplots`, `tikz`, `subcaption`, `hyperref`, `microtype`.
- The TikZ architecture diagram (Figure 1) renders correctly with colored boxes and arrows.
- All 5 tables use `booktabs` formatting (`\toprule`, `\midrule`, `\bottomrule`).
- Algorithm 1 is properly formatted with the `algorithmic` environment.
- Hyperlinks are styled with colored link text.
- No compilation warnings or errors observed in the output.

### 6. Writing Quality (4/5)

**Strengths:**
- Professional academic tone throughout, appropriate for a top venue.
- Clear motivation: the Euclidean-vs-road-network gap is well-articulated in the introduction.
- Logical flow from problem definition through method, experiments, and discussion.
- Honest self-assessment of limitations (Section 7.3) including statistical power, GNN precision shortfall, scalability ceiling, and training data bottleneck.
- Practical recommendations for practitioners organized by time budget.
- Custom LaTeX commands for consistency (`\cij`, `\ie`, `\eg`).

**Weaknesses:**
- The paper refers to its LKH baseline as "LKH" throughout, which could mislead readers into thinking the comparison is against Helsgaun's optimized LKH-3 implementation. The fact that it is a pure-Python reimplementation should be made explicit early (e.g., in the abstract or Section 5.2).
- Section 6.4 (Scalability) notes that at 500+ nodes "Nearest Neighbor becomes the best known" — this reflects incomplete experimentation rather than a meaningful result, and the phrasing could be clearer.
- The paper scope is ambitious (5 contributions) for what is essentially a study on small instances (20-50 nodes for the main LKH comparison). The framing could better match the actual scale of results.

### 7. Figure Quality (3/5)

**Assessment of each figure:**

| Figure | File | Assessment |
|---|---|---|
| Fig. 1 (Architecture) | TikZ in LaTeX | Good. Clean colored boxes with arrows. Publication-quality. |
| Fig. 2 (Pareto front) | `pareto_front.png` | Good. Distinctive markers per solver, error bars, log-scale x-axis. Could benefit from a visible Pareto frontier line. |
| Fig. 3 (Ablation) | `ablation_heatmap.png` | **Mislabeled.** Caption says "heatmap" but it is a bar chart. The figure itself is functional with error bars and value annotations, but the naming discrepancy is a problem. |
| Fig. 4 (Scalability) | `scalability.png` | Good. Two-panel layout with quality and runtime. Log scale on runtime axis. Clear legends. Only shows 4 solvers (NN, Greedy, Savings, ALNS) — missing LKH, OR-Tools, GNN-LK lines for small instances where they were evaluated. |
| Fig. 5 (Training loss) | `training_loss.png` | **Issue.** Left panel shows training loss curve clearly but the validation loss appears stuck near zero — likely a scale issue with weighted BCE causing val loss to be invisible at the training loss scale. Right panel (precision/recall/F1) is fine. |
| Fig. 6 (GNN scores) | `gnn_edge_scores.png` | Good. Three-panel visualization is informative. Edge score distribution clearly shows bimodality. Tour vs. non-tour discrimination is visible. |
| Fig. 7 (Tours) | `tour_visualization.png` | Good. Directed arrows colored by asymmetry ratio on real geographic coordinates. Color bar present. **Caption error:** says "LKH" but figure shows "Hybrid LK". |
| Fig. 8 (Benchmark) | `benchmark_comparison.png` | Acceptable. Grouped bars with error bars and value annotations. Missing "Large" category. |

**Overall:** Figures use a reasonable matplotlib style (not raw defaults — custom colors, proper sizing), have axis labels and legends. However, the mislabeled heatmap, caption mismatches, and training loss plotting issue need to be fixed. Figures are adequate for a workshop paper but need polish for a top venue.

---

## Required Revisions

### Critical (Must Fix)

1. **Fix citation `kwon2021matnet`:** Replace fabricated author names ("Oh, Munsang" and "Park, Inwoo") with the correct authors: Kwon, Yeong-Dae and Choo, Jinho and Yoon, Iljoo and Park, Minah and Park, Duwon and Gwon, Youngjune. Add the arXiv URL (2106.11113).

2. **Fix citation `ma2022dact`:** Correct the year from 2022 to **2021**, the volume from 35 to **34**, and the last author from "Tang, Jian" to "Tang, **Jing**".

3. **Fix citation `perron2023ortools`:** Add the 4 missing co-authors: Cuvelier, Thibaut and Didier, Frederic and Gay, Steven and Mohajeri, Sarah.

4. **Fix citation `johnson2007experimental`:** Consider updating the year from 2007 to **2002** (original Kluwer publication) for accuracy, or at minimum add a note.

### Major (Should Fix)

5. **Clarify LKH baseline identity:** State explicitly (in abstract, Section 5.2, and Table 3 caption) that the "LKH" baseline is a pure-Python reimplementation of LKH-style local search, **not** Helsgaun's optimized LKH-3 binary. The current presentation risks overstating the significance of the 1.04% improvement.

6. **Fix Figure 3 (ablation):** Either regenerate as an actual 2x2 heatmap (GNN on/off vs. Asymmetry on/off) to match the "heatmap" caption, or update the caption to describe it as a bar chart.

7. **Fix Figure 7 (tour visualization) caption:** Change "LKH (bottom)" to "Hybrid LK" to match the actual figure content.

8. **Fix Figure 5 (training loss):** The validation loss curve appears invisible/near-zero in the left panel. Either plot training and validation on separate y-axes, or use a subplot that shows the validation loss at its actual scale.

### Minor (Recommended)

9. **Remove uncited bib entries:** `nazari2018reinforcement` and `valhalla2024` are in `sources.bib` but never cited with `\cite` in the paper. Either cite them or remove them.

10. **Figure 4 (scalability):** Consider adding LKH, OR-Tools, and GNN-LK data points for the instance sizes where they were evaluated (20-50 nodes), to give a complete picture.

11. **Ablation table (Table 4):** The identical values for "Full" and "No GNN" (4,922.7) and for "No Asymmetry" and "No GNN, No Asym" (4,966.7) should be discussed more carefully. This means GNN guidance has literally zero effect on these instances, which suggests the GNN component may not be contributing meaningfully at any tested scale.

12. **Scalability framing:** At 500+ nodes, only construction heuristics were evaluated. The claim that NN achieves "0.00% gap" at large scales is misleading — it simply means NN was the only solver producing the best-known solution because no better solver was run. Consider rephrasing or adding a caveat.

---

## Positive Aspects

- The problem motivation is compelling and practically relevant (Euclidean vs. road network TSP).
- The experimental framework is comprehensive: 15 instances, 8 solvers, ablation study, Pareto analysis, scalability study.
- The paper is refreshingly honest about its limitations (Section 7.3), including statistical power, precision shortfall, and scalability ceiling.
- All quantitative claims in the text match the underlying data files — no fabricated results.
- The TikZ architecture diagram and tour visualization figures are particularly well-done.
- The practical recommendations organized by time budget (Section 7.4) add real value for practitioners.
- The asymmetry-aware evaluation contribution (0.9% improvement) is a genuine and useful finding for the community.

---

## Summary

This paper addresses an important and underexplored problem — TSP on real road networks with asymmetric costs. The experimental methodology is sound and the results, while modest in scale, are reported honestly. The main barrier to acceptance is **citation accuracy**: three references contain serious errors including fabricated author names, which is unacceptable for any venue. Additionally, several figure-caption mismatches and the misleading "LKH baseline" framing need correction. After addressing these issues, the paper would be a solid contribution to the combinatorial optimization community.

**Verdict: REVISE** — Fix the 3 incorrect citations, clarify the LKH baseline identity, and correct figure-caption mismatches. The underlying research is sound and the revision should be straightforward.

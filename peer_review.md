# Peer Review: FARB — Fragmentation-Aware Resource Balance for Online 2D Vector Bin Packing in Cloud VM Scheduling

**Reviewer:** Automated Peer Reviewer (Nature/NeurIPS standard)
**Date:** 2026-02-24
**Verdict:** **REVISE**

---

## Criterion Scores

| # | Criterion | Score (1–5) | Summary |
|---|-----------|:-----------:|---------|
| 1 | Completeness | **4** | All required sections present and well-structured |
| 2 | Technical Rigor | **3** | Solid formalization but seed-variance issue undermines statistical claims |
| 3 | Results Integrity | **3** | Core numbers match data files; two broken figures and zero cross-seed variance |
| 4 | Citation Accuracy | **2** | 3 of 19 citations contain incorrect or fabricated metadata |
| 5 | Compilation | **4** | PDF compiles, well-formatted, proper use of LaTeX environments |
| 6 | Writing Quality | **4** | Professional tone, clear arguments, honest limitations discussion |
| 7 | Figure Quality | **2** | 2 of 9 figures are broken/uninformative; others are acceptable |

**Overall: REVISE** — Does not meet the threshold of 3+ on all criteria.

---

## 1. Completeness (4/5)

All required sections are present: Abstract, Introduction, Related Work (Section 2), Background & Preliminaries (Section 3), Method (Section 4), Experimental Setup (Section 5), Results (Section 6), Discussion (Section 7), Conclusion (Section 8), and References. The paper is well-structured with a logical flow. The notation table (Table 1) and hyperparameter table (Table 5) are appreciated.

**Minor gap:** No explicit "Threats to Validity" subsection, though limitations are partially covered in Section 7.

---

## 2. Technical Rigor (3/5)

### Strengths
- The FARB scoring function is cleanly formalized with three components (Eqs. 5–8), and Algorithm 1 provides clear pseudocode.
- The fragmentation potential function Φ (Eq. 9) provides theoretical motivation.
- O(n) time complexity analysis is straightforward and correct.
- The paper compares against 8 baselines, which is comprehensive.
- Statistical tests (paired t-tests, Wilcoxon, Cohen's d, 95% CI) are reported.

### Critical Issue: Zero Variance Across Seeds
Examination of the raw result files reveals that **all three random seeds (42, 123, 456) produce identical results** for every heuristic on both traces. For example:

- `azure_like_BFD_seed42_summary.json`: avg_waste_pct = 6.009836403367846
- `azure_like_BFD_seed123_summary.json`: avg_waste_pct = 6.009836403367846
- `azure_like_BFD_seed456_summary.json`: avg_waste_pct = 6.009836403367846

The aggregate files confirm: `std_waste_pct: 0.0` across all heuristics and traces.

This means the "tie-breaking randomness" described in Section 5.4 has **zero effect** on placement outcomes. The claim that experiments are "run with three random seeds... to assess variance" (Section 5.4) is misleading — there is no variance to assess. The heuristics are fully deterministic for these workloads, and reporting "means and standard deviations across seeds" (Section 5.4) obscures the fact that the standard deviation is literally zero.

The statistical significance tests (Table 4) use per-time-window paired samples from what is effectively a single simulation run, not independent replications. While paired time-window comparisons are methodologically valid, the paper should not claim that three-seed replication provides robustness when the seeds have no effect.

**Action required:** Either (a) introduce genuine stochasticity (e.g., tie-breaking randomization that actually affects outcomes, or trace perturbation), or (b) transparently state that the heuristics are deterministic for these workloads and that statistical tests are over time windows of a single run.

---

## 3. Results Integrity (3/5)

### Numbers That Match
The paper's headline results are consistent with the `results/azure_trace/` and `results/google_trace/` data files:

| Claim | Paper | Data File | Match? |
|-------|-------|-----------|--------|
| FARB Azure waste | 5.36% | 5.357% (`azure_trace/FARB_seed42`) | Yes (rounding) |
| BFD Azure waste | 6.01% | 6.010% (`baselines/azure_like_BFD_seed42`) | Yes |
| FARB Azure fragmentation | 14.0% | 14.01% (`azure_trace/FARB_seed42`) | Yes |
| BFD Azure fragmentation | 23.4% | 23.36% (`baselines/azure_like_BFD_seed42`) | Yes |
| FARB Google waste | 11.65% | 11.655% (`google_trace/FARB_seed42`) | Yes |
| BFD Google waste | 11.23% | 11.235% (`baselines/google_like_BFD_seed42`) | Yes |
| FARB+defrag(500,20) waste | 4.01% | 4.010% (`defrag/defrag_results.json`) | Yes |
| BFD no-defrag waste | 7.75% | 7.747% (`defrag/defrag_results.json`) | Yes |

### Concerns

1. **Two discrepant result sets exist.** The `results/advanced_baselines/` directory contains a different run where FARB Google waste = 12.47% (vs. the 11.65% reported in the paper from `results/google_trace/`). While the paper uses the `google_trace/` data consistently, the existence of a substantially different earlier run without explanation is concerning. Were parameters or trace generation changed between runs?

2. **Broken figures make claims unverifiable** (see Section 7 below). The paper describes patterns in Figures 6a (stranded resources) and 5b (heatmap) that cannot be confirmed from the actual rendered figures.

---

## 4. Citation Accuracy (2/5)

### Verification Methodology
Every entry in `sources.bib` (19 citations) was verified via web search against publisher pages (ACM DL, IEEE Xplore, Springer, Elsevier/ScienceDirect, USENIX, arXiv, GitHub), Semantic Scholar, DBLP, and Google Scholar.

### Citation Verification Report

| # | Key | Status | Details |
|---|-----|--------|---------|
| 1 | `christensen2017approximation` | **VERIFIED** | Authors, title, journal (Computer Science Review, vol. 24), year, DOI all correct |
| 2 | `hadary2020protean` | **VERIFIED** | Authors, title, venue (OSDI '20), pages 845–861 all correct |
| 3 | `panigrahy2011heuristics` | **VERIFIED** | Authors, title, institution (MSR), year, URL all correct |
| 4 | `han2011upper` | **VERIFIED** | Authors, title, journal (ACM TALG, vol. 7 no. 4), DOI all correct |
| 5 | `verma2015borg` | **VERIFIED** | Authors, title, venue (EuroSys '15), DOI all correct |
| 6 | `seiden2002online` | **VERIFIED** | Author, title, journal (JACM, vol. 49 no. 5), DOI all correct |
| 7 | `seiden2003stee` | **VERIFIED (minor issues)** | Paper is real. Year should be 2002 for SODA proceedings (2003 = Algorithmica journal version). Possible page off-by-one (485 vs 486) |
| 8 | `barbalho2023vm` | **VERIFIED (minor issue)** | Paper is real, MLSys '23 Outstanding Paper Award confirmed. One author (Tamires Santos) omitted from author list |
| 9 | `lopez2015hybrid` | **INCORRECT / FABRICATED** | **Wrong author**: "Maria Teresa López-Herrero" has no connection to this work; actual authors are **Kaaouache & Bouamama**. **Wrong volume/pages**: actual is vol. 60, pp. 1061–1069 (not vol. 52, pp. 950–955). **DOI resolves to unrelated paper**: DOI 10.1016/j.procs.2015.05.171 points to "A CA Model for Bidirectional Pedestrian Streams" by Lämmel & Flötteröd |
| 10 | `sheng2022vmagent` | **VERIFIED** | Authors, title, arXiv ID, URL all correct. Year 2022 justified by IJCAI 2022 demo |
| 11 | `tirmazi2020borg` | **VERIFIED** | Authors, title, venue (EuroSys '20), DOI all correct |
| 12 | `google2019clusterdata` | **VERIFIED** | Title, year, GitHub URL all correct |
| 13 | `azure2020packing` | **VERIFIED** | Title, year, GitHub URL all correct |
| 14 | `nagel2023analysis` | **INCORRECT** | **Wrong author first name**: "Matthias Nagel" should be **Lars Nagel**. Full author list (Lars Nagel, Nikolay Popov, Tim Süss, Ze Wang) should replace "and others". Title, venue (LION 2023, LNCS 14286), DOI all correct |
| 15 | `coffman1996approximation` | **INCORRECT (minor)** | Year likely **1997** (not 1996). Entry type should be `@incollection` not `@article`. Editor (Dorit S. Hochbaum) missing. Authors, title, pages, publisher correct |
| 16 | `heydrich2016beating` | **VERIFIED** | Authors, title, venue (ICALP '16), DOI all correct |
| 17 | `song2014adaptive` | **VERIFIED** | Authors, title, journal (IEEE TC, vol. 63 no. 11), DOI all correct |
| 18 | `grandl2014tetris` | **VERIFIED** | Authors, title, venue (SIGCOMM '14), pages, DOI all correct |
| 19 | `gabay2017vector` | **INCORRECT / FABRICATED** | **Completely wrong authors**: "Marinés Gabay, Sebastian Pokutta, Alberto Caprara" should be **Michaël Gabay & Sofia Zaourar** (2 authors, not 3). Pokutta and Caprara are real researchers but did not author this paper. **Wrong year**: should be 2016 (not 2017). DOI, title, journal, volume, pages are correct |
| 20 | `delorme2016binpacking` | **VERIFIED** | Authors, title, journal (EJOR, vol. 255 no. 1), DOI all correct |

### Summary
- **13 fully verified** (no issues)
- **2 verified with minor issues** (seiden2003stee: year mismatch; barbalho2023vm: missing author)
- **1 minor error** (coffman1996approximation: year, entry type, missing editor)
- **2 with fabricated/incorrect author names** (nagel2023analysis: wrong first name; gabay2017vector: entirely wrong authors)
- **1 clearly fabricated** (lopez2015hybrid: wrong author, wrong metadata, DOI resolves to unrelated paper)

All in-text `\cite` commands have matching entries in `sources.bib`. No dangling references.

**This citation error rate (3 substantive errors out of 19) is unacceptable for a publication-quality paper.**

---

## 5. Compilation (4/5)

The compiled PDF (`research_paper.pdf`, 2.1 MB) exists and is well-formatted. LaTeX environments (algorithm, booktabs tables, TikZ architecture diagram, subfigures) are used correctly. Hyperlinks are functional. The TikZ system architecture diagram (Figure 1) is a nice touch.

No compilation errors observed.

---

## 6. Writing Quality (4/5)

### Strengths
- Professional academic tone throughout.
- Clear, well-motivated introduction with concrete dollar-value impact.
- Honest discussion of limitations (Section 7), including cases where FARB underperforms.
- The insight framing ("resource fragmentation is primarily caused by placements that worsen dimensional imbalance") is compelling and clearly articulated.
- Comprehensive related work section with appropriate positioning.

### Minor Issues
- The paper would benefit from explicitly noting in the abstract or introduction that FARB alone does not meet the 2pp waste target (0.65pp on Azure, worse on Google).
- Some redundancy between the Background section's notation and the Method section.

---

## 7. Figure Quality (2/5)

### Broken Figures (Critical)

**Figure 5b / fig3_utilization_heatmap.png — BROKEN.** The CPU vs. RAM utilization heatmap is completely uninformative:
- Both the BFD and FARB panels show a uniform orange field with no visible differentiation.
- The colorbar ranges from -0.1 to 0.1 for "Number of Hosts" — **negative host counts are nonsensical**.
- The paper claims (line 679–681): "FARB concentrates host states along the diagonal (balanced utilization), while BFD shows off-diagonal spread indicating dimensional imbalance." **This claim cannot be verified from the figure** — both panels look identical and show nothing.
- **Root cause:** Likely a scaling/binning error in the heatmap generation code, where counts are so sparse relative to the bin grid that nothing is visible.

**Figure 6a / fig8_stranded_resources.png — BROKEN.** The stranded resource distribution chart is non-functional:
- Both panels show "Active=0, Empty=500" — the snapshot was taken at end-of-trace when all VMs have departed and all hosts are empty.
- All bar heights are effectively zero (y-axis range: -0.04 to 0.04).
- The figure has extreme aspect ratio issues (rendered as very tall narrow image with mostly whitespace).
- The paper claims (line 691–693): "Under BFD, approximately equal numbers of CPU-stranded and RAM-stranded hosts emerge... FARB reduces both types of stranding." **This claim cannot be verified from the figure.**
- **Root cause:** The snapshot was taken at simulation end (t=final) rather than during steady-state operation.

### Acceptable Figures

| Figure | Assessment |
|--------|-----------|
| fig1_waste_comparison.png | Good. Proper bar chart with error bars, labeled axes, all 9 heuristics shown for both traces. Uses "(ours)" labeling. |
| fig2_fragmentation_timeseries.png | Good. Clear time-series with 4 heuristics, line styles distinguish approaches, both traces shown side-by-side. |
| fig4_scalability.png | Good. Dual-panel (latency + waste vs. cluster size), clean lines with markers. |
| fig5_waste_boxplot.png | Acceptable. Box plots with proper labels. Shows FARB's tighter distribution on Azure. |
| fig6_sensitivity_heatmap.png | Good. Annotated heatmap with values, clear color gradient. |
| fig7_defrag_benefit.png | Good. Grouped bar chart showing defrag impact by budget. |
| fig9_vm_size_fragmentation.png | Acceptable. Histogram of VM resource ratios with balanced line. |

### Style Assessment
The working figures use custom color palettes (not raw matplotlib defaults), have proper axis labels, legends, and titles. However, two critically broken figures lower the overall score significantly.

---

## 8. Additional Technical Observations

### The 2pp Waste Reduction Target
The research rubric defined success as "reducing resource waste by at least 2 percentage points compared to the best baseline." FARB alone achieves:
- Azure-like: −0.65pp waste vs. BFD (significant, p < 10⁻¹³³)
- Google-like: +0.42pp waste vs. BFD (FARB is *worse*)

Only FARB + defragmentation(500, 20) exceeds 2pp (3.74pp vs. BFD no-defrag). However, the fair comparison is FARB+defrag vs. BFD+defrag: 4.01% vs. 5.05% = 1.04pp — still below the 2pp target.

The paper's primary contribution (fragmentation reduction: 9.4pp on Azure) is arguably more valuable than waste reduction, and this is well-argued in the Discussion. But the stated target was not met.

### Sensitivity Analysis Raises Concerns
Table 7 shows FARB is worse than BFD on 5 out of 6 tested workload distributions (CPU-heavy: +1.03pp, RAM-heavy: +1.02pp, uniform small: +0.93pp, bimodal: +0.28pp, realistic: +0.07pp). FARB only outperforms on the Azure-like distribution (−0.65pp). This suggests FARB's advantage is narrow and specific to workloads with heterogeneous VM types with complementary resource ratios.

---

## Verdict: REVISE

### Mandatory Fixes Before Resubmission

1. **Fix all incorrect citations** (Critical):
   - `lopez2015hybrid`: Replace with correct authors (Kaaouache & Bouamama), correct volume/pages (60, pp. 1061–1069), and correct DOI, OR replace with a different legitimate reference for GA hybrids.
   - `gabay2017vector`: Fix authors to "Michaël Gabay and Sofia Zaourar" (2 authors), fix year to 2016.
   - `nagel2023analysis`: Fix first author to "Lars Nagel" and expand "and others" to full author list (Lars Nagel, Nikolay Popov, Tim Süss, Ze Wang).
   - `coffman1996approximation`: Fix year to 1997, change to `@incollection`, add editor field (Dorit S. Hochbaum).
   - `seiden2003stee`: Fix year to 2002 for SODA proceedings version.
   - `barbalho2023vm`: Add missing author Tamires Santos.

2. **Regenerate broken figures** (Critical):
   - **fig3_utilization_heatmap.png**: Fix heatmap binning/scaling so that host counts are visible. Ensure colorbar shows non-negative integer counts. Consider using a logarithmic color scale or kernel density estimation. The visualization should clearly show diagonal concentration for FARB vs. off-diagonal spread for BFD.
   - **fig8_stranded_resources.png**: Take the snapshot during steady-state operation (e.g., at peak utilization or averaged over mid-simulation windows), NOT at end-of-trace when all VMs have departed. Fix aspect ratio. Bars should show meaningful counts of CPU-stranded, RAM-stranded, and balanced hosts.

3. **Address seed variance issue** (Important):
   - Transparently acknowledge that the heuristics are deterministic for these workloads (seeds have zero effect).
   - Either introduce genuine stochasticity (trace perturbation, arrival order shuffling) or remove the claim of multi-seed replication from Section 5.4 and reframe the statistical tests as time-window comparisons within a single run.

### Recommended Improvements

4. **Clarify the 2pp target assessment**: State clearly in the abstract that FARB alone achieves 0.65pp waste reduction (below the 2pp target) and that the 2pp target is only exceeded with the additional defragmentation module.

5. **Reconcile result sets**: Explain or remove the discrepant `advanced_baselines/` data that shows different numbers than `google_trace/` and `azure_trace/`.

6. **Strengthen the sensitivity analysis narrative**: The finding that FARB is worse than BFD on 5/6 workload distributions deserves more prominent discussion. Consider framing FARB as a workload-specific heuristic rather than a general improvement.

7. **Add actual production trace evaluation**: The paper acknowledges this limitation — evaluation on the real Azure Packing 2020 and Google ClusterData2019 traces (both publicly available) would substantially strengthen the contribution.

---

## Summary

This paper presents a well-motivated and clearly described heuristic (FARB) for reducing resource fragmentation in cloud VM scheduling. The core insight — that dimensional balance should be a first-class scoring objective — is sound and supported by the Azure-like trace results. The experimental framework is comprehensive with 9 heuristics, multiple workloads, and scalability analysis.

However, three categories of issues prevent acceptance at this stage: (1) **citation integrity** — 3 citations have fabricated or incorrect author names, which is unacceptable; (2) **figure quality** — 2 figures are broken and do not support the claims made about them in the text; (3) **statistical methodology** — the three-seed replication is an illusion (zero variance), undermining the robustness narrative.

These issues are all fixable. After addressing the mandatory fixes above, this paper would be a solid contribution to the bin packing heuristics literature, particularly for the fragmentation-reduction angle. The honest discussion of limitations and the sensitivity analysis showing where FARB struggles are commendable.

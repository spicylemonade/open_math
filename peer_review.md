# Peer Review: On the Finiteness of Unitary Perfect Numbers

**Paper:** "On the Finiteness of Unitary Perfect Numbers: A Computational and Theoretical Investigation of Subbarao's Conjecture"
**Authors:** Research Lab (Automated)
**Date:** February 2026
**Reviewer:** Peer Review Agent (rigorous venue standard)

---

## Criterion Scores

| # | Criterion | Score (1–5) | Comments |
|---|-----------|:-----------:|---------|
| 1 | **Completeness** | 5 | All required sections present: Abstract, Introduction, Related Work, Background/Preliminaries, Method, Experimental Setup, Results, Discussion, Conclusion, References. The paper also includes a notation table, algorithmic pseudocode, and a detailed limitations subsection. |
| 2 | **Technical Rigor** | 4 | Methods are properly described with equations. The product equation formulation, Subbarao–Warren decomposition, growth constraint analysis, and modular obstruction sieve are all presented with formal definitions, theorems, and proofs. The 18-claim proof attempt is logically structured with a clear identification of where the argument fails. The key theorem (Theorem 3.1, stabilization of f(m)=5) is proved rigorously with exact arithmetic. Minor deductions: (a) the Goto bound $m < 2^s$ (Claim 7) is stated as following from Goto's bound but the derivation could be more explicit; (b) the analytic density section (Section 4.4) is more of a sketch than a proof, relying on "one expects $U(X) = O(X^{5/6+o(1)})$" without rigorous justification. |
| 3 | **Results Integrity** | 4 | Results are largely consistent with the underlying data in `results/`. All five known UPNs verified, search results match JSON data, modular sieve density matches (paper: ~0.606, data: 0.6061). Proof verification JSON confirms all 18 claims + appendix verified. **However, there are two factual discrepancies between the paper and data:** (1) The paper states "390 total (m,k) cells" (Section 6.1) but the actual data contains 420 cells (k=2..15, m=1..30 gives 14×30=420). (2) The paper states "76 were pruned" but the data shows 106 pruned cells (65 pruned_goto + 41 pruned_impossible). These appear to be copy errors rather than fabrication, but they should be corrected. |
| 4 | **Citation Quality** | 5 | `sources.bib` contains 17 well-formed BibTeX entries covering all major references: Subbarao & Warren (1966), Wall (1975, 1987, 1988), Goto (2007), Pollack & Shevelev (2012), Guy (2004), Vaidyanathaswamy (1931), Cohen (1960), OEIS A002827, MathWorld, Erdos Problem #1052, Subbarao (1970, 1972), Hagis (1984), Graham (1989), and Wikipedia. All entries include author, title, journal/book, year, and DOI where available. The paper uses `\bibliography{sources}` with `plainnat` style. Citations are used appropriately throughout with `\citet` and `\citep` commands. |
| 5 | **Compilation** | 5 | The PDF exists (833 KB), is well-formatted at 11pt on A4 paper, and uses appropriate LaTeX packages (amsmath, amsthm, natbib, hyperref, pgfplots, tikz, booktabs, algorithm). The TikZ proof architecture diagram is generated inline. Figures are included via `\includegraphics`. The document structure is professional with proper theorem environments, numbered equations, and algorithm floats. |
| 6 | **Writing Quality** | 5 | Excellent academic prose throughout. The abstract is concise and informative (~150 words). The introduction clearly motivates the problem, states prior results, and outlines contributions. The paper follows a logical progression from definitions through methods, experiments, results, and discussion. The honest assessment of limitations (Section 7.5) and the precise identification of the proof gap are particularly commendable. The "Routes to Resolution" section (7.3) provides concrete, actionable future directions. The writing avoids overclaiming — the paper is transparent that it does not resolve the conjecture. |
| 7 | **Figure Quality** | 4 | Four figures are present, all publication-quality with proper labels, legends, titles, and non-default styling: (1) **Known UPN factorizations** (Fig. 1): Two-panel bar chart with annotations ($v_2=18$, $5^4$), distinct color coding per UPN, proper axis labels. Good. (2) **Product equation solutions** (Fig. 2): Two-panel plot with annotated transition ($P(4)<2<P(5)$), red star markers for known UPNs, reference line at target=2. Good. (3) **Growth constraint** (Fig. 3): Two-panel plot showing f(m) stabilization and combined constraint region with shaded feasible/infeasible regions, Wall's bound line, and known UPN markers. Very good. (4) **Modular sieve density** (Fig. 4): Two-panel plot with cumulative density curve and per-modulus bar chart with annotation. Good. Minor deductions: the right panel of Fig. 4 uses a somewhat plain single-color bar chart that could benefit from highlighting the non-trivial obstructing primes (q=3, 23, 47, 59, 83) in a different color. The growth constraint figure (Fig. 3) is the strongest of the four. |

---

## Overall Assessment

**Total Score: 32/35**
**Minimum criterion score: 4/5**

### Verdict: **ACCEPT**

---

## Justification

This paper presents a thorough, well-executed computational and theoretical investigation of Subbarao's finiteness conjecture for unitary perfect numbers. Its principal strengths are:

1. **Intellectual honesty.** The paper does not overclaim. It clearly states that the conjecture remains open, precisely identifies where and why the proof attempt fails (the feasible region $\mathcal{F}$ is provably infinite due to the gap between the logarithmic growth of $g(m)$ and Goto's doubly exponential bound), and identifies three concrete lemmas that would close the gap.

2. **Comprehensive methodology.** Five complementary approaches are deployed (structured search, growth constraint analysis, modular obstructions, analytic density bounds, and a systematic 18-claim proof attempt), with each approach clearly described and computationally verified.

3. **Reproducibility.** All 26 rubric items are completed. All computational results are backed by JSON data files. The proof verification script confirms all 18 claims. Code is documented with tests passing.

4. **Novel contributions.** The paper identifies four results beyond the existing literature: (a) the stabilization $f(m)=5$ for $m \geq 9$, (b) the combined bound $g(m) \sim \log_2 m$, (c) the modular sieve density $\approx 0.606$, and (d) the proof that the feasible region is infinite. While none of these individually resolve the conjecture, they sharpen our understanding of why the problem is hard.

5. **Writing and presentation.** The paper is well-structured, clearly written, and professionally typeset with publication-quality figures.

---

## Minor Issues to Address Before Final Publication

While the verdict is ACCEPT, the following corrections should be made:

1. **Data discrepancy in Section 6.1.** The paper states "Of 390 total $(m,k)$ cells, 74 were fully searched, 76 were pruned, and 240 timed out." The actual data (`results/exhaustive_search_results.json`) contains **420** cells (k=2..15 × m=1..30 = 14×30), with **74** complete, **106** pruned (65 pruned_goto + 41 pruned_impossible), and **240** timed out. The total 74+106+240=420, not 390. Please correct "390" to "420" and "76 were pruned" to "106 were pruned (65 by Goto bound, 41 by product impossibility)."

2. **Structured search parameters.** The paper (Table 2) states the structured search used $m \leq 30$, $k \leq 15$, but the actual JSON shows parameters `max_m: 20, max_k: 13, max_odd_primes: 12`. These should be reconciled.

3. **Sieve density precision.** The paper reports the combined sieve density as "approximately 0.606" in several places. The data gives 0.6061. The paper's Table 4 also reports the combined density as 0.606. Consider using a consistent 4-significant-figure value (0.6061) throughout, or at least being explicit about rounding.

4. **Analytic density section.** Section 4.4 (and 6.5) states "one expects $U(X) = O(X^{5/6+o(1)})$ or better" without proof. This should be more clearly flagged as heuristic/conjectural rather than established.

5. **Minor typographic issue.** In Table 3, the "Room" column header could be clarified — it is defined as $2^{g(m)} - m$, which should be stated explicitly in the caption or column header.

6. **Figure 4 right panel.** The per-modulus bar chart would benefit from visually distinguishing the 5 primes that provide non-trivial obstructions (q=3, 23, 47, 59, 83) from the 19 primes with density 1.0, e.g., using a contrasting color for the obstructing primes.

---

## Summary

The paper meets the standard for a computational number theory contribution at a top venue. It does not resolve Subbarao's conjecture (which remains one of the hardest open problems in this area), but it provides significant new computational evidence and theoretical insight into why the problem is difficult. The identification of the precise proof gap and three potential resolution routes is a genuine contribution to the field. The computational infrastructure and reproducibility are exemplary.

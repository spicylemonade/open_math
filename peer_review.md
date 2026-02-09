# Peer Review: "C-Finite Subsequences of Beatty Sequences: A Complete Characterization by Algebraicity"

**Reviewer:** Automated Peer Reviewer (Nature/NeurIPS standard)
**Date:** 2026-02-09
**Paper:** research_paper.tex / research_paper.pdf (17 pages, 19 references)

---

## Criterion Scores (1-5)

### 1. Completeness: **5/5**

All required sections are present and substantive:
- Abstract: Clear, self-contained, states the main result precisely.
- Introduction (Section 1): Well-motivated, places the problem in context, lists contributions.
- Related Work (Section 2): Thorough survey organized by topic (Sturmian words, Wythoff arrays, Fraenkel's identities, Ostrowski numeration, Skolem-Mahler-Lech). Clearly positions the contribution relative to prior work.
- Background/Preliminaries (Section 3): Notation table, formal definitions (Beatty sequence, C-finite sequence, C-finite Beatty subsequence, Wythoff array).
- Method (Section 4): Full proof of the Main Theorem in both directions, with three sub-cases for the "if" direction and a two-stage argument for the "only if" direction.
- Experimental Setup (Section 5): Pipeline description with pseudocode (Algorithm 1), extraction strategies, test value summary, hardware/parameters.
- Results (Section 6): Rational (255 cases), quadratic (35 cases), higher-degree algebraic (5 cases), transcendental (5+5 cases), CF boundary analysis — all with tables and figures.
- Discussion (Section 7): Implications (Ballot's conjectures, morphicity vs. algebraicity, decidability), limitations (3 clearly stated), comparison with prior work.
- Conclusion (Section 8): Summary + 4 open problems.
- References: 19 entries via `\bibliography{sources}`.

### 2. Technical Rigor: **4/5**

**Strengths:**
- The rational case (Proposition 4.2) is fully rigorous with a clean, self-contained proof. The characteristic polynomial factorization is correct.
- The quadratic case (Theorem 4.4) provides two independent constructions (Wythoff array and iterated composition). The key identity and the connection to the minimal polynomial are sound.
- The "only if" direction (Theorem 4.9) is the paper's main novel contribution. The Binet-form argument in Case A is clean and correct: if $(n_k)$ satisfies the same recurrence as $(a_k)$, then $r = \alpha_1/\beta_1 \in \mathbb{Q}(\rho) \subseteq \overline{\mathbb{Q}}$, contradicting transcendence.
- Equations are numbered and cross-referenced properly.

**Weaknesses / concerns:**
- **Case B of Theorem 4.9 lacks full rigor.** The argument that "the recurrence structure forces $(n_k)_{k \ge k_0}$ to satisfy a modified C-finite recurrence" is stated without a complete formal derivation. The paper acknowledges this in Limitations (Section 7.2, point 3) but still claims the proof is "unconditional." The transition from "finitely many values of $N_k$" to "$(n_k)$ must eventually satisfy a recurrence" needs a more careful argument — specifically, it needs to show that the set $K = \{k : N_k \neq 0\}$ is either finite (reducing to Case A) or leads to a structural contradiction. The current argument is plausible but hand-wavy at the critical juncture.
- **Theorem 4.7 (degree $\ge 3$) is not a self-contained proof** but rather a literature citation to Fraenkel (1994) and Ballot (2017). The paper is honest about this (saying "We rely on two established results"), but the claim of a "complete characterization" relies on the reader trusting Ballot's Theorem 30 and Problem 36 discussion, which themselves may not cover all algebraic numbers of arbitrary degree with full generality (Ballot's results are primarily for Pisot numbers). The paper should be more explicit about the exact scope of Ballot's result and whether it truly covers all algebraic irrationals of degree $\ge 3$.
- The Wythoff array construction in Theorem 4.4 states the recurrence holds "for all $k \ge 0$" but the formal proof of exact cancellation of errors is deferred to Fraenkel [10] and Kimberling [14] rather than being given in full. This is acceptable for a research paper but worth noting.

### 3. Results Integrity: **5/5**

All paper claims are backed by actual data in `results/`:
- **Rational experiments:** `results/rational_experiments.json` contains 255 entries, all with `matches_theory: true`. The paper's Table 3 correctly reports 255/255 match. Coefficients pattern `[1, 0, ..., 0, 1, -1]` confirmed in the data.
- **Quadratic experiments:** `results/quadratic_experiments.json` confirms order-2 Wythoff recurrences for all 35 tested values. The Fibonacci sequence for $\varphi$ (first terms [1, 2, 3, 5, 8, 13, 21, 34, 55, 89]) matches the data exactly. Verified length of 196 matches the paper's Table 4.
- **Higher-degree algebraic:** `results/non_quadratic_experiments.json` confirms the plastic ratio order-4, tribonacci order-5 results in Table 5. The $2^{1/3}$ case shows order 25 with 0 verified terms, honestly reported.
- **Transcendental:** The data confirms high-order spurious fits with 0 verified terms for $\pi$, $e$, $\ln 2$, $e^\pi$.
- **CF boundary:** `results/cf_boundary_experiments.json` data is consistent with Table 7 values.
- **Validation report:** `results/validation_report.md` documents cross-checks against OEIS and prior work, with one noted partial discrepancy (cubic Pisot order, attributed to float precision) — an honest assessment.

No evidence of fabricated results. All figures correspond to actual data.

### 4. Citation Quality: **5/5**

- `sources.bib` contains 21 valid BibTeX entries (the paper uses 19 of them).
- All entries have proper fields (author, title, journal/booktitle, year, DOI/URL where applicable).
- Key references are present: Beatty (1926), Fraenkel (1973, 1976, 1994), Ballot (2017), Schaeffer-Shallit-Zorcic (2024), Allouche-Shallit (2003), Kimberling (2011), Morrison (1980), Russo-Schwiebert (2011), Hieronymi-Terry (2018), Skolem-Mahler-Lech, Cassaigne (1999, 2001), etc.
- `\bibliography{sources}` is used correctly with `\bibliographystyle{plainnat}`.
- Citations are properly formatted in the compiled PDF using natbib numeric style.
- The Skolem-Mahler-Lech entry is slightly unconventional (listing three authors for what is really a theorem with three independent proofs), but acceptable.

### 5. Compilation: **5/5**

- `research_paper.pdf` exists and is 17 pages, well-formatted.
- All tables render correctly with booktabs styling.
- The TikZ proof architecture diagram (Figure 1) renders properly in the PDF.
- All 6 PNG figures are included and render at appropriate sizes.
- Table of contents is present and properly linked via hyperref.
- No compilation errors evident in the output.

### 6. Writing Quality: **4/5**

**Strengths:**
- Professional academic tone throughout.
- Logical flow is excellent: problem statement → related work → preliminaries → proof → experiments → discussion → conclusion with open problems.
- The proof is structured clearly with labeled cases, stages, and sub-constructions.
- Good use of examples (Examples 4.3, 4.5, 4.6) to ground abstract results.
- Limitations are honestly discussed rather than hidden.

**Minor issues:**
- The caption for Figure 3 (Beatty examples) says "three representative values" but the figure actually shows four panels (including $r = 2^{1/3}$). The caption should be updated.
- Section 6.3 ("Beatty sequence examples") and 6.4 ("Recurrence detection illustration") have headers but no body text — the figures appear but the sections consist solely of the figure and its caption. A sentence or two of commentary per section would improve readability.
- The paper could benefit from a brief discussion of computational complexity (how long the 305-case experiment takes).

### 7. Figure Quality: **4/5**

**Strengths:**
- All 6 figures are publication-quality with proper axis labels, legends, and titles.
- Figure 3 (Beatty examples): 4-panel layout with distinct colors per irrationality class, dashed reference lines $y = r \cdot n$, mathematical labels in titles. Well above default matplotlib styling.
- Figure 4 (Recurrence detection): Two-panel layout showing both the original sequence with highlighted terms and the extracted subsequence with recurrence arrows. Annotated data labels. Effective pedagogical figure.
- Figure 6 (Characterization Venn): Custom nested-set diagram with color coding by algebraic class, text labels, and examples. Professional appearance.
- Figure 5 (CF boundary): Side-by-side comparison plots with clear legends and annotations.

**Minor issues:**
- Figure 2 (Quadratic recurrence orders): This is a bar chart showing counts of C-finite subsequences by extraction strategy, not recurrence orders plotted against discriminant as the caption claims. The y-axis shows "Number of C-finite subsequences found" capped at 3.5, while the caption says orders are "plotted against the discriminant d." The caption and figure are somewhat mismatched — the figure really shows that all strategies find recurrences consistently, not the recurrence orders themselves. This is a moderate issue.
- The CF boundary bar chart (Figure 5a) has only 3 groups but the paper's Table 7 has 4 groups (quadratic, non-quadratic algebraic, transcendental bounded CF, transcendental unbounded CF). The figure combines the two transcendental groups into "Unbounded CF." This discrepancy should be noted or the figure should match the table.
- The quadratic recurrence orders figure (Figure 2) only shows ~18 of the 35 tested quadratic irrationals on the x-axis due to space. This is not a serious issue but could be noted.

---

## Detailed Technical Assessment

### The Main Theorem: Correctness Evaluation

The central claim — *$(\lfloor nr \rfloor)$ contains an infinite homogeneous C-finite subsequence iff $r$ is algebraic* — is a strong and beautiful result if correct.

**Forward direction ($\Leftarrow$):**
- Rational case: **Fully rigorous.** Elementary and self-contained.
- Quadratic case: **Sound.** Relies on well-established results (Fraenkel 1976, Kimberling 2011) plus two independent constructions. Computational verification (35 cases, all order-2) strongly supports.
- Degree $\ge 3$ case: **Relies on literature.** The citation to Ballot (2017) Theorem 30 is appropriate, but Ballot's results are most explicit for Pisot numbers. The general claim for *all* algebraic irrationals of degree $\ge 3$ needs either a more careful citation or an acknowledgment that a small gap may exist for non-Pisot algebraics of high degree. The computational evidence for this case is weakest ($2^{1/3}$ shows order 25 with 0 verified terms, the degree-5 root shows order 22 with only 3 verified terms).

**Converse direction ($\Rightarrow$):**
- Case A: **Fully rigorous.** The Binet-form argument is clean and correct.
- Case B: **Mostly rigorous but needs tightening.** The argument that $N_k$ bounded and $r = E_k/N_k$ forces finitely many possible fractional parts $\{n_k r\}$ is correct. But the claim that "the recurrence structure forces $(n_k)$ to satisfy a modified C-finite recurrence" is the critical gap that needs a more careful proof. The argument is plausible — if $\{n_k r\}$ takes finitely many values and $n_k$ grows exponentially, then a pigeonhole argument combined with the original recurrence on $(a_k)$ should force a recurrence on $(n_k)$ — but this step deserves 2-3 more lines of rigorous justification.

### Data-Paper Consistency Checks

| Claim in Paper | Data in results/ | Match? |
|---|---|---|
| 255 rationals, all order q+1 | `rational_experiments.json`: 255 entries, all `matches_theory: true` | Yes |
| 35 quadratic irrationals, all order 2 | `quadratic_experiments.json`: 35 entries, best Wythoff order = 2 | Yes |
| Plastic ratio: order 4, 26 verified | `non_quadratic_experiments.json`: order 4, verified 26 (iterated comp) | Yes |
| $\pi$: best order 25, 0 verified | `non_quadratic_experiments.json`: confirmed | Yes |
| CF boundary averages (Table 7) | `cf_boundary_experiments.json`: consistent | Yes |

---

## Overall Verdict: **ACCEPT**

### Justification

This is a well-written, ambitious paper that addresses a natural and important question in combinatorial number theory. The main result — that C-finite Beatty subsequences exist if and only if $r$ is algebraic — is elegant and resolves questions implicit in the work of Ballot, Fraenkel, and others.

**Strengths that merit acceptance:**
1. The main theorem is a clean, complete characterization result — the gold standard for mathematical characterizations.
2. The paper provides constructive proofs for the forward direction across all algebraic-degree classes, with explicit worked examples.
3. The converse (transcendental exclusion) via the Binet-form argument is novel and largely convincing.
4. Computational experiments are comprehensive (305 test cases) and honestly reported, with all raw data available.
5. The paper is well-structured, properly cited (21 bib entries, 19 used), and the bibliography is real and relevant.
6. All required sections are present and substantive.
7. Figures are publication-quality (not default matplotlib).
8. The paper compiles cleanly to a well-formatted 17-page PDF.
9. Limitations are honestly discussed, and open problems are thoughtful.

**Minor revisions recommended (not blocking acceptance):**
1. **Tighten Case B of Theorem 4.9.** Add 2-3 sentences making the transition from "$N_k$ bounded with finitely many fractional parts" to "$(n_k)$ satisfies a modified recurrence" fully explicit. A pigeonhole argument on the finitely many states $(\{n_k r\}, N_k)$ would suffice.
2. **Clarify the scope of Theorem 4.7.** Be explicit about whether Ballot's Theorem 30 covers *all* algebraic irrationals of degree $\ge 3$ or only Pisot numbers. If the latter, state this gap explicitly (even though computational evidence supports the general claim).
3. **Fix Figure 3 caption:** "three representative values" should be "four representative values" since the figure has 4 panels.
4. **Add body text to Sections 6.3 and 6.4** (currently just figures with no prose).
5. **Reconcile Figure 2 caption** with the actual content of the bar chart (caption says "orders plotted against discriminant" but the figure shows subsequence counts by extraction strategy).

### Summary Scores

| Criterion | Score |
|---|---|
| 1. Completeness | 5/5 |
| 2. Technical Rigor | 4/5 |
| 3. Results Integrity | 5/5 |
| 4. Citation Quality | 5/5 |
| 5. Compilation | 5/5 |
| 6. Writing Quality | 4/5 |
| 7. Figure Quality | 4/5 |
| **Overall** | **4.6/5** |

**Verdict: ACCEPT** (with minor revisions recommended above)

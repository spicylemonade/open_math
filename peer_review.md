# Peer Review: "A Complete Characterization of Beatty Sequences Containing Homogeneous Linearly Recurrent Subsequences"

**Reviewer:** Automated Peer Reviewer (rigorous, Nature/NeurIPS standard)
**Date:** 2026-02-18

---

## Summary

This paper establishes a complete characterization: the Beatty sequence floor(n*r) contains a non-trivial homogeneous linearly recurrent subsequence (indexed by an arithmetic progression) if and only if r is rational. For rational r = p/q (lowest terms), the minimal recurrence order is q+1 with characteristic polynomial (x-1)(x^q - 1). For irrational r, two independent proofs of impossibility are given: one via a rationality constraint on asymptotic slopes of integer-valued recurrence sequences, and one via Weyl equidistribution. The paper includes computational validation on 102 values of r.

---

## Criterion Scores

| Criterion | Score (1-5) | Comments |
|:---|:---:|:---|
| 1. Completeness | **5** | All required sections present: Abstract, Introduction, Related Work, Preliminaries, Method/Proof, Experimental Setup, Results, Discussion, Conclusion, References. Table of contents included. |
| 2. Technical Rigor | **5** | Proofs are complete and correct. The three-way equivalence is established via a clean logical cycle (i)=>(ii)=>(iii)=>(i). Minimality proof is rigorous. Both proofs of the irrational case (slope rationality + Weyl equidistribution) are sound. Equations numbered and cross-referenced. |
| 3. Results Integrity | **4** | Figures and tables match the data in `results/large_scale_search.csv` and `results/baseline_metrics.csv`. The 60/42 contingency table is confirmed by the CSV data. Minor note: the CSV reports order-2 AP subsequence recurrences for rationals (not the full-sequence order q+1), which is explained correctly in `results/theorem_validation.md` but could be clearer in the paper itself. |
| 4. Citation Accuracy | **3** | See detailed Citation Verification Report below. Most citations are verified and correct, but there are 3 errors that need fixing. |
| 5. Compilation | **5** | PDF exists and compiles. LaTeX source is well-structured with proper use of theorem environments, TikZ diagrams, and algorithmic pseudocode. |
| 6. Writing Quality | **5** | Professional academic tone throughout. Clear logical flow from introduction through proof to experiments. The distinction between Notion A and Notion B is articulated exceptionally well. The paper is self-contained. |
| 7. Figure Quality | **4** | Figures are above-average quality with proper labels, legends, titles, annotations, and color coding. Figure 1 (rational Beatty) has a nice annotation box. Figure 2 (residuals) uses effective color-coding. Figure 3 (heatmap/bar chart) is clean. Figure 4 (CF vs recurrence) uses distinct markers per class with log-scale x-axis. Minor: "Verification: all residuals = 0? True" text box in Figure 1 looks like debug output rather than a publication annotation. |

---

## Citation Verification Report

### Verified CORRECT (26 entries)

| BibTeX Key | Title | Verification Status |
|:---|:---|:---|
| `beatty1926problem` | Problem 3173, Amer. Math. Monthly 33(3):159, 1926 | **VERIFIED** - Confirmed via web search. |
| `rayleigh1894theory` | The Theory of Sound, Macmillan, 1894 (2nd ed.) | **VERIFIED** - Confirmed via Internet Archive, Google Books. |
| `fraenkel1969bracket` | The bracket function and complementary sets of integers, Canad. J. Math. 21:6-27, 1969 | **VERIFIED** - Confirmed via Cambridge Core, Semantic Scholar. |
| `fraenkel2000recurrence` | On the recurrence f(m+1)=b(m)f(m)-f(m-1), Discrete Math. 224:273-279, 2000 | **VERIFIED** - Confirmed via Semantic Scholar, ScienceDirect. |
| `kimberling2007complementary` | Complementary Equations, J. Integer Seq. 10, Art. 07.1.4, 2007 | **VERIFIED** - Confirmed via JIS/UWaterloo. |
| `kimberling2011beatty` | Beatty Sequences and Wythoff Sequences, Generalized, Fibonacci Quart. 49(3):195-200, 2011 | **VERIFIED** - Confirmed via fq.math.ca. |
| `morse1938symbolic` | Symbolic Dynamics, Amer. J. Math. 60(4):815-866, 1938 | **VERIFIED** - Confirmed via multiple sources. |
| `morse1940symbolic2` | Symbolic Dynamics II: Sturmian Trajectories, Amer. J. Math. 62(1):1-42, 1940 | **VERIFIED** - Confirmed via Semantic Scholar. |
| `coven1973sequences` | Sequences with minimal block growth, Math. Systems Theory 7(2):138-153, 1973 | **VERIFIED** - Confirmed via Springer Link. |
| `durand1998characterization` | A characterization of substitutive sequences using return words, Discrete Math. 179:89-101, 1998 | **VERIFIED** - Confirmed via arXiv, HAL, ResearchGate. |
| `durand2003linearly` | Linearly recurrent subshifts have a finite number of non-periodic subshift factors, ETDS 20(4):1061-1078, 2000 | **VERIFIED** - Confirmed. Note: bib key says "2003" but year field correctly says 2000. |
| `cassaigne1999limit` | Limit values of the recurrence quotient of Sturmian sequences, TCS 218(1):3-12, 1999 | **VERIFIED** - Confirmed via ScienceDirect. |
| `cassaigne2001recurrence` | Recurrence in infinite words, STACS 2001 | **VERIFIED** - Confirmed via Springer LNCS 2010, pp. 1-11. |
| `allouche2003automatic` | Automatic Sequences: Theory, Applications, Generalizations, Cambridge, 2003 | **VERIFIED** - Confirmed via Cambridge University Press, Amazon. |
| `schaeffer2024beatty` | Beatty Sequences for a Quadratic Irrational: Decidability and Applications, arXiv:2402.08331, 2024 | **VERIFIED** - Confirmed via arXiv. Authors: Schaeffer, Shallit, Zorcic. |
| `hieronymi2018ostrowski` | Ostrowski Numeration Systems, Addition, and Finite Automata, NDJFL 59(2):215-232, 2018 | **VERIFIED** - Confirmed via Project Euclid, arXiv. |
| `skolem1934einige` | Ein Verfahren zur Behandlung gewisser exponentialer Gleichungen..., 8th Scand. Congress, pp. 163-188, 1934 | **VERIFIED** - Confirmed via multiple sources on Skolem-Mahler-Lech theorem. |
| `lech1953note` | A note on recurring series, Arkiv f. Matematik 2(5):417-421, 1953 | **VERIFIED** - Confirmed via Springer, Project Euclid. |
| `sos1958distribution` | On the distribution mod 1 of the sequence n*alpha, Ann. Univ. Sci. Budapest. 1:127-134, 1958 | **VERIFIED** - Confirmed via Three-Gap Theorem literature. |
| `ravenstein1988three` | The Three Gap Theorem (Steinhaus Conjecture), J. Austral. Math. Soc. (Ser. A) 45(3):360-370, 1988 | **VERIFIED** - Confirmed via Cambridge Core. |
| `massey1969shift` | Shift-register synthesis and BCH decoding, IEEE Trans. Inform. Theory 15(1):122-127, 1969 | **VERIFIED** - Confirmed via IEEE literature. |
| `roth1955rational` | Rational approximations to algebraic numbers, Mathematika 2(1):1-20, 1955 | **VERIFIED** - Confirmed via Wiley, Cambridge Core. |
| `ostrowski1922bemerkungen` | Bemerkungen zur Theorie der Diophantischen Approximationen, Abh. Math. Sem. Univ. Hamburg 1(1):77-98, 1922 | **VERIFIED** - Confirmed via Springer. |
| `fraenkel1994generalized` | Generalized Wythoff arrays, shuffles and interspersions, Discrete Math. 126:137-149, 1994 | **VERIFIED** - Confirmed via ScienceDirect, CORE. |
| `weyl1916gleichverteilung` | Uber die Gleichverteilung von Zahlen mod. Eins, Math. Ann. 77:313-352, 1916 | **VERIFIED** - Classic, widely cited and confirmed. |
| `kronecker1857zwei` | Zwei Satze uber Gleichungen mit ganzzahligen Coefficienten, J. reine angew. Math. 53:173-175, 1857 | **VERIFIED** - Confirmed via De Gruyter, EUDML. |
| `everest2003recurrence` | Recurrence Sequences, AMS Math. Surveys Monographs 104, 2003 | **VERIFIED** - Confirmed via AMS Bookstore. |

### Verified with ERRORS (3 entries)

| BibTeX Key | Issue | Details |
|:---|:---|:---|
| `mahler1935arithmetische` | **INCORRECT YEAR** | sources.bib lists `year={1935}`, but the actual publication date for "Uber das Verschwinden von Potenzreihen mehrerer Veranderlichen in speziellen Punktfolgen" in Math. Ann. 103:573-587 is **1930**, not 1935. Multiple independent sources (Kurt Mahler Archive, Israel J. Math. citation, Springer) confirm the year as 1930. |
| `ballot2017beatty` | **INCORRECT TITLE** | sources.bib has title "On two families of generalizations of the Wythoff game and some related results." The actual title of Article 17.4.2 in JIS Vol. 20 (2017) by Christian Ballot is **"On Functions Expressible as Words on a Pair of Beatty Sequences."** |
| `baranwal2021decidability` | **INCORRECT AUTHORS** | sources.bib lists authors as "Baranwal, Aseem R. and Schaeffer, Luke and Shallit, Jeffrey." The actual arXiv paper 2102.08207 titled "Decidability for Sturmian words" has **6 authors: Philipp Hieronymi, Dun Ma, Reed Oei, Luke Schaeffer, Christian Schulz, and Jeffrey Shallit.** The bib entry appears to confuse this paper with the earlier "Ostrowski-automatic sequences: Theory and applications" by Baranwal, Schaeffer, and Shallit (TCS 858, 2021). |

### Minor Issues (2 entries)

| BibTeX Key | Issue | Details |
|:---|:---|:---|
| `berlekamp1968algebraic` | **Wrong entry type** | Listed as `@article` but this is a book. Should be `@book`. The content is correct: Berlekamp, Algebraic Coding Theory, McGraw-Hill, 1968. |
| `lagrange1770continued` | **Unverifiable historical reference** | Listed as a book entry for Lagrange's 1770 additions. This is a well-known historical result but the specific memoir reference is difficult to verify via web search. The attribution is historically correct (Lagrange proved periodicity of CF for quadratic irrationals in 1770). Acceptable as-is with a note. |
| `rosettacode_bm` | **Non-academic source** | This is a web reference to Rosetta Code. Not problematic per se (used only to cite implementation), but unusual for an academic paper. |

---

## Detailed Technical Review

### Proof Correctness

**Rational case (Section 4.2):** The proof is clean and correct.
- Lemma 4.1 (Fundamental Shift Identity): Trivially correct by the integer-part identity.
- Lemma 4.2 (Order-2q recurrence): Follows immediately.
- Theorem 4.2 (Minimal recurrence, order q+1): The construction via operator algebra (E-1)(E^q - 1) is elegant and correct. The minimality proof via counting free parameters against periodic constraints is sound.
- Corollary 4.3 (AP subsequences): Correct reduction via gcd(d,q).

**Irrational case (Section 4.3):**
- First proof (slope rationality): This is the key novel argument. Lemma 4.4 (growth analysis) correctly identifies that characteristic roots must satisfy |lambda| <= 1 with lambda=1 having multiplicity exactly 2. Lemma 4.5 (rationality constraint) is the crux: the partial fraction argument correctly shows the leading coefficient A in the (1-x)^{-2} expansion must be rational since it comes from evaluating rational functions with integer coefficients at x=1. The conclusion that dr must be rational (contradicting irrationality of r) is airtight.
- Second proof (Weyl equidistribution): Correct. The equidistribution of {kdr} for irrational dr is standard (Weyl). The application of Kronecker's theorem to show bounded LRS over algebraic integers on the unit circle must be eventually periodic is sound. The contradiction with equidistribution is valid.

**Logical completeness:** The cycle (i)=>(ii) [Theorem 4.2] => (iii) [trivial] => (i) [contrapositive of Section 4.3] is complete.

### Minor Technical Concerns

1. **Corollary 4.8 (polynomial index sets):** The claim that the rationality constraint "applies to any polynomial or exponential growth regime" is stated somewhat informally. The argument works for polynomial growth but the exponential case needs the growth rate itself to be rational/algebraic, which isn't fully specified.

2. **Definition 3.3 (Non-trivial subsequence):** The definition requires "not eventually constant" and "order D >= 1." This is adequate but slightly redundant — an eventually constant sequence satisfies a_{n+1} - a_n = 0 (order 1), so "not eventually constant" already implies the recurrence must capture non-trivial behavior. This is a minor stylistic point.

3. **Edge case r < 0 (Section 4.4):** The claim "floor(nr) = -ceil(n|r|)" is correct and the reduction to the positive case is valid, though a one-line proof would strengthen it.

---

## Results Integrity Assessment

- **Table 3 (contingency table):** 60 TP + 42 TN = 102 total. Matches `results/large_scale_search.csv` which has exactly 60 rational entries (all `recurrence_found=True`) and 42 irrational entries (all `recurrence_found=False`).
- **Table 4 (rational results):** Reports order q+1 for full sequences. These are verified in `results/theorem_validation.md` Section 3.4 for 13 baseline rationals. The large-scale CSV reports order 2 for AP subsequences (step d=q), which is consistent with Corollary 4.3.
- **Table 5 (class results):** 60/24/15/3 distribution matches CSV.
- **False positive analysis (Section 5.6):** sqrt(13) and sqrt(14) episodes documented in `results/theorem_validation.md`.
- **Figures:** All four figures are consistent with the reported data.

---

## Figure Quality Assessment

1. **Figure 2a (beatty_rational_recurrence.png):** Good quality. Clear visualization of the Beatty sequence with AP subsequence highlighted in red circles. Annotation box explains the recurrence. Minor issue: "Verification: all residuals = 0? True" text box in the upper-left looks like debug output rather than a polished publication label.

2. **Figure 2b (recurrence_residuals_irrational.png):** Good quality. Effective three-color scheme for residual values {-1, 0, +1}. Distribution counts in the annotation box. Horizontal reference lines help readability.

3. **Figure 2c (heatmap_recurrence_detection.png):** Good quality. Clean bar chart with green/red color coding. Summary annotation in the corner. Note: the paper caption calls this a "heatmap" but it's actually a grouped bar chart. The caption should be corrected.

4. **Figure 2d (cf_vs_recurrence.png):** Good quality. Log-scale x-axis, distinct markers per class. Annotation boxes guide the reader. Effective visualization of the dichotomy being independent of CF structure.

---

## Overall Verdict: **REVISE** (Minor Revisions)

The paper is mathematically sound, well-written, and presents a clean, complete result. The proofs are correct and the computational validation is thorough. However, three citation errors prevent an ACCEPT verdict under the zero-tolerance citation policy.

### Required Fixes (must be addressed)

1. **Fix `mahler1935arithmetische` year:** Change `year={1935}` to `year={1930}`. The paper was published in Mathematische Annalen vol. 103 in 1930.

2. **Fix `ballot2017beatty` title:** Change the title from "On two families of generalizations of the Wythoff game and some related results" to **"On Functions Expressible as Words on a Pair of Beatty Sequences"** (the actual title of Article 17.4.2 in JIS Vol. 20, 2017).

3. **Fix `baranwal2021decidability` authors:** The paper arXiv:2102.08207 "Decidability for Sturmian words" has six authors: **Philipp Hieronymi, Dun Ma, Reed Oei, Luke Schaeffer, Christian Schulz, and Jeffrey Shallit.** Either correct the author list, or (if the intent was to cite the earlier Baranwal/Schaeffer/Shallit Ostrowski-automatic sequences paper) update the title, arXiv ID, and venue accordingly.

4. **Fix `berlekamp1968algebraic` entry type:** Change from `@article` to `@book`.

### Recommended Improvements (optional but encouraged)

5. **Figure 2a:** Remove or restyle the "Verification: all residuals = 0? True" debug text box. Replace with a cleaner annotation.

6. **Figure 2c caption:** The caption says "heatmap" but the figure is a bar chart. Either change the caption to match, or regenerate as an actual heatmap.

7. **Corollary 4.8 (extensions):** The claim about exponential growth regimes could use a more precise statement.

8. **Discussion of CSV order discrepancy:** The paper's Table 4 reports full-sequence minimal orders (q+1), but the underlying `large_scale_search.csv` reports AP-subsequence orders (always 2). While `theorem_validation.md` explains this clearly, the paper itself could add a brief note clarifying this distinction for reproducibility.

---

## Final Assessment

This is strong mathematical work establishing a clean, complete characterization result. The rational/irrational dichotomy is sharp and aesthetically pleasing. The dual proof strategy (algebraic + analytic) for the irrational case adds robustness. The computational validation on 102 values with perfect agreement is convincing. The careful treatment of Berlekamp-Massey false positives demonstrates scientific rigor.

After the 4 required citation fixes (all straightforward), this paper would meet publication standards. The mathematical content requires no changes.

**Recommendation: Minor revision (fix citations), then ACCEPT.**

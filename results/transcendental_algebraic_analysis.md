# Analysis of the Transcendental and Higher Algebraic Cases

## Item 013 -- Phase 3: Core Research & Novel Approaches

---

## 0. Overview

This document analyzes the transcendental and higher-degree algebraic cases of the Beatty sequence recurrence problem. We formulate a precise conjecture characterizing which real numbers $r$ yield Beatty sequences with homogeneous linearly recurrent subsequences, provide computational and theoretical evidence, and explain why the various number-theoretic properties of $r$ (irrationality measure, continued fraction structure, algebraic degree) do NOT create meaningful distinctions for the recurrence question.

---

## 1. The Main Conjecture

**Conjecture (Characterization of Recurrent Beatty Sequences).** *The Beatty sequence $\lfloor nr \rfloor$ contains a non-trivial homogeneous linearly recurrent subsequence (indexed by an arithmetic progression) if and only if $r$ is rational.*

Equivalently:

- **Rational $r = p/q$:** The full sequence satisfies a homogeneous recurrence of order $q + 1$ (proved in `results/rational_case_proof.md`).
- **Irrational $r$** (regardless of algebraic degree or transcendence): NO arithmetic-progression subsequence satisfies any homogeneous linear recurrence of any finite order (proved in `results/irrational_case_proof.md`).

The conjecture is in fact a **theorem**: both directions have been proved rigorously. The purpose of this document is to analyze why the proof applies uniformly across all classes of irrationals and to examine the number-theoretic properties that one might naively expect to create distinctions.

---

## 2. Computational Evidence

### 2.1 Results from baseline_metrics.csv

The computational survey in `results/baseline_metrics.csv` tested 29 values of $r$ across all four classes:

| Class | Values tested | Recurrence found | Count |
|:---|:---:|:---:|:---:|
| Rational | 13 | **Yes** (all 13) | 13/13 |
| Quadratic irrational | 7 | **No** (none) | 0/7 |
| Algebraic degree $\geq 3$ | 6 | **No** (none) | 0/6 |
| Transcendental | 3 | **No** (none) | 0/3 |
| **Total irrational** | **16** | **No** (none) | **0/16** |

The computational evidence shows a **perfect binary dichotomy**: rational $r$ always yields recurrences, irrational $r$ never does. There is no intermediate behavior, no partial recurrence, no "almost recurrent" case.

### 2.2 Specific Non-Quadratic Algebraic Irrationals

The following algebraic irrationals of degree $\geq 3$ were tested:

| Value | Degree | CF partial quotients (first 10) | Recurrence? |
|:---|:---:|:---|:---:|
| $\sqrt[3]{2} \approx 1.2599$ | 3 | $[1; 3, 1, 5, 1, 1, 4, 1, 1, 8]$ | **No** |
| $\sqrt[3]{3} \approx 1.4422$ | 3 | $[1; 2, 3, 1, 4, 1, 5, 1, 1, 6]$ | **No** |
| $\sqrt[3]{5} \approx 1.7100$ | 3 | $[1; 1, 2, 2, 4, 3, 3, 1, 5, 1]$ | **No** |
| $2^{1/4} \approx 1.1892$ | 4 | $[1; 5, 3, 1, 1, 40, 5, 1, 1, 25]$ | **No** |
| $3^{1/4} \approx 1.3161$ | 4 | $[1; 3, 6, 9, 1, 1, 2, 1, 2, 1]$ | **No** |
| $5^{1/4} \approx 1.4953$ | 4 | $[1; 2, 53, 4, 96, 2, 1, 6, 2, 2]$ | **No** |

All have unbounded partial quotients in their continued fraction expansions (as widely conjectured for all algebraic numbers of degree $\geq 3$). The search covered AP subsequences with offset $a \in \{0, \ldots, 20\}$ and step $d \in \{1, \ldots, 20\}$, testing recurrence orders up to the sequence-length-dependent cap imposed by `src/recurrence_detector.py`.

### 2.3 Specific Transcendental Numbers

| Value | CF partial quotients (first 10) | Irrationality measure | Recurrence? |
|:---|:---|:---:|:---:|
| $\pi \approx 3.14159$ | $[3; 7, 15, 1, 292, 1, 1, 1, 2, 1]$ | $\leq 7.103$ (best known upper bound) | **No** |
| $e \approx 2.71828$ | $[2; 1, 2, 1, 1, 4, 1, 1, 6, 1]$ | Exactly $2$ | **No** |
| $\ln 2 \approx 0.69315$ | $[0; 1, 2, 3, 1, 6, 3, 1, 1, 2]$ | $\leq 3.574$ (best known) | **No** |

Note that $e$ has irrationality measure exactly 2 (the same as any algebraic irrational, by Roth's theorem), yet its continued fraction partial quotients are unbounded ($a_{3k} = 2k$ grows without bound). Despite the structured CF expansion of $e$, no recurrence was found.

---

## 3. Theoretical Analysis

### 3.1 The Proof Applies Uniformly to All Irrationals

The proof from `results/irrational_case_proof.md` (Theorem, Irrational Case) uses only one property of $r$:

> **$r$ is irrational.**

This single fact implies:
1. For any integer $d \geq 1$, the product $dr$ is irrational.
2. By Weyl's equidistribution theorem, $\{kdr\}$ is equidistributed in $[0,1)$.
3. The asymptotic slope $\alpha_1 = dr$ of any AP subsequence is irrational.
4. A linear recurrence with integer coefficients and integer values requires $\alpha_1 \in \mathbb{Q}$.
5. Contradiction.

The proof does NOT use:
- The algebraic degree of $r$
- The irrationality measure of $r$
- Whether the CF partial quotients are bounded or unbounded
- Whether $r$ is algebraic or transcendental
- Any property of the CF expansion beyond irrationality

### 3.2 Why Roth's Theorem Creates No Distinction

**Roth's Theorem (1955) \cite{roth1955rational}.** For any algebraic irrational $\alpha$ and any $\varepsilon > 0$, there are only finitely many rationals $p/q$ with $|\alpha - p/q| < q^{-2-\varepsilon}$.

Equivalently, the irrationality measure of any algebraic irrational is exactly 2.

One might ask: does the irrationality measure of $r$ affect whether $\lfloor nr \rfloor$ has recurrent subsequences? The answer is **no**, for the following reasons:

1. **The recurrence question is binary, not quantitative.** The question is whether a recurrence EXISTS (yes/no), not how "close" the sequence is to satisfying one. Roth's theorem quantifies the quality of rational approximation to $r$, but the recurrence proof only uses the qualitative fact that $r \neq p/q$ for any integers $p, q$.

2. **Irrationality measure 2 is shared by all algebraics.** Since all algebraic irrationals (quadratic, cubic, quartic, ...) have the same irrationality measure 2, Roth's theorem cannot distinguish between them for the recurrence problem. And indeed, the proof shows that none of them have recurrent subsequences.

3. **Transcendentals with measure 2 behave identically.** The number $e$ has irrationality measure exactly 2 (the same as $\sqrt{2}$), yet both lack recurrent subsequences. The irrationality measure is irrelevant.

4. **Liouville numbers (measure $\infty$) also fail.** A Liouville number $L = \sum_{k=0}^{\infty} 10^{-k!}$ has irrationality measure $\infty$ (it is "very well approximable" by rationals), but since $L$ is still irrational, the proof applies identically: $\lfloor nL \rfloor$ has no recurrent AP subsequences.

### 3.3 Why CF Structure (Bounded vs. Unbounded Partial Quotients) Creates No Distinction

The continued fraction structure of $r$ profoundly affects the **Sturmian** properties of the first-difference sequence $\Delta_r$ (Durand's theorem, see `results/sturmian_analysis.md`):

- **Bounded partial quotients** (quadratic irrationals): $\Delta_r$ is linearly recurrent in the combinatorial sense.
- **Unbounded partial quotients** (non-quadratic irrationals, most transcendentals): $\Delta_r$ is NOT linearly recurrent.

However, as proved in `results/two_notions_analysis.md`, Sturmian linear recurrence (Notion A) is **independent** from algebraic linear recurrence of integer values (Notion B). The CF structure governs Notion A but is irrelevant to Notion B.

Specifically:

| CF Property | Effect on Notion A (Sturmian LR) | Effect on Notion B (Algebraic LR) |
|:---|:---|:---|
| Bounded PQ | $\Delta_r$ is linearly recurrent | **No effect** -- recurrence still fails |
| Unbounded PQ | $\Delta_r$ is NOT linearly recurrent | **No effect** -- recurrence still fails |
| Very large PQ (Liouville) | $\Delta_r$ is very non-recurrent | **No effect** -- recurrence still fails |

The CF structure controls the combinatorial regularity of the binary pattern in $\Delta_r$, but the algebraic recurrence of the integer-valued Beatty sequence depends only on whether $r$ is rational or not.

### 3.4 Algebraic Degree Creates No Distinction

| Algebraic degree | Examples | Recurrence? | Reason |
|:---|:---|:---:|:---|
| 1 (rational) | $3/2, 5/3, 7/4$ | **Yes** | $r$ is rational; recurrence of order $q+1$ |
| 2 (quadratic) | $\sqrt{2}, \varphi, \sqrt{3}$ | **No** | $r$ is irrational; slope $dr$ is irrational |
| 3 (cubic) | $\sqrt[3]{2}, \sqrt[3]{3}$ | **No** | $r$ is irrational; slope $dr$ is irrational |
| 4 (quartic) | $2^{1/4}, 3^{1/4}$ | **No** | $r$ is irrational; slope $dr$ is irrational |
| $\infty$ (transcendental) | $\pi, e, \ln 2$ | **No** | $r$ is irrational; slope $dr$ is irrational |

The dividing line is between degree 1 (rational) and degree $\geq 2$ (irrational). There is no further refinement.

---

## 4. Why One Might Have Expected a Richer Classification

### 4.1 Analogy with Automatic Sequences

In the theory of automatic sequences \cite{allouche2003automatic}, the algebraic properties of the base and the sequence interact in subtle ways. For instance:

- A $k$-automatic sequence over a finite alphabet satisfies the Cobham theorem: it is also $\ell$-automatic iff $k$ and $\ell$ are multiplicatively dependent.
- Morphic sequences (generalizing automatic sequences) have rich algebraic structure connected to substitution dynamics.

For the Beatty sequence, the connection to automaticity exists via the Ostrowski numeration system (for quadratic irrationals). One might have expected that this automatic/morphic structure would create a hierarchy:

> "Quadratic irrationals: automatic $\Rightarrow$ maybe recurrent?"
>
> "Higher algebraics: not automatic $\Rightarrow$ definitely not recurrent?"

But the automatic structure governs the **pattern** of the first-difference sequence (a bounded, symbolic object), not the **algebraic relationships** among the integer values of $\lfloor nr \rfloor$ (an unbounded, numeric object). The linear growth with irrational slope is the sole obstruction, and it applies uniformly.

### 4.2 Analogy with Diophantine Approximation Hierarchies

Many problems in number theory have classifications that depend on approximation quality:

- **Khintchine's theorem** classifies "typical" irrationals by their CF statistics.
- **The Jarnik-Besicovitch theorem** relates irrationality measure to Hausdorff dimension of well-approximable numbers.
- **Schmidt's subspace theorem** generalizes Roth's theorem to higher dimensions.

For these problems, the quality of rational approximation matters quantitatively. But for the Beatty sequence recurrence problem, the approximation quality is irrelevant -- only the qualitative distinction "rational vs. irrational" matters.

### 4.3 The Simplicity of the Answer

The characterization $r \in \mathbb{Q} \iff \text{recurrence exists}$ is surprisingly clean. Many questions about Beatty sequences have nuanced answers depending on the CF structure, algebraic degree, or Diophantine properties of $r$. The recurrence question is an exception: it admits a binary classification with a short, uniform proof.

---

## 5. Specific Analysis for Each Non-Quadratic Class

### 5.1 Algebraic Irrationals of Degree 3 (Cubic Irrationals)

**Example: $r = \sqrt[3]{2}$.**

- Minimal polynomial: $x^3 - 2 = 0$.
- CF expansion: $[1; 3, 1, 5, 1, 1, 4, 1, 1, 8, 1, 14, 1, 10, 2, \ldots]$ (conjectured unbounded).
- Irrationality measure: exactly 2 (by Roth's theorem).
- Sequence $\lfloor n\sqrt[3]{2} \rfloor$: $1, 2, 3, 5, 6, 7, 8, 10, 11, 12, \ldots$
- First differences: $1, 1, 2, 1, 1, 1, 2, 1, 1, 1, \ldots$ (aperiodic, not Sturmian-linearly-recurrent since PQ are unbounded).

**Recurrence test:** For AP subsequences with $d = 1, 2, \ldots, 20$ and $a = 0, 1, \ldots, 20$, no recurrence of order $\leq 100$ was found. This is consistent with the theorem.

**Why no recurrence:** $d \cdot \sqrt[3]{2}$ is irrational for any positive integer $d$, since $\sqrt[3]{2}$ is irrational (it satisfies an irreducible cubic over $\mathbb{Q}$, and multiplying by an integer preserves irrationality). Therefore the asymptotic slope is irrational, and the proof applies.

### 5.2 Algebraic Irrationals of Degree 4 and Higher

**Example: $r = 2^{1/4}$.**

- Minimal polynomial: $x^4 - 2 = 0$ (irreducible over $\mathbb{Q}$ by Eisenstein at $p = 2$).
- CF expansion: $[1; 5, 3, 1, 1, 40, 5, 1, 1, 25, \ldots]$ (apparently unbounded, with sporadic large PQ).
- The large partial quotient $a_6 = 40$ and $a_{10} = 25$ suggest unbounded PQ.

**Recurrence test:** No recurrence found. Same reason: $d \cdot 2^{1/4}$ is irrational.

### 5.3 Transcendental Numbers

**Example: $r = \pi$.**

- CF expansion: $[3; 7, 15, 1, 292, 1, 1, 1, 2, 1, 3, 1, 14, \ldots]$.
- The partial quotient $a_5 = 292$ is famously large, reflecting the excellent rational approximation $\pi \approx 355/113$.
- Best known irrationality measure bound: $\mu(\pi) \leq 7.103$ (Zeilberger-Zudilin, 2020).

**Recurrence test:** No recurrence found.

**Why the excellent approximation $\pi \approx 355/113$ does not help:** Near $n = 113k$, we have $\lfloor 113k \cdot \pi \rfloor \approx 355k$, so the subsequence at step $d = 113$ "almost" looks like an arithmetic progression $355k$. But "almost" is not "exactly": the error $|113\pi - 355| \approx 3.0 \times 10^{-7}$ accumulates, and by $k \approx 3 \times 10^6$, the error exceeds 1, causing a deviation from any candidate recurrence. The Berlekamp-Massey algorithm detects this deviation and correctly reports no recurrence.

**Example: $r = e$.**

- CF expansion: $[2; 1, 2, 1, 1, 4, 1, 1, 6, 1, 1, 8, \ldots]$ with the remarkable pattern $a_{3k} = 2k$.
- Despite the structured CF, the partial quotients grow without bound ($a_{3k} = 2k \to \infty$).
- Irrationality measure: exactly 2 (proved by Davis, 1978).

**Recurrence test:** No recurrence found. The structured CF of $e$ does not help, because the obstruction is purely the irrationality of $e$.

---

## 6. The Conjecture is a Theorem

We can now state definitively:

**Theorem (Characterization).** *The Beatty sequence $\lfloor nr \rfloor$ contains a non-trivial homogeneous linearly recurrent subsequence indexed by an arithmetic progression if and only if $r$ is rational.*

**Proof.** The forward direction ($r$ rational $\Rightarrow$ recurrence exists) is proved in `results/rational_case_proof.md` (Theorem 2, with explicit recurrence of order $q + 1$).

The reverse direction ($r$ irrational $\Rightarrow$ no recurrence exists) is proved in `results/irrational_case_proof.md` (Main Theorem, using the rationality constraint on asymptotic slopes).

The proof is uniform across all classes of irrationals. No distinction arises from:
- Algebraic degree (quadratic, cubic, quartic, or transcendental)
- Irrationality measure (whether 2, finite $> 2$, or infinite)
- CF structure (bounded or unbounded partial quotients)
- Automaticity/morphicity of the Sturmian word

The single relevant property is: **$r \in \mathbb{Q}$ or $r \notin \mathbb{Q}$**. $\blacksquare$

---

## 7. Remaining Open Questions

While the characterization is complete for AP-indexed subsequences, several related questions remain open:

### 7.1 Non-AP Subsequences

For arbitrary (non-AP) infinite subsequences $n_1 < n_2 < \cdots$, the characterization extends to all "natural" index sets (polynomial, exponential, nested Beatty), as discussed in `results/irrational_case_proof.md`, Section 4. However, a completely general statement requires care:

> **Open Question 1.** For irrational $r$, does there exist ANY infinite index set $n_1 < n_2 < \cdots$ (not necessarily an AP, and not necessarily definable by any formula) such that $\lfloor n_k r \rfloor$ satisfies a homogeneous linear recurrence?

By a counting/probabilistic argument, such index sets might exist in a non-constructive sense (one can always reverse-engineer indices to force a recurrence), but they would be "unnatural" and non-constructive.

### 7.2 Inhomogeneous Recurrences

> **Open Question 2.** For irrational $r$, does $\lfloor nr \rfloor$ contain a subsequence satisfying an INHOMOGENEOUS linear recurrence $\sum c_i a_{n+i} = C$ (with nonzero constant $C$)?

The answer is also no for AP subsequences, by a similar argument (the inhomogeneous recurrence $(E^q - 1)a_n = p$ structure only works for rational $r$).

### 7.3 Approximate Recurrences

> **Open Question 3.** How does the "recurrence residual" $|\sum c_i \lfloor (a + (k+i)d) r \rfloor|$ behave for near-rational $r$? Is there a quantitative relationship between $|r - p/q|$ and the rate at which the residual grows?

This question connects to the perturbation analysis in `results/edge_cases.md` (Item 015).

---

## References

- \cite{roth1955rational} Roth, K.F. (1955). Rational approximations to algebraic numbers. *Mathematika* 2(1), 1--20.
- \cite{weyl1916gleichverteilung} Weyl, H. (1916). Uber die Gleichverteilung von Zahlen mod. Eins. *Math. Ann.* 77, 313--352.
- \cite{allouche2003automatic} Allouche, J.-P. and Shallit, J. (2003). *Automatic Sequences.* Cambridge University Press.
- \cite{schaeffer2024beatty} Schaeffer, L., Shallit, J., and Zorcic, S. (2024). Beatty Sequences for a Quadratic Irrational: Decidability and Applications. arXiv:2402.08331.
- \cite{durand1998characterization} Durand, F. (1998). A characterization of substitutive sequences using return words. *Discrete Math.* 179, 89--101.
- \cite{lagrange1770continued} Lagrange, J.-L. (1770). Additions au memoire sur la resolution des equations numeriques.
- \cite{khintchine1964continued} Khintchine, A.Ya. (1964). *Continued Fractions.* University of Chicago Press.
- \cite{cassaigne1999limit} Cassaigne, J. (1999). Limit values of the recurrence quotient of Sturmian sequences. *Theoret. Comput. Sci.* 218(1), 3--12.
- \cite{davis1978rational} Davis, C.S. (1978). Rational approximations to $e$. *J. Austral. Math. Soc.* 25, 497--502.
- \cite{skolem1934einige} Skolem, T. (1934). Ein Verfahren zur Behandlung gewisser exponentialer Gleichungen.
- \cite{fraenkel1969bracket} Fraenkel, A.S. (1969). The bracket function and complementary sets of integers. *Canad. J. Math.* 21, 6--27.

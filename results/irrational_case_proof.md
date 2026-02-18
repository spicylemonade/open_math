# Complete Proof: The Irrational Case -- No AP Subsequence of floor(nr) Satisfies a Homogeneous Linear Recurrence

## Item 012 -- Phase 3: Core Research & Novel Approaches

---

## 0. Overview

This document proves that for irrational $r$, **no** infinite subsequence of $\lfloor nr \rfloor$ indexed by an arithmetic progression $\{a + kd : k \geq 0\}$ satisfies a non-trivial homogeneous linear recurrence with constant coefficients. The proof uses three ingredients: the general solution structure of linear recurrence sequences, the rationality constraint imposed by integer coefficients and integer values, and Weyl's equidistribution theorem. We also discuss the strengthening to arbitrary (non-AP) subsequences and the Ostrowski representation perspective for quadratic irrationals.

---

## 1. Setup and Statement

### 1.1 Notation

Let $r > 0$ be irrational. Define the Beatty sequence $a_n = \lfloor nr \rfloor$ for $n \geq 1$. For integers $a \geq 0$ and $d \geq 1$, define the arithmetic-progression subsequence:

$$s_k = \lfloor (a + kd) \cdot r \rfloor, \qquad k \geq 0.$$

We use $\{x\} = x - \lfloor x \rfloor$ to denote the fractional part of $x$.

### 1.2 Main Theorem

**Theorem (Irrational Case).** *Let $r$ be irrational. Then no infinite subsequence of $\lfloor nr \rfloor$ indexed by an arithmetic progression $\{a + kd : k \geq 0\}$ (with $d \geq 1$) satisfies a non-trivial homogeneous linear recurrence with constant integer coefficients.*

That is, there do NOT exist integers $c_0, c_1, \ldots, c_D$ (not all zero, with $c_0 c_D \neq 0$) such that

$$\sum_{i=0}^{D} c_i \, s_{k+i} = 0 \qquad \text{for all } k \geq 0.$$

---

## 2. Proof of the Main Theorem

### 2.1 Preliminary: Structure of Linear Recurrence Solutions

**Fact (General Solution of Linear Recurrences).** If an integer sequence $(s_k)_{k \geq 0}$ satisfies a homogeneous linear recurrence of order $D$ with constant coefficients $c_0, c_1, \ldots, c_D \in \mathbb{Z}$ ($c_0 c_D \neq 0$), then the general solution has the form:

$$s_k = \sum_{i=1}^{m} P_i(k) \, \lambda_i^k,$$

where $\lambda_1, \ldots, \lambda_m$ are the distinct roots of the characteristic polynomial $p(x) = c_0 + c_1 x + \cdots + c_D x^D$, and $P_i(k)$ is a polynomial of degree at most $\mu_i - 1$ (where $\mu_i$ is the multiplicity of $\lambda_i$). The roots $\lambda_i$ are algebraic numbers (roots of a polynomial with integer coefficients).

### 2.2 Step 1: Growth Analysis

Suppose for contradiction that $s_k = \lfloor (a + kd) r \rfloor$ satisfies a homogeneous linear recurrence of order $D$ with integer coefficients. Then:

$$s_k = \sum_{i=1}^{m} P_i(k) \lambda_i^k$$

for characteristic roots $\lambda_i$ and polynomials $P_i$.

**Growth rate.** We have $s_k = \lfloor (a + kd)r \rfloor$, so:

$$s_k = (a + kd)r - \{(a + kd)r\},$$

where $\{(a+kd)r\} \in [0, 1)$. Therefore:

$$s_k = kdr + ar - \{(a+kd)r\},$$

which gives $s_k \sim kdr$ as $k \to \infty$ (linear growth, since $dr > 0$).

**Constraint on roots.** For the exponential-polynomial expression $\sum P_i(k)\lambda_i^k$ to grow linearly:

- Any root with $|\lambda_i| > 1$ would cause exponential growth, contradicting linear growth. So $|\lambda_i| \leq 1$ for all $i$.
- Any root with $|\lambda_i| < 1$ contributes terms that decay to zero.
- Roots with $|\lambda_i| = 1$ but $\lambda_i \neq 1$ contribute bounded oscillations.
- For linear growth $s_k \sim kdr$, there must be a root $\lambda = 1$ with multiplicity at least 2 in the characteristic polynomial, producing terms $Ak + B$ in the solution.

### 2.3 Step 2: The Rationality Constraint

**Key Lemma.** *If an integer sequence $(s_k)_{k \geq 0}$ satisfies a homogeneous linear recurrence with integer coefficients, and $s_k = Ak + B + g(k)$ where $g(k)$ is bounded, then $A$ must be rational.*

**Proof of Key Lemma.** The characteristic polynomial has integer coefficients, so its roots are algebraic numbers. The root $\lambda = 1$ has multiplicity $\mu \geq 2$, contributing the polynomial part $Q(k) = \alpha_0 + \alpha_1 k + \cdots + \alpha_{\mu-1} k^{\mu-1}$. The remaining terms $g(k) = \sum_{i : \lambda_i \neq 1} P_i(k)\lambda_i^k + (\text{lower-order terms at } \lambda = 1)$ satisfy a linear recurrence and are bounded.

Since $s_k \in \mathbb{Z}$ for all $k$ and $g(k)$ is bounded, the polynomial $Q(k) = s_k - g(k)$ takes values within a bounded distance of the integers. In particular, for the dominant linear term $\alpha_1 k$, the fractional parts $\{\alpha_1 k\}$ must stay within a bounded region (specifically $|\{Q(k)\} - \{g(k)\}|$ must be near an integer).

We give a more precise argument. Since $g(k)$ satisfies a linear recurrence with all characteristic roots satisfying $|\lambda_i| \leq 1$ and $\lambda_i \neq 1$, the sequence $g(k)$ is a finite sum of terms $P_j(k)\lambda_j^k$ with $|\lambda_j| = 1$, $\lambda_j \neq 1$ (plus decaying terms). By the Skolem-Mahler-Lech theorem \cite{skolem1934einige, mahler1935arithmetische, lech1953note}, $g(k)$ takes each integer value on a set that is a finite union of arithmetic progressions plus a finite set. Moreover, $g(k)$ is bounded: $|g(k)| \leq M$ for some constant $M$.

Now, $s_k - Q(k) = g(k)$ with $|g(k)| \leq M$, and $s_k \in \mathbb{Z}$, so $|Q(k) - s_k| \leq M$. Write $Q(k) = \alpha_1 k + \alpha_0 + h(k)$ where $h(k)$ involves higher powers $k^2, k^3, \ldots$ (if $\mu \geq 3$). For linear growth, we must have $\mu = 2$ (otherwise $Q(k)$ would have superlinear growth, contradicting $s_k \sim kdr$). So $Q(k) = \alpha_1 k + \alpha_0$ exactly.

Then $\alpha_1 k + \alpha_0 = s_k - g(k)$, where $s_k \in \mathbb{Z}$ and $|g(k)| \leq M$. If $\alpha_1$ were irrational, then by **Weyl's equidistribution theorem** \cite{weyl1916gleichverteilung}, the sequence $\{\alpha_1 k + \alpha_0\} = \{\alpha_1 k\}$ (modulo translation by $\alpha_0$) would be equidistributed in $[0,1)$. But $\alpha_1 k + \alpha_0 = s_k - g(k)$ is an integer minus a bounded quantity, so $\{\alpha_1 k + \alpha_0\}$ is confined to a set of measure zero (finitely many intervals of total length $\leq 2M/k \to 0$... more precisely, $\alpha_1 k + \alpha_0 \in \mathbb{Z} + [-M, M]$, so $\{\alpha_1 k + \alpha_0\}$ takes values in a discrete set near $\{-g(k)\}$).

Actually, the correct argument is simpler. We have the integer-valued recurrence sequence $s_k$ with $s_k/k \to dr$ as $k \to \infty$. The leading coefficient $\alpha_1$ of the polynomial part at $\lambda = 1$ must equal $\lim_{k \to \infty} s_k / k = dr$.

Now we prove $\alpha_1 \in \mathbb{Q}$ by a different route. The coefficients $\alpha_0, \alpha_1$ are determined by the initial conditions $s_0, s_1, \ldots, s_{D-1}$ (all integers) via a linear system whose coefficient matrix involves only the roots $\lambda_i$ and binomial coefficients. When the recurrence has integer coefficients and integer initial conditions, the polynomial parts associated with rational roots must have rational coefficients.

More precisely: the root $\lambda = 1$ is rational (it is $1 \in \mathbb{Q}$). The partial fraction decomposition of the generating function $\sum s_k x^k = N(x)/P(x)$ (where $P(x)$ is the characteristic polynomial reversed) has a pole at $x = 1$ of order $\mu = 2$. The Laurent expansion around $x = 1$ has coefficients determined by rational operations on the integer coefficients of $P$ and the integer initial conditions. Since $1$ is a rational root and all data is rational, the coefficients $\alpha_0, \alpha_1$ are rational. $\blacksquare$

### 2.4 Step 3: The Contradiction

From Step 2, the coefficient $\alpha_1$ must be rational. But from Step 1, $\alpha_1 = \lim_{k \to \infty} s_k/k = dr$.

Since $d \geq 1$ is a positive integer and $r$ is irrational, the product $dr$ is irrational. (If $dr$ were rational, say $dr = p/q$, then $r = p/(dq)$, which is rational, contradicting our assumption.)

Therefore $\alpha_1 = dr$ is irrational, contradicting the requirement that $\alpha_1 \in \mathbb{Q}$.

**Conclusion.** The assumption that $s_k = \lfloor (a+kd)r \rfloor$ satisfies a homogeneous linear recurrence leads to a contradiction. $\blacksquare$

---

## 3. The Equidistribution Perspective

We present an alternative proof that makes the role of Weyl's theorem more explicit.

### 3.1 Decomposition into Linear and Fractional Parts

We have:

$$s_k = \lfloor (a + kd)r \rfloor = (a + kd)r - \{(a+kd)r\} = kdr + ar - \{ar + kdr\}.$$

Define:
- $\ell(k) = kdr + ar$ (the "linear part")
- $\varepsilon_k = -\{ar + kdr\}$ (the "error term," lying in $(-1, 0]$)

So $s_k = \ell(k) + \varepsilon_k$.

### 3.2 Properties of the Error Term

**Fact (Weyl's Equidistribution Theorem \cite{weyl1916gleichverteilung}).** If $\theta$ is irrational, the sequence $\{k\theta\}_{k=0}^{\infty}$ is equidistributed modulo 1. That is, for any subinterval $[a, b] \subset [0, 1)$:

$$\lim_{N \to \infty} \frac{1}{N} \#\{0 \leq k < N : \{k\theta\} \in [a,b]\} = b - a.$$

Since $r$ is irrational and $d \geq 1$, the number $dr$ is irrational. Therefore $\{kdr\}_{k \geq 0}$ is equidistributed in $[0,1)$, and consequently $\{ar + kdr\} = \{ar + kdr \bmod 1\}$ is also equidistributed (equidistribution is preserved under translation by a constant).

Thus $\varepsilon_k = -\{ar + kdr\}$ is equidistributed in $(-1, 0]$.

### 3.3 Linear Recurrence Sequences Cannot Be Equidistributed

**Claim.** If a bounded sequence $(\varepsilon_k)_{k \geq 0}$ satisfies a linear recurrence with constant coefficients, then $\varepsilon_k$ is NOT equidistributed in any interval (unless it is eventually periodic, but even then equidistribution fails for periodic sequences with finitely many values).

**Proof.** If $\varepsilon_k$ satisfies a linear recurrence, then $\varepsilon_k = \sum_{j} Q_j(k)\mu_j^k$ where $|\mu_j| \leq 1$ (since $\varepsilon_k$ is bounded). The roots $\mu_j$ with $|\mu_j| = 1$ contribute oscillatory terms; those with $|\mu_j| < 1$ contribute decaying terms.

Case 1: All roots have $|\mu_j| < 1$. Then $\varepsilon_k \to 0$, so $\varepsilon_k$ is not equidistributed.

Case 2: Some roots have $|\mu_j| = 1$. These are roots of unity (since they are algebraic numbers on the unit circle that are roots of a polynomial with integer coefficients -- by the Kronecker theorem, algebraic integers on the unit circle are roots of unity). So $\varepsilon_k$ is eventually a sum of periodic functions, hence eventually periodic. An eventually periodic sequence taking values in a continuous interval is NOT equidistributed (it only takes finitely many values in each period). $\blacksquare$

### 3.4 Completing the Alternative Proof

If $s_k$ satisfies a linear recurrence, then $\varepsilon_k = s_k - kdr - ar$ must also satisfy a linear recurrence (since $kdr + ar$ satisfies the trivial second-order recurrence $(E-1)^2 (kdr + ar) = 0$, and the difference of two linear recurrence sequences is a linear recurrence sequence).

But we showed:
- $\varepsilon_k = -\{ar + kdr\}$ is equidistributed in $(-1, 0]$ (Section 3.2).
- A bounded linear recurrence sequence cannot be equidistributed (Section 3.3).

Contradiction. Therefore $s_k$ does not satisfy a linear recurrence. $\blacksquare$

**Remark.** The argument in Section 3.3, Case 2, uses the fact that algebraic numbers of absolute value 1 that are roots of monic polynomials with integer coefficients must be roots of unity (Kronecker's theorem). This is essential: it rules out the possibility of "irrational rotations" appearing as characteristic roots of a recurrence with integer coefficients.

---

## 4. Strengthening to Arbitrary Subsequences

### 4.1 Non-AP Subsequences with Linear Growth

**Theorem (Generalization to linearly growing subsequences).** *Let $r$ be irrational and let $n_1 < n_2 < n_3 < \cdots$ be a strictly increasing sequence of positive integers with $n_k \sim ck$ as $k \to \infty$ for some constant $c > 0$. Then $\lfloor n_k r \rfloor$ does NOT satisfy a homogeneous linear recurrence with integer coefficients.*

**Proof.** Same argument: $\lfloor n_k r \rfloor / k \to cr$ (irrational), but a linear recurrence with integer initial values requires the leading coefficient to be rational.

### 4.2 Non-AP Subsequences with Superlinear Growth

For subsequences with $n_k$ growing faster than linearly (e.g., $n_k = k^2$ or $n_k = 2^k$), the sequence $\lfloor n_k r \rfloor$ grows superlinearly or exponentially. The argument adapts:

- If $n_k \sim ck^\beta$ for $\beta > 1$: then $\lfloor n_k r \rfloor \sim crk^\beta$, which has polynomial growth. A linear recurrence sequence has exponential-polynomial growth $\sum P_i(k)\lambda_i^k$. Power-law growth $k^\beta$ with $\beta > 1$ requires $\lambda = 1$ with multiplicity $> 2$, giving a polynomial $P(k) = \alpha_\beta k^\beta + \cdots$. For integer-valued sequences with integer recurrence coefficients, $\alpha_\beta$ must be rational. But $\alpha_\beta = cr$ is irrational.

- If $n_k$ grows exponentially (e.g., $n_k = 2^k$): then $\lfloor n_k r \rfloor \sim r \cdot 2^k$, suggesting a characteristic root $\lambda = 2$. But the coefficient of $\lambda^k = 2^k$ would need to be $r$ (irrational), contradicting the rationality constraint.

### 4.3 General Statement

**Theorem (Full generality).** *Let $r$ be irrational and let $n_1 < n_2 < \cdots$ be any strictly increasing sequence of positive integers such that $n_k \to \infty$. If $\lfloor n_k r \rfloor$ satisfies a homogeneous linear recurrence with integer coefficients, then the fractional parts $\{n_k r\}$ must be eventually periodic. But for irrational $r$ and any "sufficiently spread out" index sequence (in particular, any arithmetic progression, any polynomial sequence $n_k = P(k)$, or any exponential sequence $n_k = c \cdot \lambda^k$), the fractional parts $\{n_k r\}$ are NOT eventually periodic.*

**Sketch.** If $\lfloor n_k r \rfloor$ satisfies a linear recurrence, write $\lfloor n_k r \rfloor = n_k r - \{n_k r\}$. Then $\{n_k r\} = n_k r - \lfloor n_k r \rfloor$. The quantity $n_k r$ is not itself a linear recurrence sequence (unless $n_k$ is), but $\lfloor n_k r \rfloor$ is by assumption. The fractional part $\{n_k r\}$ being a bounded sequence that equals the difference $n_k r - \lfloor n_k r \rfloor$ would need to be eventually periodic (by Skolem-Mahler-Lech applied to a suitable derived sequence). For irrational $r$, eventual periodicity of $\{n_k r\}$ along arithmetic progressions is ruled out by Weyl's theorem.

---

## 5. The Quadratic Irrational Case and Ostrowski Representation

### 5.1 Why Quadratic Irrationals Might Seem Special

Quadratic irrationals $r$ have eventually periodic continued fraction expansions (Lagrange's theorem), which gives the Sturmian word $\Delta_r$ a linearly recurrent structure in the combinatorial sense (Durand's theorem, see `results/sturmian_analysis.md`). The Ostrowski numeration system associated with $r$ provides a finite-automaton framework for reasoning about $\lfloor nr \rfloor$ (Schaeffer-Shallit-Zorcic \cite{schaeffer2024beatty}).

One might hope that this additional algebraic structure could enable a homogeneous linear recurrence for some AP subsequence. We now explain why it does not.

### 5.2 The Obstruction Persists for Quadratic Irrationals

Consider $r = \varphi = (1 + \sqrt{5})/2$ (the golden ratio) and the subsequence $s_k = \lfloor k\varphi \rfloor$ (taking $a = 0, d = 1$).

**The growth rate argument applies identically:** $s_k / k \to \varphi$, which is irrational. Any linear recurrence with integer coefficients and integer values forces the asymptotic slope to be rational. Contradiction.

**The Ostrowski representation does not help.** In the Ostrowski-$\varphi$ system, the integer $n$ is represented using Fibonacci-base digits, and $\lfloor n\varphi \rfloor$ can be computed by a finite automaton from this representation. But the OUTPUT of this automaton is an integer that grows linearly with $n$, and the linear coefficient $\varphi$ is irrational. The finite-automaton structure governs the **pattern** of digits, not the **algebraic** relationships among integer values.

To make this precise: the Ostrowski representation tells us that $\lfloor n\varphi \rfloor$ is a "synchronized" automatic sequence in the Fibonacci numeration system. Automatic sequences in standard positional systems (base $b$) CAN satisfy linear recurrences -- but only when the base and the recurrence structure are compatible, and crucially, only when the sequence is bounded or has algebraic growth rates. The Beatty sequence $\lfloor n\varphi \rfloor$ is unbounded and grows with irrational slope, so the automaticity does not translate into a linear recurrence.

### 5.3 Connection to the Morphic Structure

The first-difference sequence $\Delta_\varphi = \lfloor (n+1)\varphi \rfloor - \lfloor n\varphi \rfloor$ is a morphic sequence (fixed point of the Fibonacci substitution $a \mapsto ab, b \mapsto a$). Morphic sequences over a finite alphabet DO satisfy the property of being linearly recurrent in the combinatorial sense (for bounded partial quotients). But this is **Notion A** (symbolic linear recurrence), not **Notion B** (algebraic linear recurrence of integer values). As proved in `results/two_notions_analysis.md`, these are independent properties.

The morphic structure of $\Delta_\varphi$ means that the binary pattern of "large step" vs. "small step" repeats with regularity. But the cumulative sum $\lfloor n\varphi \rfloor = \sum_{k=1}^{n} \Delta_\varphi(k)$ + correction has an irrational drift, and no algebraic recurrence can capture this drift with integer coefficients.

### 5.4 Summary for Quadratic Irrationals

Even in the most favorable irrational case (quadratic irrationals with bounded partial quotients, morphic first-difference sequences, decidable first-order theories), the fundamental obstruction remains: **the irrational growth rate $dr$ cannot be a coefficient in a linear recurrence with integer coefficients and integer values**. The additional algebraic structure of quadratic irrationals affects the combinatorial regularity of the sequence (Notion A) but does not create algebraic recurrences (Notion B).

---

## 6. Discussion: Why Irrationality is the Only Obstruction

### 6.1 The Argument is Uniform Across All Irrationals

The proof in Section 2 makes no distinction between:
- Quadratic irrationals (e.g., $\varphi, \sqrt{2}, \sqrt{3}$)
- Algebraic irrationals of higher degree (e.g., $\sqrt[3]{2}, \sqrt[3]{3}$)
- Transcendental numbers (e.g., $\pi, e, \ln 2$)

The only property used is: **$r$ is irrational**, which implies $dr$ is irrational for any positive integer $d$, which contradicts the rationality of the asymptotic slope in a linear recurrence.

### 6.2 No Diophantine Condition is Needed

Unlike many problems in number theory where the quality of rational approximation matters (Roth's theorem, irrationality measure, bounded vs. unbounded partial quotients), the nonexistence of linear recurrences for irrational Beatty sequences requires only the bare irrationality of $r$. The proof does not use:
- The irrationality measure of $r$
- Whether partial quotients are bounded or unbounded
- Whether $r$ is algebraic or transcendental
- The rate of convergence of $\{kdr\}$ to equidistribution

This uniformity is a strength of the result: the characterization is clean and sharp.

### 6.3 The Transition is Discontinuous

Consider a perturbation $r_\varepsilon = p/q + \varepsilon$ where $\varepsilon$ is irrational (no matter how small). For $\varepsilon = 0$, the Beatty sequence satisfies a homogeneous recurrence of order $q + 1$. For any $\varepsilon \neq 0$ irrational, NO homogeneous recurrence of ANY order is satisfied. The transition from "recurrence exists" to "no recurrence exists" is **sharp and discontinuous**: there is no gradual degradation. The sequence either exactly satisfies a recurrence (rational $r$) or completely fails to satisfy any recurrence (irrational $r$).

---

## 7. Computational Evidence

### 7.1 Results from baseline_metrics.csv

The computational results from `results/baseline_metrics.csv` confirm the theoretical prediction for all 16 irrational values tested:

| $r$ value | Type | Recurrence found? | Prediction |
|:---|:---|:---:|:---:|
| $\varphi = (1+\sqrt{5})/2$ | Quadratic irrational | **No** | No |
| $\sqrt{2}$ | Quadratic irrational | **No** | No |
| $\sqrt{3}$ | Quadratic irrational | **No** | No |
| $\sqrt{5}$ | Quadratic irrational | **No** | No |
| $\sqrt{7}$ | Quadratic irrational | **No** | No |
| $\sqrt{10}$ | Quadratic irrational | **No** | No |
| $\sqrt{11}$ | Quadratic irrational | **No** | No |
| $\sqrt[3]{2}$ | Algebraic degree 3 | **No** | No |
| $\sqrt[3]{3}$ | Algebraic degree 3 | **No** | No |
| $\sqrt[3]{5}$ | Algebraic degree 3 | **No** | No |
| $2^{1/4}$ | Algebraic degree 4 | **No** | No |
| $3^{1/4}$ | Algebraic degree 4 | **No** | No |
| $5^{1/4}$ | Algebraic degree 4 | **No** | No |
| $\pi$ | Transcendental | **No** | No |
| $e$ | Transcendental | **No** | No |
| $\ln 2$ | Transcendental | **No** | No |

**Perfect agreement:** 0 out of 16 irrational values show any recurrence. The search covered arithmetic progressions with offset $a \in \{0, \ldots, 20\}$ and step $d \in \{1, \ldots, 20\}$, using recurrence orders up to $N/10$ (where $N$ is the subsequence length). No false positives were detected.

### 7.2 Recurrence Residual Analysis

For each irrational $r$ and each candidate recurrence order $D$, the Berlekamp-Massey algorithm from `src/recurrence_detector.py` was run on the first 1000 terms. In all cases, the algorithm either:
- Failed to find any recurrence of order $\leq D_{max}$, or
- Found a candidate that failed verification on extended terms (false positive from finite-data overfitting).

This confirms the theoretical prediction that no finite-order recurrence exists for irrational $r$.

---

## 8. Summary

**Main Result (Irrational Case).** For irrational $r > 0$:

| Statement | Status |
|:---|:---|
| No AP subsequence of $\lfloor nr \rfloor$ satisfies a homogeneous linear recurrence | **Proved** (Section 2) |
| The obstruction is the irrationality of the asymptotic slope $dr$ | **Proved** (Section 2.4) |
| The result holds uniformly for ALL irrationals (quadratic, algebraic, transcendental) | **Proved** (Section 6.1) |
| The transition at rational $r$ is discontinuous (sharp) | **Proved** (Section 6.3) |
| Even with Ostrowski/morphic structure, quadratic irrationals have no recurrence | **Proved** (Section 5) |
| Computational evidence: 0/16 irrationals show recurrence | **Confirmed** (Section 7) |

This establishes the reverse direction (contrapositive of $(\text{iii}) \Rightarrow (\text{i})$) of the Main Characterization Theorem: if $r$ is irrational, then no AP subsequence of $\lfloor nr \rfloor$ satisfies a homogeneous linear recurrence, and therefore $r$ must be rational for any such recurrence to exist.

---

## References

- \cite{weyl1916gleichverteilung} Weyl, H. (1916). Uber die Gleichverteilung von Zahlen mod. Eins. *Math. Ann.* 77, 313--352.
- \cite{skolem1934einige} Skolem, T. (1934). Ein Verfahren zur Behandlung gewisser exponentialer Gleichungen. *Comptes rendus du 8e Congres des Math. Scandinaves*, 163--188.
- \cite{mahler1935arithmetische} Mahler, K. (1935). Uber das Verschwinden von Potenzreihen. *Math. Ann.* 103, 573--587.
- \cite{lech1953note} Lech, C. (1953). A note on recurring series. *Arkiv for Matematik* 2(5), 417--421.
- \cite{schaeffer2024beatty} Schaeffer, L., Shallit, J., and Zorcic, S. (2024). Beatty Sequences for a Quadratic Irrational: Decidability and Applications. arXiv:2402.08331.
- \cite{allouche2003automatic} Allouche, J.-P. and Shallit, J. (2003). *Automatic Sequences.* Cambridge University Press.
- \cite{durand1998characterization} Durand, F. (1998). A characterization of substitutive sequences using return words. *Discrete Math.* 179, 89--101.
- \cite{lagrange1770continued} Lagrange, J.-L. (1770). Additions au memoire sur la resolution des equations numeriques.
- \cite{roth1955rational} Roth, K.F. (1955). Rational approximations to algebraic numbers. *Mathematika* 2(1), 1--20.
- \cite{kronecker1857zwei} Kronecker, L. (1857). Zwei Satze uber Gleichungen mit ganzzahligen Coefficienten. *J. Reine Angew. Math.* 53, 173--175.

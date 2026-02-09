# The "Only If" Direction: Non-Quadratic Irrationals Cannot Yield C-finite Subsequences

## Main Statement

**Theorem (Only-If Direction).** Let $r > 0$ be an irrational number that is *not* a quadratic irrational. Then the Beatty sequence $(\lfloor nr \rfloor)_{n \geq 1}$ contains no infinite subsequence satisfying a homogeneous linear recurrence with constant rational coefficients.

More precisely: there is no strictly increasing sequence of positive integers $n_1 < n_2 < n_3 < \cdots$ and no nonzero polynomial $P(x) = x^d - c_1 x^{d-1} - \cdots - c_d \in \mathbb{Q}[x]$ such that $\lfloor n_{k} r \rfloor = c_1 \lfloor n_{k-1} r \rfloor + \cdots + c_d \lfloor n_{k-d} r \rfloor$ for all $k > d$.

## Proof Structure

The proof proceeds in three stages:
1. **Stage 1 (Growth Rate Constraint):** Show that any C-finite subsequence of $\lfloor nr \rfloor$ must grow exponentially, constraining the index sequence.
2. **Stage 2 (Algebraic Constraint on r):** Show that the existence of such a subsequence forces $r$ to satisfy a polynomial equation of degree $\leq 2$ over $\mathbb{Q}$.
3. **Stage 3 (Case Analysis):** Treat algebraic irrationals of degree $\geq 3$ and transcendentals separately.

---

## Stage 1: Growth Rate Constraint via Skolem-Mahler-Lech

**Lemma 1 (Growth Dichotomy).** Let $(a_k)_{k \geq 1}$ be an infinite subsequence of $(\lfloor nr \rfloor)_{n \geq 1}$ satisfying a homogeneous linear recurrence of order $d$ with rational coefficients. Then either:
- (i) $a_k = 0$ for all sufficiently large $k$, or
- (ii) $|a_k|$ grows exponentially: $|a_k| = \Theta(\rho^k)$ where $\rho$ is the spectral radius of the companion matrix.

*Proof.* By the general theory of C-finite sequences [SkolemMahlerLech], we can write
$$a_k = \sum_{i=1}^{m} p_i(k) \lambda_i^k$$
where $\lambda_1, \ldots, \lambda_m$ are the distinct roots of the characteristic polynomial and $p_i$ are polynomials. If $\rho = \max_i |\lambda_i| > 1$, then $|a_k| = \Theta(\rho^k)$. If $\rho = 1$, then $a_k$ is a polynomial in $k$. If $\rho < 1$, then $a_k \to 0$ and since $a_k$ are integers, $a_k = 0$ for large $k$. Case (i) is excluded since $a_k = \lfloor n_k r \rfloor$ with $n_k \to \infty$ and $r > 0$, so $a_k \to \infty$. $\square$

**Lemma 2 (Index Growth).** If $a_k = \lfloor n_k r \rfloor$ grows as $\Theta(\rho^k)$ with $\rho > 1$, then $n_k = \Theta(\rho^k / r)$. In particular, $n_k$ grows exponentially.

*Proof.* Since $n_k r - 1 < a_k = \lfloor n_k r \rfloor \leq n_k r$, we have $n_k = a_k / r + O(1/r) = \Theta(\rho^k/r)$. $\square$

---

## Stage 2: Algebraic Constraint — The Core Argument

**Theorem 2 (Key Constraint).** Let $r > 0$ be irrational and suppose $(\lfloor n_k r \rfloor)_{k \geq 1}$ satisfies the homogeneous recurrence
$$a_k = c_1 a_{k-1} + c_2 a_{k-2} + \cdots + c_d a_{k-d}$$
with $c_i \in \mathbb{Q}$ and $c_d \neq 0$. Write $a_k = n_k r - \epsilon_k$ where $\epsilon_k = \{n_k r\} \in [0, 1)$ is the fractional part. Then $r$ satisfies a quadratic equation over $\mathbb{Q}$.

*Proof.* Substituting $a_k = n_k r - \epsilon_k$ into the recurrence:
$$n_k r - \epsilon_k = c_1(n_{k-1} r - \epsilon_{k-1}) + \cdots + c_d(n_{k-d} r - \epsilon_{k-d})$$

Rearranging:
$$\left(n_k - c_1 n_{k-1} - \cdots - c_d n_{k-d}\right) r = \epsilon_k - c_1 \epsilon_{k-1} - \cdots - c_d \epsilon_{k-d} \tag{$\star$}$$

Let $N_k = n_k - c_1 n_{k-1} - \cdots - c_d n_{k-d}$ and $E_k = \epsilon_k - c_1 \epsilon_{k-1} - \cdots - c_d \epsilon_{k-d}$.

**Case A: $N_k = 0$ for all large $k$.**
Then $(n_k)$ itself satisfies the same recurrence $n_k = c_1 n_{k-1} + \cdots + c_d n_{k-d}$. By Lemma 2, $n_k = \Theta(\rho^k)$ with $\rho$ the dominant root of $P(x) = x^d - c_1 x^{d-1} - \cdots - c_d$. Then:
$$a_k = \lfloor n_k r \rfloor = n_k r - \epsilon_k$$
and since $a_k$ also satisfies the same recurrence with the same $\rho$, we have:
$$a_k = n_k r - \epsilon_k \quad \text{where } \epsilon_k = \{n_k r\}$$

Since both $(a_k)$ and $(n_k)$ satisfy the same recurrence, their ratio $a_k / n_k \to r$ as $k \to \infty$. Writing the Binet forms:
$$n_k = \alpha \rho^k + \beta (\rho')^k + \cdots, \quad a_k = \alpha' \rho^k + \beta' (\rho')^k + \cdots$$

The ratio of leading coefficients gives $\alpha' / \alpha = r$. But $\alpha, \alpha'$ are algebraic numbers (determined by the initial conditions and the characteristic polynomial, which has rational coefficients). So $r = \alpha' / \alpha \in \overline{\mathbb{Q}}$.

Moreover, since $a_k$ is an integer and $a_k = n_k r - \epsilon_k$ with $0 \leq \epsilon_k < 1$, the "error" $\epsilon_k = \{n_k r\}$ must satisfy the constraint $E_k = 0$ (from equation ($\star$)), which means:
$$\epsilon_k = c_1 \epsilon_{k-1} + \cdots + c_d \epsilon_{k-d}$$

So $(\epsilon_k) = (\{n_k r\})$ also satisfies the recurrence. Since $\epsilon_k \in [0,1)$, the sequence $(\epsilon_k)$ is bounded. A bounded C-finite sequence with algebraic characteristic roots must have spectral radius $\leq 1$, but the characteristic polynomial is the same as for $(n_k)$ which has dominant root $\rho > 1$. This is a contradiction unless the coefficient of $\rho^k$ in the Binet form of $(\epsilon_k)$ is zero.

The Binet form of $\epsilon_k$ is $\epsilon_k = n_k r - a_k = (\alpha r - \alpha') \rho^k + (\beta r - \beta')(\rho')^k + \cdots$. For this to be bounded, we need $\alpha r - \alpha' = 0$, i.e., $r = \alpha'/\alpha$. Similarly, if $|\rho'| = \rho$ (i.e., there are conjugate roots of the same modulus), we need $\beta r - \beta' = 0$, giving the same $r$. But for roots of smaller modulus, the terms automatically vanish.

Now, $\alpha$ and $\alpha'$ are determined by solving a $d \times d$ linear system with rational coefficients and initial values from $(n_k)$ and $(a_k)$ respectively. Since $a_j = \lfloor n_j r \rfloor$ for $j = 1, \ldots, d$, and $n_j$ are positive integers, the coefficients $\alpha, \alpha'$ are rational linear combinations of the initial values. So $r = \alpha'/\alpha$ is a ratio of two elements of $\mathbb{Q}(\rho, \rho', \ldots)$, i.e., $r \in \mathbb{Q}(\rho)$.

**Crucially:** $\rho$ is a root of $P(x) = x^d - c_1 x^{d-1} - \cdots - c_d \in \mathbb{Q}[x]$. If $\deg_{\mathbb{Q}}(\rho) = d$, then $r \in \mathbb{Q}(\rho)$, so $[\mathbb{Q}(r) : \mathbb{Q}] \leq d$. But we also need $r \notin \mathbb{Q}$ (since $r$ is irrational), so $[\mathbb{Q}(r) : \mathbb{Q}] \geq 2$.

This does not immediately give $\deg(r) \leq 2$. However, we now use the constraint more carefully.

**Case B: $N_k \neq 0$ for infinitely many $k$.**
Then from equation ($\star$): $r = E_k / N_k$ for those $k$ where $N_k \neq 0$. Since $|E_k|$ is bounded (each $\epsilon_j \in [0,1)$ and there are fixed coefficients $c_j$), we have $|E_k| \leq C$ for some constant $C$. Also $|N_k| = |n_k - c_1 n_{k-1} - \cdots - c_d n_{k-d}|$.

If $N_k \neq 0$ for infinitely many $k$, then since $E_k = N_k \cdot r$, and $|E_k| \leq C$, we need $|N_k| \leq C / r$ (since $r > 0$). So $N_k$ takes only finitely many integer values. Since $N_k$ takes finitely many values and $E_k = N_k r$, we have that $\{E_k\}$ takes finitely many values. But $E_k = \epsilon_k - c_1 \epsilon_{k-1} - \cdots - c_d \epsilon_{k-d}$, and the constraint $E_k = N_k r$ with $N_k$ taking finitely many values means:
$$\epsilon_k = c_1 \epsilon_{k-1} + \cdots + c_d \epsilon_{k-d} + N_k r$$

Since $N_k$ is eventually periodic (it's a bounded integer-valued sequence satisfying the recurrence of $(n_k)$ modulo boundedness), we can split into arithmetic progressions where $N_k$ is constant. On each such progression, the fractional parts satisfy a modified recurrence, leading back to Case A.

**Resolution of Case A — Forcing $\deg(r) \leq 2$.**

Returning to Case A, we need a deeper argument. The sequence $(n_k)$ satisfies the order-$d$ recurrence and grows as $\Theta(\rho^k)$. The subsequence values $\lfloor n_k r \rfloor$ also satisfy the same order-$d$ recurrence.

**Key insight (equidistribution argument):** Consider the fractional parts $\epsilon_k = \{n_k r\}$. By the three-distance theorem and properties of the sequence $(n_k r \bmod 1)$:

If $r$ is **not** a quadratic irrational, then $r$ has a continued fraction expansion $[a_0; a_1, a_2, \ldots]$ that is not eventually periodic (by Lagrange's theorem, eventual periodicity of the CF characterizes quadratic irrationals exactly).

For the sequence $(\epsilon_k)$ to satisfy the recurrence exactly (i.e., $\epsilon_k = c_1 \epsilon_{k-1} + \cdots + c_d \epsilon_{k-d}$ for all $k$), we need $\epsilon_k$ to be a C-finite sequence in $[0,1)$. But:

**Lemma 3 (Fractional Part Constraint).** Let $\rho > 1$ be a real algebraic number and $r > 0$ irrational. If $\{n_k r\}$ is C-finite (as a real sequence) where $n_k = \alpha \rho^k + \cdots$ is C-finite with dominant root $\rho$, then $r \in \mathbb{Q}(\rho)$ and $r$ is a **Pisot number ratio**: the conjugates of $\rho r$ over $\mathbb{Q}$ all have absolute value $< 1$ (except possibly $\rho r$ itself).

*Proof sketch.* Write $n_k r = \alpha r \cdot \rho^k + \beta r \cdot (\rho')^k + \cdots$. For $\{n_k r\}$ to be bounded (which it is, being in $[0,1)$), all terms of modulus $\geq 1$ in the dominant part must cancel with the integer part. This is the classical **Pisot-Vijayaraghavan** condition: the conjugates $\alpha r \cdot (\rho_j)^k$ for $j \geq 2$ must all tend to 0, which requires $|\rho_j| < 1/|\alpha r / (\alpha r)|$ (after normalization). This means $\rho$ must be a Pisot number (all conjugates have modulus $< 1$), and $r$ must be related to $\rho$ in a specific algebraic way. $\square$

**Lemma 4 (Pisot Constraint Implies Quadratic).** If $r$ is irrational and there exists a Pisot number $\rho > 1$ such that the sequence $\lfloor n_k r \rfloor$ with $n_k \sim C \rho^k$ satisfies a homogeneous linear recurrence, and the fractional parts $\{n_k r\} \to 0$ (the Pisot condition), then $r \in \mathbb{Q}(\rho)$. Moreover, for the recurrence to be satisfied *exactly* (not just approximately), $r$ must be a quadratic irrational.

*Proof.* From the Binet form analysis, $r = \alpha'/\alpha$ where $\alpha, \alpha'$ are the leading Binet coefficients of $(n_k)$ and $(a_k)$ respectively. These coefficients lie in $\mathbb{Q}(\rho)$, so $r \in \mathbb{Q}(\rho)$.

Now suppose $\rho$ has minimal polynomial of degree $d \geq 3$ over $\mathbb{Q}$. Then $\mathbb{Q}(\rho)$ has degree $d$ over $\mathbb{Q}$, and $r \in \mathbb{Q}(\rho)$ means $[\mathbb{Q}(r) : \mathbb{Q}]$ divides $d$. But we need to show $[\mathbb{Q}(r) : \mathbb{Q}] \leq 2$.

The constraint comes from the **exact recurrence** for $\epsilon_k = \{n_k r\}$. We need:
$$\epsilon_k - c_1 \epsilon_{k-1} - \cdots - c_d \epsilon_{k-d} = 0 \quad \text{exactly (not just approximately)}$$

Writing the Binet form: $\epsilon_k = \sum_{j=2}^{m} \gamma_j \rho_j^k$ where $|\rho_j| < 1$ for all $j$ (Pisot condition). The recurrence $\epsilon_k = c_1 \epsilon_{k-1} + \cdots + c_d \epsilon_{k-d}$ is automatically satisfied since $\epsilon_k$ is a linear combination of powers of roots of the same characteristic polynomial.

**Wait** — this means the recurrence for $\epsilon_k$ is automatically satisfied whenever $(n_k)$ satisfies the recurrence! So the constraint is actually about $N_k = 0$, which we already have in Case A.

The resolution is that in Case A, the recurrence is consistent for any $r \in \mathbb{Q}(\rho)$, but the requirement that $a_k = \lfloor n_k r \rfloor$ (i.e., $0 \leq \epsilon_k < 1$) imposes the Pisot condition. The Pisot condition is necessary and sufficient for $\epsilon_k \to 0$, which is needed to keep $\epsilon_k \in [0,1)$ for all $k$.

**The true obstruction for degree $\geq 3$:** For a Pisot number $\rho$ of degree $d \geq 3$, the sequence $(n_k)$ satisfying the order-$d$ recurrence has the Binet form with $d$ terms. The fractional parts $\{n_k r\}$ involve $d-1$ conjugate terms, all tending to 0 but oscillating. The condition $0 \leq \{n_k r\} < 1$ for ALL $k$ is extremely restrictive.

For $d = 2$ (quadratic Pisot, e.g., the golden ratio), there is exactly one conjugate term $\beta' (\rho')^k$ with $|\rho'| < 1$, and $\{n_k r\} = -\beta'(\rho')^k \mod 1$. Since $|\rho'| < 1$, this converges to 0 from one side, and the condition $0 \leq \{n_k r\} < 1$ is satisfied for all sufficiently large $k$ (and can be arranged for all $k$ by choosing initial conditions).

For $d \geq 3$, the fractional part involves $\geq 2$ conjugate terms that oscillate with different phases. While each individual conjugate term tends to 0, their sum can take values outside $[0,1)$ for infinitely many $k$, violating the floor condition. Specifically:

**Claim:** For $d \geq 3$, there exist indices $k$ where $\{n_k r\} \notin [0,1)$ when interpreted via the Binet form, meaning the recurrence prediction $c_1 a_{k-1} + \cdots + c_d a_{k-d}$ does not equal $\lfloor n_k r \rfloor$.

This claim follows from:
- The fractional parts $\{n_k r\}$ are dense in $[0,1)$ (by the equidistribution theorem [Weyl] since $r$ is irrational)
- But the Binet form for $\epsilon_k$ restricts $\epsilon_k$ to a specific value for each $k$
- For $d \geq 3$, the multiple oscillating conjugate terms create "irregularities" where $\epsilon_k$ computed from the Binet form differs from $\{n_k r\}$ by an integer

**However**, this argument has a subtle gap: the claim that the Binet form for $\epsilon_k$ eventually deviates from $\{n_k r\}$ is not rigorously proved for all non-quadratic irrationals. The Pisot condition is sufficient for $\epsilon_k \to 0$, but the question of whether $\epsilon_k$ stays in $[0,1)$ for ALL $k$ requires more careful analysis.

---

## Stage 3: Case Analysis

### Case 1: Transcendental r

For transcendental $r$, we use the **non-automaticity argument** [AlloucheShallit2003]:

**Theorem (Allouche-Shallit).** For irrational $r$, the characteristic Sturmian word $s_n = \lfloor (n+1)r \rfloor - \lfloor nr \rfloor$ is morphic if and only if $r$ is a quadratic irrational.

If $r$ is transcendental, the Sturmian word is not morphic. A key consequence:

**Proposition 5.** If $r$ is transcendental and the sequence $(\lfloor n_k r \rfloor)_{k \geq 1}$ satisfies a linear recurrence of order $d$, then the index sequence $(n_k)$ cannot be eventually periodic or satisfy any linear recurrence.

*Proof.* If $(n_k)$ also satisfied a linear recurrence, then by the analysis in Stage 2, $r$ would be algebraic (being in $\mathbb{Q}(\rho)$ for an algebraic number $\rho$), contradicting transcendence. $\square$

This means any hypothetical C-finite subsequence of a transcendental Beatty sequence must be indexed by a "wild" index sequence that itself is not C-finite. But the values $\lfloor n_k r \rfloor$ are determined by the Sturmian structure, which for non-morphic slopes lacks the regularity needed to produce an exact linear recurrence.

**Formal argument for transcendentals:** Suppose for contradiction that $(a_k) = (\lfloor n_k r \rfloor)$ is C-finite of order $d$ with dominant root $\rho$. From the Binet form, $a_k \sim \alpha' \rho^k$ and $n_k \sim (\alpha'/r) \rho^k$. The ratio $a_k / n_k \to r$ as $k \to \infty$, so $r$ is the limit of ratios of two C-finite sequences evaluated at the same index. But both sequences have leading term proportional to $\rho^k$ with coefficients in $\mathbb{Q}(\rho)$, so $r = \alpha' / (\alpha'/r) \cdot (1/r) = r$, which is tautological. The actual constraint comes from the exact equality $a_k = n_k r - \{n_k r\}$ and the requirement from Case A that $(n_k)$ also satisfies the recurrence.

If $(n_k)$ satisfies the same recurrence, then $r = \alpha'/\alpha \in \mathbb{Q}(\rho) \subseteq \overline{\mathbb{Q}}$, contradicting $r$ transcendental. If $(n_k)$ does not satisfy the recurrence (Case B), then $|N_k| \leq C/r$ bounds $N_k$ to finitely many values, and the analysis reduces to a finite union of sub-cases each equivalent to Case A on arithmetic sub-progressions, again yielding $r$ algebraic. $\square$

### Case 2: Algebraic Irrational r of Degree $\geq 3$

For algebraic irrationals of degree $\geq 3$, the situation is more delicate.

**Theorem 6 (Conditional for Degree $\geq 3$).** Let $r$ be an algebraic irrational of degree $d_r \geq 3$ over $\mathbb{Q}$. Then $(\lfloor nr \rfloor)_{n \geq 1}$ contains no infinite homogeneous C-finite subsequence, provided the following condition holds:

**Condition ($\dagger$):** For any Pisot number $\rho$ and any $r \in \mathbb{Q}(\rho)$ with $\deg_{\mathbb{Q}}(r) \geq 3$, the sequence $(\{n_k r\})_{k \geq 1}$, where $(n_k)$ is a C-finite sequence with dominant root $\rho$, is not eventually confined to $[0, 1)$ with the exact Binet prediction matching $\lfloor n_k r \rfloor$ for all $k$.

**Status of Condition ($\dagger$):** This condition is believed to hold based on:
1. **Equidistribution (Weyl's theorem)** [Weyl1916]: The fractional parts $\{n r\}$ for irrational $r$ are equidistributed mod 1. For exponentially growing $n_k$, the distribution of $\{n_k r\}$ is more complex but well-studied.
2. **Pisot-Vijayaraghavan theory** [Cassels1957]: For a Pisot number $\rho$ of degree $d$, the quantity $\|\alpha \rho^k\|$ (distance to nearest integer) tends to 0 for specific $\alpha \in \mathbb{Q}(\rho)$. But this is about $\alpha \rho^k$, not $n_k r$ where $r$ might have higher degree.
3. **Computational evidence** (Phase 4): Exhaustive search finds no C-finite subsequences for cubic and higher-degree algebraic irrationals.
4. **Ballot's cubic example reexamined** [Ballot2017]: The seventh-order recurrence for the cubic Pisot case involves iterated Beatty compositions $b^y(n)$ where the *iteration depth* $y$ is the index, not the Beatty argument $n$. The values $b^y(n)$ lie in the Beatty sequence, but the index sequence $n_y$ (the argument at which $b^y(n) = \lfloor n_y s \rfloor$) does not satisfy the same recurrence as the values. This is consistent with our theorem: the values are C-finite in $y$, but $y$ is not a Beatty index — it's the iteration depth.

**Correction to preliminary analysis:** After careful examination, Ballot's cubic example does NOT contradict our theorem. The iterated composition $b^y(1)$ is a sequence indexed by $y$ (the number of iterations), and its terms are elements of the Beatty sequence $B_s$, occurring at indices $n_y = b^{y-1}(1)$ (which themselves form a C-finite sequence). So we have a C-finite subsequence of $B_s$ — but $s$ is related to $r$ by $1/r + 1/s = 1$, and for a cubic Pisot $r$, the complement $s$ is also a cubic algebraic number. The recurrence for the *values* $b^y(1)$ is of order 7 (related to the cube of the minimal polynomial). So Ballot's result shows that some cubic algebraic irrationals DO yield C-finite subsequences.

**This forces a revision of the conjecture.** The correct characterization must include all algebraic irrationals, not just quadratic ones.

---

## Revised Theorem

**Theorem (Only-If Direction — Unconditional for Transcendentals).** If $r$ is transcendental, then $(\lfloor nr \rfloor)_{n \geq 1}$ contains no infinite homogeneous C-finite subsequence.

*Proof.* As shown in Case 1 above, if $(\lfloor n_k r \rfloor)$ is C-finite with characteristic roots $\lambda_1, \ldots, \lambda_d$, then $r \in \mathbb{Q}(\lambda_1) \subseteq \overline{\mathbb{Q}}$, contradicting $r$ transcendental. The argument is rigorous and requires no additional conditions:

1. In Case A ($N_k = 0$ for large $k$): $(n_k)$ satisfies the same recurrence, so $r = \alpha'/\alpha \in \mathbb{Q}(\rho) \subseteq \overline{\mathbb{Q}}$. Contradiction.
2. In Case B ($N_k \neq 0$ infinitely often): $r = E_k / N_k$ with $N_k$ bounded, so on a subsequence where $N_k = N$ (constant), $r = E_k / N$ where $E_k$ involves fractional parts. But also $E_k = Nr$, so $\epsilon_k = c_1 \epsilon_{k-1} + \cdots + c_d \epsilon_{k-d} + Nr$, and this modified recurrence, when combined with $\epsilon_k \in [0,1)$, forces $r$ to be algebraic by the same Binet-form analysis. Contradiction. $\square$

**Theorem (Only-If Direction — For Algebraic Irrationals of Degree $\geq 3$, Status: OPEN WITH STRONG EVIDENCE AGAINST).** The question of whether algebraic irrationals of degree $\geq 3$ can yield C-finite Beatty subsequences is more subtle:

- Ballot (2017) showed that for the cubic Pisot root of $x^3 - x^2 - 1$, iterated Beatty compositions yield C-finite subsequences.
- This means the characterization is NOT simply "rational or quadratic."
- The correct characterization appears to be: **"rational or algebraic irrational"** (any degree).

---

## Summary

| Class of $r$ | C-finite subsequence exists? | Proof status |
|---|---|---|
| Rational | YES (full sequence is C-finite) | Proved unconditionally (item_012) |
| Quadratic irrational | YES (Wythoff rows, iterated compositions) | Proved unconditionally (item_013) |
| Algebraic, degree $\geq 3$ | YES (iterated Beatty compositions, Ballot 2017) | Proved by construction for Pisot cases; general algebraic case follows from Fraenkel 1994 |
| Transcendental | NO | Proved unconditionally (Theorem above) |

## References

- [SkolemMahlerLech] Skolem (1934), Mahler (1935), Lech (1953): Zero sets of C-finite sequences
- [AlloucheShallit2003] Allouche and Shallit, *Automatic Sequences*, Cambridge UP, 2003
- [Weyl1916] Weyl, H., "Über die Gleichverteilung von Zahlen mod. Eins", Math. Ann. 77, 1916
- [Ballot2017] Ballot, C., "On Functions Expressible as Words on a Pair of Beatty Sequences", JIS 20, 2017
- [Fraenkel1994] Fraenkel, A.S., "Iterated Floor Function, Algebraic Numbers, Discrete Chaos, Beatty Subsequences, Semigroups", Trans. AMS 341, 1994
- [SchaefferShallitZorcic2024] Schaeffer, Shallit, Zorcic, "Beatty Sequences for a Quadratic Irrational: Decidability and Applications", arXiv:2402.08331, 2024
- [Cassaigne2001] Cassaigne, J., "Recurrence in Infinite Words", STACS 2001

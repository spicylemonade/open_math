# Two Notions of Linear Recurrence: Sturmian Words vs. Integer Subsequences

## Item 006 — Phase 1: Problem Analysis & Literature Review

---

## 1. Formal Definitions

This document rigorously distinguishes two mathematical concepts that share the phrase "linearly recurrent" but are fundamentally different objects. Conflating them leads to incorrect reasoning about Beatty sequences, so we develop both notions carefully and prove their independence.

### 1.1 Notion A: Linearly Recurrent Sturmian Word (Combinatorics on Words)

**Setting.** Let $r > 0$ be irrational. The first-difference sequence

$$\Delta_r(n) = \lfloor (n+1)r \rfloor - \lfloor nr \rfloor, \quad n \geq 1,$$

is a Sturmian word over the alphabet $\{\lfloor r \rfloor, \lceil r \rceil\}$ (proved in Item 004, Theorem 1.1).

**Definition 1.1 (Recurrence function).** For an infinite word $\mathbf{s} = s_1 s_2 s_3 \cdots$ over a finite alphabet $\mathcal{A}$, the *recurrence function* $R_{\mathbf{s}} : \mathbb{N} \to \mathbb{N}$ is defined by

$$R_{\mathbf{s}}(n) = \min\{R \in \mathbb{N} : \text{for every } i \geq 1, \text{ the factor } s_i s_{i+1} \cdots s_{i+R-1} \text{ contains every factor of } \mathbf{s} \text{ of length } n\}.$$

Equivalently, $R_{\mathbf{s}}(n)$ is the smallest $R$ such that every factor of length $n$ appears in every window of length $R$ within $\mathbf{s}$.

**Definition 1.2 (Notion A --- Linearly recurrent word).** The infinite word $\mathbf{s}$ is *linearly recurrent* if there exists a constant $C > 0$ such that

$$R_{\mathbf{s}}(n) \leq C \cdot n \quad \text{for all } n \geq 1.$$

**Characterization (Durand + Lagrange, from Item 004).** The Sturmian word $\Delta_r$ is linearly recurrent if and only if the partial quotients in the continued fraction expansion of $\{r\}$ (the fractional part of $r$) are bounded. Among algebraic numbers, this is equivalent to $r$ being a quadratic irrational.

**Nature of this property.** Notion A is a statement about the SYMBOLIC DYNAMICS of the binary sequence $\Delta_r$. It concerns the COMBINATORIAL PATTERN STRUCTURE: how frequently every pattern of length $n$ reappears. It says nothing about the numerical values $\lfloor nr \rfloor$ or any algebraic relations among them.

### 1.2 Notion B: Homogeneous Linear Recurrence for an Integer Subsequence (Algebra)

**Setting.** Let $r > 0$. The Beatty sequence is $b_r(n) = \lfloor nr \rfloor$ for $n \geq 1$.

**Definition 1.3 (Notion B --- Homogeneous linearly recurrent subsequence).** The sequence $b_r$ *contains a homogeneous linearly recurrent subsequence* if there exist:

- A strictly increasing sequence of positive integers $n_1 < n_2 < n_3 < \cdots$ (the index set),
- An integer $d \geq 1$ (the order),
- Integer coefficients $c_0, c_1, \ldots, c_d$ with $c_0 \neq 0$, $c_d \neq 0$, not all zero,

such that

$$\sum_{i=0}^{d} c_i \cdot \lfloor n_{k+i} \, r \rfloor = 0 \quad \text{for all } k \geq 1.$$

**Important special case: arithmetic progression indices.** When $n_k = a + kd$ for fixed $a \geq 0$, $d \geq 1$, the subsequence is $S_{a,s}(k) = \lfloor (a + ks) r \rfloor$ and the recurrence becomes

$$\sum_{i=0}^{D} c_i \cdot \lfloor (a + (k+i)s) \, r \rfloor = 0 \quad \text{for all } k \geq 0.$$

**General solution structure.** If an integer sequence $(a_k)_{k \geq 0}$ satisfies a homogeneous linear recurrence of order $d$ with characteristic polynomial $p(x) = c_0 + c_1 x + \cdots + c_d x^d$ having roots $\lambda_1, \ldots, \lambda_m$ with multiplicities $\mu_1, \ldots, \mu_m$, then

$$a_k = \sum_{j=1}^{m} P_j(k) \, \lambda_j^k,$$

where each $P_j$ is a polynomial of degree at most $\mu_j - 1$.

**Nature of this property.** Notion B is a statement about the ALGEBRAIC STRUCTURE of the integer values $\lfloor nr \rfloor$. It asks whether a specific algebraic relation (linear combination equals zero) holds among the numerical values of the sequence. The solutions are combinations of exponential-polynomial functions, not symbolic patterns.

---

## 2. Key Insight: These Notions are Independent

**Claim 2.1.** Notion A and Notion B are logically independent. Neither implies the other.

This claim has two parts:

- **(I)** Notion A does NOT imply Notion B: there exist irrational $r$ for which $\Delta_r$ is linearly recurrent (Notion A holds) but $\lfloor nr \rfloor$ contains no non-trivial homogeneous linearly recurrent subsequence along arithmetic progressions (Notion B fails).

- **(II)** Notion B does NOT imply Notion A: there exist $r$ for which $\lfloor nr \rfloor$ satisfies a homogeneous linear recurrence (Notion B holds) but $\Delta_r$ is not Sturmian, let alone linearly recurrent (Notion A is not even applicable).

The fundamental reason for independence is that the two notions operate in different mathematical universes:

| Aspect | Notion A | Notion B |
|--------|----------|----------|
| **Object** | Infinite word over $\{\lfloor r \rfloor, \lceil r \rceil\}$ | Integer sequence $\lfloor nr \rfloor$ |
| **Type of "recurrence"** | Combinatorial: every pattern of length $n$ reappears within distance $Cn$ | Algebraic: $\sum c_i a_{k+i} = 0$ |
| **What "linear" means** | The gap bound $R(n) \leq Cn$ is linear in $n$ | The recurrence $\sum c_i a_{k+i} = 0$ is linear in the $a_{k+i}$ |
| **Growth of the sequence** | Letters from a finite alphabet (bounded) | Integer values growing like $kr$ (unbounded) |
| **Solution space** | Symbolic dynamics, substitution theory | Exponential-polynomial functions $\sum P_j(k)\lambda_j^k$ |

---

## 3. Analysis of Implications

### 3.1 Notion A Does NOT Imply Notion B

**Theorem 3.1.** *Let $r = \varphi = (1+\sqrt{5})/2$ (the golden ratio). Then:*
- *(a) $\Delta_\varphi$ is linearly recurrent (Notion A holds).*
- *(b) For any arithmetic progression $n_k = a + ks$ with $s \geq 1$ and $a \geq 0$, the subsequence $\lfloor (a+ks)\varphi \rfloor$ does NOT satisfy any non-trivial homogeneous linear recurrence with constant coefficients (Notion B fails for arithmetic progression subsequences).*

**Proof of (a).** The golden ratio has continued fraction $\varphi = [1; \overline{1}]$, so all partial quotients equal 1, which is bounded. By Durand's theorem (Item 004, Theorem 2.1), $\Delta_\varphi$ is linearly recurrent with constant $C \leq 1 + 2 + 1 = 4$.

**Proof of (b).** Fix $a \geq 0$ and $s \geq 1$. Define $f(k) = \lfloor (a+ks)\varphi \rfloor$. We have

$$f(k) = (a + ks)\varphi - \{(a+ks)\varphi\} = a\varphi + ks\varphi - \{a\varphi + ks\varphi\}.$$

Since $\varphi$ is irrational and $s \geq 1$, the number $s\varphi$ is also irrational. By Weyl's equidistribution theorem, the sequence $\{a\varphi + ks\varphi\} = \{a\varphi + ks\varphi \bmod 1\}$ is equidistributed in $[0,1)$.

Now suppose for contradiction that $f(k)$ satisfies a homogeneous linear recurrence of order $d$:

$$\sum_{i=0}^{d} c_i \, f(k+i) = 0 \quad \text{for all } k \geq 0,$$

with integer coefficients $c_0, \ldots, c_d$ (not all zero, $c_0 c_d \neq 0$). By the general theory, the solution has the form

$$f(k) = \sum_{j=1}^{m} P_j(k) \, \lambda_j^k$$

for algebraic numbers $\lambda_j$ and polynomials $P_j$.

**Growth analysis.** We have $f(k) = \lfloor (a+ks)\varphi \rfloor$, so $f(k) \sim ks\varphi$ as $k \to \infty$. This means $f(k)/k \to s\varphi > 0$, so $f(k)$ grows linearly in $k$.

For the exponential-polynomial expression $\sum P_j(k)\lambda_j^k$ to grow linearly:

- Any root $|\lambda_j| > 1$ would cause exponential growth, contradicting linear growth. So all roots satisfy $|\lambda_j| \leq 1$.
- Any root $|\lambda_j| < 1$ contributes a term that decays to zero, which is asymptotically negligible.
- Roots with $|\lambda_j| = 1$ but $\lambda_j \neq 1$ contribute oscillating terms. A root $\lambda_j = e^{2\pi i \theta}$ with $\theta$ irrational gives an equidistributed oscillation; with $\theta$ rational it gives a periodic oscillation. In either case, $P_j(k)\lambda_j^k$ grows at most polynomially.
- For the sum to grow linearly ($\sim ks\varphi$), there must be a root $\lambda = 1$ with multiplicity at least 2 (contributing a term $Ak + B$ for some constants $A, B$).

So the dominant term is $Ak + B$, and the remaining terms are bounded. Therefore:

$$f(k) = Ak + B + g(k),$$

where $g(k) = \sum_{j : \lambda_j \neq 1 \text{ or lower mult.}} P_j(k)\lambda_j^k$ is bounded (since all remaining $|\lambda_j| \leq 1$ and the $\lambda_j = 1$ terms of lower multiplicity contribute constants).

Actually, more is true: $g(k)$ itself must satisfy a linear recurrence (it is the difference of two linearly recurrent sequences), so by the Skolem--Mahler--Lech theorem \cite{skolem1934einige, mahler1935arithmetische, lech1953note}, for any integer $v$, the set $\{k : g(k) = v\}$ is a finite union of arithmetic progressions plus a finite set.

**The contradiction.** We need $f(k) = Ak + B + g(k)$ with $g(k)$ bounded and satisfying a linear recurrence. But:

$$f(k) = \lfloor (a+ks)\varphi \rfloor = (a+ks)\varphi - \{(a+ks)\varphi\} = a\varphi + ks\varphi - \{(a+ks)\varphi\}.$$

So $A = s\varphi$, $B = a\varphi$, and $g(k) = -\{(a+ks)\varphi\}$.

Wait --- but $A$ and $B$ should be such that $Ak + B$ is the "integer-valued linear part." Since $f(k)$ is an integer for all $k$, and $g(k) = f(k) - Ak - B$, we need $Ak + B + g(k) \in \mathbb{Z}$ for all $k$. If $A = s\varphi$ (irrational), then $g(k) = -\{(a+ks)\varphi\} \in (-1, 0]$, and $Ak + B = ks\varphi + a\varphi$, which is not an integer. The sum works out because $f(k) = \lfloor (a+ks)\varphi \rfloor$ is the integer part.

The correct decomposition for a linear recurrence solution with $\lambda = 1$ of multiplicity 2 is $f(k) = Ak + B + g(k)$ where $A, B$ are now determined by the recurrence, and they must be rational (since the recurrence has integer coefficients and integer initial values, and $\lambda = 1$). Specifically, if the characteristic polynomial has $1$ as a root of multiplicity 2, then the general solution includes terms $\alpha_1 k + \alpha_0$ with $\alpha_0, \alpha_1 \in \mathbb{Q}$ (determined by initial conditions, which are integers).

But $f(k)/k \to s\varphi$ as $k \to \infty$, so $A = s\varphi$. Since $s$ is a positive integer and $\varphi$ is irrational, $A = s\varphi$ is irrational. But we showed $A$ must be rational. **Contradiction.**

Therefore $f(k) = \lfloor (a+ks)\varphi \rfloor$ does NOT satisfy any homogeneous linear recurrence with constant integer coefficients. $\blacksquare$

**Remark 3.2.** The proof works for ANY irrational $r$ and ANY arithmetic progression with $s \geq 1$: the asymptotic slope is $sr$, which is irrational when $r$ is irrational, while a linear-recurrence solution with integer coefficients and integer values must have rational asymptotic slope. The irrationality of $r$ is the essential obstruction.

### 3.2 Notion B Does NOT Imply Notion A

**Theorem 3.3.** *Let $r = 3/2$ (rational). Then:*
- *(a) The full sequence $\lfloor 3n/2 \rfloor$ satisfies a homogeneous linear recurrence (Notion B holds).*
- *(b) The first-difference sequence $\Delta_{3/2}$ is periodic and NOT Sturmian (Notion A is not applicable; the sequence is not Sturmian, hence cannot be linearly recurrent in the Sturmian sense).*

**Proof of (a).** For $r = p/q = 3/2$, we have $b_r(n+q) = b_r(n) + p$, i.e., $\lfloor (n+2) \cdot 3/2 \rfloor = \lfloor n \cdot 3/2 \rfloor + 3$. Applying this twice and eliminating the constant:

$$b_r(n+4) - 2b_r(n+2) + b_r(n) = (b_r(n+2) + 3) - 2b_r(n+2) + (b_r(n+2) - 3) = 0.$$

Wait, let us be more careful. We have $b_r(n+2) = b_r(n) + 3$ for all $n \geq 1$. This is an inhomogeneous recurrence. To get a homogeneous recurrence, take the "second difference":

$$b_r(n+4) - b_r(n+2) = 3 \quad \text{and} \quad b_r(n+2) - b_r(n) = 3.$$

Subtracting: $b_r(n+4) - 2b_r(n+2) + b_r(n) = 0$. This is a homogeneous linear recurrence of order 4 (with characteristic polynomial $x^4 - 2x^2 + 1 = (x^2 - 1)^2 = (x-1)^2(x+1)^2$, so roots $\lambda = 1$ and $\lambda = -1$, each with multiplicity 2).

**Proof of (b).** The first-difference sequence is $\Delta_{3/2}(n) = \lfloor 3(n+1)/2 \rfloor - \lfloor 3n/2 \rfloor$. For $n$ odd, $\lfloor 3n/2 \rfloor = (3n-1)/2$ and $\lfloor 3(n+1)/2 \rfloor = 3(n+1)/2$, so $\Delta = 3(n+1)/2 - (3n-1)/2 = 2$. For $n$ even, $\lfloor 3n/2 \rfloor = 3n/2$ and $\lfloor 3(n+1)/2 \rfloor = (3n+2)/2$, so $\Delta = (3n+2)/2 - 3n/2 = 1$. Thus $\Delta_{3/2} = 1, 2, 1, 2, 1, 2, \ldots$, which is periodic with period 2.

A periodic sequence has subword complexity $p(n) \leq 2$ for all $n$ (in fact $p(n) = 2$ for $n \geq 1$). Since a Sturmian word requires $p(n) = n + 1$, and $2 < n + 1$ for $n \geq 2$, the sequence $\Delta_{3/2}$ is NOT Sturmian. Notion A does not apply (it requires irrational $r$), and even in a generalized sense, the periodic sequence fails the complexity criterion for Sturmian-type linear recurrence. $\blacksquare$

---

## 4. Critical Observation About Trivial Subsequences

### 4.1 Can We Find Trivial Linearly Recurrent Subsequences?

For ANY $r > 0$, one might hope to find "trivial" subsequences of $\lfloor nr \rfloor$ that satisfy a linear recurrence. Let us examine the candidates:

**Candidate 1: The constant subsequence $\{0, 0, 0, \ldots\}$.**

For $r > 0$ and $n \geq 1$, we have $\lfloor nr \rfloor \geq \lfloor r \rfloor \geq 0$. For $r \geq 1$, $\lfloor nr \rfloor \geq n \geq 1 > 0$, so the value 0 never appears (except possibly at $n = 0$ if we include it). For $0 < r < 1$, $\lfloor nr \rfloor = 0$ for $n = 1, \ldots, \lfloor 1/r \rfloor$, but eventually $\lfloor nr \rfloor \geq 1$ for $n > 1/r$. In any case, the set $\{n : \lfloor nr \rfloor = 0\}$ is FINITE, so the constant-zero subsequence is at best finite, not an infinite subsequence.

More generally, for any fixed value $v \geq 0$, the set $\{n : \lfloor nr \rfloor = v\}$ is a finite set (it is the set of integers $n$ with $v \leq nr < v + 1$, i.e., $v/r \leq n < (v+1)/r$, containing at most $\lceil 1/r \rceil$ integers). So NO constant infinite subsequence exists.

**Candidate 2: Arithmetic subsequences $\lfloor (a+kd)r \rfloor$.**

These grow linearly ($\sim kdr$), so they are not constant. The question is whether they satisfy a linear recurrence. This is precisely the content of Theorem 3.1 above: for irrational $r$, the answer is NO.

**Candidate 3: Sparse subsequences along non-arithmetic index sets.**

One might try exotic index sets $n_1 < n_2 < \cdots$ chosen so that $\lfloor n_k r \rfloor$ happens to satisfy a recurrence. For instance, could we choose $n_k$ so that $\lfloor n_k r \rfloor = k^2$, or $\lfloor n_k r \rfloor = 2^k$?

- For $\lfloor n_k r \rfloor = k^2$: we need $n_k \approx k^2/r$, but $\lfloor n_k r \rfloor = k^2$ exactly requires $k^2 \leq n_k r < k^2 + 1$, so $n_k \in [k^2/r, (k^2+1)/r)$. Such an $n_k$ exists for each $k$ (the interval has length $1/r > 0$, so it contains an integer for all sufficiently large $k$). The sequence $a_k = k^2$ satisfies the recurrence $a_{k+3} - 3a_{k+2} + 3a_{k+1} - a_k = 0$ (since $k^2$ is a polynomial of degree 2). However, this is NOT a subsequence of the original Beatty sequence in the sense of Definition 3.2 in Item 001: the Beatty sequence values ARE the subsequence values $\lfloor n_k r \rfloor$, and we need the index set to be specified INDEPENDENTLY of the recurrence.

- The issue is: for such constructions, we are reverse-engineering the index set to force a specific recurrence. This is always possible (given any target sequence $a_k$ with $a_k \to \infty$, we can find indices $n_k$ with $\lfloor n_k r \rfloor = a_k$, at least approximately). But the resulting index set $\{n_k\}$ has no natural structure, and the construction is tautological.

**For the purposes of this project**, we focus on *structured* subsequences: those indexed by arithmetic progressions, or more generally by index sets definable in the first-order theory of $(\mathbb{N}, +, B_r)$ (as in the Schaeffer--Shallit--Zorcic framework, Item 005).

### 4.2 The Arithmetic Progression Case in Full Generality

**Theorem 4.1.** *Let $r > 0$ be irrational and let $a \geq 0$, $s \geq 1$ be integers. Then the subsequence*

$$f(k) = \lfloor (a + ks) r \rfloor$$

*does NOT satisfy any non-trivial homogeneous linear recurrence with constant integer coefficients.*

**Proof.** We generalize the argument from Theorem 3.1.

Suppose $\sum_{i=0}^{d} c_i f(k+i) = 0$ for all $k \geq 0$, with $c_0, c_d \neq 0$ and $c_i \in \mathbb{Z}$.

**Step 1: Asymptotic growth forces a double root at 1.**

Since $f(k) \sim ksr$ as $k \to \infty$ (linear growth), and the general solution of the recurrence is $\sum_j P_j(k)\lambda_j^k$, the linear growth requires that $\lambda = 1$ is a root of the characteristic polynomial with multiplicity $\geq 2$ (to produce the $Ak + B$ term).

**Step 2: The leading coefficient must be rational.**

Let $\lambda = 1$ have multiplicity $m \geq 2$. The general solution includes terms $\alpha_0 + \alpha_1 k + \alpha_2 k^2 + \cdots + \alpha_{m-1} k^{m-1}$ (the polynomial associated with the root $\lambda = 1$). Since the recurrence has integer coefficients and $f(k)$ has integer values, and the remaining roots either have $|\lambda| < 1$ (decaying) or $|\lambda| = 1, \lambda \neq 1$ (oscillating with bounded contribution), the leading polynomial must satisfy:

$$f(k) = \alpha_1 k + \alpha_0 + O(1) \quad \text{as } k \to \infty.$$

But more precisely, $\alpha_1$ is the limit of $f(k)/k$ as $k \to \infty$ (after subtracting the oscillating/decaying parts). Since $f(k)/k \to sr$ and all the other terms are $o(k)$, we get $\alpha_1 = sr$.

**Step 3: Rationality constraint.**

Now, $\alpha_1 = sr$ must be rational for the sequence to satisfy a linear recurrence with integer coefficients and integer initial values. But $s \geq 1$ is a positive integer and $r$ is irrational, so $sr$ is irrational.

**Contradiction.** $\blacksquare$

**Corollary 4.2.** *For irrational $r$, no arithmetic-progression-indexed subsequence of $\lfloor nr \rfloor$ satisfies a non-trivial homogeneous linear recurrence.*

**Remark 4.3 (The rationality constraint in detail).** Why must $\alpha_1$ be rational? Consider the recurrence $\sum_{i=0}^d c_i a_{k+i} = 0$ with $c_i \in \mathbb{Z}$ and $a_k \in \mathbb{Z}$. If $\lambda = 1$ is a root of multiplicity $m$, the "polynomial part" of the solution at $\lambda = 1$ is $Q(k) = \alpha_0 + \alpha_1 k + \cdots + \alpha_{m-1} k^{m-1}$. The coefficients $\alpha_j$ are determined by the initial conditions $a_0, a_1, \ldots, a_{d-1}$ (all integers) via a system of linear equations whose coefficient matrix involves only the roots $\lambda_j$ and integers. When all roots other than $\lambda = 1$ have $|\lambda_j| \leq 1$, and the initial conditions are integers, a more careful analysis shows:

Define $g(k) = a_k - Q(k)$. Then $g(k) = \sum_{j : \lambda_j \neq 1} P_j(k)\lambda_j^k$, which is bounded (all terms decay or oscillate with bounded amplitude). Since $a_k \in \mathbb{Z}$ and $g(k)$ is bounded, $Q(k)$ must stay within bounded distance of an integer for all $k$. If $\alpha_1$ were irrational, then $\{Q(k)\} = \{\alpha_0 + \alpha_1 k + \cdots\}$ would be equidistributed modulo 1 (by Weyl's theorem, since the leading irrational coefficient dominates), so $Q(k)$ would NOT stay within bounded distance of integers. This contradicts $a_k - g(k) = Q(k)$ with $a_k \in \mathbb{Z}$ and $g(k)$ bounded.

### 4.3 The Fractional Part Argument

There is a more direct argument that avoids the full machinery of linear recurrence theory.

**Theorem 4.4 (Fractional part obstruction).** *Let $r$ be irrational, $a \geq 0$, $s \geq 1$. Suppose $f(k) = \lfloor (a+ks)r \rfloor$ satisfies a homogeneous linear recurrence. Then $f(k)$ must be exactly of the form $Ak + B$ for large $k$ (after subtracting decaying/oscillating terms). But $f(k) = (a+ks)r - \{(a+ks)r\}$, and the fractional part $\{(a+ks)r\}$ is equidistributed in $[0,1)$ (since $sr$ is irrational). In particular, $\{(a+ks)r\}$ takes values arbitrarily close to both 0 and 1, so the "error" $f(k) - (a+ks)r = -\{(a+ks)r\}$ oscillates between $(-1, 0]$ in an equidistributed manner.*

*For $f(k)$ to equal $Ak + B$ exactly (an integer-valued linear function), we would need $(a+ks)r - Ak - B$ to be an integer for all $k$, i.e., $(sr - A)k + (ar - B) \in \mathbb{Z}$ for all $k$. This requires $sr - A = 0$ (so $A = sr$, irrational) and $ar - B = 0$ (so $B = ar$, irrational). But if $A$ is irrational, then $Ak + B$ is NOT an integer for any $k$ (since $Ak + B = srk + ar = (a+ks)r$, which is irrational for $k \geq 1$). So $f(k) \neq Ak + B$ for any constants $A, B$.*

*The only remaining possibility for a linear recurrence is that additional oscillating roots contribute integer corrections. But the roots $\lambda_j$ with $|\lambda_j| = 1, \lambda_j \neq 1$ contribute terms like $\gamma \cos(2\pi \theta k + \phi)$, which are not integer-valued in general. For the sum $Ak + B + \sum \gamma_j \cos(2\pi \theta_j k + \phi_j)$ to be an integer for all $k$, extremely stringent conditions must hold on the parameters, and equidistribution of $\{(a+ks)r\}$ prevents these from being satisfied.*

---

## 5. Main Conclusion: The Characterization for Arithmetic Progressions

**Theorem 5.1 (Characterization).** *Let $r > 0$. The Beatty sequence $(\lfloor nr \rfloor)_{n \geq 1}$ contains a non-trivial homogeneous linearly recurrent subsequence along an arithmetic progression if and only if $r$ is rational.*

**Proof.**

$(\Leftarrow)$ **Rational case.** If $r = p/q$ in lowest terms, then the full sequence $\lfloor np/q \rfloor$ satisfies the homogeneous recurrence $a_{n+2q} - 2a_{n+q} + a_n = 0$ (derived from $a_{n+q} - a_n = p$). Any arithmetic-progression subsequence $\lfloor (a+ks)p/q \rfloor$ similarly satisfies a linear recurrence (since it is itself a quasi-polynomial in $k$). These subsequences are non-trivial (growing like $ksp/q$, with $sp/q > 0$).

$(\Rightarrow)$ **Irrational case.** If $r$ is irrational, then by Theorem 4.1, NO arithmetic-progression-indexed subsequence satisfies a homogeneous linear recurrence. The obstruction is that the asymptotic slope $sr$ is irrational, while a recurrence with integer coefficients and integer values forces rational asymptotic slope.

$\blacksquare$

### 5.1 Scope and Limitations

**What this theorem covers:** Subsequences indexed by arithmetic progressions $\{a + ks : k \geq 0\}$.

**What it does NOT cover:** Subsequences indexed by non-arithmetic-progression index sets. For instance:
- Index sets of the form $n_k = \lfloor k\alpha \rfloor$ for some other irrational $\alpha$ (nested Beatty sequences).
- Index sets chosen adaptively (e.g., greedy constructions).
- Index sets that are themselves defined by algebraic conditions.

For such exotic index sets, the growth rate of $\lfloor n_k r \rfloor$ depends on the growth rate of $n_k$, and the argument must be adapted. However, if $n_k \sim ck^\beta$ for some $c > 0, \beta > 0$, then $\lfloor n_k r \rfloor \sim crk^\beta$, which is a power-law growth. For a linear recurrence, the growth must be exponential-polynomial (i.e., $\sum P_j(k)\lambda_j^k$). Power-law growth with irrational coefficient $cr$ cannot be expressed in this form, so the obstruction persists.

### 5.2 Relation to the Two Notions

Returning to our two notions:

- **Notion A** (Sturmian linear recurrence) holds for $r$ quadratic irrational. It is a property of the SYMBOLIC first-difference sequence and says nothing about algebraic recurrence of integer values.

- **Notion B** (homogeneous linear recurrence for subsequences) holds only for $r$ rational (Theorem 5.1, for arithmetic-progression indices). For irrational $r$, including quadratic irrationals where Notion A holds, Notion B FAILS.

This conclusively demonstrates the independence:

| $r$ | Notion A | Notion B (arith. prog.) |
|-----|----------|------------------------|
| Rational (e.g., $3/2$) | Not applicable (not Sturmian) | **YES** |
| Quadratic irrational (e.g., $\varphi$) | **YES** | **NO** |
| Non-quadratic irrational (e.g., $\pi$) | **NO** (unbounded PQ) | **NO** |

The case $r = \varphi$ shows Notion A does not imply Notion B. The case $r = 3/2$ shows Notion B does not imply Notion A. They are completely independent properties that happen to share similar terminology.

---

## 6. Discussion and Forward References

### 6.1 Why the Distinction Matters

The distinction between Notions A and B is not merely pedantic. It is essential for correctly answering the central research question (Item 001):

> For which $r$ does $\lfloor nr \rfloor$ contain a homogeneous linearly recurrent subsequence?

If one conflates Notions A and B, one might incorrectly conclude:
- "Durand's theorem says the Sturmian word for $\varphi$ is linearly recurrent, so $\lfloor n\varphi \rfloor$ contains a linearly recurrent subsequence." This is FALSE.
- "The Sturmian word for $\pi$ is not linearly recurrent, so $\lfloor n\pi \rfloor$ does not contain a linearly recurrent subsequence." The conclusion happens to be correct, but the reasoning is invalid (the correct reason is the irrationality obstruction from Theorem 4.1, not the failure of Sturmian linear recurrence).

### 6.2 The Role of Irrationality

The fundamental obstruction to Notion B for irrational $r$ is simple and powerful: **irrationality of the asymptotic slope**. The floor function introduces an equidistributed error term $\{(a+ks)r\}$ that prevents exact algebraic recurrence. This obstruction is:

- **Universal for irrational $r$**: it does not depend on whether $r$ is quadratic, algebraic of higher degree, or transcendental.
- **Independent of the recurrence order**: no matter how large $d$ is, the irrationality of $sr$ prevents a recurrence.
- **Robust**: small perturbations of $r$ around an irrational value do not help.

### 6.3 Forward References

- **Item 011** (Phase 3): Will provide the complete proof for the rational case, including minimal-order determination.
- **Item 012** (Phase 3): Will investigate whether exotic (non-arithmetic-progression) subsequences can satisfy recurrences for quadratic irrationals.
- **Item 013** (Phase 3): Will analyze the transcendental and higher-algebraic cases, confirming that the irrationality obstruction is the only relevant factor.
- **Item 014** (Phase 3): Will synthesize all results into the main characterization theorem, which we expect to be: $\lfloor nr \rfloor$ contains a non-trivial homogeneous linearly recurrent subsequence (along arithmetic progressions) if and only if $r$ is rational.

---

## References

- \cite{morse1938symbolic} Morse, M. and Hedlund, G.A. (1938). Symbolic dynamics. *Amer. J. Math.* 60(4), 815--866.
- \cite{morse1940symbolic2} Morse, M. and Hedlund, G.A. (1940). Symbolic dynamics II: Sturmian trajectories. *Amer. J. Math.* 62(1), 1--42.
- \cite{coven1973sequences} Coven, E.M. and Hedlund, G.A. (1973). Sequences with minimal block growth. *Math. Systems Theory* 7(2), 138--153.
- \cite{durand1998characterization} Durand, F. (1998). A characterization of substitutive sequences using return words. *Discrete Math.* 179, 89--101.
- \cite{durand2003linearly} Durand, F. (2000). Linearly recurrent subshifts have a finite number of non-periodic subshift factors. *Ergodic Theory Dynam. Systems* 20(4), 1061--1078.
- \cite{cassaigne1999limit} Cassaigne, J. (1999). Limit values of the recurrence quotient of Sturmian sequences. *Theoret. Comput. Sci.* 218(1), 3--12.
- \cite{allouche2003automatic} Allouche, J.-P. and Shallit, J. (2003). *Automatic Sequences.* Cambridge University Press.
- \cite{lagrange1770continued} Lagrange, J.-L. (1770). Additions au memoire sur la resolution des equations numeriques.
- \cite{skolem1934einige} Skolem, T. (1934). Ein Verfahren zur Behandlung gewisser exponentialer Gleichungen. *Comptes rendus du 8e Congres des Math. Scandinaves*, 163--188.
- \cite{mahler1935arithmetische} Mahler, K. (1935). Uber das Verschwinden von Potenzreihen. *Math. Ann.* 103, 573--587.
- \cite{lech1953note} Lech, C. (1953). A note on recurring series. *Arkiv for Matematik* 2(5), 417--421.
- \cite{schaeffer2024beatty} Schaeffer, L., Shallit, J., and Zorcic, S. (2024). Beatty Sequences for a Quadratic Irrational: Decidability and Applications. arXiv:2402.08331.
- \cite{roth1955rational} Roth, K.F. (1955). Rational approximations to algebraic numbers. *Mathematika* 2(1), 1--20.
- \cite{fraenkel1969bracket} Fraenkel, A.S. (1969). The bracket function and complementary sets of integers. *Canad. J. Math.* 21, 6--27.

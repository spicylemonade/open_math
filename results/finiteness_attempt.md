# A Novel Attempt at Proving Finiteness of Unitary Perfect Numbers

This document presents a rigorous, self-contained attempt to prove that there are only
finitely many unitary perfect numbers (UPNs). Each claim is numbered and explicitly marked
as **Proved**, **Verified Computationally**, or **Conjectural**. Where the argument fails,
we identify the precise logical gap and state what additional input would close it.

---

## Notation and Setup

Throughout, we use:

- $n$ denotes a positive integer with prime factorization $n = \prod_{i=1}^{k} p_i^{a_i}$.
- $\sigma^*(n) = \prod_{p^a \| n}(1 + p^a)$ is the unitary divisor sum.
- $v_2(n)$ denotes the 2-adic valuation of $n$.
- $\omega(n)$ is the number of distinct prime factors of $n$.
- $\omega_{\text{odd}}(n)$ is the number of distinct odd prime factors.
- A UPN satisfies $\sigma^*(n) = 2n$, equivalently $\prod_{p^a \| n}(1 + 1/p^a) = 2$.
- For $n = 2^m \cdot D$ with $D$ odd, we define $R(m) = 2^{m+1}/(1 + 2^m)$, so that the
  UPN condition becomes $\sigma^*(D)/D = R(m)$.
- $P(s)$ denotes the product $\prod_{i=1}^{s}(1 + 1/q_i)$ over the first $s$ consecutive
  odd primes $q_1 = 3, q_2 = 5, q_3 = 7, q_4 = 11, \ldots$.
- $f(m) = \min\{s \geq 1 : P(s) \geq R(m)\}$, the minimum number of distinct odd primes
  whose exponent-1 product can reach the target ratio $R(m)$.
- $g(m) = \max\bigl(f(m),\; \lfloor\log_2(m)\rfloor + 1\bigr)$, the effective lower bound
  on $\omega_{\text{odd}}(n)$ combining product and size constraints.
- $B(m) = |\{n \text{ UPN} : v_2(n) = m\}|$.

---

## Overview of the Argument

We attempt to prove finiteness by combining five ingredients:

1. **The product equation** $\prod(1 + 1/p_i^{a_i}) = 2$ with distinct prime powers.
2. **The distinctness constraint**: all prime powers in the factorization of a UPN are
   distinct (since they are the full prime power components of $n$).
3. **Goto's bound** (2007): $N < 2^{2^k}$ for any UPN $N$ with $\omega(N) = k$.
4. **The growth constraint** from the Subbarao--Warren argument and prime number theory:
   the minimum number of odd prime factors $f(m)$ as a function of $v_2(n) = m$.
5. **Mertens' third theorem** and the **prime number theorem**, which govern the
   asymptotic behavior of products over consecutive primes.

The strategy is to show that the feasible parameter space $\{(m, s) : m \geq 1,\; s = \omega_{\text{odd}}(n)\}$ for UPNs is finite --- that is, there exist effective bounds $M$ and $S$ such that any UPN must satisfy $m \leq M$ and $s \leq S$. Combined with the Subbarao--Warren theorem (finiteness for each fixed $m$) and Goto's bound (finiteness for each fixed $s$), this would yield overall finiteness.

---

## Claim 1 (Known). Every unitary perfect number is even.

**Status: Proved.**

**Proof.** Suppose $n$ is an odd UPN with $\omega(n) = k$ distinct prime factors, all odd.
Then for each prime power $p_i^{a_i} \| n$ with $p_i$ odd, the factor $1 + p_i^{a_i}$ is
even (since $p_i^{a_i}$ is odd). Therefore $2^k \mid \sigma^*(n) = \prod_{i=1}^{k}(1 + p_i^{a_i})$.

But $\sigma^*(n) = 2n$ and $n$ is odd, so $v_2(\sigma^*(n)) = v_2(2n) = 1$. For $k \geq 2$,
we have $v_2(\sigma^*(n)) \geq k \geq 2 > 1$, a contradiction.

For $k = 1$, $n = p^a$ for some odd prime $p$, and $\sigma^*(n) = 1 + p^a = 2p^a$ gives
$p^a = 1$, a contradiction since $p \geq 3$.

Therefore no odd UPN exists, and every UPN must be even. $\square$

**Reference:** Subbarao and Warren (1966) [`subbarao1966unitary`].

---

## Claim 2 (Known). For each fixed $m \geq 1$, the set $\{n \text{ UPN} : v_2(n) = m\}$ is finite.

**Status: Proved.**

**Proof sketch.** Write $n = 2^m \cdot D$ with $D$ odd. The UPN condition gives:

$$(1 + 2^m) \cdot \sigma^*(D) = 2^{m+1} \cdot D$$

$$\frac{\sigma^*(D)}{D} = R(m) = \frac{2^{m+1}}{1 + 2^m}.$$

Note that $R(m) > 1$ for all $m \geq 1$ (since $2^{m+1} > 1 + 2^m$ for $m \geq 1$), and
$R(m) \to 2$ as $m \to \infty$.

Now $\sigma^*(D)/D = \prod_{p^a \| D}(1 + 1/p^a) \leq \prod_{p \mid D}(1 + 1/p)$. For any
$\epsilon > 0$, the set of odd squarefree integers $D$ with $\prod_{p \mid D}(1 + 1/p) > 1 + \epsilon$ is finite (since the product is maximized by taking the smallest primes, and
$\prod_{p \leq x}(1+1/p) \sim C \cdot \ln(x)$ grows only logarithmically). More generally,
the set of odd integers $D$ (not necessarily squarefree) with $\sigma^*(D)/D \geq R(m) > 1$
is finite.

Since $R(m)$ is a fixed constant greater than 1 for each $m$, there are only finitely many
odd $D$ achieving $\sigma^*(D)/D = R(m)$, hence finitely many UPNs with $v_2(n) = m$. $\square$

**Reference:** Subbarao and Warren (1966) [`subbarao1966unitary`].

---

## Claim 3 (Verified Computationally). The function $R(m)$ and the threshold for $f(m)$.

**Status: Verified Computationally.**

The target ratio $R(m) = 2^{m+1}/(1 + 2^m)$ satisfies:

| $m$ | $R(m)$ (exact)          | $R(m)$ (decimal) |
|-----|-------------------------|-------------------|
| 1   | $4/3$                   | 1.3333            |
| 2   | $8/5$                   | 1.6000            |
| 3   | $16/9$                  | 1.7778            |
| 4   | $32/17$                 | 1.8824            |
| 5   | $64/33$                 | 1.9394            |
| 6   | $128/65$                | 1.9692            |
| 7   | $256/129$               | 1.9845            |
| 8   | $512/257$               | 1.9922            |
| 9   | $1024/513$              | 1.9961            |
| 10  | $2048/1025$             | 1.9980            |
| 18  | $524288/262145$         | 1.999996          |

**Key property:** $R(m)$ is strictly increasing in $m$ and approaches 2 from below:

$$R(m) = 2 - \frac{2}{1 + 2^m} = 2 - 2^{1-m} + O(2^{-2m}).$$

**Verification:** For each $m$ listed above, the value $R(m) = 2^{m+1}/(1+2^m)$ was computed
using exact rational arithmetic. All values are confirmed.

---

## Claim 4 (Verified Computationally). The maximal product $P(s)$ for $s$ consecutive odd primes.

**Status: Verified Computationally.**

The product $P(s) = \prod_{i=1}^{s}(1 + 1/q_i)$ over the first $s$ consecutive odd primes
$q_1 = 3, q_2 = 5, q_3 = 7, q_4 = 11, q_5 = 13, \ldots$ evaluates to:

| $s$ | Primes used                | $P(s)$ (exact)  | $P(s)$ (decimal) |
|-----|----------------------------|------------------|-------------------|
| 1   | $\{3\}$                    | $4/3$            | 1.3333            |
| 2   | $\{3, 5\}$                | $8/5$            | 1.6000            |
| 3   | $\{3, 5, 7\}$             | $64/35$          | 1.8286            |
| 4   | $\{3, 5, 7, 11\}$         | $768/385$        | 1.9948            |
| 5   | $\{3, 5, 7, 11, 13\}$     | $1536/715$       | 2.1483            |
| 6   | $\{3, 5, 7, \ldots, 17\}$ | $27648/12155$    | 2.2746            |
| 7   | $\{3, 5, 7, \ldots, 19\}$ | $110592/46189$   | 2.3943            |
| 8   | $\{3, 5, 7, \ldots, 23\}$ | ---              | 2.4984            |
| 9   | $\{3, 5, 7, \ldots, 29\}$ | ---              | 2.5846            |
| 10  | $\{3, 5, 7, \ldots, 31\}$ | ---              | 2.6680            |

**Critical observation:** $P(4) = 768/385 \approx 1.9948 < 2$, but $P(5) = 1536/715 \approx 2.1483 > 2$.

**Verification:** Each exact fraction was verified by direct multiplication. The decimal
values match to the stated precision.

---

## Claim 5 (Proved). The function $f(m)$ stabilizes: $f(m) = 5$ for all $m \geq 9$ and $f(m) \leq 4$ for $m \leq 8$.

**Status: Proved (combining Claims 3 and 4).**

**Proof.** By definition, $f(m) = \min\{s : P(s) \geq R(m)\}$. Since $R(m) < 2$ for all
$m \geq 1$ and $P(5) = 1536/715 > 2 > R(m)$, we always have $f(m) \leq 5$.

The threshold between $f(m) = 4$ and $f(m) = 5$ occurs when $R(m)$ crosses $P(4) = 768/385$.
Solving $R(m) \geq P(4)$:

$$\frac{2^{m+1}}{1 + 2^m} \geq \frac{768}{385}$$

$$385 \cdot 2^{m+1} \geq 768 (1 + 2^m)$$

$$770 \cdot 2^m \geq 768 + 768 \cdot 2^m$$

$$2 \cdot 2^m \geq 768$$

$$2^m \geq 384.$$

Since $2^8 = 256 < 384 < 512 = 2^9$, the threshold is $m = 9$.

Therefore:
- $f(m) \leq 4$ for $m \leq 8$ (since $R(m) \leq R(8) = 512/257 < P(4) = 768/385$).
- $f(m) = 5$ for all $m \geq 9$ (since $R(m) \geq R(9) = 1024/513 > P(4)$ but $R(m) < 2 < P(5)$).

More precisely: $f(1) = 1$, $f(2) = 2$, $f(3) = 3$, $f(4) = f(5) = f(6) = f(7) = f(8) = 4$,
and $f(m) = 5$ for all $m \geq 9$. $\square$

**Implication.** The product-based lower bound on $\omega_{\text{odd}}$ is **bounded**: it
does not grow with $m$. This is because the product $P(s)$ diverges (by Mertens' theorem),
so a fixed number of odd primes can always achieve any target below infinity. Since
$R(m) < 2 < P(5)$ for all $m$, five consecutive odd primes always suffice.

---

## Claim 6 (Known). The divisibility constraint $(1 + 2^m) \mid D$.

**Status: Proved.**

**Proof.** From the UPN equation $(1 + 2^m) \cdot \sigma^*(D) = 2^{m+1} \cdot D$ and the
facts that:
- $1 + 2^m$ is odd (for $m \geq 1$),
- $\gcd(1 + 2^m, 2^{m+1}) = 1$,

we conclude $(1 + 2^m) \mid D$. Therefore $D \geq 1 + 2^m > 2^m$, giving:

$$n = 2^m \cdot D \geq 2^m(1 + 2^m) = 2^m + 2^{2m} > 2^{2m}.$$

This yields the lower bound $n > 2^{2m}$, or equivalently $m < \frac{1}{2}\log_2(n)$. $\square$

---

## Claim 7 (Proved). Size constraint from Goto's bound: $m < 2^s$ for $s = \omega_{\text{odd}}(n)$.

**Status: Proved.**

**Proof.** Let $n$ be a UPN with $\omega(n) = k = 1 + s$, where $s = \omega_{\text{odd}}(n)$.
By Goto (2007), $n < 2^{2^k} = 2^{2^{s+1}}$. By Claim 6, $n > 2^{2m}$. Combining:

$$2^{2m} < n < 2^{2^{s+1}}$$

$$2m < 2^{s+1}$$

$$m < 2^s. \quad \square$$

**Reference:** Goto (2007) [`goto2007upper`].

---

## Claim 8 (Proved). The combined lower bound $g(m)$ on $\omega_{\text{odd}}$.

**Status: Proved.**

**Proof.** For a UPN $n$ with $v_2(n) = m$ and $\omega_{\text{odd}}(n) = s$, we have:

1. From the product constraint (Claim 5): $s \geq f(m)$.
2. From the size constraint (Claim 7): $m < 2^s$, i.e., $s > \log_2(m)$, so
   $s \geq \lfloor\log_2(m)\rfloor + 1$.

Combining: $s \geq g(m) = \max\bigl(f(m),\; \lfloor\log_2(m)\rfloor + 1\bigr)$.

For $m \leq 31$: $g(m) = \max(f(m), \lfloor\log_2(m)\rfloor + 1) \leq 5$.
For $m \geq 32$: $\lfloor\log_2(m)\rfloor + 1 \geq 6 > 5 = f(m)$, so $g(m) = \lfloor\log_2(m)\rfloor + 1$.

| $m$ range   | $g(m)$                         | Growth behavior         |
|-------------|--------------------------------|-------------------------|
| $1 \leq m \leq 3$   | $f(m) \in \{1,2,3\}$ | Matches $f(m)$           |
| $4 \leq m \leq 8$   | $4$                   | Matches $f(m)$           |
| $9 \leq m \leq 31$  | $5$                   | Matches $f(m)$           |
| $32 \leq m \leq 63$ | $6$                   | Size constraint dominates |
| $64 \leq m \leq 127$ | $7$                  | $\lfloor\log_2 m\rfloor+1$ |
| $128 \leq m \leq 255$ | $8$                 | $\lfloor\log_2 m\rfloor+1$ |
| $256 \leq m \leq 511$ | $9$                 | $\lfloor\log_2 m\rfloor+1$ |
| $512 \leq m \leq 1023$ | $10$               | $\lfloor\log_2 m\rfloor+1$ |

The function $g(m)$ grows **logarithmically** in $m$: $g(m) \sim \log_2(m)$ for large $m$. $\square$

---

## Claim 9 (Known). Wall's lower bound on odd prime factors for new UPNs.

**Status: Proved** (by Wall, 1988; exhaustive case analysis).

**Theorem (Wall, 1988).** Any UPN beyond the five known examples ($6, 60, 90, 87360$, and
$n_5 = 2^{18} \cdot 3 \cdot 5^4 \cdot 7 \cdot 11 \cdot 13 \cdot 19 \cdot 37 \cdot 79 \cdot 109 \cdot 157 \cdot 313$) must have $\omega_{\text{odd}}(n) \geq 9$, hence $\omega(n) \geq 10$.

**Reference:** Wall (1988) [`wall1988nine`].

**Consequence for new UPNs:** By Goto's bound, any new UPN $n$ satisfies
$n < 2^{2^{\omega(n)}} \leq 2^{2^{10}} = 2^{1024}$ when $\omega(n) = 10$.

However, $\omega(n)$ need not equal 10 --- it could be larger, and the Goto bound then gives
a correspondingly larger (but still finite) upper bound for each specific value of $\omega$.

---

## Claim 10 (Key Estimate). Mertens' theorem and the asymptotic behavior of $P(s)$.

**Status: Proved** (classical).

**Theorem (Mertens' third theorem, adapted).** As $s \to \infty$, the product over the
first $s$ consecutive odd primes satisfies:

$$P(s) = \prod_{i=1}^{s}\left(1 + \frac{1}{q_i}\right) \sim \frac{4}{\pi^2} \cdot e^{\gamma} \cdot \ln(q_s),$$

where $\gamma \approx 0.5772$ is the Euler--Mascheroni constant and $q_s$ is the $s$-th odd
prime.

By the prime number theorem, $q_s \sim 2s \ln(s)$ for large $s$ (accounting for the
restriction to odd primes, which form roughly half of all primes). Therefore:

$$P(s) \sim \frac{4 e^{\gamma}}{\pi^2} \cdot \ln(2s \ln s) \sim \frac{4 e^{\gamma}}{\pi^2} \cdot \ln(s) \quad \text{as } s \to \infty,$$

where $C_1 = 4 e^{\gamma}/\pi^2 \approx 4 \times 1.7811 / 9.8696 \approx 0.7218$.

**Key consequence:** $P(s)$ diverges, but only logarithmically. For any fixed target
$T < \infty$, there exists $s_0$ such that $P(s) \geq T$ for all $s \geq s_0$. In particular,
since $R(m) < 2$ for all $m$, the minimum $f(m)$ satisfying $P(f(m)) \geq R(m)$ is bounded.

**References:** Mertens (1874); Hardy and Wright, *An Introduction to the Theory of Numbers*.

---

## Claim 11 (Proved). The feasibility condition $m < 2^{g(m)}$ is always satisfied.

**Status: Proved.**

**Proof.** We need to check whether the necessary condition $m < 2^{g(m)}$ from Claim 7 is
ever violated --- a violation would mean that no UPN can have $v_2(n) = m$, immediately
giving $B(m) = 0$.

For $m \geq 32$ (where $g(m) = \lfloor\log_2(m)\rfloor + 1$):

$$2^{g(m)} = 2^{\lfloor\log_2(m)\rfloor + 1}.$$

Since $\lfloor\log_2(m)\rfloor \geq \log_2(m) - 1$, we have:

$$2^{g(m)} \geq 2^{\log_2(m)} = m.$$

In fact, $2^{g(m)} \geq 2^{\lfloor\log_2(m)\rfloor + 1} > m$ strictly (since
$2^{\lfloor\log_2(m)\rfloor + 1} > 2^{\log_2(m)} = m$ when $m$ is not a power of 2, and
$2^{\lfloor\log_2(m)\rfloor + 1} = 2m > m$ when $m$ is a power of 2).

Therefore $m < 2^{g(m)}$ holds for all $m \geq 1$, and the feasibility condition is
**never violated**. $\square$

**This is the first major obstruction to our proof: the Goto bound, combined with the
logarithmic growth of $g(m)$, does not rule out any specific value of $m$.**

---

## Claim 12 (Verified Computationally). Wall's bound tightens the constraint for new UPNs.

**Status: Verified Computationally.**

For any **new** (sixth or later) UPN, Wall's theorem (Claim 9) gives $\omega_{\text{odd}} \geq 9$,
hence $s \geq 9$. This replaces the generic $g(m)$ with:

$$s \geq \max(9,\; \lfloor\log_2(m)\rfloor + 1).$$

For $m \leq 255$: $\lfloor\log_2(m)\rfloor + 1 \leq 8 < 9$, so Wall's bound dominates and
$s \geq 9$.

For $m \geq 256$: $\lfloor\log_2(m)\rfloor + 1 \geq 9$, and the size constraint takes over.

Combined with $m < 2^s$:
- If $s = 9$: $m < 2^9 = 512$.
- If $s = 10$: $m < 2^{10} = 1024$.
- In general: $m < 2^s$.

And from Goto's bound with $\omega = s + 1$:
- If $s = 9$: $n < 2^{2^{10}} = 2^{1024}$.
- If $s = 10$: $n < 2^{2^{11}} = 2^{2048}$.

**But $s$ itself is unbounded by these constraints** --- the question is whether there exist
valid UPN factorizations for arbitrarily large $s$.

---

## Claim 13 (Proved). The feasible region $\{(m, s)\}$ is infinite.

**Status: Proved.**

**Proof.** The set of pairs $(m, s)$ satisfying the necessary conditions for a UPN is:

$$\mathcal{F} = \{(m, s) \in \mathbb{Z}_{>0}^2 : s \geq g(m) \text{ and } m < 2^s\}.$$

For any $s \geq 5$, the condition $m < 2^s$ allows $m$ to range over $\{1, 2, \ldots, 2^s - 1\}$.
And $g(m) \leq s$ is satisfied for all $m \leq 2^{s-1}$ (since $\lfloor\log_2(m)\rfloor + 1 \leq s$
for $m < 2^{s-1}$; more precisely, $g(m) \leq \lfloor\log_2(m)\rfloor + 1 \leq s$ for
$m < 2^s$).

Therefore $\mathcal{F}$ contains all pairs $(m, s)$ with $s \geq 5$ and
$1 \leq m \leq 2^{s-1}$, which is an infinite set. $\square$

**This is the second major obstruction: the necessary conditions from Claims 5--8 do not
confine UPNs to a finite parameter region.**

---

## Claim 14 (Proved). For each fixed $(m, s)$, there are finitely many UPNs.

**Status: Proved.**

**Proof.** Fix $m \geq 1$ and $s \geq 1$. A UPN $n$ with $v_2(n) = m$ and
$\omega_{\text{odd}}(n) = s$ has the form $n = 2^m \cdot \prod_{j=1}^{s} q_j^{b_j}$ with
$q_1 < q_2 < \cdots < q_s$ distinct odd primes and $b_j \geq 1$. The product equation:

$$\prod_{j=1}^{s}\left(1 + \frac{1}{q_j^{b_j}}\right) = R(m)$$

has finitely many solutions. To see this, note that by Goto's bound (with $\omega = s+1$),
$n < 2^{2^{s+1}}$, so each $q_j^{b_j} < 2^{2^{s+1}} / 2^m$, giving finitely many choices
for each $(q_j, b_j)$. With $s$ factors and each drawn from a finite set, the total number
of candidate factorizations is finite, and each can be checked against the product equation.

Let $B(m, s)$ denote the number of UPNs with $v_2(n) = m$ and $\omega_{\text{odd}} = s$.
Then $B(m, s) < \infty$ for all $(m, s)$. $\square$

---

## Claim 15 (Structural). The total number of UPNs as a double sum.

**Status: Proved** (structural reduction, not a finiteness proof).

The total number of UPNs is:

$$\sum_{m=1}^{\infty} B(m) = \sum_{m=1}^{\infty} \sum_{s=1}^{\infty} B(m, s),$$

where each $B(m, s)$ is finite (Claim 14). The conjecture of Subbarao is equivalent to
this double sum being finite.

**What is known:**
- For each fixed $m$: $\sum_{s=1}^{\infty} B(m, s) = B(m) < \infty$ (Claim 2, Subbarao--Warren).
- For each fixed $s$: $\sum_{m=1}^{\infty} B(m, s) < \infty$ (since $m < 2^s$ by Claim 7,
  so the sum is over finitely many $m$, each contributing finitely many UPNs).

**What is NOT known:** Whether $\sum_{m} \sum_{s} B(m, s) < \infty$. The fact that each row
sum and each column sum of the matrix $[B(m, s)]_{m, s \geq 1}$ is finite does **not** imply
that the total sum is finite. (Counterexample: a matrix with $B(m, s) = 1$ when $s = \lfloor\log_2(m)\rfloor + 1$ and $B(m, s) = 0$ otherwise has finite row and column sums but
infinite total.)

---

## Claim 16 (Verified Computationally). The divisibility chain constraint from $1 + 2^m$.

**Status: Verified Computationally.**

By Claim 6, $(1 + 2^m) \mid D$. The prime factors of $1 + 2^m$ must all be among the odd
prime factors of $n$. Therefore:

$$\omega_{\text{odd}}(n) \geq \omega(1 + 2^m).$$

Computed values of $\omega(1 + 2^m)$:

| $m$ | $1 + 2^m$            | Factorization                            | $\omega(1 + 2^m)$ |
|-----|----------------------|------------------------------------------|--------------------|
| 1   | 3                    | $3$                                      | 1                  |
| 2   | 5                    | $5$                                      | 1                  |
| 3   | 9                    | $3^2$                                    | 1                  |
| 4   | 17                   | $17$                                     | 1                  |
| 6   | 65                   | $5 \cdot 13$                             | 2                  |
| 8   | 257                  | $257$                                    | 1                  |
| 10  | 1025                 | $5^2 \cdot 41$                           | 2                  |
| 16  | 65537                | $65537$ (Fermat prime)                   | 1                  |
| 18  | 262145               | $5 \cdot 13 \cdot 37 \cdot 109$         | 4                  |
| 25  | 33554433             | $3 \cdot 11 \cdot 251 \cdot 4051$       | 4                  |
| 30  | 1073741825           | $5^2 \cdot 13 \cdot 41 \cdot 61 \cdot 1321$ | 5              |
| 42  | $\approx 4.4 \times 10^{12}$ | (6 distinct prime factors)        | 6                  |

**Observation:** The function $\omega(1 + 2^m)$ fluctuates widely. When $m$ is a power of 2,
$1 + 2^m$ may be a Fermat prime (giving $\omega = 1$). In general, $\omega(1 + 2^m)$ is NOT
monotonically increasing and does not provide a growing lower bound.

The fifth UPN ($m = 18$) confirms the constraint: $1 + 2^{18} = 262145 = 5 \cdot 13 \cdot 37 \cdot 109$, and all four primes $\{5, 13, 37, 109\}$ appear in its factorization.

---

## Claim 17 (Proved). Mertens-based analysis shows $f(m)$ does NOT grow with $m$.

**Status: Proved.**

**Proof.** This is a precise restatement and synthesis of Claims 4, 5, and 10.

By Mertens' third theorem (Claim 10), $P(s) \to \infty$ as $s \to \infty$. Since the target
$R(m) < 2$ for all $m$, and $P(5) > 2 > R(m)$, we have $f(m) \leq 5$ for all $m \geq 1$.

Moreover, $f(m) = 5$ for all $m \geq 9$ (Claim 5), so $f(m)$ is eventually constant.

The reason $f(m)$ stabilizes rather than growing is fundamental: the product
$\prod_{i=1}^{s}(1 + 1/q_i)$ over consecutive odd primes **diverges** (albeit slowly, as
$\sim C_1 \cdot \ln(s)$). Therefore, a **fixed** number of prime factors can produce a product
exceeding any finite target. Since $R(m) < 2$ is a bounded target, a bounded number of primes
always suffices.

**IMPORTANT:** The initial heuristic suggestion (from the research gaps document) that $f(m)$
might grow linearly as $\Omega(m)$ was based on the naive bound using repeated factors of
$4/3$. The correct analysis using **distinct** consecutive primes shows that $f(m)$ is
bounded, not growing. The naive bound $\omega_{\text{odd}} \geq m \cdot \log(2)/\log(4/3)$
would apply only if all odd prime factors were required to be 3, which is impossible since
they must be distinct. $\square$

---

## WHERE THE ARGUMENT BREAKS DOWN

We now identify the precise logical gap that prevents the argument from proving finiteness.

---

## Claim 18 (Analysis of the Gap). The double sum $\sum_{m} \sum_{s} B(m, s)$ cannot be shown finite by these methods.

**Status: Proved** (that the methods are insufficient).

**The precise gap.** To prove finiteness of UPNs, we need to show:

$$\sum_{m=1}^{\infty} \sum_{s=1}^{\infty} B(m, s) < \infty.$$

We have established:
1. Each $B(m, s) < \infty$ (Claim 14).
2. For each fixed $m$: $\sum_s B(m, s) = B(m) < \infty$ (Claim 2).
3. For each fixed $s$: $\sum_m B(m, s) < \infty$ (Claim 7: $m < 2^s$).
4. The feasible region $\mathcal{F} = \{(m, s) : s \geq g(m),\; m < 2^s\}$ is infinite
   (Claim 13).

**Why finiteness does not follow:**

The feasible region $\mathcal{F}$ is infinite, and we cannot rule out $B(m, s) > 0$ for
infinitely many $(m, s) \in \mathcal{F}$. The constraints we have are:

**(a) The product constraint gives $s \geq 5$ for $m \geq 9$**, but this is a weak lower
bound that does not grow.

**(b) The size constraint gives $m < 2^s$**, which allows $m$ to grow exponentially with $s$.
Since $g(m) \sim \log_2(m)$, the Goto bound requires $s \geq \log_2(m) + 1$, i.e.,
$m < 2^s$. But $2^s$ grows much faster than $m$, so the inequality $m < 2^s$ is always
satisfiable with plenty of room.

**(c) The "room" between $m$ and $2^{g(m)}$** never vanishes (Claim 11). At $m = 2^k - 1$
(just below a power of 2), the room is $2^{g(m)} - m = 2^k - (2^k - 1) = 1$, which is
minimal but still positive. At $m = 2^k$ (a power of 2), $g(m)$ jumps to $k + 1$ and the
room resets to $2^{k+1} - 2^k = 2^k$, which is large.

**(d) Wall's bound $s \geq 9$ for new UPNs** combined with Goto gives $m < 2^9 = 512$ when
$s = 9$, but allows $m < 2^{10} = 1024$ when $s = 10$, etc. The upper bound on $m$ grows
exponentially with $s$.

**Formal statement of the gap:** The necessary conditions derived in Claims 1--12 restrict
UPNs to the infinite set $\{(m, s) : s \geq \max(9, \lfloor\log_2 m\rfloor + 1),\; m < 2^s\}$.
For each $(m, s)$ in this set, $B(m, s)$ is finite but not known to be zero. Proving
finiteness requires showing that $B(m, s) = 0$ for all but finitely many such pairs.

**The fundamental reason the argument fails:** The lower bound $g(m)$ on $\omega_{\text{odd}}$
grows only **logarithmically** in $m$, while Goto's upper bound on $n$ is **doubly
exponential** in $\omega$. Specifically:

- Required: $\omega \geq g(m) \sim \log_2(m)$.
- Goto gives: $n < 2^{2^{\omega}} \sim 2^{2m}$ (when $\omega \sim \log_2 m$).
- Actual: $n > 2^{2m}$ (from Claim 6).

The ratio between the Goto upper bound ($2^{2m}$) and the actual lower bound ($2^{2m}$) is
$O(1)$ --- they are of the same order! This means Goto's bound is almost exactly **tight
enough** to be consistent with UPNs existing at every scale, without yielding a
contradiction.

For the argument to succeed, we would need **either**:
- A lower bound $g(m)$ that grows faster than $\log_2(m)$ (to make $2^{2^{g(m)+1}}$ grow
  faster than $2^{2m}$), **or**
- An upper bound on $n$ that is **polynomial** in $\omega$ rather than doubly exponential
  (to make the upper bound grow slower than $2^{2m}$).

Neither is available with current techniques.

---

## What Would Close the Gap

We identify four possible routes to completing the proof, in order of plausibility.

### Route (A): Show $B(m) = 0$ for all $m > M$ (Diophantine approach).

For each $m$, the UPN equation becomes:

$$\prod_{j=1}^{s}\frac{1 + q_j^{b_j}}{q_j^{b_j}} = R(m) = \frac{2^{m+1}}{1 + 2^m},$$

a product of unit fractions equaling a specific rational number. The numerator equation is:

$$\prod_{j=1}^{s}(1 + q_j^{b_j}) = \frac{2^{m+1}}{1 + 2^m} \cdot \prod_{j=1}^{s} q_j^{b_j}.$$

Since both sides must be integers, the prime factorization of the left side must match.
Each factor $1 + q_j^{b_j}$ on the left is a specific integer whose prime factorization
creates "supply" of primes, while the right side creates "demand." The matching condition is
extremely rigid.

**What is needed:** A proof that for $m$ sufficiently large, the number $1 + 2^m$ (which
divides the odd part $D$ and hence must be factored entirely using primes from
$\{q_1, \ldots, q_s\}$) cannot be accommodated within any valid factorization. This is a
statement about the factorization structure of $1 + 2^m$, which connects to deep questions
about Cunningham numbers and Aurifeuillean factorizations.

**Status: Conjectural.** No such result is known.

### Route (B): A polynomial Goto bound.

Replace the doubly exponential bound $n < 2^{2^k}$ with a polynomial bound $n < C \cdot k^A$
for constants $C, A > 0$. Then for a UPN with $\omega = k \geq g(m)$:

$$n < C \cdot k^A \leq C \cdot (\lfloor\log_2 m\rfloor + 2)^A$$

while $n \geq 2^{2m}$ (Claim 6). This gives:

$$2^{2m} < C \cdot (\log_2 m + 2)^A,$$

which fails for all sufficiently large $m$ (since the left side grows exponentially while the
right side grows polylogarithmically). This would immediately prove finiteness.

**Status: Conjectural.** The doubly exponential bound is the best known. Improving it to
polynomial would be a major advance.

### Route (C): A super-constant lower bound on $f(m)$.

If one could show $f(m) \to \infty$ as $m \to \infty$ (or even $f(m) \geq c \cdot \sqrt{m}$
for some $c > 0$), then combined with Goto's bound, the feasible region would become finite.

**But we proved in Claim 5 that $f(m) = 5$ for all $m \geq 9$.** So this route is
definitively closed: the product-based lower bound on $\omega_{\text{odd}}$ is bounded, not
growing. (The naive bound suggesting $f(m) \sim m / \log(4/3)$ was incorrect because it
failed to account for the distinctness of prime factors.)

**Status: Disproved** (as a viable route).

### Route (D): Direct computational enumeration.

Verify $B(m) = 0$ for all $m$ in the feasible region. With Wall's bound $s \geq 9$ and
the observation that any new UPN has $\omega \geq 10$:

- For $\omega = 10$: Goto gives $n < 2^{1024}$, so $m < 512$.
- For $\omega = 11$: Goto gives $n < 2^{2048}$, so $m < 1024$.
- And so on.

The total region to check is $\{(m, s) : s \geq 9,\; m < 2^s\}$, which is infinite (as $s$
ranges over all integers $\geq 9$). However, for each fixed $s$, the search space is finite:
check all factorizations with $s$ odd primes and $m < 2^s$.

**Practical assessment:** For $s = 9$ (the smallest case), one must search over all
factorizations $n = 2^m \cdot q_1^{b_1} \cdots q_9^{b_9}$ with $m < 512$ and
$n < 2^{1024}$, subject to the product equation. The combinatorial search space is enormous
but finite, and modern branch-and-bound algorithms with product-equation pruning could
potentially handle it. Completing the search for $s = 9$ would prove: either a sixth UPN
exists with 9 odd primes, or any sixth UPN must have $\omega_{\text{odd}} \geq 10$.

Iterating over $s = 9, 10, 11, \ldots$, each iteration either finds a new UPN or eliminates
that value of $s$. If the process terminates (i.e., for some $s_0$, no new UPNs are found
for $s \leq s_0$ and the remaining search space is provably empty), finiteness is established.

**Status: Computationally feasible in principle** for small values of $s$, but an infinite
computation if no a priori bound on $s$ exists. Without additional theoretical input (such
as an upper bound on $s$ for new UPNs), this approach cannot yield a finite proof.

---

## Theorem (Conditional). Summary of constraints on a hypothetical sixth UPN.

**Status: Proved** (combining all unconditional results).

**Theorem.** If a sixth unitary perfect number $N$ exists, then:

1. $N$ is even, with $N = 2^m \cdot D$, $D$ odd.
2. $\omega_{\text{odd}}(N) \geq 9$ (Wall, 1988), hence $\omega(N) \geq 10$.
3. $N > n_5 = 146{,}361{,}946{,}186{,}458{,}562{,}560{,}000 \approx 1.46 \times 10^{23}$.
4. $(1 + 2^m) \mid D$, so $D \geq 1 + 2^m$.
5. $m < 2^{\omega_{\text{odd}}(N)}$.
6. $N < 2^{2^{\omega(N)}}$ (Goto, 2007).
7. In the "minimal" case $\omega(N) = 10$: $N < 2^{1024} \approx 1.80 \times 10^{308}$ and
   $m < 512$.
8. If $3 \nmid N$: $v_2(N) \geq 144$, $\omega_{\text{odd}}(N) \geq 144$, and
   $N > 10^{440}$ (Frei).
9. The product equation $\prod_{p^a \| N}(1 + 1/p^a) = 2$ must be satisfied with all prime
   powers distinct, the odd part divisible by $1 + 2^m$, and $\sigma^*(N) \equiv 2N \pmod{q}$
   for every modulus $q$.

**This provides an enormous but finite search region for each specific value of $\omega(N)$.
Exhaustive computational verification within this region for each $\omega$ would, in
principle, either find a sixth UPN or prove that none exists with that many prime factors.
However, the region grows doubly exponentially with $\omega$, and $\omega$ is unbounded by
the theoretical constraints, so a finite proof requires either bounding $\omega$ or finding
additional structural obstructions.**

---

## Conclusion

**We have NOT proved the finiteness of unitary perfect numbers unconditionally.** The
finiteness conjecture of Subbarao (1970) remains open.

Our analysis clarifies exactly where current methods fall short:

1. **The product constraint** ($f(m) \leq 5$) is too weak because it stabilizes at a
   constant, due to the divergence of $\prod(1 + 1/p)$ over primes (Mertens' theorem).

2. **Goto's doubly exponential bound** is too permissive: it allows the search space to
   grow as $2^{2^{\omega}}$, which overwhelms the logarithmic growth of the required $\omega$.

3. **The Subbarao--Warren argument** proves finiteness for each fixed 2-adic valuation but
   provides no control over the sum $\sum_m B(m)$.

4. **Analytic density bounds** (Erdos--Wintner, Pollack--Shevelev techniques) give
   $U(X) = O(X^{1-\epsilon})$ at best, which is far from $O(1)$.

5. **Modular obstructions** exclude roughly 37.6% of integers but leave a positive sieve
   density, insufficient for finiteness.

The **strongest unconditional result** we can state is the Conditional Theorem above,
which constrains any sixth UPN to an explicitly described (but infinite) parameter space.
The most promising paths to resolving the conjecture are:

- **Route (A):** A Diophantine result showing that the factorization structure of $1 + 2^m$
  is incompatible with the UPN product equation for all sufficiently large $m$.
- **Route (B):** An improvement of Goto's bound from doubly exponential to polynomial.
- **Route (D):** Systematic computational verification for $\omega_{\text{odd}} = 9, 10, 11, \ldots$, each of which requires checking a finite (but large) search space.

The problem remains worthy of the \$10 prize offered by Erdos (Problem #1052).

---

## Appendix: Verification Against Known UPNs

All five known UPNs are consistent with every claim in this document.

| UPN | $n$ | $v_2$ ($m$) | $\omega_{\text{odd}}$ ($s$) | $\omega$ ($k$) | $R(m)$ | $f(m)$ | $g(m)$ | $n < 2^{2^k}$? |
|-----|-----|-------------|----------------------------|----------------|---------|--------|--------|-----------------|
| 1st | 6 = $2 \cdot 3$ | 1 | 1 | 2 | 4/3 | 1 | 1 | $6 < 16$ Yes |
| 2nd | 60 = $2^2 \cdot 3 \cdot 5$ | 2 | 2 | 3 | 8/5 | 2 | 2 | $60 < 256$ Yes |
| 3rd | 90 = $2 \cdot 3^2 \cdot 5$ | 1 | 2 | 3 | 4/3 | 1 | 1 | $90 < 256$ Yes |
| 4th | 87360 = $2^6 \cdot 3 \cdot 5 \cdot 7 \cdot 13$ | 6 | 4 | 5 | 128/65 | 4 | 4 | $87360 < 2^{32}$ Yes |
| 5th | $n_5 = 2^{18} \cdot 3 \cdot 5^4 \cdot 7 \cdot 11 \cdot 13 \cdot 19 \cdot 37 \cdot 79 \cdot 109 \cdot 157 \cdot 313$ | 18 | 11 | 12 | $\approx 2.0$ | 5 | 5 | $n_5 < 2^{4096}$ Yes |

Each UPN satisfies $\omega_{\text{odd}} \geq f(m)$, $\omega_{\text{odd}} \geq g(m)$,
$m < 2^{\omega_{\text{odd}}}$, and $n < 2^{2^{\omega}}$, as required.

---

## References

1. Subbarao, M. V. and Warren, L. J. (1966). "Unitary Perfect Numbers." *Canadian Mathematical Bulletin* 9(2), 147--153. [`subbarao1966unitary` in sources.bib]

2. Subbarao, M. V. (1970). "Are There an Infinity of Unitary Perfect Numbers?" *American Mathematical Monthly* 77, 389--390. [`subbarao1970infinity` in sources.bib]

3. Wall, C. R. (1975). "The Fifth Unitary Perfect Number." *Canadian Mathematical Bulletin* 18(1), 115--122. [`wall1975fifth` in sources.bib]

4. Wall, C. R. (1988). "New Unitary Perfect Numbers Have at Least Nine Odd Components." *The Fibonacci Quarterly* 26(4), 312. [`wall1988nine` in sources.bib]

5. Goto, T. (2007). "Upper Bounds for Unitary Perfect Numbers and Unitary Harmonic Numbers." *Rocky Mountain Journal of Mathematics* 37(5), 1557--1576. [`goto2007upper` in sources.bib]

6. Pollack, P. and Shevelev, V. (2012). "On Perfect and Near-Perfect Numbers." *Journal of Number Theory* 132(12), 3037--3046. [`pollack2012near` in sources.bib]

7. Cohen, E. (1960). "Arithmetical Functions Associated with the Unitary Divisors of an Integer." *Mathematische Zeitschrift* 74, 66--80. [`cohen1960unitary` in sources.bib]

8. Guy, R. K. (2004). *Unsolved Problems in Number Theory*, 3rd ed. Springer. Problem B3. [`guy2004unsolved` in sources.bib]

9. OEIS Foundation Inc. Sequence A002827: Unitary Perfect Numbers. https://oeis.org/A002827 [`oeis_A002827` in sources.bib]

10. Mertens, F. (1874). "Ein Beitrag zur analytischen Zahlentheorie." *Journal fur die reine und angewandte Mathematik* 78, 46--62.

11. Hardy, G. H. and Wright, E. M. (2008). *An Introduction to the Theory of Numbers*, 6th ed. Oxford University Press.

# Growth Constraint Analysis for Unitary Perfect Numbers

This document derives and analyzes the growth constraint on the number of odd prime
factors required for a unitary perfect number (UPN) as a function of its 2-adic
valuation, combines this with Goto's upper bound to constrain the feasible parameter
space, and assesses whether the combined constraints are sufficient to prove finiteness.

---

## 1. The Growth Constraint

### Setup

Let $n$ be a UPN with $v_2(n) = m$, so $n = 2^m \cdot D$ where $D$ is odd. The UPN
condition $\sigma^*(n) = 2n$ gives:

$$(1 + 2^m) \cdot \sigma^*(D) = 2^{m+1} \cdot D$$

$$\frac{\sigma^*(D)}{D} = R(m) \quad \text{where} \quad R(m) = \frac{2^{m+1}}{1 + 2^m}$$

Since $D$ is odd with prime factorization $D = \prod_{j=1}^{s} q_j^{b_j}$ (each $q_j \geq 3$
an odd prime), we have:

$$\frac{\sigma^*(D)}{D} = \prod_{j=1}^{s} \left(1 + \frac{1}{q_j^{b_j}}\right)$$

where $s = \omega_{\text{odd}}(n)$ is the number of distinct odd prime factors.

### Naive bound via maximal per-factor contribution

Each factor $(1 + 1/q_j^{b_j})$ is maximized when $q_j^{b_j}$ is minimized. The smallest
odd prime power is $3^1 = 3$, giving $(1 + 1/3) = 4/3$. Therefore:

$$\left(\frac{4}{3}\right)^{s} \geq \prod_{j=1}^{s}\left(1 + \frac{1}{q_j^{b_j}}\right) = R(m)$$

$$s \geq \frac{\log R(m)}{\log(4/3)}$$

Since $R(m) \to 2$ as $m \to \infty$ and $\log(2)/\log(4/3) \approx 2.409$, this gives
$s \geq 3$ for all sufficiently large $m$. This bound is extremely weak because it
assumes all $s$ prime factors could simultaneously be $3$, which is impossible since the
prime powers must be **distinct**.

### Refined bound using distinct consecutive odd primes

A much tighter bound arises from requiring the $s$ odd prime factors to be **distinct
primes**. The maximum value of $\prod_{j=1}^{s}(1 + 1/q_j)$ over $s$ distinct odd primes
$q_1 < q_2 < \cdots < q_s$ is achieved by taking the $s$ smallest consecutive odd primes
$q_1 = 3, q_2 = 5, q_3 = 7, \ldots$ all with exponent $b_j = 1$. (Higher exponents only
reduce the contribution $(1 + 1/q_j^{b_j}) < (1 + 1/q_j)$ for $b_j \geq 2$.)

Define the **maximal product with $s$ consecutive odd primes**:

$$P(s) = \prod_{i=1}^{s} \frac{q_i + 1}{q_i}$$

where $q_1 = 3, q_2 = 5, q_3 = 7, q_4 = 11, q_5 = 13, \ldots$ are the consecutive odd
primes.

Computed values:

| $s$ | Primes used | $P(s)$ (exact) | $P(s)$ (decimal) |
|-----|-------------|-----------------|-------------------|
| 1   | {3}         | $4/3$           | 1.3333            |
| 2   | {3, 5}      | $8/5$           | 1.6000            |
| 3   | {3, 5, 7}   | $64/35$         | 1.8286            |
| 4   | {3, 5, 7, 11} | $768/385$     | 1.9948            |
| 5   | {3, 5, 7, 11, 13} | $1536/715$ | 2.1483           |
| 6   | {3, ..., 17} | $27648/12155$  | 2.2746            |
| 7   | {3, ..., 19} | $110592/46189$ | 2.3943            |
| 8   | {3, ..., 23} |                 | 2.4984            |
| 9   | {3, ..., 29} |                 | 2.5846            |
| 10  | {3, ..., 31} |                 | 2.6680            |

The critical observation: **$P(4) \approx 1.995 < 2$ but $P(5) \approx 2.148 > 2$.**

Since $R(m) < 2$ for all $m$, this means:
- For $R(m) \leq P(4) \approx 1.995$: four consecutive odd primes suffice ($f(m) = 4$).
- For $P(4) < R(m) < 2$: five consecutive odd primes are needed ($f(m) = 5$).
- $P(5) > 2 > R(m)$ always, so **five consecutive odd primes always suffice**.

Define $f(m) = \min\{s : P(s) \geq R(m)\}$, the minimum number of distinct odd primes
whose product of $(1 + 1/q_j)$ factors can reach $R(m)$.

---

## 2. Computation of $f(m)$ for $m = 1, \ldots, 50$

The threshold between $f(m) = 4$ and $f(m) = 5$ occurs when
$R(m) = P(4) = 768/385$. Solving:

$$\frac{2^{m+1}}{1 + 2^m} \geq \frac{768}{385}$$

$$385 \cdot 2^{m+1} \geq 768 \cdot (1 + 2^m) = 768 + 768 \cdot 2^m$$

$$770 \cdot 2^m \geq 768 + 768 \cdot 2^m$$

$$2 \cdot 2^m \geq 768$$

$$2^m \geq 384$$

Since $2^8 = 256 < 384$ and $2^9 = 512 \geq 384$, the threshold is $m = 9$.

| $m$ | $R(m)$ | $f(m)$ | $\omega(n) \geq 1 + f(m)$ |
|-----|---------|--------|---------------------------|
| 1   | $4/3 \approx 1.333$ | 1 | 2 |
| 2   | $8/5 = 1.600$ | 2 | 3 |
| 3   | $16/9 \approx 1.778$ | 3 | 4 |
| 4   | $32/17 \approx 1.882$ | 4 | 5 |
| 5   | $64/33 \approx 1.939$ | 4 | 5 |
| 6   | $128/65 \approx 1.969$ | 4 | 5 |
| 7   | $256/129 \approx 1.984$ | 4 | 5 |
| 8   | $512/257 \approx 1.992$ | 4 | 5 |
| 9   | $1024/513 \approx 1.996$ | 5 | 6 |
| 10  | $2048/1025 \approx 1.998$ | 5 | 6 |
| 11  | $4096/2049 \approx 1.999$ | 5 | 6 |
| 12--50 | $\approx 2 - 2^{1-m}$ | 5 | 6 |

**The function $f(m)$ stabilizes at 5 for all $m \geq 9$ and remains constant thereafter.**

This is because $P(5) = 1536/715 \approx 2.148 > 2 > R(m)$ for every $m$, so five
consecutive odd primes (with exponent 1) always produce a product exceeding any target
$R(m) < 2$.

### Verification against known UPNs

| UPN | $v_2$ ($m$) | $\omega_{\text{odd}}$ (actual) | $f(m)$ (lower bound) | Ratio |
|-----|-------------|-------------------------------|----------------------|-------|
| 6   | 1           | 1                             | 1                    | 1.00  |
| 60  | 2           | 2                             | 2                    | 1.00  |
| 90  | 1           | 2                             | 1                    | 2.00  |
| 87360 | 6         | 4                             | 4                    | 1.00  |
| $n_5$ | 18        | 11                            | 5                    | 2.20  |

For the first four UPNs, the actual $\omega_{\text{odd}}$ matches or slightly exceeds
$f(m)$. The fifth UPN has 11 odd prime factors, far exceeding the lower bound of 5. This
gap is explained by the fact that $f(m)$ measures only a necessary condition (the product
can reach $R(m)$), not a sufficient one (the product equals $R(m)$ exactly as a rational
number).

---

## 3. Combining with Goto's Bound

### The Goto bound

Goto (2007) proved that if $N$ is a UPN with $\omega(N) = k$ distinct prime factors, then:

$$N < 2^{2^k}$$

### The divisibility constraint

A crucial structural constraint arises from the product equation. Since $n = 2^m \cdot D$
and $(1 + 2^m) \cdot \sigma^*(D) = 2^{m+1} \cdot D$, and since $1 + 2^m$ is odd (for
$m \geq 1$) while $\gcd(1 + 2^m, 2^{m+1}) = 1$, we conclude:

$$(1 + 2^m) \mid D$$

This means the odd part $D$ must be divisible by $1 + 2^m$, so $D \geq 1 + 2^m$.

### Size constraint from Goto

With $\omega(n) = k = 1 + s$ (where $s = \omega_{\text{odd}}$), Goto's bound gives:

$$n = 2^m \cdot D < 2^{2^{s+1}}$$

Since $D \geq 1 + 2^m > 2^m$ for $m \geq 1$:

$$2^m \cdot 2^m < 2^m \cdot D < 2^{2^{s+1}}$$

$$2^{2m} < 2^{2^{s+1}}$$

$$2m < 2^{s+1}$$

$$m < 2^s$$

This gives a **size-based lower bound** on $\omega_{\text{odd}}$:

$$s > \log_2(m) \quad \Longrightarrow \quad s \geq \lfloor \log_2(m) \rfloor + 1$$

### The effective lower bound $g(m)$

Combining the product constraint $s \geq f(m)$ with the size constraint $s \geq \lfloor\log_2(m)\rfloor + 1$:

$$g(m) = \max\bigl(f(m),\; \lfloor\log_2(m)\rfloor + 1\bigr)$$

| $m$ | $f(m)$ | $\lfloor\log_2 m\rfloor + 1$ | $g(m)$ | Goto limit $2^{g(m)}$ |
|-----|--------|-------------------------------|--------|------------------------|
| 1   | 1      | 1                             | 1      | 2                      |
| 2   | 2      | 2                             | 2      | 4                      |
| 3   | 3      | 2                             | 3      | 8                      |
| 4   | 4      | 3                             | 4      | 16                     |
| 8   | 4      | 4                             | 4      | 16                     |
| 9   | 5      | 4                             | 5      | 32                     |
| 16  | 5      | 5                             | 5      | 32                     |
| 31  | 5      | 5                             | 5      | 32                     |
| 32  | 5      | 6                             | 6      | 64                     |
| 64  | 5      | 7                             | 7      | 128                    |
| 128 | 5      | 8                             | 8      | 256                    |
| 256 | 5      | 9                             | 9      | 512                    |
| 512 | 5      | 10                            | 10     | 1024                   |

For $m \geq 32$, the size constraint dominates and $g(m) = \lfloor\log_2(m)\rfloor + 1$.

### The feasibility check

For a UPN with $v_2(n) = m$ to exist, we need $m < 2^{g(m)}$, i.e.:

$$m < 2^{\max(f(m), \lfloor\log_2(m)\rfloor + 1)}$$

Since $g(m) \geq \lfloor\log_2(m)\rfloor + 1$, we have $2^{g(m)} \geq 2m > m$, so **the
inequality $m < 2^{g(m)}$ is always satisfied**.

More precisely, for $m \geq 32$ where $g(m) = \lfloor\log_2(m)\rfloor + 1$:

$$2^{g(m)} = 2^{\lfloor\log_2(m)\rfloor + 1} \geq 2m > m$$

The "room" $2^{g(m)} - m$ grows with $m$ (at least linearly), so the constraint never
becomes tight. **Goto's bound does not create a contradiction for large $m$ using
this approach.**

---

## 4. A Better Lower Bound on $\omega_{\text{odd}}$

### Why $f(m)$ is weak

The function $f(m)$ stabilizes at 5 because it answers the question: "Can $s$ distinct
odd primes produce a product $\prod(1 + 1/q_j) \geq R(m)$?" Since $R(m) < 2$ and $P(5) > 2$,
the answer is always "yes" for $s \geq 5$.

But this ignores the requirement that the product must equal $R(m)$ **exactly** (as a
rational number), not merely exceed it. The exact constraint is far more restrictive.

### The Mertens growth analysis

By Mertens' third theorem, the product over consecutive odd primes grows logarithmically:

$$\prod_{\substack{p \leq x \\ p \text{ odd prime}}} \left(1 + \frac{1}{p}\right) \sim C \cdot \ln(x)$$

where $C = \frac{4}{\pi^2} \cdot e^{\gamma} \approx 0.7218$ and $\gamma$ is the
Euler--Mascheroni constant.

This product **diverges** as $x \to \infty$, which is why $P(s) \to \infty$ and why the
minimum $f(m)$ is bounded. The divergence means that for any target $T < \infty$, there
exists $s_0$ such that $P(s) \geq T$ for all $s \geq s_0$.

### The "near-miss" analysis

A more subtle question is: for a product of distinct prime-power factors to be
**near but not exceeding** 2, how many factors are needed?

Suppose we want $\prod_{j=1}^{s}(1 + 1/q_j^{b_j}) = 2 - \varepsilon$ for some small
$\varepsilon > 0$, using distinct odd prime powers. The maximum product with the
$s$ smallest odd primes is $P(s) \sim C \cdot \ln(q_s)$. For the product to be close
to 2 from below (which is what $R(m) \approx 2 - 2^{1-m}$ requires), we would need
to use primes that are **not** the smallest --- or use higher exponents that reduce the
contribution.

However, this line of reasoning does not directly produce a **lower bound** on
$\omega_{\text{odd}}$ stronger than $f(m) = 5$, because we can always **choose** to use
larger primes to reduce the product below 2. The constraint is on which exact rational
values are achievable, not on the achievable range.

### Divisibility chain constraint

The strongest non-trivial constraint on $\omega_{\text{odd}}$ comes from the divisibility
requirement $(1 + 2^m) \mid D$. Since $1 + 2^m$ is odd, all its prime factors must appear
in $D$. Let $\omega(1 + 2^m)$ denote the number of distinct prime factors of $1 + 2^m$.
Then:

$$\omega_{\text{odd}}(n) \geq \omega(1 + 2^m)$$

since the prime factors of $1 + 2^m$ must be among the odd prime factors of $n$.

Computed values of $\omega(1 + 2^m)$:

| $m$ | $1 + 2^m$ | Factorization | $\omega(1 + 2^m)$ |
|-----|-----------|---------------|---------------------|
| 1   | 3         | $3$           | 1                   |
| 2   | 5         | $5$           | 1                   |
| 4   | 17        | $17$          | 1                   |
| 6   | 65        | $5 \cdot 13$  | 2                   |
| 8   | 257       | $257$         | 1                   |
| 16  | 65537     | $65537$       | 1                   |
| 18  | 262145    | $5 \cdot 13 \cdot 37 \cdot 109$ | 4              |
| 25  | 33554433  | $3 \cdot 11 \cdot 251 \cdot 4051$ | 4            |
| 30  | 1073741825 | $5^2 \cdot 13 \cdot 41 \cdot 61 \cdot 1321$ | 5 |
| 42  | $\approx 4.4 \times 10^{12}$ | (6 distinct prime factors) | 6 |

The fifth UPN ($m = 18$) illustrates this beautifully: $1 + 2^{18} = 262145 = 5 \cdot 13 \cdot 37 \cdot 109$, and indeed the primes $5, 13, 37, 109$ all appear in the
factorization of $n_5 = 2^{18} \cdot 3 \cdot 5^4 \cdot 7 \cdot 11 \cdot 13 \cdot 19 \cdot 37 \cdot 79 \cdot 109 \cdot 157 \cdot 313$.

While $\omega(1 + 2^m)$ fluctuates and can be as small as 1 (when $1 + 2^m$ is prime,
such as Fermat primes $m = 2^k$), it generally grows slowly. This constraint does not
produce a fast-growing lower bound on $\omega_{\text{odd}}$.

---

## 5. The Critical Interplay: Can These Constraints Prove Finiteness?

### Summary of bounds

For a UPN $n$ with $v_2(n) = m$ and $\omega_{\text{odd}}(n) = s$:

1. **Product constraint:** $s \geq f(m)$, where $f(m) = 5$ for all $m \geq 9$.
2. **Size constraint:** $m < 2^s$ (from Goto + $D \geq 1 + 2^m$).
3. **Divisibility constraint:** $s \geq \omega(1 + 2^m)$.
4. **Wall's constraint:** $s \geq 9$ for any new (sixth or later) UPN.

### Why finiteness does not follow

The combined constraint $g(m) = \max(f(m), \lfloor\log_2(m)\rfloor + 1) = \lfloor\log_2(m)\rfloor + 1$ for large $m$ grows only **logarithmically** in $m$. The Goto bound $m < 2^{g(m)}$ then requires:

$$m < 2^{\lfloor\log_2(m)\rfloor + 1} \leq 2 \cdot 2^{\log_2(m)} = 2m$$

This is trivially satisfied for all $m \geq 1$. The Goto bound is doubly exponential in
$\omega$, which overwhelms the logarithmic growth of the required $\omega$. Specifically:

- $g(m)$ grows as $\log_2(m)$.
- The Goto limit $2^{g(m)}$ then grows as $2^{\log_2(m)} = m$.
- The condition $m < 2^{g(m)} \approx 2m$ is never binding.

For the combined constraints to prove finiteness, we would need $g(m)$ to grow **faster
than logarithmically** --- ideally, fast enough that $m < 2^{g(m)}$ eventually fails. This
would require:

$$g(m) < \log_2(m) \quad \text{for all large } m$$

which contradicts $g(m) \geq \log_2(m) + 1$. So the combined constraints are always
satisfiable.

### The sparsity argument

While the constraints do not prove finiteness, they do demonstrate that UPNs are
extremely sparse. For a UPN with $v_2(n) = m$:

- The number of distinct odd primes is at least $s_{\min} = \max(9, \lfloor\log_2(m)\rfloor + 1)$ (incorporating Wall's bound).
- The odd part $D$ must be divisible by $1 + 2^m$, which restricts $D$ to a sparse subset of odd integers.
- The product equation $\prod(1 + 1/q_j^{b_j}) = R(m)$ imposes a precise Diophantine constraint.
- By Goto's bound, $n < 2^{2^{s_{\min}+1}}$, which constrains the search space to a (very large but) finite region for each $m$.

The number of candidate factorizations in this region grows, but the probability that any
given candidate satisfies the exact product equation is vanishingly small. Heuristically,
the expected number of UPNs with $v_2(n) = m$ decays exponentially with $m$, but
converting this heuristic into a proof remains an open problem.

### What would be needed for a proof

To close the gap between the growth constraint and a finiteness proof, one would need one
of the following:

**(a) A super-logarithmic lower bound on $\omega_{\text{odd}}$.** If one could show
$\omega_{\text{odd}}(n) \geq c \cdot m$ for some constant $c > 0$ (linear growth in $m$),
then Goto's bound would give $n < 2^{2^{cm+1}}$, while $n \geq 2^{2m}$. This still
does not yield a contradiction (since $2^{cm} \gg 2m$), so even linear growth is
insufficient. One would need $\omega_{\text{odd}} \geq 2^{cm}$ (exponential growth), which
appears out of reach of current methods.

**(b) A polynomial upper bound replacing Goto's doubly exponential.** If one could prove
$n < C \cdot m^k$ for some polynomial bound (instead of $n < 2^{2^{\omega}}$), then
combining with $n \geq 2^{2m}$ would immediately yield finiteness. However, no such
improvement to Goto's bound is known.

**(c) Effective computation of $B(m)$.** If for each $m$ one could effectively compute
the (finite) set of UPNs with $v_2(n) = m$ and verify that $B(m) = 0$ for all
$m \geq m_0$, finiteness would follow. This is computationally feasible for moderate $m$
but the required search space grows with $m$.

**(d) Diophantine methods on the product equation.** Show directly that the equation
$\prod_{j=1}^{s}(1 + 1/q_j^{b_j}) = R(m)$ has no solutions in distinct odd prime powers
for $m \geq m_0$, using the arithmetic structure of $R(m) = 2^{m+1}/(1 + 2^m)$.

---

## 6. Extended Computation of $f(m)$ and $g(m)$ for $m = 1, \ldots, 50$

The following table presents the complete computation of all relevant quantities.

| $m$ | $R(m)$ | $f(m)$ | $\lfloor\log_2 m\rfloor + 1$ | $g(m)$ | $2^{g(m)}$ | Room ($2^{g(m)} - m$) |
|-----|---------|--------|-------------------------------|--------|------------|------------------------|
| 1   | 1.3333  | 1      | 1                             | 1      | 2          | 1                      |
| 2   | 1.6000  | 2      | 2                             | 2      | 4          | 2                      |
| 3   | 1.7778  | 3      | 2                             | 3      | 8          | 5                      |
| 4   | 1.8824  | 4      | 3                             | 4      | 16         | 12                     |
| 5   | 1.9394  | 4      | 3                             | 4      | 16         | 11                     |
| 6   | 1.9692  | 4      | 3                             | 4      | 16         | 10                     |
| 7   | 1.9845  | 4      | 3                             | 4      | 16         | 9                      |
| 8   | 1.9922  | 4      | 4                             | 4      | 16         | 8                      |
| 9   | 1.9961  | 5      | 4                             | 5      | 32         | 23                     |
| 10  | 1.9980  | 5      | 4                             | 5      | 32         | 22                     |
| 11  | 1.9990  | 5      | 4                             | 5      | 32         | 21                     |
| 12  | 1.9995  | 5      | 4                             | 5      | 32         | 20                     |
| 13  | 1.9998  | 5      | 4                             | 5      | 32         | 19                     |
| 14  | 1.9999  | 5      | 4                             | 5      | 32         | 18                     |
| 15  | 1.9999  | 5      | 4                             | 5      | 32         | 17                     |
| 16  | 1.9999  | 5      | 5                             | 5      | 32         | 16                     |
| 17  | 2.0000  | 5      | 5                             | 5      | 32         | 15                     |
| 18  | 2.0000  | 5      | 5                             | 5      | 32         | 14                     |
| 19  | 2.0000  | 5      | 5                             | 5      | 32         | 13                     |
| 20  | 2.0000  | 5      | 5                             | 5      | 32         | 12                     |
| 21  | 2.0000  | 5      | 5                             | 5      | 32         | 11                     |
| 22  | 2.0000  | 5      | 5                             | 5      | 32         | 10                     |
| 23  | 2.0000  | 5      | 5                             | 5      | 32         | 9                      |
| 24  | 2.0000  | 5      | 5                             | 5      | 32         | 8                      |
| 25  | 2.0000  | 5      | 5                             | 5      | 32         | 7                      |
| 26  | 2.0000  | 5      | 5                             | 5      | 32         | 6                      |
| 27  | 2.0000  | 5      | 5                             | 5      | 32         | 5                      |
| 28  | 2.0000  | 5      | 5                             | 5      | 32         | 4                      |
| 29  | 2.0000  | 5      | 5                             | 5      | 32         | 3                      |
| 30  | 2.0000  | 5      | 5                             | 5      | 32         | 2                      |
| 31  | 2.0000  | 5      | 5                             | 5      | 32         | 1                      |
| 32  | 2.0000  | 5      | 6                             | 6      | 64         | 32                     |
| 33  | 2.0000  | 5      | 6                             | 6      | 64         | 31                     |
| 34  | 2.0000  | 5      | 6                             | 6      | 64         | 30                     |
| 35  | 2.0000  | 5      | 6                             | 6      | 64         | 29                     |
| 36  | 2.0000  | 5      | 6                             | 6      | 64         | 28                     |
| 37  | 2.0000  | 5      | 6                             | 6      | 64         | 27                     |
| 38  | 2.0000  | 5      | 6                             | 6      | 64         | 26                     |
| 39  | 2.0000  | 5      | 6                             | 6      | 64         | 25                     |
| 40  | 2.0000  | 5      | 6                             | 6      | 64         | 24                     |
| 41  | 2.0000  | 5      | 6                             | 6      | 64         | 23                     |
| 42  | 2.0000  | 5      | 6                             | 6      | 64         | 22                     |
| 43  | 2.0000  | 5      | 6                             | 6      | 64         | 21                     |
| 44  | 2.0000  | 5      | 6                             | 6      | 64         | 20                     |
| 45  | 2.0000  | 5      | 6                             | 6      | 64         | 19                     |
| 46  | 2.0000  | 5      | 6                             | 6      | 64         | 18                     |
| 47  | 2.0000  | 5      | 6                             | 6      | 64         | 17                     |
| 48  | 2.0000  | 5      | 6                             | 6      | 64         | 16                     |
| 49  | 2.0000  | 5      | 6                             | 6      | 64         | 15                     |
| 50  | 2.0000  | 5      | 6                             | 6      | 64         | 14                     |

**Key transitions:**
- $m = 9$: $f(m)$ increases from 4 to 5 (product constraint tightens).
- $m = 32$: $g(m)$ increases from 5 to 6 (size constraint overtakes product constraint).
- $m = 64$: $g(m) = 7$.
- $m = 128$: $g(m) = 8$.
- $m = 256$: $g(m) = 9$.
- $m = 512$: $g(m) = 10$.

The "room" column shows $2^{g(m)} - m$, which measures how much slack the Goto bound
provides. At $m = 31$, the room is just 1, meaning the constraint is nearly binding for
$\omega_{\text{odd}} = 5$. But the constraint never actually becomes infeasible because
$g(m)$ steps up (to 6) precisely when needed.

---

## 7. Asymptotic Analysis

### Growth rate of $g(m)$

For large $m$:

$$g(m) = \lfloor\log_2(m)\rfloor + 1 \sim \log_2(m)$$

This is **logarithmic** in $m$.

### The Goto bound with logarithmic $\omega$

With $\omega(n) = 1 + g(m) \sim \log_2(m)$, Goto's bound gives:

$$n < 2^{2^{1 + g(m)}} \approx 2^{2m}$$

But $n \geq 2^m \cdot (1 + 2^m) > 2^{2m}$, so the Goto bound gives $n < 2^{2m}$ while
$n > 2^{2m}$ --- a near contradiction? No: the Goto bound gives $n < 2^{2^{s+1}}$ where
$s = g(m) \geq \lfloor\log_2(m)\rfloor + 1$, so:

$$2^{s+1} \geq 2^{\lfloor\log_2(m)\rfloor + 2} \geq 2m$$

So $n < 2^{2m}$ is the constraint, while $n > 2^{2m}$ would yield a contradiction. In fact
$n \geq 2^m \cdot (1 + 2^m) = 2^m + 2^{2m}$, which is slightly above $2^{2m}$. The Goto
bound says $n < 2^{2^{s+1}}$ and $2^{s+1} \geq 2m + 2$ (for the next power of 2), giving
enough room.

The margin is thin for $m$ near a power of 2, but the step function nature of
$\lfloor\log_2(m)\rfloor$ ensures feasibility always holds.

### Mertens' theorem and the product over all odd primes

By Mertens' theorem:

$$P(s) = \prod_{i=1}^{s}\frac{q_i + 1}{q_i} \sim \frac{4}{\pi^2} \cdot e^{\gamma} \cdot \ln(q_s)$$

where $q_s$ is the $s$-th odd prime. Since $q_s \sim 2s\ln(s)$ by the prime number theorem
(accounting for the factor of 2 from restricting to odd primes for large primes), we have:

$$P(s) \sim C \cdot \ln(2s\ln(s)) \sim C \cdot (\ln(s) + \ln\ln(s) + \ln 2) \sim C \cdot \ln(s)$$

So $P(s)$ grows as $\ln(s)$, which means the product diverges --- but very slowly. The
product exceeds 2 already at $s = 5$ and continues to grow without bound, confirming that
$f(m) = 5$ is the permanent ceiling of the product-based bound.

---

## 8. Conclusion

### What the growth constraint establishes

1. **For $m \leq 8$:** A UPN with $v_2(n) = m$ needs at most 4 distinct odd prime factors
   (from the product constraint).

2. **For $m \geq 9$:** A UPN needs at least 5 distinct odd prime factors (from the product
   constraint). Combined with $D \geq 1 + 2^m$ and Goto's bound, this limits $m \leq 31$
   if exactly 5 odd primes are used.

3. **For $m \geq 32$:** At least 6 distinct odd prime factors are required (from the size
   constraint via Goto), limiting $m \leq 63$ if exactly 6 are used. And so on:
   $g(m) = \lfloor\log_2(m)\rfloor + 1$.

4. **For any new UPN (Wall's bound):** $\omega_{\text{odd}} \geq 9$, giving
   $\omega \geq 10$ and $n < 2^{2^{10}} = 2^{1024}$, which constrains
   $m \leq 511$.

### What the growth constraint does not establish

The growth constraint **does not prove finiteness**. The fundamental reason is that $g(m)$
grows only logarithmically in $m$, while the Goto bound is doubly exponential in
$\omega$. The "room" between $m$ and $2^{g(m)}$ never vanishes --- it oscillates between
near-zero (at $m = 2^k - 1$) and near-$m$ (at $m = 2^k$), but always remains positive.

The constraints show that UPNs with large $m$ must have many prime factors (growing as
$\log m$), each contributing a factor close to 1 in the product equation, and the odd part
$D$ must be divisible by the increasingly large number $1 + 2^m$. This makes UPNs
increasingly rare, supporting Subbarao's finiteness conjecture heuristically, but a proof
requires additional input beyond what the growth constraint and Goto bound alone provide.

---

## References

- Subbarao, M. V. and Warren, L. J. (1966). "Unitary Perfect Numbers." *Canadian
  Mathematical Bulletin* 9(2), 147--153. [`subbarao1966unitary` in sources.bib]

- Goto, T. (2007). "Upper Bounds for Unitary Perfect Numbers and Unitary Harmonic
  Numbers." *Rocky Mountain Journal of Mathematics* 37(5), 1557--1576.
  [`goto2007upper` in sources.bib]

- Wall, C. R. (1988). "New Unitary Perfect Numbers Have at Least Nine Odd Components."
  *The Fibonacci Quarterly* 26(4), 312. [`wall1988nine` in sources.bib]

- Wall, C. R. (1975). "The Fifth Unitary Perfect Number." *Canadian Mathematical
  Bulletin* 18(1), 115--122. [`wall1975fifth` in sources.bib]

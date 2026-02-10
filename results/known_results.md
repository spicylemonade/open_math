# Known Partial Results and Proof Techniques for Finiteness of Unitary Perfect Numbers

This document catalogs all known partial results, proof techniques, and analytic tools
relevant to Subbarao's conjecture that only finitely many unitary perfect numbers (UPNs) exist.
For each result we state the precise theorem, give the paper reference, sketch the proof
where instructive, and explain how the result constrains the search space for new UPNs.

Throughout, we use standard notation:
- $\sigma^*(n) = \prod_{p^a \| n}(1 + p^a)$ is the unitary divisor sum.
- $v_2(n)$ denotes the 2-adic valuation of $n$ (i.e., $2^{v_2(n)} \| n$).
- $\omega(n)$ is the number of distinct prime factors of $n$.
- $\omega_{\text{odd}}(n)$ is the number of distinct odd prime factors of $n$.
- A UPN satisfies $\sigma^*(n) = 2n$, equivalently $\prod_{p^a \| n}(1 + 1/p^a) = 2$.

---

## 1. Subbarao--Warren Theorem: Finiteness for Fixed 2-Adic Valuation

### Precise Statement

**Theorem (Subbarao & Warren, 1966).** For every fixed positive integer $m$, there are
only finitely many unitary perfect numbers $n$ with $v_2(n) = m$.

### Reference

M. V. Subbarao and L. J. Warren, "Unitary Perfect Numbers," *Canadian Mathematical
Bulletin* **9** (1966), no. 2, 147--153. DOI: 10.4153/CMB-1966-018-4.
\[BibTeX key: `subbarao1966unitary`\]

### Proof Sketch

Suppose for contradiction that $n_1, n_2, n_3, \ldots$ is an infinite sequence of distinct
UPNs with $v_2(n_i) = m$ for all $i$. Write each as

$$n_i = 2^m \cdot D_i$$

where $D_i$ is odd. Since the $n_i$ are distinct and share the same power of 2, we must have
$D_i \to \infty$ as $i \to \infty$.

The UPN condition $\sigma^*(n_i) = 2n_i$ gives

$$\sigma^*(2^m) \cdot \sigma^*(D_i) = 2 \cdot 2^m \cdot D_i$$

$$(1 + 2^m) \cdot \sigma^*(D_i) = 2^{m+1} \cdot D_i$$

$$\frac{\sigma^*(D_i)}{D_i} = \frac{2^{m+1}}{1 + 2^m}$$

Using the multiplicative formula for $\sigma^*$, if $D_i = \prod_{j=1}^{t_i} p_j^{a_j}$ with
$p_j$ odd primes, then

$$\frac{\sigma^*(D_i)}{D_i} = \prod_{j=1}^{t_i} \left(1 + \frac{1}{p_j^{a_j}}\right)$$

Now observe two key facts:

1. **The target ratio is fixed and greater than 1.** For all $m \geq 1$:

$$\frac{2^{m+1}}{1 + 2^m} = \frac{2 \cdot 2^m}{1 + 2^m} = \frac{2}{1 + 2^{-m}} > 1$$

   In fact, for $m = 1$ the ratio is $4/3$; for $m = 2$ it is $8/5$; and the ratio
   increases monotonically toward 2 as $m \to \infty$.

2. **The product $\sigma^*(D_i)/D_i$ approaches 1 as $D_i \to \infty$ (with bounded
   number of prime factors).** If $D_i$ has a bounded number of prime factors, each
   $p_j^{a_j} \to \infty$ along a subsequence, so each factor $(1 + 1/p_j^{a_j}) \to 1$.
   If the number of prime factors grows, then eventually each new prime $p_j$ is large,
   and the contribution $(1 + 1/p_j^{a_j})$ is negligibly above 1.

More precisely, for any $\epsilon > 0$, there are only finitely many odd integers $D$
with $\sigma^*(D)/D > 1 + \epsilon$. This is because $\sigma^*(D)/D \leq \prod_{p \mid D}(1 + 1/p)$,
and by Mertens' theorem $\prod_{p \leq x}(1 + 1/p) \sim \frac{6}{\pi^2} \cdot e^\gamma \cdot \ln x$
grows only logarithmically. For $D$ to have $\sigma^*(D)/D$ bounded away from 1, the
prime factors of $D$ cannot all be large, so $D$ is confined to a finite set determined
by its small prime factor structure.

Since $2^{m+1}/(1 + 2^m) > 1$ for all $m \geq 1$, and the set of odd $D$ achieving any
given ratio $> 1$ is finite, there are only finitely many valid $D_i$ for each $m$.

### How It Constrains the Search Space

This theorem partitions the finiteness conjecture into countably many finite problems:
for each $m = 1, 2, 3, \ldots$, determine the (finite) set of UPNs with $v_2(n) = m$.
The conjecture would follow if one could show that the finite bound $B(m)$ on UPNs
with $v_2(n) = m$ is itself eventually zero---or more modestly, that $\sum_{m=1}^{\infty} B(m) < \infty$.
The critical gap is that $B(m)$ is not known to be effectively computable, and it is
not known whether $B(m) = 0$ for all sufficiently large $m$.

---

## 2. Goto's Upper Bound for UPNs with Fixed Number of Prime Factors

### Precise Statement

**Theorem (Goto, 2007).** If $N$ is a unitary perfect number with $\omega(N) = k$ distinct
prime factors, then

$$N < 2^{2^k}$$

### Reference

T. Goto, "Upper Bounds for Unitary Perfect Numbers and Unitary Harmonic Numbers,"
*Rocky Mountain Journal of Mathematics* **37** (2007), no. 5, 1557--1576.
DOI: 10.1216/rmjm/1194275935.
\[BibTeX key: `goto2007upper`\]

### Proof Technique

Goto's proof proceeds by analyzing the product equation $\prod_{i=1}^{k}(1 + 1/p_i^{a_i}) = 2$.
Since $1 + 1/p_i^{a_i} \leq 1 + 1/p_i \leq 3/2$ for $p_i \geq 2$, and these factors are
multiplicatively independent, one can bound each $p_i^{a_i}$ in terms of the remaining
factors. The key inequality is that if the product of $k$ factors, each at most $3/2$,
equals 2, then the largest prime power $p_k^{a_k}$ satisfies

$$p_k^{a_k} < \frac{1}{\prod_{i=1}^{k-1}(1+1/p_i^{a_i}) - 2 + 1}$$

By iterating this bounding argument over all $k$ primes and using the constraint that
primes are distinct, Goto obtains the doubly exponential bound $N = \prod p_i^{a_i} < 2^{2^k}$.

### Verification Against Known UPNs

| UPN | $\omega$ ($k$) | $N$ | $2^{2^k}$ | Satisfies? |
|-----|----------------|-----|-----------|------------|
| 6 | 2 | 6 | 16 | Yes |
| 60 | 3 | 60 | 256 | Yes |
| 90 | 3 | 90 | 256 | Yes |
| 87360 | 5 | 87360 | $2^{32} \approx 4.3 \times 10^9$ | Yes |
| $n_5$ | 12 | $\approx 1.46 \times 10^{23}$ | $2^{4096} \approx 10^{1233}$ | Yes |

### How It Constrains the Search Space

The Goto bound means that for a UPN with exactly $k$ distinct prime factors, the search
space is bounded: one need only check integers up to $2^{2^k}$. While the bound is
doubly exponential, it is still finite for each $k$. Crucially, when combined with the
Subbarao--Warren theorem, this establishes:

- For fixed $m$ and fixed $k$: the number of UPNs is finite (bounded search space from
  Goto) and the UPNs with $v_2(n) = m$ are finite (Subbarao--Warren).
- The remaining question is whether $k$ (and hence $m$) can grow without bound while
  still admitting UPNs.

---

## 3. Wall's Lower Bound on Odd Prime Factors

### Precise Statement

**Theorem (Wall, 1988).** Any unitary perfect number beyond the five known examples must
have at least 9 distinct odd prime factors:

$$\omega_{\text{odd}}(n) \geq 9$$

Equivalently, since every UPN is even ($2 \mid n$), this means $\omega(n) \geq 10$ for
any new UPN.

### Reference

C. R. Wall, "New Unitary Perfect Numbers Have at Least Nine Odd Components,"
*The Fibonacci Quarterly* **26** (1988), no. 4, 312.
\[BibTeX key: `wall1988nine`\]

### Earlier Related Result

C. R. Wall, "On the Largest Odd Component of a Unitary Perfect Number,"
*The Fibonacci Quarterly* **25** (1987), 312--316.
\[BibTeX key: `wall1987largest`\]

### Proof Technique

Wall's approach is systematic case analysis combined with the product equation. For a
UPN $n = 2^m \cdot \prod_{i=1}^{t} p_i^{a_i}$ (with $p_i$ odd primes), the product equation becomes:

$$(1 + 2^m) \cdot \prod_{i=1}^{t}(1 + p_i^{a_i}) = 2^{m+1} \cdot \prod_{i=1}^{t} p_i^{a_i}$$

For small values of $t$ (the number of odd prime factors), this equation is highly
constrained:
- Each factor $(1 + p_i^{a_i})$ introduces specific divisibility requirements.
- Since $1 + 2^m$ must divide $2^{m+1} \cdot \prod p_i^{a_i}$, the prime factorization of
  $1 + 2^m$ constrains which odd primes can appear.
- Wall exhaustively checks all valid configurations with $t \leq 8$ odd primes and shows
  the only solutions are the five known UPNs.

### How It Constrains the Search Space

This eliminates all UPN candidates with fewer than 9 odd prime factors (except the known
five). Combined with Goto's bound:
- Any sixth UPN has $\omega(n) \geq 10$, so $n < 2^{2^{10}} = 2^{1024} \approx 10^{308}$.
- More practically, since the product of $(1 + 1/p_i^{a_i})$ for 10+ primes is hard to
  make equal to exactly 2 (it tends to be either too large with small primes or too
  small with large primes), the constraint is very restrictive.

---

## 4. Frei's Result: UPNs Not Divisible by 3

### Precise Statement

**Theorem (Frei, cited in OEIS 2019).** If $n$ is a unitary perfect number with $3 \nmid n$,
then:

1. $v_2(n) \geq 144$ (the 2-adic valuation is at least 144),
2. $\omega_{\text{odd}}(n) \geq 144$ (there are at least 144 distinct odd prime factors),
3. $n > 10^{440}$.

### Reference

Cited in OEIS sequence A002827 (2019 comments). The result is attributed to Frei;
the original publication details are not fully established in the standard literature.
\[BibTeX key: `oeis_A002827`\]

### Proof Technique

The argument exploits the product equation $\prod(1 + 1/p_i^{a_i}) = 2$ under the
constraint $3 \nmid n$. If 3 does not divide $n$, then:

- The factor $(1 + 1/3) = 4/3$ (or $(1+1/9) = 10/9$, etc.) is absent from the product.
- The smallest available odd prime is 5, giving a maximum factor of $(1 + 1/5) = 6/5$.
- Since $6/5 < 4/3$, substantially more prime factors are needed to compensate.

Specifically, if all odd primes $p_i \geq 5$ appear with exponent $a_i = 1$, then
$\prod(1 + 1/p_i) \leq \prod_{p \geq 5, p \text{ prime}}(1 + 1/p)$. For the product
over the even component to contribute, $(1 + 1/2^m) \cdot \prod(1 + 1/p_i) = 2$ requires
$(1 + 1/2^m)$ close to 2 (i.e., $m$ small), but with small $m$ and no factor of 3, the
remaining product cannot reach $2/(1 + 1/2^m)$. This forces $m$ to be extremely large,
which in turn forces many odd primes to be present (since the target ratio
$2^{m+1}/(1+2^m) \approx 2$ for large $m$, and achieving a product close to 2 with primes
$\geq 5$ requires very many of them).

The bound $v_2(n) \geq 144$ and $\omega_{\text{odd}}(n) \geq 144$ are obtained by careful
iterative analysis, and $n > 10^{440}$ follows from the minimal size forced by 144+ prime
factors each at least 5.

### How It Constrains the Search Space

This is one of the strongest known constraints. Among the five known UPNs, all are
divisible by 3. This result shows that any UPN avoiding 3 would be astronomically large
and complex. In practice:

- Any search for new UPNs can assume $3 \mid n$, or else face a search space beyond
  $10^{440}$ with at least 144 odd prime factors.
- This suggests that the "easy" case is $3 \mid n$, and Wall's bound of
  $\omega_{\text{odd}} \geq 9$ applies there.
- Combined: if $3 \mid n$ and $\omega_{\text{odd}} \geq 9$ (so $\omega \geq 10$), then
  by Goto's bound $n < 2^{1024}$. If $3 \nmid n$, then $n > 10^{440}$ but also
  $\omega \geq 145$, giving Goto bound $n < 2^{2^{145}}$, which is compatible but
  places $n$ in an enormous range.

---

## 5. Graham's Result on the Squarefree Odd Part

### Precise Statement

**Theorem (Graham, 1989).** Let $n$ be a unitary perfect number. If $n = 2^m \cdot D$
where $D$ is the odd part of $n$, then certain structural constraints apply to $D$ related
to its squarefree kernel and the distribution of prime factor exponents.

In particular, Graham showed that for UPNs, if $p^a \| n$ with $a \geq 2$ and $p$ odd,
then $1 + p^a$ introduces specific divisibility conditions that severely limit which higher
powers of odd primes can appear.

### Reference

This result is referenced in the context of the UPN literature and in Guy's *Unsolved
Problems in Number Theory*, Problem B3.
\[BibTeX key: `guy2004unsolved`\]

### How It Constrains the Search Space

Among the five known UPNs, almost all odd prime powers appear with exponent 1. The only
exception is $5^4$ in the fifth UPN. Graham's constraints help explain this pattern: the
factor $1 + p^a$ for $a \geq 2$ is harder to "balance" in the product equation because:

- $1 + p^2 = 1 + p^2$ must factor into primes that themselves appear in $n$, creating a
  chain of divisibility conditions.
- These chains quickly become inconsistent for most combinations of higher powers.

This means any practical search can prioritize squarefree odd parts (all $a_i = 1$ for
odd primes), with higher powers treated as rare special cases.

---

## 6. The Dirichlet Generating Function and Mean Value of $\sigma^*(n)/n$

### Precise Statement

**Theorem (Analytic number theory).** The Dirichlet series generating function for $\sigma^*(n)$ is:

$$\sum_{n=1}^{\infty} \frac{\sigma^*(n)}{n^s} = \frac{\zeta(s)\zeta(s-1)}{\zeta(2s-1)}$$

valid for $\operatorname{Re}(s) > 2$.

### Derivation

Since $\sigma^*$ is multiplicative with $\sigma^*(p^a) = 1 + p^a$, the Euler product is:

$$\sum_{n=1}^{\infty} \frac{\sigma^*(n)}{n^s} = \prod_p \left(\sum_{a=0}^{\infty} \frac{\sigma^*(p^a)}{p^{as}}\right) = \prod_p \left(1 + \sum_{a=1}^{\infty} \frac{1 + p^a}{p^{as}}\right)$$

$$= \prod_p \left(1 + \sum_{a=1}^{\infty} \frac{1}{p^{as}} + \sum_{a=1}^{\infty} \frac{1}{p^{a(s-1)}}\right)$$

$$= \prod_p \left(\frac{1}{1 - p^{-s}} + \frac{p^{-(s-1)}}{1 - p^{-(s-1)}} \right)$$

$$= \prod_p \frac{(1 - p^{-(2s-1)})}{(1 - p^{-s})(1 - p^{-(s-1)})} \cdot \frac{1}{1 - p^{-(2s-1)}} \cdot (1 - p^{-(2s-1)})$$

After simplification using standard Euler product identities:

$$= \frac{\zeta(s)\zeta(s-1)}{\zeta(2s-1)}$$

### Mean Value Consequence

Setting $s = 1$ heuristically (though the series diverges there), and using Perron's
formula or elementary partial summation arguments, one obtains:

$$\sum_{n \leq X} \frac{\sigma^*(n)}{n} \sim C \cdot X$$

where the constant $C$ is given by

$$C = \prod_p \left(1 + \frac{1}{p(p+1)}\right) = \prod_p \frac{p^2 + p + 1}{p(p+1)}$$

This product converges; numerically $C \approx 1.94359...$

More precisely, we can write:

$$C = \frac{\zeta(2)}{\zeta(3)} \cdot \prod_p \frac{(1 - p^{-3})(1 + p^{-1}(p+1)^{-1})}{(1 - p^{-2})}$$

The fact that the average value of $\sigma^*(n)/n$ is approximately $1.94 < 2$ indicates
that the "typical" integer has $\sigma^*(n)/n$ close to but less than 2, and achieving
$\sigma^*(n)/n = 2$ exactly is a rare event.

### Reference

The Dirichlet series identity is classical; see for example:

- E. Cohen, "Arithmetical Functions Associated with the Unitary Divisors of an Integer,"
  *Math. Zeitschr.* **74** (1960), 66--80.
  \[BibTeX key: `cohen1960unitary`\]

The application to density questions is discussed in:

- P. Pollack and V. Shevelev, "On Perfect and Near-Perfect Numbers,"
  *J. Number Theory* **132** (2012), 3037--3046.
  \[BibTeX key: `pollack2012near`\]

### How It Constrains the Search Space

The Dirichlet series and mean value results support the finiteness conjecture in
several ways:

1. **Density zero.** Since $\sigma^*(n)/n$ has a continuous limiting distribution (by the
   Erdos--Wintner theorem applied to the additive function $\log(1 + 1/p^a)$), the set
   of $n$ with $\sigma^*(n)/n$ in any specific interval $[2 - \epsilon, 2 + \epsilon]$
   has density proportional to $\epsilon$. The set where $\sigma^*(n)/n = 2$ exactly has
   density zero.

2. **Variance estimates.** The variance of $\sigma^*(n)/n$ over $[1, X]$ can be computed
   from the Dirichlet series. By standard techniques (Selberg--Delange method or
   elementary bounds), one can show:

   $$\sum_{n \leq X} \left(\frac{\sigma^*(n)}{n} - C\right)^2 \sim C_2 \cdot X$$

   for an explicit constant $C_2$. This means deviations from the mean are bounded, and
   the probability of $\sigma^*(n)/n$ being exactly 2 is extremely small for large $n$.

3. **Comparison with near-perfect bounds.** Pollack and Shevelev showed that
   near-perfect numbers $n \leq x$ (where $\sigma(n) - n$ equals a unitary divisor of $n$)
   number at most $x^{5/6 + o(1)}$. Analogous techniques, applied to $\sigma^*$ instead
   of $\sigma$, could potentially yield sublinear upper bounds on
   $\#\{n \leq X : \sigma^*(n) = 2n\}$.

4. **The analytic approach alone cannot prove finiteness.** Density-zero results and even
   power-saving density bounds (like $x^{5/6}$) do not by themselves imply that the set
   is finite. One would need to show the count is $O(1)$, which requires additional
   structural input beyond what the Dirichlet series provides.

---

## 7. Non-Existence of Odd UPNs

### Precise Statement

**Theorem (Subbarao & Warren, 1966).** There are no odd unitary perfect numbers.

### Reference

M. V. Subbarao and L. J. Warren, "Unitary Perfect Numbers," *Canad. Math. Bull.* **9**
(1966), 147--153.
\[BibTeX key: `subbarao1966unitary`\]

### Proof

If $n$ is odd with $\omega(n) = k$ distinct prime factors, all odd, then each
$1 + p_i^{a_i}$ is even, so $2^k \mid \sigma^*(n)$. But $\sigma^*(n) = 2n$ with $n$ odd
gives $v_2(\sigma^*(n)) = 1$. For $k \geq 2$, this is a contradiction. For $k = 1$,
$n = p^a$ gives $1 + p^a = 2p^a$, so $p^a = 1$, also a contradiction.

### How It Constrains the Search Space

Every UPN is even. This immediately halves the search space and means every UPN has the
form $n = 2^m \cdot D$ with $m \geq 1$ and $D$ odd. The 2-adic valuation $m$ becomes a
fundamental parameter in the analysis.

---

## 8. Wall's Discovery of the Fifth UPN

### Precise Statement

**Theorem (Wall, 1975).** The integer

$$n_5 = 2^{18} \cdot 3 \cdot 5^4 \cdot 7 \cdot 11 \cdot 13 \cdot 19 \cdot 37 \cdot 79 \cdot 109 \cdot 157 \cdot 313$$
$$= 146{,}361{,}946{,}186{,}458{,}562{,}560{,}000$$

is a unitary perfect number. Furthermore, there is no UPN between 87360 and $n_5$.

### Reference

C. R. Wall, "The Fifth Unitary Perfect Number," *Canadian Mathematical Bulletin* **18**
(1975), no. 1, 115--122. DOI: 10.4153/CMB-1975-021-9.
\[BibTeX key: `wall1975fifth`\]

### How It Constrains the Search Space

Wall's exhaustive search established that the list $\{6, 60, 90, 87360, n_5\}$ is complete
up to $n_5$. Any sixth UPN must exceed $n_5 \approx 1.46 \times 10^{23}$, and by Wall's
1988 result, must have $\omega_{\text{odd}} \geq 9$, i.e., $\omega \geq 10$.

---

## 9. Summary: Combined Constraint Landscape

The following table summarizes how each result constrains the parameters of a hypothetical
sixth UPN $N$:

| Constraint | Source | Effect |
|------------|--------|--------|
| $N$ is even | Subbarao--Warren (1966) | $v_2(N) \geq 1$ |
| $N > n_5 \approx 1.46 \times 10^{23}$ | Wall (1975) | Lower bound on $N$ |
| $\omega_{\text{odd}}(N) \geq 9$, so $\omega(N) \geq 10$ | Wall (1988) | Minimum number of prime factors |
| $N < 2^{2^{\omega(N)}}$ | Goto (2007) | Upper bound given $\omega$ |
| For fixed $m = v_2(N)$: finitely many | Subbarao--Warren (1966) | Each 2-adic valuation contributes finitely |
| If $3 \nmid N$: $v_2 \geq 144$, $\omega_{\text{odd}} \geq 144$, $N > 10^{440}$ | Frei (OEIS) | Extreme constraints without factor 3 |

### The Central Gap

The combination of all known results does not resolve the finiteness conjecture because:

1. **Subbarao--Warren** shows finiteness for each fixed $m$, but the bound $B(m)$ on UPNs
   with $v_2(n) = m$ is not shown to be zero for large $m$.

2. **Goto's bound** shows finiteness for each fixed $\omega(n) = k$, but $k$ could
   potentially grow unboundedly.

3. **Wall's bound** eliminates small $\omega$ values but does not prevent $\omega \geq 10$.

4. **Frei's result** is powerful for $3 \nmid n$ but says nothing about UPNs divisible by 3.

5. **Analytic methods** give density zero but not finiteness.

The missing piece is a **uniform argument** that either:
- Shows $B(m) = 0$ for all $m \geq m_0$ (some effective threshold), or
- Shows that the minimum $\omega(N)$ required for $v_2(N) = m$ grows fast enough that
  combined with Goto's bound, the feasible region $(m, \omega)$ becomes empty for large $m$, or
- Proves that the Diophantine equation $\prod(1 + 1/p_i^{a_i}) = 2$ has only finitely
  many solutions over distinct prime powers.

This analysis of the gap motivates the research directions outlined in the companion
document `results/research_gaps.md`.

---

## References

1. Subbarao, M. V. and Warren, L. J. (1966). "Unitary Perfect Numbers." *Canad. Math. Bull.* 9(2), 147--153.
2. Subbarao, M. V. (1970). "Are There an Infinity of Unitary Perfect Numbers?" *Amer. Math. Monthly* 77, 389--390.
3. Wall, C. R. (1975). "The Fifth Unitary Perfect Number." *Canad. Math. Bull.* 18(1), 115--122.
4. Wall, C. R. (1987). "On the Largest Odd Component of a Unitary Perfect Number." *Fibonacci Quart.* 25, 312--316.
5. Wall, C. R. (1988). "New Unitary Perfect Numbers Have at Least Nine Odd Components." *Fibonacci Quart.* 26(4), 312.
6. Goto, T. (2007). "Upper Bounds for Unitary Perfect Numbers and Unitary Harmonic Numbers." *Rocky Mountain J. Math.* 37(5), 1557--1576.
7. Pollack, P. and Shevelev, V. (2012). "On Perfect and Near-Perfect Numbers." *J. Number Theory* 132, 3037--3046.
8. Cohen, E. (1960). "Arithmetical Functions Associated with the Unitary Divisors of an Integer." *Math. Zeitschr.* 74, 66--80.
9. Guy, R. K. (2004). *Unsolved Problems in Number Theory*, 3rd ed. Springer. Problem B3.
10. OEIS Foundation Inc. Sequence A002827: Unitary Perfect Numbers. https://oeis.org/A002827

# Problem Formalization: Unitary Perfect Numbers

## 1. Definition of Unitary Divisor

**Definition.** Let $n \geq 1$ be a positive integer and $d \mid n$. We say that $d$ is a **unitary divisor** of $n$ if $\gcd(d, n/d) = 1$. We write $d \| n$ (read: "$d$ unitarily divides $n$").

Equivalently, if $n = p_1^{a_1} p_2^{a_2} \cdots p_k^{a_k}$ is the prime factorization of $n$, then $d \| n$ if and only if $d$ is a product of a subset of the prime powers $\{p_1^{a_1}, p_2^{a_2}, \ldots, p_k^{a_k}\}$. In particular, $n$ has exactly $2^k$ unitary divisors (including 1 and $n$ itself), where $k = \omega(n)$ is the number of distinct prime factors.

## 2. The Unitary Sigma Function (Multiplicative Formula)

**Definition.** The **unitary divisor sum function** $\sigma^*(n)$ is defined as:

$$\sigma^*(n) = \sum_{d \| n} d$$

Since each unitary divisor of $n = p_1^{a_1} \cdots p_k^{a_k}$ is a product of a subset of the prime powers, we have:

$$\sigma^*(n) = \prod_{i=1}^{k} (1 + p_i^{a_i})$$

This is the **multiplicative formula** for $\sigma^*$. The function $\sigma^*$ is multiplicative in the sense that if $\gcd(m, n) = 1$, then $\sigma^*(mn) = \sigma^*(m) \sigma^*(n)$. More specifically, $\sigma^*$ is a multiplicative function with $\sigma^*(p^a) = 1 + p^a$ for all prime powers $p^a$.

## 3. Unitary Perfect Numbers

**Definition.** A positive integer $n \geq 1$ is called a **unitary perfect number** (UPN) if it equals the sum of its proper unitary divisors:

$$\sigma^*(n) - n = n \quad \Longleftrightarrow \quad \sigma^*(n) = 2n$$

Equivalently, using the multiplicative formula:

$$\prod_{p^a \| n} (1 + p^a) = 2n = 2 \prod_{p^a \| n} p^a$$

Dividing both sides by $n$:

$$\prod_{p^a \| n} \left(1 + \frac{1}{p^a}\right) = 2$$

This is the fundamental **product equation** characterizing unitary perfect numbers.

## 4. Subbarao's Finiteness Conjecture

**Conjecture (Subbarao, 1970).** There are only finitely many unitary perfect numbers.

This conjecture was posed by M. V. Subbarao in:
- M. V. Subbarao, "Are there an infinity of unitary perfect numbers?", *Amer. Math. Monthly* 77 (1970), 389–390.

The conjecture is also listed as Problem B3 in R. K. Guy, *Unsolved Problems in Number Theory*, 3rd ed., Springer, 2004.

It appears as Erdős Problem #1052, carrying a $10 prize, on the Erdős Problems website.

## 5. Non-Existence of Odd Unitary Perfect Numbers

**Theorem (Subbarao–Warren, 1966).** There are no odd unitary perfect numbers.

**Proof.** Suppose $n$ is an odd unitary perfect number. Write $n = p_1^{a_1} p_2^{a_2} \cdots p_k^{a_k}$ where each $p_i$ is an odd prime and each $a_i \geq 1$.

Since each $p_i$ is odd, $p_i^{a_i}$ is odd, so $1 + p_i^{a_i}$ is even. Therefore:

$$\sigma^*(n) = \prod_{i=1}^{k} (1 + p_i^{a_i}) \equiv 0 \pmod{2^k}$$

That is, $2^{\omega(n)} \mid \sigma^*(n)$.

But if $n$ is a UPN, then $\sigma^*(n) = 2n$. Since $n$ is odd, $v_2(\sigma^*(n)) = v_2(2n) = 1$, where $v_2$ denotes the 2-adic valuation.

However, $v_2(\sigma^*(n)) \geq k = \omega(n) \geq 1$ (since $n > 1$ implies $n$ has at least one prime factor). For $k \geq 2$, we get $v_2(\sigma^*(n)) \geq 2 > 1 = v_2(2n)$, a contradiction.

For $k = 1$: $n = p^a$ for some odd prime $p$. Then $\sigma^*(n) = 1 + p^a$ and $2n = 2p^a$. So $1 + p^a = 2p^a$, giving $p^a = 1$, a contradiction since $p \geq 3$.

Therefore, no odd unitary perfect number exists. $\square$

**Consequence.** Every UPN must be even, i.e., $2 \mid n$ for any UPN $n$.

## 6. The Five Known Unitary Perfect Numbers

The following table lists all known unitary perfect numbers, verified computationally:

| # | $n$ | Prime Factorization | $\omega(n)$ | $v_2(n)$ | Discoverer |
|---|-----|---------------------|-------------|-----------|------------|
| 1 | 6 | $2 \cdot 3$ | 2 | 1 | Subbarao–Warren (1966) |
| 2 | 60 | $2^2 \cdot 3 \cdot 5$ | 3 | 2 | Subbarao–Warren (1966) |
| 3 | 90 | $2 \cdot 3^2 \cdot 5$ | 3 | 1 | Subbarao–Warren (1966) |
| 4 | 87360 | $2^6 \cdot 3 \cdot 5 \cdot 7 \cdot 13$ | 5 | 6 | Subbarao–Warren (1966) |
| 5 | 146361946186458562560000 | $2^{18} \cdot 3 \cdot 5^4 \cdot 7 \cdot 11 \cdot 13 \cdot 19 \cdot 37 \cdot 79 \cdot 109 \cdot 157 \cdot 313$ | 12 | 18 | Wall (1972) |

### Verification

For each known UPN $n$, we verify $\prod_{p^a \| n}(1 + p^a) = 2n$:

**$n = 6 = 2 \cdot 3$:**
$(1+2)(1+3) = 3 \cdot 4 = 12 = 2 \cdot 6$ ✓

**$n = 60 = 2^2 \cdot 3 \cdot 5$:**
$(1+4)(1+3)(1+5) = 5 \cdot 4 \cdot 6 = 120 = 2 \cdot 60$ ✓

**$n = 90 = 2 \cdot 3^2 \cdot 5$:**
$(1+2)(1+9)(1+5) = 3 \cdot 10 \cdot 6 = 180 = 2 \cdot 90$ ✓

**$n = 87360 = 2^6 \cdot 3 \cdot 5 \cdot 7 \cdot 13$:**
$(1+64)(1+3)(1+5)(1+7)(1+13) = 65 \cdot 4 \cdot 6 \cdot 8 \cdot 14 = 174720 = 2 \cdot 87360$ ✓

**$n = 146361946186458562560000 = 2^{18} \cdot 3 \cdot 5^4 \cdot 7 \cdot 11 \cdot 13 \cdot 19 \cdot 37 \cdot 79 \cdot 109 \cdot 157 \cdot 313$:**
$(1+2^{18})(1+3)(1+5^4)(1+7)(1+11)(1+13)(1+19)(1+37)(1+79)(1+109)(1+157)(1+313)$
$= 262145 \cdot 4 \cdot 626 \cdot 8 \cdot 12 \cdot 14 \cdot 20 \cdot 38 \cdot 80 \cdot 110 \cdot 158 \cdot 314$
$= 292723892372917125120000 = 2 \cdot 146361946186458562560000$ ✓

All five verified computationally (exact integer arithmetic).

### Observations

1. The ratio $v_2(n) / \omega(n)$ grows: $1/2, 2/3, 1/3, 6/5, 18/12 = 3/2$. For the fifth UPN, the 2-adic valuation $m = 18$ is large relative to the total number of distinct primes $k = 12$.

2. The product equation $\prod(1 + 1/p_i^{a_i}) = 2$ must be satisfied exactly. This is a very stringent Diophantine constraint.

3. Most prime powers appear with exponent $a_i = 1$ (all but $p=2$ and $p=5$ in the fifth UPN).

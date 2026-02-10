# Research Gaps and Unexplored Directions in Unitary Perfect Number Theory

This document identifies specific gaps in the existing literature on unitary perfect numbers (UPNs) and proposes concrete directions for future investigation. Each gap is grounded in prior work and articulated with enough precision to serve as a starting point for new research.

---

## Gap 1: Uniformity of the Subbarao--Warren Fixed-Valuation Argument

### Prior work

Subbarao and Warren (1966) proved that for each fixed non-negative integer $m$, there are only finitely many UPNs $n$ with $v_2(n) = m$, where $v_2$ denotes the 2-adic valuation. The argument proceeds by fixing the power of 2 in the factorization $n = 2^m \cdot D$ (with $D$ odd) and observing that the product equation

$$\frac{1 + 2^m}{2^m} \cdot \prod_{p^a \| D} \left(1 + \frac{1}{p^a}\right) = 2$$

forces the odd part $D$ to satisfy a product constraint with a fixed left factor $(1 + 2^m)/2^m$. As $D$ grows, the product $\prod(1 + 1/p^a)$ over its prime power components tends to 1, so only finitely many odd parts $D$ can satisfy the equation for each fixed $m$.

### The gap

Let $B(m)$ denote the number of UPNs $n$ with $v_2(n) = m$. The Subbarao--Warren theorem establishes that $B(m) < \infty$ for every $m$, but the finiteness of the total count $\sum_{m=1}^{\infty} B(m)$ does not follow. This summation is finite if and only if there are finitely many UPNs overall --- precisely Subbarao's conjecture.

The critical question is whether $B(m) = 0$ for all sufficiently large $m$. If there exists an explicit threshold $m_0$ such that $B(m) = 0$ for all $m \geq m_0$, then finiteness follows immediately since only finitely many $m$-values contribute, each contributing finitely many UPNs.

### Why this is hard

For large $m$, the factor $(1 + 2^m)/2^m = 1 + 2^{-m}$ is very close to 1, so the remaining odd prime powers must collectively produce a product very close to 2. This requires many odd prime factors (since each factor $(1 + 1/p^a)$ is at most $(1 + 1/3) = 4/3$ for the smallest odd prime power). The number of required odd primes $k(m)$ grows roughly as $m / \log(4/3)$, but whether the combinatorial explosion of possible factorizations with $k(m)$ primes can always be ruled out remains open. The Subbarao--Warren proof gives no effective bound on $B(m)$ as a function of $m$, let alone a proof that $B(m) = 0$ eventually.

### Proposed direction

1. Make the bound $B(m)$ effective: for each $m$, derive an explicit upper bound on $B(m)$ by bounding the size of the largest prime that can appear in the odd part and then bounding the number of valid factorizations.
2. Study the growth rate of $B(m)$: compute $B(m)$ for $m = 1, 2, \ldots, 30$ by exhaustive search. From the known UPNs, we have $B(1) = 2$ (from $n = 6$ and $n = 90$), $B(2) = 1$ (from $n = 60$), $B(6) = 1$ (from $n = 87360$), $B(18) = 1$ (from the fifth UPN), and $B(m) = 0$ for all other known $m$-values.
3. Combine with Goto's bound: Goto (2007) proved $n < 2^{2^k}$ for $\omega(n) = k$. For $v_2(n) = m$, the odd part has $\omega_{\text{odd}}(n) = k - 1$ prime factors and $n = 2^m \cdot D$ with $D < 2^{2^k}$. This constrains both the number of odd prime factors and their sizes. If $k(m) \to \infty$ fast enough relative to $2^{2^{k(m)}}$, the feasible region may become empty.

### References

- Subbarao, M. V. and Warren, L. J. (1966), "Unitary Perfect Numbers", *Canad. Math. Bull.* 9, 147--153.
- Goto, T. (2007), "Upper Bounds for Unitary Perfect Numbers and Unitary Harmonic Numbers", *Rocky Mountain J. Math.* 37(5), 1557--1576.

---

## Gap 2: Analytic Density Bounds via Mean-Value Theorems for $\sigma^*(n)/n$

### Prior work

The Dirichlet series generating function for the unitary divisor sum is

$$\sum_{n=1}^{\infty} \frac{\sigma^*(n)}{n^s} = \frac{\zeta(s)\,\zeta(s-1)}{\zeta(2s-1)},$$

valid for $\operatorname{Re}(s) > 2$. This identity follows from the multiplicativity of $\sigma^*$ and the Euler product. It provides analytic access to the average behavior of $\sigma^*(n)/n$.

Pollack and Shevelev (2012) used properties of unitary divisors to bound the counting function of near-perfect numbers (numbers $n$ with $\sigma(n) - 2n = d$ for some proper divisor $d$ of $n$), showing their count up to $x$ is at most $x^{5/6 + o(1)}$. Their technique leverages the fact that if $m \| n$, then $\sigma(m) \mid \sigma(n)$, which creates strong divisibility constraints.

### The gap

No one has applied mean-value theorems or large-sieve techniques specifically to bound the counting function

$$U(x) = \#\{n \leq x : \sigma^*(n) = 2n\}.$$

The standard approach would be:

1. **Mean value:** Compute the average of $\sigma^*(n)/n$ over $[1, x]$ using partial summation and the Dirichlet series. The mean value of $\sigma^*(n)/n$ is asymptotically $c \cdot x$ for an explicit constant $c = \prod_p (1 + 1/p(p+1))$, so the "expected" value of $\sigma^*(n)/n$ is roughly constant (not 2), suggesting UPNs are rare.

2. **Variance:** Estimate the second moment $\sum_{n \leq x} (\sigma^*(n)/n - \mu)^2$ to quantify concentration. If the variance is small, then $\sigma^*(n)/n$ is close to its mean for most $n$, making the equation $\sigma^*(n)/n = 2$ increasingly unlikely.

3. **Large deviation bounds:** Use exponential moment methods or Hal\'asz-type theorems to bound the probability that a multiplicative function deviates far from its typical value. The function $f(n) = \sigma^*(n)/n = \prod_{p^a \| n}(1 + 1/p^a)$ is a multiplicative function taking values near 1 for most $n$, and hitting the value 2 is a large deviation event.

### Key question

Can such analytic bounds prove $U(x) = O(1)$ (finiteness), or do they only yield density-zero results such as $U(x) = o(x)$ or $U(x) = O(x^{\theta})$ for some $\theta < 1$? The Pollack--Shevelev bound for near-perfect numbers gives a power-saving density bound ($x^{5/6+o(1)}$) but not finiteness. It is unclear whether the unitary setting, where the constraint $\sigma^*(n) = 2n$ is more rigid due to exact multiplicativity, allows for stronger conclusions.

### Proposed direction

1. Compute the mean and variance of $\sigma^*(n)/n$ over $[1, x]$ explicitly, using the Euler product representation.
2. Apply Hal\'asz's theorem or the Granville--Soundararajan framework for multiplicative functions to bound $U(x)$.
3. Investigate whether the "pretentious" distance of $\sigma^*(n)/n$ from the constant function 2 can be made effective enough to yield finiteness.
4. Compare the achievable bounds with Pollack--Shevelev to assess whether the unitary setting is fundamentally different.

### References

- Pollack, P. and Shevelev, V. (2012), "On Perfect and Near-Perfect Numbers", *J. Number Theory* 132(12), 3037--3046.
- The Dirichlet series identity $\zeta(s)\zeta(s-1)/\zeta(2s-1)$ (see Cohen, 1960; also Guy, 2004, Problem B3).

---

## Gap 3: Diophantine Finiteness of the Product Equation $\prod(1 + 1/p_i^{a_i}) = 2$

### Prior work

Every UPN corresponds to a solution of the product equation

$$\prod_{i=1}^{k} \left(1 + \frac{1}{p_i^{a_i}}\right) = 2,$$

where $p_1^{a_1}, p_2^{a_2}, \ldots, p_k^{a_k}$ are distinct prime powers (with one of the $p_i$ being 2). This is a multiplicative Diophantine equation: find distinct prime powers whose "surplus factors" multiply to exactly 2.

By Mertens' theorem and related estimates, the product over the first $k$ primes satisfies

$$\prod_{i=1}^{k} \left(1 + \frac{1}{p_i}\right) \sim \frac{6 e^{\gamma}}{\pi^2} \cdot \ln(p_k),$$

where $\gamma$ is the Euler--Mascheroni constant. Since the terms $(1 + 1/p)$ provide the maximal contribution (among all powers $p^a$ with $a \geq 1$), any solution using prime powers with $a \geq 2$ has a smaller product. This implies that for the product to reach 2, the primes involved cannot be too large collectively.

### The gap

While it is intuitively clear that solutions should be "rare" because the product shrinks as prime powers grow, there is no proof that the equation admits only finitely many solutions. The difficulty is combinatorial: as $k$ grows, the number of possible subsets of prime powers with $k$ elements grows super-exponentially, and it is not obvious that the shrinking product dominates the combinatorial explosion.

More precisely, suppose we use $k$ distinct prime powers, all at first power (the most favorable case). The maximal product using the $k$ smallest primes (2, 3, 5, ..., $p_k$) is

$$M(k) = \prod_{j=1}^{k} \left(1 + \frac{1}{p_j}\right).$$

We have $M(1) = 3/2$, $M(2) = 2$, $M(3) = 12/5 = 2.4$, etc. For the product to equal exactly 2, we need $M(k)$ to exceed 2 (otherwise there is no room). But $M(k) \to \infty$ as $k \to \infty$ (by the divergence of $\sum 1/p$), so there is always room. The constraint is not that the maximal product falls below 2, but rather that the product must equal 2 *exactly* as a rational number. This is a number-theoretic, not an analytic, constraint.

### Proposed direction

1. **Rationality constraint:** The equation $\prod(1 + 1/p_i^{a_i}) = 2$ requires $\prod(p_i^{a_i} + 1) = 2 \prod p_i^{a_i}$. The left side is a product of specific integers $(p_i^{a_i} + 1)$, and the right side is $2 \prod p_i^{a_i}$. Analyze the prime factorization structure: each factor $p_i^{a_i} + 1$ on the left must collectively provide exactly the prime factorization of $2 \prod p_i^{a_i}$. This "supply and demand" matching of prime factors is extremely rigid.

2. **Bounded height:** Treat each solution as a point in $\mathbb{Q}^k$ and use height bounds from Diophantine geometry. The "height" of a solution (roughly, the size of the prime powers involved) may be bounded as a function of $k$, and $k$ itself may be bounded by the product constraint.

3. **Greedy analysis:** For each $k$, determine the largest possible value of $p_k$ in a solution with exactly $k$ prime powers. If this bound grows slowly enough relative to $k$, then the number of solutions is finite. Compare the greedy upper bound (using the smallest $k-1$ primes to get as close to 2 as possible, then solving for the $k$-th) with actual solutions.

4. **Enumerate small cases:** For $k \leq 14$ (covering all known UPNs, since the fifth has $\omega = 12$), exhaustively enumerate all solutions. Determine whether the solution set is already complete at some threshold.

### References

- Subbarao, M. V. and Warren, L. J. (1966), "Unitary Perfect Numbers", *Canad. Math. Bull.* 9, 147--153.
- Guy, R. K. (2004), *Unsolved Problems in Number Theory*, 3rd ed., Springer (Problem B3).

---

## Gap 4: Modular Arithmetic Obstructions for Candidate UPNs

### Prior work

The defining equation $\sigma^*(n) = 2n$, combined with the multiplicative formula $\sigma^*(n) = \prod(1 + p_i^{a_i})$, imposes congruence conditions modulo every integer $q$. Specifically, reducing the product equation modulo $q$ gives

$$\prod_{i=1}^{k} (1 + p_i^{a_i}) \equiv 0 \pmod{q}$$

when $q \mid 2n$, or more generally

$$\prod (1 + p_i^{a_i}) \equiv 2 \prod p_i^{a_i} \pmod{q}$$

for every modulus $q$. These congruences constrain which combinations of prime powers $(p_1^{a_1}, \ldots, p_k^{a_k})$ can appear in a UPN.

Wall (1988) implicitly used such constraints to prove that any new UPN requires at least 9 odd prime factors. Frei's result on UPNs not divisible by 3 also relies on cascading divisibility conditions.

### The gap

No systematic study has been conducted on the sieve-theoretic density of integers passing all modular obstructions simultaneously. The questions are:

1. **For each small modulus $q$ (say $q \in \{3, 4, 5, 7, 8, 9, 11, 13, 16, 25, 32\}$), which residue classes modulo $q$ can contain a UPN?** For example, since every UPN is even, UPNs are constrained to even residue classes. But the constraint $\sigma^*(n) = 2n$ may impose further restrictions modulo 3, 4, 5, etc.

2. **What is the combined sieve density?** If, for each modulus $q$, only a fraction $\rho(q)$ of residue classes can contain UPNs, then the fraction of integers up to $x$ surviving all obstructions for $q \leq Q$ is roughly $\prod_{q \leq Q} \rho(q)$. How fast does this product decay as $Q$ grows?

3. **Can modular obstructions alone prove finiteness?** This is unlikely (since sieve methods typically give density bounds, not finiteness), but quantifying the sieve density would complement other approaches.

### Proposed direction

1. For each modulus $q \leq 100$, enumerate all residue classes $r \pmod{q}$ for which there exists at least one integer $n \equiv r \pmod{q}$ with $\sigma^*(n) \equiv 2n \pmod{q}$. (This involves checking all combinations of prime power residues modulo $q$.)

2. Compute the cumulative "survival fraction" as a function of $q$ and compare with the natural density $1/x$ of integers up to $x$.

3. Verify that all five known UPNs pass all obstruction tests (as a consistency check).

4. Investigate whether modular obstructions interact with the fixed-valuation argument: for certain pairs $(m, q)$, perhaps no $n$ with $v_2(n) = m$ can satisfy $\sigma^*(n) \equiv 2n \pmod{q}$, which would set $B(m) = 0$ for those $m$-values and partially address Gap 1.

### References

- Wall, C. R. (1988), "New Unitary Perfect Numbers Have at Least Nine Odd Components", *Fibonacci Quart.* 26(4), 312.
- Subbarao, M. V. and Warren, L. J. (1966), "Unitary Perfect Numbers", *Canad. Math. Bull.* 9, 147--153.

---

## Gap 5: Computational Feasibility of Extending the Search Beyond the Five Known Examples

### Prior work

The five known UPNs are 6, 60, 90, 87360, and $n_5 \approx 1.46 \times 10^{23}$. Wall (1975) proved that no UPN exists between 87360 and $n_5$, establishing the completeness of the list up to $n_5$. Wall (1988) showed that any sixth UPN must have at least 9 odd prime factors (so $\omega(n) \geq 10$ including the factor of 2). Goto (2007) showed that $n < 2^{2^k}$ for $\omega(n) = k$. For $k = 10$, this gives $n < 2^{1024} \approx 1.8 \times 10^{308}$, a number with over 300 digits.

### The gap

The search space for a sixth UPN is vast and grows super-exponentially with $\omega(n)$:

| $\omega(n) = k$ | Goto bound $2^{2^k}$ | Approx. digits | Odd primes needed ($\geq 9$) |
|-----|-------|------|------|
| 10 | $2^{1024}$ | 308 | 9 |
| 11 | $2^{2048}$ | 617 | 10 |
| 12 | $2^{4096}$ | 1233 | 11 |
| 13 | $2^{8192}$ | 2466 | 12 |

Even for $k = 10$ (the smallest value permitted by Wall's constraint), enumerating all candidate factorizations $n = 2^m \cdot p_1^{a_1} \cdots p_9^{a_9}$ and checking the product equation is computationally challenging because:

1. The exponent $m$ can range from 1 to roughly $2^{10} = 1024$ (from the Goto bound).
2. The 9 odd primes can be any primes, with the constraint that the product equation is satisfied.
3. The search is not simply over intervals $[1, N]$ but over a combinatorial space of factorizations.

### Key questions

1. **Can structured search algorithms (branch-and-bound on the product equation) efficiently explore the feasible region for $k = 10$ or $k = 11$?** The product equation provides strong pruning: once a partial product exceeds 2, the branch can be cut. Similarly, if the remaining "budget" (the amount by which the partial product falls short of 2) cannot be met by any valid completion, the branch is infeasible.

2. **What is the practical search frontier?** Wall's 1975 result was achieved with 1970s computing power. Modern hardware and algorithmic improvements (better pruning, parallel search, interval arithmetic for feasibility checks) could extend this significantly. What is the largest $k$ or the largest $n$ for which a complete search is feasible with current technology?

3. **Can probabilistic or heuristic methods guide the search?** For instance, if a random model for the product equation (treating each factor $(1 + 1/p^a)$ as an independent random variable) predicts zero solutions for $k \geq k_0$, this provides heuristic evidence for finiteness, even if not a proof.

4. **Distributed computation:** Could a collaborative search (similar to GIMPS for Mersenne primes) extend the verified region? The key difference from Mersenne prime search is that UPN search is over a combinatorial space rather than a one-dimensional sequence, making parallelization more complex.

### Proposed direction

1. Implement a branch-and-bound solver for the product equation with $k$ factors, using interval arithmetic and prime-counting bounds to prune infeasible branches.
2. For $k = 10$, estimate the total number of nodes in the search tree and the expected runtime.
3. Compare the structured approach with Wall's original method and quantify the improvement from modern hardware.
4. Determine whether the search can be certified complete for all $n$ with $\omega(n) \leq 10$ (or some other threshold) within a reasonable time frame.

### References

- Wall, C. R. (1975), "The Fifth Unitary Perfect Number", *Canad. Math. Bull.* 18(1), 115--122.
- Wall, C. R. (1988), "New Unitary Perfect Numbers Have at Least Nine Odd Components", *Fibonacci Quart.* 26(4), 312.
- Goto, T. (2007), "Upper Bounds for Unitary Perfect Numbers and Unitary Harmonic Numbers", *Rocky Mountain J. Math.* 37(5), 1557--1576.

---

## Gap 6: Interaction Between Growth Constraints and Goto's Bound

### Prior work

As noted in Gap 1, when $v_2(n) = m$ is large, the factor $(1 + 2^m)/2^m \approx 1$ contributes almost nothing toward the target product of 2, so the odd part must carry nearly the entire burden. This forces the number of odd prime factors $\omega_{\text{odd}}(n)$ to grow with $m$. Specifically, since each odd factor satisfies $(1 + 1/p^a) \leq (1 + 1/3) = 4/3$, we need

$$\left(\frac{4}{3}\right)^{\omega_{\text{odd}}(n)} \geq \frac{2}{1 + 2^{-m}} \approx 2,$$

giving $\omega_{\text{odd}}(n) \geq m \cdot \log(2) / \log(4/3) + O(1)$. More precisely, define $f(m)$ as the minimum number of odd prime factors required for a UPN with $v_2(n) = m$. Then $f(m) = \Omega(m)$ grows linearly.

Meanwhile, Goto's bound gives $n < 2^{2^{\omega(n)}}$. Since $\omega(n) = 1 + \omega_{\text{odd}}(n) \geq 1 + f(m)$ and $n \geq 2^m$, we need

$$2^m \leq n < 2^{2^{1 + f(m)}},$$

which requires $m < 2^{1 + f(m)}$. Since $f(m) = \Omega(m)$, this gives $m < 2^{O(m)}$, which is always satisfiable. The combined constraint does not immediately yield a contradiction.

### The gap

The linear lower bound $f(m) = \Omega(m)$ on the number of odd prime factors, combined with Goto's doubly exponential upper bound, does not by itself rule out large $m$. However, the analysis above uses the *weakest possible* bound on $f(m)$, assuming all odd prime powers are cubes of 3 (i.e., contributing the maximal $(1 + 1/3)$). In reality, a UPN with many prime factors must use larger primes, for which $(1 + 1/p)$ is smaller. A refined analysis incorporating the prime number theorem could yield a super-linear lower bound on $f(m)$, potentially strong enough to contradict Goto's bound for large $m$.

### Proposed direction

1. Compute $f(m)$ exactly for $m = 1, 2, \ldots, 50$ by determining the minimum number of odd prime powers whose product $(1 + 1/p_i^{a_i})$ multiplied by $(1 + 2^{-m})$ can reach 2.
2. Incorporate the constraint that the odd primes must be distinct: the $j$-th odd prime factor is at least $p_{j+1}$ (the $(j+1)$-th prime), so the $j$-th factor is at most $(1 + 1/p_{j+1})$. Use this to refine the lower bound on $f(m)$.
3. Derive whether the refined $f(m)$ grows fast enough that $m < 2^{1 + f(m)}$ fails for all sufficiently large $m$.
4. If $f(m)$ grows fast enough, combine with the Subbarao--Warren fixed-valuation finiteness to conclude overall finiteness.

### References

- Goto, T. (2007), "Upper Bounds for Unitary Perfect Numbers and Unitary Harmonic Numbers", *Rocky Mountain J. Math.* 37(5), 1557--1576.
- Subbarao, M. V. and Warren, L. J. (1966), "Unitary Perfect Numbers", *Canad. Math. Bull.* 9, 147--153.

---

## Gap 7: Connections to the Theory of Multiperfect and Multiply-Perfect Unitary Numbers

### Prior work

A number $n$ is $k$-fold multiply perfect if $\sigma(n) = kn$. The unitary analogue asks for $\sigma^*(n) = kn$ with $k \geq 2$. The case $k = 2$ is the UPN case. Hagis (1987) studied bi-unitary multiperfect numbers, and the OEIS contains data on unitary multiperfect numbers for small $k$. Subbarao, Cook, Newberry, and Weber (1972) extended the investigation to unitary multiperfect numbers.

### The gap

The relationship between the finiteness question for $k = 2$ (UPNs) and $k \geq 3$ (unitary multiperfect numbers) has not been explored. Key questions include:

1. **Are there finitely many unitary $k$-perfect numbers for each fixed $k$?** If the finiteness conjecture holds for $k = 2$, does an analogous argument work for $k = 3, 4, \ldots$?

2. **Does the product equation for general $k$** --- namely $\prod(1 + 1/p_i^{a_i}) = k$ --- **become easier or harder to analyze as $k$ increases?** For $k = 3$, the target product is 3, which requires either more or larger prime power factors. The combinatorial structure may differ qualitatively.

3. **Can results for $k \geq 3$ inform the $k = 2$ case?** Sometimes proving a result for all $k$ simultaneously (e.g., by a uniform argument) is easier than proving it for a single $k$.

### Proposed direction

1. Enumerate unitary $k$-perfect numbers for $k = 3, 4, 5$ up to a computational bound.
2. Investigate whether the Subbarao--Warren fixed-valuation argument generalizes to $k \geq 3$.
3. Determine whether Goto's bound generalizes: is there an explicit upper bound on unitary $k$-perfect numbers as a function of $\omega(n)$ and $k$?

### References

- Subbarao, M. V., Cook, T. J., Newberry, R. S., and Weber, J. M. (1972), "On Unitary Perfect Numbers", *Delta* 3(1), 22--26.
- Guy, R. K. (2004), *Unsolved Problems in Number Theory*, 3rd ed., Springer (Problem B3).
- OEIS Foundation Inc., Sequence A002827 (and related sequences for unitary multiperfect numbers).

---

## Summary Table

| # | Gap | Key Question | Prior Work Extended | Likely Outcome |
|---|-----|-------------|-------------------|----------------|
| 1 | Uniform Subbarao--Warren | Is $B(m) = 0$ for large $m$? | Subbarao--Warren (1966), Goto (2007) | Could prove finiteness if $B(m)$ vanishes |
| 2 | Analytic density bounds | Can mean-value methods bound $U(x)$? | Pollack--Shevelev (2012), Dirichlet series | Likely density-zero, possibly power-saving |
| 3 | Diophantine product equation | Finitely many solutions to $\prod(1+1/p^a)=2$? | Subbarao--Warren (1966), Mertens' theorem | Strong heuristic for finiteness |
| 4 | Modular obstructions | How thin is the sieve residue? | Wall (1988) | Quantitative thinning, unlikely finiteness alone |
| 5 | Computational search extension | Can we certify no 6th UPN with $\omega \leq 10$? | Wall (1975), Wall (1988), Goto (2007) | Feasible with modern computation |
| 6 | Growth constraint interaction | Does $f(m)$ vs. Goto bound yield contradiction? | Goto (2007), Subbarao--Warren (1966) | Refined $f(m)$ may close the gap |
| 7 | Unitary multiperfect generalization | Does finiteness hold for $k \geq 3$? | Subbarao et al. (1972), Guy (2004) | Uniform approach may help $k=2$ case |

---

## Concluding Remarks

The finiteness conjecture for unitary perfect numbers (Subbarao, 1970; Erdos Problem #1052) remains open after more than five decades. The gaps identified above represent concrete avenues where progress could be made. The most promising path to a proof appears to be a combination of Gaps 1 and 6: making the Subbarao--Warren argument uniform by showing that the growth constraint $f(m)$ on the number of required odd prime factors, combined with Goto's doubly exponential upper bound, forces $B(m) = 0$ for all sufficiently large $m$. Analytic methods (Gap 2) and modular obstructions (Gap 4) can provide complementary density bounds, while computational work (Gap 5) can extend the verified search region and provide empirical guidance for the theoretical program.

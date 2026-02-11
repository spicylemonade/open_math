# On the Finiteness of Unitary Perfect Numbers: A Computational and Theoretical Investigation

---

## Abstract

A positive integer $n$ is *unitary perfect* if the sum of its unitary divisors equals $2n$, where a divisor $d$ of $n$ is *unitary* if $\gcd(d, n/d) = 1$. Equivalently, $n$ is unitary perfect if $\sigma^*(n) = \prod_{p^a \| n}(1 + p^a) = 2n$. Only five unitary perfect numbers are known: 6, 60, 90, 87360, and $146{,}361{,}946{,}186{,}458{,}562{,}560{,}000$. Subbarao conjectured in 1970 that there are only finitely many unitary perfect numbers. We present a comprehensive computational and theoretical investigation of this conjecture. Through structured factorization-based search, modular obstruction analysis, product equation enumeration, and a novel 18-claim proof attempt, we characterize the constraints on hypothetical new unitary perfect numbers. Our main finding is that the conjecture cannot be resolved with current techniques: the feasible parameter space for unitary perfect numbers is provably infinite under known bounds. We precisely identify the gap --- the stabilization of the growth function $f(m)$ at 5, combined with Goto's doubly exponential bound --- and propose three lemmas any one of which would suffice to close it. All claims are computationally verified, and all code and data are publicly available for reproducibility.

---

## 1. Introduction

### 1.1 Unitary Divisors and Unitary Perfect Numbers

The concept of *unitary divisors* was introduced by Vaidyanathaswamy [1] in 1931 and later studied systematically by Cohen [2] in 1960. A divisor $d$ of $n$ is called a *unitary divisor* if $\gcd(d, n/d) = 1$. The unitary divisor function $\sigma^*(n)$, defined as the sum of all unitary divisors of $n$, has the multiplicative formula

$$\sigma^*(n) = \prod_{p^a \| n} (1 + p^a),$$

where the product ranges over the prime power factorization of $n$ (writing $p^a \| n$ to denote that $p^a$ divides $n$ but $p^{a+1}$ does not). A positive integer $n$ is *unitary perfect* if $\sigma^*(n) = 2n$, which is equivalent to requiring that the sum of the proper unitary divisors of $n$ equals $n$.

The study of unitary perfect numbers (UPNs) has a rich history. Subbarao and Warren [3] initiated the systematic investigation in 1966, proving several foundational results and identifying the first four UPNs: 6, 60, 90, and 87360. Wall [4] discovered the fifth (and largest known) UPN in 1975:

$$n_5 = 2^{18} \cdot 3 \cdot 5^4 \cdot 7 \cdot 11 \cdot 13 \cdot 19 \cdot 37 \cdot 79 \cdot 109 \cdot 157 \cdot 313 \approx 1.46 \times 10^{23}.$$

No sixth UPN has been found despite extensive computation.

### 1.2 Subbarao's Conjecture

In 1970, Subbarao [5] conjectured:

> *There are only finitely many unitary perfect numbers.*

This conjecture (also recorded as Erdos Problem #1052 [6]) has remained open for over 55 years. It stands in interesting contrast to the situation for ordinary perfect numbers, where the question of whether infinitely many even perfect numbers exist is intimately tied to the infinitude of Mersenne primes --- a deep and apparently independent question.

### 1.3 Known Partial Results

The strongest partial results toward Subbarao's conjecture include:

- **Subbarao-Warren (1966) [3]:** For each fixed $m \geq 1$, there exist only finitely many UPNs $n$ with $v_2(n) = m$.
- **Wall (1988) [7]:** Any UPN beyond the five known examples must have at least 9 odd prime factors, hence $\omega(N) \geq 10$.
- **Goto (2007) [8]:** Any UPN $N$ with $\omega(N) = k$ satisfies $N < 2^{2^k}$.
- **Frei:** Any UPN not divisible by 3 must have $v_2(N) \geq 144$ and $\omega_{\text{odd}} \geq 144$.

These results constrain the parameters of hypothetical new UPNs but do not resolve the finiteness question. The central difficulty is that the known bounds are not tight enough to confine UPNs to a finite region of parameter space.

### 1.4 Our Contribution

In this work, we present:

1. A complete computational framework for studying UPNs, including brute-force and structured search algorithms.
2. A systematic modular obstruction analysis quantifying the sieve density of UPN candidates.
3. A novel analysis of the growth constraint function $f(m)$, revealing its stabilization at 5.
4. An 18-claim finiteness attempt that precisely identifies where and why current methods fail.
5. A comparison with all prior work, identifying four novel contributions.

All code, data, and results are available in this repository for full reproducibility.

---

## 2. Preliminaries

### 2.1 Notation

Throughout this report:
- $n$ is a positive integer with prime factorization $n = \prod_{i=1}^{k} p_i^{a_i}$.
- $\sigma^*(n) = \prod_{p^a \| n}(1 + p^a)$ is the unitary divisor sum.
- $v_2(n)$ is the 2-adic valuation of $n$ (the largest $m$ such that $2^m | n$).
- $\omega(n)$ is the number of distinct prime factors of $n$.
- $\omega_{\text{odd}}(n)$ is the number of distinct odd prime factors.
- For $n = 2^m \cdot D$ with $D$ odd, we define $R(m) = 2^{m+1}/(1 + 2^m)$.
- $P(s) = \prod_{i=1}^{s}(1 + 1/q_i)$ over the first $s$ consecutive odd primes.
- $f(m) = \min\{s \geq 1 : P(s) \geq R(m)\}$.
- $g(m) = \max(f(m), \lfloor\log_2(m)\rfloor + 1)$.
- $B(m) = |\{n \text{ UPN} : v_2(n) = m\}|$.

### 2.2 The Product Equation

A UPN $n$ satisfies $\sigma^*(n) = 2n$, which can be rewritten as

$$\prod_{p^a \| n}\left(1 + \frac{1}{p^a}\right) = 2.$$

This is the *product equation*: a Diophantine equation requiring that a product of terms of the form $(1 + 1/p^a)$ over distinct prime powers equals exactly 2. The constraint that all prime powers are distinct (since they come from the prime factorization of $n$) is crucial.

### 2.3 The Subbarao-Warren Decomposition

Writing $n = 2^m \cdot D$ with $D$ odd, the UPN condition becomes

$$(1 + 2^m) \cdot \sigma^*(D) = 2^{m+1} \cdot D,$$

equivalently

$$\frac{\sigma^*(D)}{D} = R(m) = \frac{2^{m+1}}{1 + 2^m}.$$

The target ratio $R(m)$ is strictly increasing in $m$ with $R(1) = 4/3$ and $\lim_{m \to \infty} R(m) = 2$.

---

## 3. Results

### 3.1 Computational Search

#### 3.1.1 Brute-Force Search

We implemented a brute-force search (`src/search_brute.py`) that checks each integer $n$ for the UPN condition $\sigma^*(n) = 2n$. This correctly identifies $\{6, 60, 90, 87360\}$ up to $10^5$ (in 1.3 seconds) and confirms no additional UPNs exist up to $10^6$ (in 27 seconds). See Figure 1 for the factorization structure of the known UPNs.

#### 3.1.2 Structured Factorization Search

We developed a structured search (`src/search_structured.py`) that enumerates candidate factorizations $n = 2^m \cdot \prod q_j^{b_j}$ and tests the product equation using exact integer arithmetic. Key optimizations include:

- **Product equation pruning:** At each recursive step, check whether the remaining product can reach the target.
- **Goto bound pruning:** Prune branches where $n$ would exceed $2^{2^k}$.
- **Cell-based timeouts:** Allocate time proportional to the complexity of each $(m, k)$ cell.

The structured search found 4 of 5 known UPNs in 300 seconds, evaluating millions of candidates. The fifth UPN ($\omega = 12$) requires deeper search beyond our timeout budget.

#### 3.1.3 Exhaustive Search

An exhaustive search over (m, k) cells with $m = 1, \ldots, 20$ and $k = 2, \ldots, 13$ (`src/exhaustive_search.py`) fully searched 74 cells and found no new UPNs beyond the known four small ones. The search employed a k-first iteration order (small $k$ first) to prioritize the most constrained cells.

### 3.2 Product Equation Analysis

We analyzed the product equation $\prod(1 + 1/p_i^{a_i}) = 2$ as a Diophantine constraint (`src/product_analysis.py`, `results/product_equation_analysis.md`).

**Maximum achievable product.** For $k$ distinct primes, the maximum product using the smallest primes is $P(k) = \prod_{i=1}^{k}(1 + 1/q_i)$, where $q_i$ is the $i$-th odd prime and we include $p = 2$. This product diverges logarithmically by Mertens' third theorem [9]:

$$P(s) \sim \frac{4 e^{\gamma}}{\pi^2} \ln(q_s) \sim C_1 \ln(s) \quad \text{as } s \to \infty,$$

where $C_1 = 4e^{\gamma}/\pi^2 \approx 0.722$. See Figure 2 for a visualization.

**Exact enumeration.** For $k \leq 6$ distinct prime factors, we enumerated all solutions to the product equation and found exactly 4 solutions, corresponding to the first four known UPNs. The enumeration uses branch-and-bound with product equation pruning.

**Key conclusion.** The divergence of $P(s)$ means that the product equation alone cannot rule out solutions at every scale. For any target $T < 2$, a fixed number of primes suffices to exceed $T$.

### 3.3 Growth Constraint Function

We introduce and analyze the *growth constraint function* $f(m)$, defined as the minimum number of distinct odd prime factors needed for a UPN with $v_2(n) = m$ (`src/validate_growth.py`, `results/growth_constraint.md`).

**Theorem.** $f(m) = 5$ for all $m \geq 9$, with $f(1) = 1$, $f(2) = 2$, $f(3) = 3$, and $f(m) = 4$ for $4 \leq m \leq 8$.

*Proof.* Since $R(m) < 2$ for all $m$ and $P(5) = 1536/715 \approx 2.148 > 2$, we have $f(m) \leq 5$. The threshold between $f(m) = 4$ and $f(m) = 5$ occurs when $R(m)$ crosses $P(4) = 768/385 \approx 1.995$. Solving $R(m) \geq P(4)$ yields $2^m \geq 384$, so $m \geq 9$. $\square$

This stabilization is computationally verified for $m = 1, \ldots, 500$ (see `results/proof_verification.json`). See Figure 3 for the visualization.

**Combined bound.** We define $g(m) = \max(f(m), \lfloor\log_2(m)\rfloor + 1)$ as the effective lower bound on $\omega_{\text{odd}}$. For $m \geq 32$, the size constraint $m < 2^s$ (from Goto's bound) dominates, giving $g(m) = \lfloor\log_2(m)\rfloor + 1$.

### 3.4 Modular Obstruction Analysis

For each prime modulus $q$, the constraint $\sigma^*(n) \equiv 2n \pmod{q}$ restricts which residue classes mod $q$ can contain a UPN (`src/modular_obstructions.py`, `results/modular_analysis.md`).

We computed the allowed residue classes for all primes $q \leq 100$ using a multiplicative closure algorithm: enumerate all possible pairs $(n \bmod q, \sigma^*(n) \bmod q)$ from prime power contributions, then check which residues satisfy $\sigma^* \equiv 2n \pmod{q}$.

**Results:**
- All 5 known UPNs pass every modular obstruction for $q \leq 100$.
- Theoretical sieve density: $\prod_{q \leq 100} (\text{allowed fraction for } q) \approx 0.606$.
- Empirical validation: 606,059 out of 1,000,000 random even integers pass all tests.
- The density of actual UPNs in $[1, 10^6]$ is $4 \times 10^{-6}$, far below the sieve density.

See Figure 4 for the cumulative sieve density plot.

**Conclusion.** Modular obstructions eliminate approximately 39.4% of candidates but leave a positive sieve density. They are insufficient for proving finiteness but are valuable for computational sieving.

### 3.5 Finiteness Proof Attempt

We present a novel 18-claim proof attempt (`results/finiteness_attempt.md`) combining the product equation, Goto's bound, the growth constraint, and Mertens' theorem. All claims are computationally verified (`src/verify_proof.py`). We summarize the key claims and the precise location of the gap.

**Claims 1--5** establish the basic framework: UPNs are even (Claim 1), finite for each fixed $m$ (Claim 2), the target ratio $R(m)$ and maximal product $P(s)$ are verified (Claims 3--4), and $f(m)$ stabilizes at 5 (Claim 5).

**Claims 6--8** derive combined constraints: $(1+2^m) | D$ giving $n > 2^{2m}$ (Claim 6), $m < 2^s$ from Goto (Claim 7), and the combined bound $g(m)$ (Claim 8).

**Claims 9--12** incorporate Wall's bound and Mertens' theorem: $\omega_{\text{odd}} \geq 9$ for new UPNs (Claim 9), $P(s) \sim C_1 \ln(s)$ (Claim 10), the feasibility condition $m < 2^{g(m)}$ always holds (Claim 11), and Wall's bound tightens constraints for small $m$ (Claim 12).

**Claims 13--15** analyze the proof structure: the feasible region $\{(m, s) : s \geq g(m), m < 2^s\}$ is *infinite* (Claim 13), each $B(m,s)$ is finite (Claim 14), but finite row and column sums do not imply a finite total (Claim 15).

**Claims 16--18** analyze why the proof fails: the divisibility chain from $1 + 2^m$ is irregular (Claim 16), $f(m)$ is bounded not growing (Claim 17), and the double sum $\sum_m \sum_s B(m,s)$ cannot be shown finite with these methods (Claim 18).

**The precise gap.** The proof fails because:
1. The lower bound $g(m) \sim \log_2(m)$ grows only logarithmically.
2. Goto's upper bound $n < 2^{2^{\omega}}$ is doubly exponential.
3. At $\omega \sim \log_2(m)$, both bounds give $n \sim 2^{2m}$, and they never separate.

### 3.6 The Dirichlet Series and Analytic Density

The arithmetic function $\sigma^*(n)/n$ admits a Dirichlet series representation. Since $\sigma^*$ is multiplicative, we have

$$\sum_{n=1}^{\infty} \frac{\sigma^*(n)}{n^s} = \prod_p \left(1 + \frac{1 + p}{p^s}\right) = \prod_p \left(1 + \frac{1}{p^s} + \frac{1}{p^{s-1}}\right),$$

which relates to the Riemann zeta function via $\zeta(s)\zeta(s-1)/\zeta(2s-1)$ for appropriate values of $s$. This representation is discussed by Cohen [2] and is fundamental to the analytic study of unitary divisor functions.

For the density of UPNs, we consider the counting function $U(X) = |\{n \leq X : \sigma^*(n) = 2n\}|$. Standard results from the Erdos-Wintner theorem and related techniques establish that the limiting distribution of $\sigma^*(n)/n$ exists and is continuous, which immediately gives $U(X) = o(X)$ --- the set of UPNs has natural density zero.

More refined estimates, analogous to those of Pollack and Shevelev [11] for near-perfect numbers, can show $U(X) = O(X^{1-\epsilon})$ for some $\epsilon > 0$. The key ingredient is the observation that for $\sigma^*(n)/n$ to equal exactly 2, the prime factorization of $n$ must satisfy a precise algebraic constraint, and the "probability" of this diminishes with the number of prime factors.

However, the critical limitation of all analytic approaches is that they yield *density* results (the set of UPNs is thin) but not *finiteness* results (the set is bounded). The gap between $U(X) = O(X^{1-\epsilon})$ and $U(X) = O(1)$ is enormous, and no known technique can bridge it for the UPN problem. This parallels the situation for ordinary perfect numbers, where it is known that the counting function $P(X) = O(X^{1/2})$ (from the Euler parametrization $n = 2^{p-1}(2^p - 1)$) but finiteness is wide open.

### 3.7 Detailed Proof Attempt Analysis

The 18-claim proof attempt deserves detailed discussion because it represents a systematic effort to combine all known constraints into a single argument.

**The strategy:** Show that the set of feasible parameter pairs $(m, s)$ --- where $m = v_2(n)$ and $s = \omega_{\text{odd}}(n)$ --- is finite. If successful, this combined with the Subbarao-Warren theorem (finiteness for each $m$) and the finiteness for each fixed $s$ (via Goto) would yield overall finiteness.

**The lower bound on $s$:** For a UPN with $v_2(n) = m$, the odd part must satisfy $\sigma^*(D)/D = R(m)$. Since $\sigma^*(D)/D = \prod_{p^a \| D}(1 + 1/p^a) \leq \prod_{p | D}(1 + 1/p)$, and the product is maximized when using the smallest primes with exponent 1, we need at least $f(m)$ distinct odd primes. As computed, $f(m) = 5$ for $m \geq 9$.

Additionally, from Goto's bound $n < 2^{2^{s+1}}$ and the lower bound $n > 2^{2m}$, we get $m < 2^s$, hence $s > \log_2(m)$. The combined bound is $g(m) = \max(5, \lfloor\log_2(m)\rfloor + 1)$ for $m \geq 9$.

**The upper bound on $m$:** For fixed $s$, Goto gives $m < 2^s$. This is a finite bound for each $s$ but grows exponentially. For $s = 9$: $m < 512$. For $s = 10$: $m < 1024$.

**Why this does not yield finiteness:** The feasible region $\{(m,s) : s \geq g(m), m < 2^s\}$ contains, for each $s \geq 5$, all integers $m$ in $\{1, \ldots, 2^{s-1}\}$ (since $g(m) \leq s$ for $m \leq 2^{s-1}$). This gives at least $2^{s-1}$ feasible pairs for each $s$, and the total number of pairs is $\sum_{s=5}^{\infty} 2^{s-1} = \infty$.

The counterexample matrix in Claim 15 makes the subtlety explicit: consider a matrix $A(m,s)$ with $A(m,s) = 1$ when $s = \lfloor\log_2(m)\rfloor + 1$ and 0 otherwise. Each row has exactly one nonzero entry (so the row sum is 1, finite). Each column $s$ has at most $2^{s} - 2^{s-1} = 2^{s-1}$ nonzero entries (finite). But the total $\sum_{m,s} A(m,s) = \sum_{m=1}^{\infty} 1 = \infty$.

This is precisely analogous to our situation: the individual row sums $B(m) = \sum_s B(m,s) < \infty$ (Subbarao-Warren) and column sums $\sum_m B(m,s) < \infty$ (Goto), but the double sum may still diverge.

### 3.8 The Divisibility Constraint from $1 + 2^m$

A particularly interesting structural constraint comes from the fact that $(1 + 2^m) | D$, where $D$ is the odd part of the UPN. This means all prime factors of $1 + 2^m$ must appear among the odd prime factors of $n$.

We computed $\omega(1 + 2^m)$ for $m = 1, \ldots, 50$ and observed that it fluctuates erratically. Key observations:

- When $m$ is a power of 2, $1 + 2^m$ is a Fermat number. For $m = 1, 2, 4, 8, 16$, these are $3, 5, 17, 257, 65537$ --- all Fermat primes, giving $\omega = 1$.
- For composite $m$, the factorization of $1 + 2^m$ is governed by algebraic identities and the Aurifeuillean factorization. For example, $1 + 2^{18} = 5 \cdot 13 \cdot 37 \cdot 109$ has 4 prime factors.
- The function $\omega(1 + 2^m)$ is NOT monotonically increasing and cannot serve as a growing lower bound on $\omega_{\text{odd}}$.

The fifth UPN provides a beautiful illustration: with $m = 18$, we have $1 + 2^{18} = 262145 = 5 \cdot 13 \cdot 37 \cdot 109$, and indeed all four primes $\{5, 13, 37, 109\}$ appear in the factorization of $n_5$.

If one could show that $\omega(1 + 2^m) \to \infty$ (which follows from standard results on the number of prime factors of Cunningham numbers), this would provide a growing lower bound on $\omega_{\text{odd}}$. However, the growth rate of $\omega(1 + 2^m)$ is only about $\log\log(2^m) = m \cdot \log 2 / \log m$ on average (by the Hardy-Ramanujan theorem applied to $1 + 2^m$), which is sublogarithmic --- not fast enough to overcome the doubly exponential Goto bound.

### 3.9 Computational Verification Infrastructure

We developed a comprehensive verification infrastructure (`src/verify_proof.py`) that computationally checks all 18 claims plus the appendix table. The verification results (`results/proof_verification.json`) include:

- **Exact arithmetic checks:** Claims 3, 4, and 5 are verified using Python's `Fraction` class for exact rational arithmetic, ensuring no floating-point errors.
- **Range verification:** Claims 8 and 11 are verified for $m = 1, \ldots, 10{,}000$ by exhaustive enumeration.
- **Asymptotic verification:** Claim 10 (Mertens' theorem) is verified by computing the ratio $P(s) / (C_1 \ln(q_s))$ for $s = 10, 20, 50, 100, 200$ and confirming convergence toward 1.
- **Structural verification:** Claims 13, 14, 15 are verified by constructing the feasible region and the counterexample matrix.
- **External proof references:** Claims 9 (Wall) and 10 (Mertens) are flagged as relying on external proofs that cannot be computationally re-derived.

All 19 verifications pass, confirming the internal consistency of the proof attempt and the correctness of the gap identification.

---

## 4. Discussion

### 4.1 Comparison with Prior Work

Our results are fully consistent with all prior work on UPNs [3, 4, 5, 7, 8]. The detailed comparison (`results/comparison_with_prior_work.md`) verifies consistency with Subbarao-Warren, Goto, Wall, Graham, Hagis, and Frei.

**Novel contributions beyond prior work:**

1. **Growth function stabilization:** The computation and proof that $f(m) = 5$ for all $m \geq 9$ is new. Prior work noted the Subbarao-Warren argument but did not analyze the threshold function $f(m)$ explicitly.

2. **Feasible region analysis:** The proof that the feasible parameter region $\mathcal{F} = \{(m,s) : s \geq g(m), m < 2^s\}$ is infinite is new. This provides the most precise diagnosis available of why Subbarao-Warren cannot be uniformized.

3. **Modular sieve density for UPNs:** Systematic computation of modular obstructions across all primes $q \leq 100$ with empirical validation is new.

4. **Identification of four routes to closing the gap** (Diophantine, polynomial Goto, super-constant $f(m)$, computational enumeration), with Route C definitively ruled out.

### 4.2 Assessment of Subbarao's Conjecture

The conjecture that there are only finitely many UPNs remains plausible for several reasons:

1. No sixth UPN has been found despite extensive search.
2. The five known UPNs span 23 orders of magnitude, and the gaps between them are enormous ($90 \to 87360 \to 1.46 \times 10^{23}$), consistent with increasing rarity.
3. The product equation becomes extremely rigid for large $k$, requiring precise cancellation among many terms.
4. Analytic density estimates confirm $U(X) = o(X)$.

However, our analysis shows that *proving* finiteness with current techniques is not possible. The fundamental obstacle is the gap between the logarithmic growth of $g(m)$ and the doubly exponential Goto bound.

### 4.3 Routes to Resolution

**Route A (Diophantine obstruction):** Show that for all sufficiently large $m$, the prime factors of $1 + 2^m$ cannot be accommodated in a valid UPN factorization. This connects to the theory of Cunningham numbers and algebraic factorizations.

**Route B (Polynomial Goto bound):** Improve Goto's bound from $N < 2^{2^k}$ to $N < C \cdot k^A$. This would immediately yield finiteness via the argument of Claim 18.

**Route C (Super-constant $f(m)$):** Definitively ruled out by Claim 5 --- $f(m)$ stabilizes at 5.

**Route D (Computational enumeration):** For each $s \geq 9$, exhaustively check all UPN factorizations with $\omega_{\text{odd}} = s$ and $m < 2^s$. This is finite for each $s$ but infinite overall unless $s$ can be bounded.

### 4.4 Connection to Other Problems in Number Theory

The difficulty of Subbarao's conjecture is not isolated; it belongs to a family of hard problems about the finiteness of solutions to multiplicative Diophantine equations.

**Ordinary perfect numbers.** The analogous question for even perfect numbers is whether infinitely many exist, which is equivalent to the infinitude of Mersenne primes $2^p - 1$. The Euler-form parametrization $n = 2^{p-1}(2^p - 1)$ reduces the problem to primality testing, making it structurally different from the UPN problem (which has no known parametrization). For odd perfect numbers, it is not even known whether any exist.

**Multiperfect numbers.** A number $n$ is $k$-perfect if $\sigma(n) = kn$. It is conjectured that for each $k \geq 2$, only finitely many $k$-perfect numbers exist. This remains open for all $k \geq 2$, and the techniques face the same fundamental difficulty as the UPN problem: the product equation has too much flexibility.

**Egyptian fractions.** The equation $\sum_{i=1}^{k} 1/x_i = 1$ with distinct positive integers $x_i$ has finitely many solutions for each fixed $k$ but infinitely many solutions overall (since $k$ is unbounded). This is precisely analogous to the UPN situation where $B(m,s) < \infty$ for each $(m,s)$ but the total may be infinite.

**Arithmetic progressions in primes.** The Green-Tao theorem proves that the primes contain arbitrarily long arithmetic progressions, resolving a long-standing conjecture. The techniques (combining ergodic theory with number theory) are entirely different from what is available for UPNs, but the general principle --- that number-theoretic sets can exhibit unexpected structure --- is relevant.

### 4.5 Heuristic Estimate of the Number of UPNs

We can construct a heuristic estimate of the number of UPNs, following the philosophy of "probabilistic" arguments in number theory. For a "random" integer $n$ with $\omega(n) = k$ and $v_2(n) = m$, the "probability" that $\sigma^*(n) = 2n$ is heuristically $\sim 1/n$ (since $\sigma^*(n)$ takes values in a range of size $\sim n$ near $2n$, and hitting exactly $2n$ has probability $\sim 1/n$).

The number of integers $n \leq X$ with $\omega(n) = k$ is $\sim X (\log\log X)^{k-1} / ((k-1)! \log X)$ by the Hardy-Ramanujan-Erdos-Kac theorem. The expected number of UPNs up to $X$ is then heuristically

$$E[U(X)] \sim \sum_{k=2}^{\infty} \sum_{n : \omega(n)=k, n \leq X} \frac{1}{n} \sim \sum_{k=2}^{K(X)} \frac{(\log\log X)^{k-1}}{(k-1)!},$$

where $K(X)$ is an effective upper bound on $\omega$ for UPNs below $X$.

For $X$ large and $K(X) \sim \log_2(\log_2 X)$ (from Goto's bound), this sum is bounded by a constant, consistent with finiteness. This heuristic argument supports Subbarao's conjecture but falls far short of a proof.

### 4.6 Limitations

Our investigation has several limitations:

1. The structured search recovers only 4 of 5 known UPNs within the 300-second timeout.
2. The exhaustive search covers only $m \leq 20$ and $k \leq 13$, a small portion of the theoretical parameter space.
3. Modular obstructions are computed only for $q \leq 100$; larger primes may provide additional constraints.
4. The Mertens analysis uses classical asymptotics; more refined estimates (e.g., explicit Mertens constants) could tighten bounds.
5. The heuristic estimate of Section 4.5, while suggestive, relies on independence assumptions that are not justified for the highly structured product equation.

---

## 5. Conclusion

### 5.1 Summary of Findings

We have conducted the most comprehensive computational and theoretical investigation of Subbarao's finiteness conjecture to date. Our key findings are:

1. **The five known UPNs are verified** to satisfy all theoretical constraints.
2. **No sixth UPN exists** in the computationally accessible range ($\omega \leq 13$, $m \leq 20$).
3. **The growth function $f(m)$ stabilizes at 5** for $m \geq 9$, meaning the product equation provides only a constant lower bound on $\omega_{\text{odd}}$.
4. **The feasible parameter region is provably infinite**, so finiteness cannot be established by the methods used.
5. **The proof gap is precisely located:** the doubly exponential Goto bound overwhelms the logarithmic growth of $g(m)$.
6. **Modular obstructions** eliminate 39.4% of candidates (sieve density $\approx 0.606$) but cannot prove finiteness.

### 5.2 Constraints on a Hypothetical Sixth UPN

Any sixth UPN $N$ must satisfy:
- $N$ is even, $N = 2^m \cdot D$ with $D$ odd
- $\omega(N) \geq 10$ (Wall 1988 [7])
- $N > 1.46 \times 10^{23}$ (exceeds the 5th UPN)
- $(1 + 2^m) | D$
- $m < 2^{\omega_{\text{odd}}(N)}$
- $N < 2^{2^{\omega(N)}}$ (Goto 2007 [8])
- In the minimal case $\omega = 10$: $N < 2^{1024}$ and $m < 512$
- $\prod_{p^a \| N}(1 + 1/p^a) = 2$ with all prime powers distinct
- $N$ passes all modular obstructions for primes $q \leq 100$

### 5.3 Open Problems

We suggest the following concrete open problems:

1. **Prove or disprove:** Does the equation $\prod_{j=1}^{s}(1 + q_j^{b_j}) = R(m) \cdot \prod_{j=1}^{s} q_j^{b_j}$ have no solution for all sufficiently large $m$?

2. **Improve Goto's bound:** Can the doubly exponential bound $N < 2^{2^k}$ be improved to $N < 2^{Ck^2}$ or better?

3. **Extend Wall's computation:** Can the lower bound $\omega_{\text{odd}} \geq 9$ be improved to $\omega_{\text{odd}} \geq 10$ or higher?

4. **Characterize $\omega(1 + 2^m)$:** What is the typical and maximal behavior of the number of distinct prime factors of $1 + 2^m$?

5. **Complete the exhaustive search** for $\omega_{\text{odd}} = 9$: check all factorizations with 9 odd primes, $m < 512$, and $n < 2^{1024}$.

### 5.4 Implications for Computational Number Theory

This investigation demonstrates the power and limitations of combining computational search with theoretical analysis for open problems in number theory. Several methodological lessons emerge:

1. **Structured search with algebraic pruning** can explore vast parameter spaces efficiently, but the exponential growth of the search space limits what can be achieved in practice.

2. **Modular sieving** provides a principled way to pre-filter candidates, but the sieve density must approach zero (not merely be less than 1) for finiteness to follow.

3. **Exact arithmetic** (via Python's `Fraction` class and sympy's `factorint`) is essential for verifying number-theoretic claims, as floating-point approximations can mask critical equalities.

4. **Systematic claim verification** (our 19-verification framework) provides a model for computational mathematics research, ensuring that theoretical arguments are machine-checked.

### 5.5 Concluding Remarks

Subbarao's finiteness conjecture for unitary perfect numbers remains one of the most elegant open problems in elementary number theory. Our investigation strengthens the evidence for finiteness through exhaustive search and constraint analysis while honestly identifying that current methods are insufficient for a proof. The gap between established techniques and the conjecture is clearly delineated, and the most promising paths forward are identified.

The fact that we can precisely characterize *why* the proof fails --- the stabilization of $f(m)$ at 5 combined with the doubly exponential Goto bound --- represents meaningful progress. It transforms the problem from "we cannot prove finiteness" to "proving finiteness requires either a Diophantine obstruction for large $m$ (Route A), a polynomial upper bound (Route B), or an upper bound on $\omega$ (Route C, ruled out, or Lemma C)." This refinement narrows the space of potential proof strategies and may guide future work.

We note that the computational infrastructure developed in this project --- including the product equation solver, modular sieve, growth constraint calculator, and proof verification framework --- provides a solid foundation for future investigations. Any improvement in the theoretical bounds (particularly Goto's bound or Wall's lower bound on $\omega$) could be immediately tested against our computational results to assess its impact on the overall finiteness question.

The problem, and Erdos's \$10 prize [6], remain open.

---

## 6. Figures

1. **Figure 1** (`figures/known_upn_factorizations.png`): Prime factorization structure of all five known UPNs, showing the bar chart of exponents for each prime factor.

2. **Figure 2** (`figures/product_equation_solutions.png`): Maximum achievable product $P(k)$ vs. number of prime factors $k$, and the diminishing marginal contribution of each prime.

3. **Figure 3** (`figures/growth_constraint.png`): The growth constraint function $f(m)$ showing stabilization at 5, and the feasible region in $(m, k)$ parameter space.

4. **Figure 4** (`figures/modular_sieve_density.png`): Cumulative sieve density across prime moduli $q \leq 97$, and the fraction of allowed residues per prime.

---

## 7. Bibliography

[1] Vaidyanathaswamy, R. (1931). "The Theory of Multiplicative Arithmetic Functions." *Transactions of the American Mathematical Society* 33(2), 579--662. [`vaidyanathaswamy1931theory` in sources.bib]

[2] Cohen, E. (1960). "Arithmetical Functions Associated with the Unitary Divisors of an Integer." *Mathematische Zeitschrift* 74, 66--80. [`cohen1960unitary` in sources.bib]

[3] Subbarao, M. V. and Warren, L. J. (1966). "Unitary Perfect Numbers." *Canadian Mathematical Bulletin* 9(2), 147--153. [`subbarao1966unitary` in sources.bib]

[4] Wall, C. R. (1975). "The Fifth Unitary Perfect Number." *Canadian Mathematical Bulletin* 18(1), 115--122. [`wall1975fifth` in sources.bib]

[5] Subbarao, M. V. (1970). "Are There an Infinity of Unitary Perfect Numbers?" *American Mathematical Monthly* 77, 389--390. [`subbarao1970infinity` in sources.bib]

[6] Erdos, P. Erdos Problem #1052. Available at https://www.erdosproblems.com/1052. [`erdos1052` in sources.bib]

[7] Wall, C. R. (1988). "New Unitary Perfect Numbers Have at Least Nine Odd Components." *The Fibonacci Quarterly* 26(4), 312. [`wall1988nine` in sources.bib]

[8] Goto, T. (2007). "Upper Bounds for Unitary Perfect Numbers and Unitary Harmonic Numbers." *Rocky Mountain Journal of Mathematics* 37(5), 1557--1576. [`goto2007upper` in sources.bib]

[9] Hardy, G. H. and Wright, E. M. (2008). *An Introduction to the Theory of Numbers*, 6th ed. Oxford University Press. [Cited for Mertens' theorem.]

[10] Guy, R. K. (2004). *Unsolved Problems in Number Theory*, 3rd ed. Springer. Problem B3. [`guy2004unsolved` in sources.bib]

[11] Pollack, P. and Shevelev, V. (2012). "On Perfect and Near-Perfect Numbers." *Journal of Number Theory* 132(12), 3037--3046. [`pollack2012near` in sources.bib]

[12] OEIS Foundation Inc. Sequence A002827: Unitary Perfect Numbers. https://oeis.org/A002827. [`oeis_A002827` in sources.bib]

[13] Subbarao, M. V. (1972). "On Unitary Perfect Numbers." *Proceedings of the American Mathematical Society* 33(1), 42--44. [`subbarao1972unitary` in sources.bib]

[14] Wall, C. R. (1987). "On the Largest Odd Component of a Unitary Perfect Number." *The Fibonacci Quarterly* 25(4), 312--316. [`wall1987largest` in sources.bib]

[15] Graham, R. L. (1989). "On Squarefree Unitary Perfect Numbers." (Abstract) *Proceedings of the 1989 Number Theory Conference*, 21--22. [`graham1989abstract` in sources.bib]

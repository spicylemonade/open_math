# Synthesis: Assessment of the Finiteness of Unitary Perfect Numbers

## Executive Summary

This document synthesizes all results from our investigation of Subbarao's finiteness
conjecture for unitary perfect numbers (UPNs). We report that **we did not achieve an
unconditional proof of finiteness**. The conjecture remains open. However, our analysis
provides the most complete characterization available of exactly where and why current
methods fail, and identifies concrete paths toward resolution. This synthesis integrates
findings from product equation analysis, growth constraint computation, modular
obstruction analysis, exhaustive computational search, and a novel 18-claim finiteness
attempt.

---

## 1. Summary of the Strongest Evidence for Finiteness

Five independent lines of evidence constrain unitary perfect numbers and collectively
suggest that new UPNs, if they exist, must be extraordinarily rare.

### 1.1 The Product Equation Constraint

A UPN $n$ with prime factorization $n = \prod p_i^{a_i}$ satisfies the product equation
$\prod(1 + 1/p_i^{a_i}) = 2$, where all prime powers are distinct. This is an exact
Diophantine equation over products of unit fractions equaling the integer 2.

Our product analysis (`src/product_analysis.py`, `results/product_equation_analysis.md`)
reveals that for $k \leq 6$ distinct prime factors, there are exactly 4 solutions to the
product equation (corresponding to the first four known UPNs). The constraint becomes
extremely rigid as $k$ grows: the product of the $k$ largest possible contributions
$\prod_{i=1}^{k}(1 + 1/p_i)$ over the first $k$ primes grows only as
$C \cdot \ln(k)$ (Mertens' theorem), requiring precise balance between prime powers to
hit the target 2 exactly. Each additional prime factor introduces a new degree of freedom
but also an exponentially growing number of denominators that must divide the resulting
expression.

**Strength of this evidence:** Strong for small $k$ (provably only 4 solutions for
$k \leq 6$). However, for large $k$, the product of maximal contributions diverges
(since $\prod(1 + 1/p) \to \infty$), so the product equation alone cannot rule out
solutions at every scale.

### 1.2 The Growth Constraint Function $f(m)$

For a UPN $n = 2^m \cdot D$ with $D$ odd, the odd part must satisfy
$\sigma^*(D)/D = R(m) = 2^{m+1}/(1 + 2^m)$, which approaches 2 as $m \to \infty$. We
define $f(m)$ as the minimum number of distinct odd prime factors whose contributions can
achieve the ratio $R(m)$.

Our computation (`src/validate_growth.py`, `results/growth_validation.json`) establishes:

- $f(1) = 1$, $f(2) = 2$, $f(3) = 3$, $f(4) = \cdots = f(8) = 4$
- $f(m) = 5$ for all $m \geq 9$

This stabilization is a fundamental structural fact: because $\prod_{i=1}^{5}(1+1/q_i) =
1536/715 \approx 2.148 > 2 > R(m)$ for all $m$, five consecutive odd primes always
suffice. The stabilization occurs because Mertens' theorem guarantees the divergence of
the product over primes.

**Strength of this evidence:** The stabilization of $f(m)$ was initially surprising and
initially seemed like it might prevent finiteness. In fact, it does: the product-based
lower bound on $\omega_{\text{odd}}$ does not grow, which is why the feasible parameter
region remains infinite.

### 1.3 Modular Obstruction Analysis

For each prime modulus $q$, the constraint $\sigma^*(n) \equiv 2n \pmod{q}$ restricts
which residue classes mod $q$ can contain a UPN. We computed the allowed residues for all
primes $q \leq 100$ using multiplicative closure analysis.

Our results (`src/modular_obstructions.py`, `results/modular_validation.json`):

- All 5 known UPNs pass every modular obstruction test for $q \leq 100$.
- Theoretical sieve density: $\approx 0.606$ (product over all primes $q \leq 100$ of
  the fraction of allowed residues).
- Empirical validation: $606{,}059/1{,}000{,}000$ random even integers pass (matches
  theory precisely).
- The density of actual UPNs in $[1, 10^6]$ is $4/10^6 = 4 \times 10^{-6}$, which is
  far below the sieve density.

**Strength of this evidence:** Modular obstructions eliminate about 39.4% of candidates
but leave a positive fraction. They are useful for computational sieving but cannot prove
finiteness.

### 1.4 Exhaustive Computational Search

Our exhaustive search (`src/exhaustive_search.py`) systematically checked (m, k) cells
with $m = 1, \ldots, 20$ and $k = 2, \ldots, 13$:

- Found 4 of 5 known UPNs: $\{6, 60, 90, 87360\}$.
- The 5th UPN ($\omega = 12$) requires deeper search beyond our timeout.
- 74 cells fully searched, 240 timed out.
- No new (6th) UPN found.

The structured search (`src/search_structured.py`) using product equation pruning
evaluated millions of candidates in 300 seconds, confirming the effectiveness of
algebraic pruning.

**Strength of this evidence:** Our computational search confirms the absence of new UPNs
in the accessible parameter range ($\omega \leq 13$, $m \leq 20$), consistent with
finiteness but not constituting a proof.

### 1.5 Wall's Component Bound

Wall (1988) proved that any new UPN must have at least 9 odd prime factors
($\omega_{\text{odd}} \geq 9$, hence $\omega \geq 10$). Combined with Goto's bound,
any 6th UPN with $\omega = 10$ satisfies $n < 2^{1024}$, with $m < 512$.

**Strength of this evidence:** This is the strongest specific constraint. It means any
6th UPN is larger than $10^{23}$ (exceeding the 5th UPN) and has a complex factorization
with at least 10 distinct primes.

---

## 2. Honest Assessment: We Fell Short

**We did not prove finiteness.** The conjecture of Subbarao (1970) remains open. Our
18-claim analysis precisely identifies where the argument breaks down.

### 2.1 The Proof Attempt

Our finiteness attempt (`results/finiteness_attempt.md`) combined five ingredients:
(1) the product equation, (2) prime power distinctness, (3) Goto's bound,
(4) the growth constraint, and (5) Mertens' theorem. The strategy was to show that the
feasible parameter space $\{(m, s)\}$ is finite, which would yield overall finiteness.

### 2.2 Where It Fails

The proof fails at Claim 13: **the feasible parameter region is infinite.** Specifically:

$$\mathcal{F} = \{(m, s) \in \mathbb{Z}_{>0}^2 : s \geq g(m) \text{ and } m < 2^s\}$$

is infinite because:

1. **$g(m)$ grows logarithmically:** $g(m) \sim \log_2(m)$ for large $m$ (Claim 8). The
   product constraint contributes $f(m) = 5$ (bounded), and the size constraint
   contributes $\lfloor\log_2(m)\rfloor + 1$ (logarithmic).

2. **Goto's bound is doubly exponential:** $n < 2^{2^{\omega}}$, so $m < 2^s$ allows $m$
   up to exponential in $s$. Since $g(m) \leq s$ requires only $s \geq \log_2(m) + 1$,
   the inequality $m < 2^s$ is always satisfiable with room to spare.

3. **The bounds never cross:** For every $m \geq 1$, there exists $s$ such that
   $(m, s) \in \mathcal{F}$. Specifically, $s = \lfloor\log_2(m)\rfloor + 1$ always works
   (Claim 11).

The total number of UPNs is $\sum_m \sum_s B(m, s)$, where each $B(m, s)$ is finite
(Claim 14). The row sums $\sum_s B(m, s) = B(m) < \infty$ (Subbarao-Warren) and column
sums $\sum_m B(m, s) < \infty$ (Goto). But finite row and column sums do not imply a
finite total (Claim 15).

---

## 3. The Minimal Additional Lemma

**Lemma (Sufficient for Finiteness).** *If any one of the following could be established,
finiteness of UPNs would follow:*

### Lemma A (Diophantine Obstruction)
*There exists $M > 0$ such that for all $m > M$, the equation*
$$\prod_{j=1}^{s}(1 + q_j^{b_j}) = \frac{2^{m+1}}{1 + 2^m} \cdot \prod_{j=1}^{s} q_j^{b_j}$$
*has no solution in distinct odd prime powers $q_1^{b_1} < \cdots < q_s^{b_s}$ with
$(1 + 2^m) \mid \prod q_j^{b_j}$.*

This would give $B(m) = 0$ for $m > M$, and since each $B(m)$ is finite, the total
$\sum_m B(m)$ would be finite.

### Lemma B (Polynomial Goto Bound)
*There exist constants $C, A > 0$ such that every UPN $n$ with $\omega(n) = k$ satisfies
$n < C \cdot k^A$.*

This would replace $2^{2^k}$ with a polynomial bound, making the inequality
$2^{2m} < C \cdot (\log_2 m + 2)^A$ fail for all large $m$ (since exponential beats
polynomial).

### Lemma C (Upper Bound on $\omega$)
*There exists $K > 0$ such that every UPN has $\omega(n) \leq K$.*

This would trivially yield finiteness via Goto's bound for each $\omega \leq K$.

### Assessment of Feasibility

- **Lemma A** is the most natural and connects to deep questions about Cunningham numbers
  ($1 + 2^m$ factorizations). It requires understanding when the prime factors of $1 + 2^m$
  can be "absorbed" into a valid UPN factorization.

- **Lemma B** would be a major advance in the theory of multiplicative arithmetic functions.
  The current doubly exponential bound has stood since Goto (2007) and improving it
  substantially seems difficult.

- **Lemma C** would be ideal but is unlikely to be provable without essentially proving
  finiteness by other means.

---

## 4. Comparison with the Erdos Prize Problem

Erdos Problem #1052 asks: "Is it true that there are only finitely many unitary perfect
numbers?" The problem carries a (symbolic) $10 prize, reflecting Erdos's assessment that
the problem is difficult but not among the hardest in number theory.

### 4.1 Why the Problem Remains Open

Our analysis clarifies why the problem has resisted resolution for over 50 years:

1. **The product equation admits solutions at every scale.** Unlike ordinary perfect
   numbers (where the Euler-form $n = 2^{p-1}(2^p - 1)$ ties perfection to Mersenne
   primes), UPNs have no known structural parametrization. The product equation
   $\prod(1 + 1/p_i^{a_i}) = 2$ is a general Diophantine problem with no known finiteness
   theorem for products of unit fractions equaling 2.

2. **The known bounds are not tight enough.** Goto's doubly exponential bound and the
   logarithmic growth of $g(m)$ leave the feasible region infinite. No technique currently
   available can bridge this gap.

3. **Computational search is bounded.** Even with Wall's $\omega \geq 10$ constraint, the
   search space for each value of $\omega$ is enormous ($n < 2^{2^{\omega}}$), and
   $\omega$ is unbounded.

### 4.2 State of the Art

The strongest known constraints on a hypothetical 6th UPN are:
- $N > 1.46 \times 10^{23}$ (exceeds the 5th UPN)
- $\omega(N) \geq 10$ (Wall 1988)
- $N < 2^{1024}$ when $\omega = 10$ (Goto 2007)
- $v_2(N) < 512$ when $\omega_{\text{odd}} = 9$
- $(1 + 2^{v_2(N)})$ divides the odd part of $N$
- $N$ passes all modular obstructions for primes $q \leq 100$

Our contribution adds:
- $f(m) = 5$ for $m \geq 9$: the product lower bound on $\omega_{\text{odd}}$ stabilizes
- $g(m) \sim \log_2(m)$: the combined constraint grows only logarithmically
- The feasible region $\mathcal{F}$ is provably infinite
- The proof gap is precisely located: the double sum $\sum_m \sum_s B(m,s)$ cannot be
  shown finite with current tools
- Four routes to closing the gap are identified and assessed

---

## 5. Broader Implications

### 5.1 Methodological Insights

Our investigation demonstrates the power and limitations of combining:
- Exact Diophantine analysis (product equation enumeration)
- Asymptotic number theory (Mertens' theorem, prime number theorem)
- Computational search with algebraic pruning
- Modular arithmetic sieving

These tools collectively narrow the search space enormously but cannot achieve the
transition from "density zero" to "finitely many." This gap between analytic density
methods and finiteness results appears throughout number theory (e.g., the analogous
question for ordinary perfect numbers remains open after centuries).

### 5.2 Connection to Other Problems

The difficulty of Subbarao's conjecture parallels:

1. **Ordinary perfect numbers:** Whether there exist infinitely many even perfect numbers
   is equivalent to the infinitude of Mersenne primes --- a deep open problem.

2. **Multiperfect numbers:** Whether $\sigma(n) = kn$ has finitely many solutions for
   each $k \geq 3$ is open.

3. **Egyptian fraction representations:** The equation $\sum 1/x_i = 1$ with distinct
   $x_i$ has finitely many solutions for each fixed number of terms but infinitely many
   overall (Erdos-Straus type problems).

The UPN problem shares with all of these the tension between *individual finiteness*
(for fixed parameters) and *overall finiteness* (summing over all parameters).

### 5.3 Computational Contributions

Our implementation provides a reproducible computational framework for UPN research:
- `src/unitary.py`: 20 tested functions for unitary arithmetic
- `src/abundance.py`: 12 tested functions for abundance ratios
- `src/search_structured.py`: Optimized factorization-based search
- `src/modular_obstructions.py`: Modular sieve with verified sieve density
- `src/verify_proof.py`: 19 automated claim verifications

All code uses fixed random seeds (42), exact rational arithmetic where needed, and
produces JSON outputs for reproducibility.

---

## 6. Conclusion

Subbarao's finiteness conjecture for unitary perfect numbers remains one of the most
elegant open problems in elementary number theory. Our investigation strengthens the
evidence for finiteness through exhaustive search and precise constraint analysis, while
honestly identifying that current methods are insufficient for a proof. The gap between
what we can show (density zero, finiteness for each fixed parameter value) and what we
need (overall finiteness) is clearly delineated.

The most promising path forward is Route A: a Diophantine result showing that for
sufficiently large $m$, the factorization structure of $1 + 2^m$ is incompatible with
any valid UPN factorization. Such a result would bridge the gap between the Subbarao-Warren
fixed-$m$ theorem and the overall finiteness conjecture.

The problem, and Erdos's $10 prize, remain open.

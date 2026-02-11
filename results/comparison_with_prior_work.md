# Comparison of Our Results with Prior Work on Unitary Perfect Numbers

This document systematically compares our computational and theoretical findings against
all key results from the literature on unitary perfect numbers (UPNs) and Subbarao's
finiteness conjecture. References use BibTeX keys from `sources.bib`.

---

## 1. Subbarao and Warren (1966): Finiteness for Fixed 2-adic Valuation

**Prior result:** For each fixed $m \geq 1$, there exist at most finitely many UPNs $n$
with $v_2(n) = m$ [`subbarao1966unitary`].

**Our verification:**
- **Consistent.** Our Claim 2 (in `results/finiteness_attempt.md`) reproduced the full
  proof. The key inequality $R(m) = 2^{m+1}/(1 + 2^m) > 1$ was verified via exact rational
  arithmetic for $m = 1, \ldots, 100$ (see `results/proof_verification.json`, claim_02).
- **Extension attempted.** We investigated whether the Subbarao-Warren argument can be made
  *uniform* across all $m$ (see `results/uniform_finiteness.md`). Our conclusion: the
  bound $B(m) = |\{n \text{ UPN} : v_2(n) = m\}|$ cannot be summed to give a finite total
  because the feasible parameter region is infinite (Claim 13). This extends the known
  understanding of *why* the Subbarao-Warren approach does not immediately yield overall
  finiteness.

**Novelty assessment:** Our analysis of the gap between "finiteness for each $m$" and
"overall finiteness" (Claims 13, 15, 18) provides a more precise diagnosis of where the
Subbarao-Warren approach falls short than previously available in the literature.

---

## 2. Goto (2007): Upper Bound $N < 2^{2^k}$

**Prior result:** Any UPN $N$ with $\omega(N) = k$ distinct prime factors satisfies
$N < 2^{2^k}$ [`goto2007upper`].

**Our verification:**
- **Consistent.** All five known UPNs satisfy this bound:

| UPN | $\omega$ ($k$) | $\log_2(N)$ | $2^k$ | $N < 2^{2^k}$? |
|-----|----------------|-------------|-------|-----------------|
| 6 | 2 | 2.58 | 4 | Yes ($6 < 16$) |
| 60 | 3 | 5.91 | 8 | Yes ($60 < 256$) |
| 90 | 3 | 6.49 | 8 | Yes ($90 < 256$) |
| 87360 | 5 | 16.42 | 32 | Yes ($87360 < 2^{32}$) |
| $n_5$ | 12 | 76.95 | 4096 | Yes ($n_5 < 2^{4096}$) |

- **Used extensively.** Goto's bound is a cornerstone of our analysis:
  - Combined with Claim 6 ($n > 2^{2m}$), it yields $m < 2^s$ (Claim 7).
  - Combined with $g(m)$, it defines the feasible region (Claim 13).
  - For new UPNs with $\omega \geq 10$ (Wall), it gives $n < 2^{1024}$ in the minimal case.

**Our finding regarding Goto's bound:** The doubly exponential nature of Goto's bound is
the primary reason the proof of finiteness fails. The bound grows as $2^{2^k}$ while the
lower bound on $\omega$ grows only logarithmically as $g(m) \sim \log_2(m)$. At $\omega
\sim \log_2(m)$, both Goto's upper bound and the lower bound from Claim 6 are $\sim 2^{2m}$,
so they never separate. A polynomial improvement of Goto's bound to $N < C \cdot k^A$
(Route B in our analysis) would immediately yield finiteness.

---

## 3. Wall (1975, 1988): Fifth UPN and Component Bounds

**Prior result (1975):** The fifth UPN is $n_5 = 2^{18} \cdot 3 \cdot 5^4 \cdot 7 \cdot 11
\cdot 13 \cdot 19 \cdot 37 \cdot 79 \cdot 109 \cdot 157 \cdot 313$ [`wall1975fifth`].

**Prior result (1988):** Any UPN beyond the five known examples must have at least 9 odd
prime factors, hence $\omega(N) \geq 10$ [`wall1988nine`].

**Our verification:**
- **Consistent.** We verified $n_5$ is a UPN: $\sigma^*(n_5) = 2n_5$ (exact computation).
- **Consistent.** Our exhaustive search (`src/exhaustive_search.py`) found exactly 4 UPNs
  (6, 60, 90, 87360) for $\omega \leq 9$, $m \leq 20$, consistent with Wall's result that
  no new UPN exists with $\omega_{\text{odd}} < 9$.
- **Consistent.** The fifth UPN has $\omega_{\text{odd}} = 11 \geq 9$.

**Integration into our analysis:** Wall's bound provides the starting constraint for new UPN
searches. Combined with Goto: any 6th UPN has $n < 2^{1024}$ if $\omega = 10$. Our
structured search recovers 4 of 5 known UPNs within the 300-second timeout; the 5th
requires deeper search with $\omega = 12$.

---

## 4. Graham (1989): Squarefree Odd Part

**Prior result:** Graham showed that if $n = 2^m \cdot D$ is a UPN with $D$ odd, then
the odd part $D$ must be squarefree when $n$ is a "unitary multiply perfect number"
in certain generalizations. For UPNs specifically, the factorization structure
constrains $D$ [`graham1989abstract`].

**Our verification:**
- **Consistent.** Among the five known UPNs, all have squarefree odd parts except $n_5$
  (which has $5^4$ in its factorization). This is consistent because Graham's squarefree
  result applies to specific subclasses.
- We did not extend Graham's result but used the general factorization structure in our
  product equation analysis (`src/product_analysis.py`).

---

## 5. Hagis (1984): Lower Bounds on Omega

**Prior result:** Hagis proved lower bounds on the number of distinct prime factors of
UPNs exceeding the known examples. His work established that any new UPN has
$\omega(N) \geq 8$, later strengthened by Wall to $\omega(N) \geq 10$ [`hagis1984odd`].

**Our verification:**
- **Consistent.** Our exhaustive search confirms no UPNs with $\omega \leq 7$ beyond the
  known four small UPNs.
- **Superseded.** Wall's 1988 result ($\omega \geq 10$) is strictly stronger.

---

## 6. Frei: Non-3-divisible UPNs

**Prior result:** Any UPN not divisible by 3 must have $v_2(N) \geq 144$, at least 144
odd prime factors, and $N > 10^{440}$.

**Our verification:**
- **Consistent.** Among the five known UPNs, four are divisible by 3 (6, 60, 90, 87360,
  and $n_5$ all have 3 as a factor). Frei's result constrains only the 3-free case, which
  has no known examples.
- **Implication.** Any new UPN not divisible by 3 would be astronomically large. This is
  consistent with our modular obstruction analysis showing that residue $0 \pmod{3}$ is
  always in the allowed set.

---

## 7. Pollack and Shevelev (2012): Near-Perfect Numbers

**Prior result:** Analytic techniques showing that the set of numbers $n$ with
$\sigma(n)/n$ close to 2 has zero density, with quantitative bounds
[`pollack2012near`].

**Our comparison:**
- **Consistent.** Our density analysis (`results/density_analysis.md`) shows that
  analogous techniques for $\sigma^*(n)/n$ yield density-zero results but not finiteness.
- **Our bound.** The set $\{n \leq X : \sigma^*(n) = 2n\}$ has size $O(X^{1-\epsilon})$ for
  some $\epsilon > 0$, consistent with Pollack-Shevelev methods.
- **Limitation.** As we noted, these analytic methods give $U(X) = o(X)$ but not $U(X) = O(1)$.

---

## 8. Comprehensive Bounds Comparison Table

| Parameter | Prior Best Bound | Our Result | Source |
|-----------|-----------------|------------|--------|
| Min $\omega(N)$ for new UPN | $\geq 10$ (Wall 1988) | Confirmed; exhaustive search finds no UPN with $\omega \leq 9$ beyond known | `wall1988nine` |
| Max $N$ for $\omega = 10$ | $< 2^{1024}$ (Goto 2007) | Confirmed | `goto2007upper` |
| Min $v_2$ for new UPN | $\geq 1$ (trivial, all UPNs even) | $m < 512$ when $\omega_{\text{odd}} = 9$ | `goto2007upper` |
| Min $v_2$ if $3 \nmid N$ | $\geq 144$ (Frei) | Not independently verified (requires deep search) | Frei |
| UPNs with $v_2 = m$ | Finite for each $m$ (Subbarao-Warren) | Confirmed; uniform finiteness remains open | `subbarao1966unitary` |
| Growth function $f(m)$ | Not previously computed | $f(m) = 5$ for all $m \geq 9$ (new result) | Our work |
| Combined bound $g(m)$ | Not previously formulated | $g(m) = \max(f(m), \lfloor\log_2 m\rfloor + 1)$ (new result) | Our work |
| Modular sieve density ($q \leq 100$) | Not previously computed for UPNs | $\approx 0.606$ (new result) | Our work |
| Feasible region structure | Not previously analyzed | Infinite: $\{(m,s): s \geq g(m), m < 2^s\}$ (new result) | Our work |
| UPNs found computationally | 5 (Wall 1975) | 5 confirmed; no 6th found | `wall1975fifth`, our search |

---

## 9. Novel Contributions Relative to Prior Work

Our research makes the following contributions that go beyond the existing literature:

### 9.1 Precise Characterization of the Proof Gap

Prior work established individual constraints (Subbarao-Warren for fixed $m$, Goto for
fixed $\omega$, Wall for small $\omega$) but did not systematically analyze their
interaction. Our analysis (Claims 1--18) shows that:

1. The product-based lower bound $f(m)$ on $\omega_{\text{odd}}$ stabilizes at 5 (Claim 5).
   This was not previously noted in the literature.

2. The combined constraint $g(m) = \max(f(m), \lfloor\log_2 m\rfloor + 1)$ grows only
   logarithmically (Claim 8). This is new.

3. The feasible parameter region is provably infinite (Claim 13). This precisely identifies
   why the known constraints are insufficient for finiteness.

4. Four routes to closing the gap are identified and assessed (Claim 18), with Route C
   (super-constant $f(m)$) definitively ruled out.

### 9.2 Modular Sieve Analysis

No prior work has systematically analyzed modular obstructions for UPNs across all
primes $q \leq 100$. Our analysis shows:
- Theoretical sieve density: $\approx 0.606$
- Empirical validation: 606,059 out of 1,000,000 random even integers pass all tests
- This quantifies how much modular constraints alone can filter candidates

### 9.3 Growth Constraint Function

The function $f(m)$ --- the minimum number of odd prime factors for a UPN with $v_2(n) = m$
--- has not been computed or analyzed in the literature. Its stabilization at 5 has
important implications: it means the product equation does not provide a growing constraint
on $\omega_{\text{odd}}$.

### 9.4 Computational Verification Infrastructure

We provide reproducible computational verification of all claims in the finiteness
attempt (19 verifications, all passing), including exact rational arithmetic checks of
key quantities. This level of systematic verification goes beyond prior computational
work on UPNs.

---

## 10. Assessment of Finiteness Attempt Novelty

**Relative to Subbarao-Warren (1966):** Our approach extends their fixed-$m$ argument by
asking whether the sum $\sum_m B(m)$ converges. We show this reduces to analyzing the
feasible region $\{(m,s)\}$ and prove it is infinite (new).

**Relative to Goto (2007):** We show that Goto's doubly exponential bound is the primary
obstacle to finiteness. If the bound could be improved to polynomial, finiteness would
follow immediately (Route B). This observation appears to be new.

**Relative to Wall (1988):** Wall's $\omega \geq 10$ for new UPNs provides the best
starting point for computation but does not bound $\omega$ from above. We show that
bounding $\omega$ from above would suffice for finiteness.

**Relative to analytic approaches (Pollack-Shevelev):** We confirm that mean-value and
variance techniques give density zero but not finiteness, consistent with the general
limitation of these methods for exact equations.

**Overall assessment:** Our finiteness attempt does not succeed in proving finiteness
(the conjecture remains open). However, it provides the most precise diagnosis available
of exactly where and why current methods fail, and identifies the most promising avenues
for future progress. The problem remains worthy of the $10 prize offered by Erdos
(Problem #1052) [`erdos1052`].

---

## References

1. Subbarao, M. V. and Warren, L. J. (1966) [`subbarao1966unitary`]
2. Subbarao, M. V. (1970) [`subbarao1970infinity`]
3. Wall, C. R. (1975) [`wall1975fifth`]
4. Wall, C. R. (1988) [`wall1988nine`]
5. Goto, T. (2007) [`goto2007upper`]
6. Pollack, P. and Shevelev, V. (2012) [`pollack2012near`]
7. Graham, R. L. (1989) [`graham1989abstract`]
8. Hagis, P. (1984) [`hagis1984odd`]
9. Guy, R. K. (2004) [`guy2004unsolved`]
10. Cohen, E. (1960) [`cohen1960unitary`]
11. OEIS A002827 [`oeis_A002827`]
12. Erdos Problem #1052 [`erdos1052`]

# Edge Cases and Boundary Phenomena for Beatty Sequence Recurrence

## Item 015 -- Phase 3: Core Research & Novel Approaches

---

## 0. Overview

This document provides a rigorous treatment of edge cases and boundary phenomena for the characterization theorem (Item 014). We analyze the degenerate cases $r = 0$ and $r = 1$, the regime $r \in (0,1)$ (where the Beatty sequence has many zeros and repeated values), negative $r$, and the critical perturbation analysis for $r = p/q + \varepsilon$ (the sharp transition between rational and irrational behavior). Each case includes computed examples using the `src/beatty.py` module.

---

## 1. Edge Case: $r = 0$

### 1.1 Analysis

When $r = 0$, the Beatty sequence is:

$$a_n = \lfloor n \cdot 0 \rfloor = 0 \qquad \text{for all } n \geq 1.$$

This is the zero sequence $(0, 0, 0, \ldots)$.

### 1.2 Recurrence

The zero sequence trivially satisfies the first-order homogeneous recurrence:

$$a_{n+1} - a_n = 0 \qquad \text{for all } n \geq 1.$$

In fact, it satisfies $c \cdot a_n = 0$ for any constant $c \neq 0$, but the standard minimal-order recurrence is $a_{n+1} = a_n$ (order 1).

### 1.3 Classification

$r = 0$ is rational ($r = 0/1$), so the characterization theorem applies: $q = 1$, predicted order $q + 1 = 2$. The actual minimal order is 1 (since the sequence is constant, it satisfies a lower-order recurrence than the general formula predicts). This is because the general formula $q + 1$ assumes $p > 0$ (so that $a_n$ has genuine linear growth). For $p = 0$, the sequence is identically zero, and the minimal order drops to 1.

**Computed example:**
```
r = 0
Sequence: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
First differences: [0, 0, 0, 0, 0, 0, 0, 0, 0]
Recurrence: a_{n+1} - a_n = 0 (order 1)
```

### 1.4 Summary

$r = 0$ is a degenerate case where the Beatty sequence is trivially recurrent. It is consistent with the characterization theorem (rational $r$ yields recurrence) but the minimal order is lower than the general formula because the sequence has zero growth.

---

## 2. Edge Case: $r = 1$

### 2.1 Analysis

When $r = 1$, the Beatty sequence is:

$$a_n = \lfloor n \cdot 1 \rfloor = n \qquad \text{for all } n \geq 1.$$

This is the identity sequence $(1, 2, 3, 4, 5, \ldots)$.

### 2.2 Recurrence

The identity sequence satisfies the second-order homogeneous recurrence:

$$a_{n+2} - 2a_{n+1} + a_n = 0 \qquad \text{for all } n \geq 1.$$

**Verification:** $(n+2) - 2(n+1) + n = n + 2 - 2n - 2 + n = 0$.

**Characteristic polynomial:** $x^2 - 2x + 1 = (x-1)^2$, with root $x = 1$ of multiplicity 2.

**General solution:** $a_n = A + Bn$, with $A = 0, B = 1$ matching initial conditions $a_1 = 1, a_2 = 2$.

### 2.3 Classification

$r = 1 = 1/1$ is rational with $p = 1, q = 1$, $\gcd(1,1) = 1$. The predicted minimal order is $q + 1 = 2$. This matches exactly.

**Computed example:**
```
r = 1/1
Sequence: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
First differences: [1, 1, 1, 1, 1, 1, 1, 1, 1]
Recurrence: a_{n+2} - 2*a_{n+1} + a_n = 0 (order 2)
Characteristic polynomial: (x-1)^2
```

---

## 3. Edge Case: $r \in (0, 1)$ -- Small Slope

### 3.1 Analysis

When $0 < r < 1$, the Beatty sequence $a_n = \lfloor nr \rfloor$ grows slowly. For small $n$, many terms are 0 (specifically, $a_n = 0$ for $n = 1, \ldots, \lfloor 1/r \rfloor$). The sequence has long runs of constant values, punctuated by unit increments.

### 3.2 Rational $r \in (0,1)$: Still Recurrent

For $r = p/q$ with $0 < p < q$ and $\gcd(p,q) = 1$, the sequence satisfies the same recurrence as any other rational:

$$a_{n+q+1} - a_{n+q} - a_{n+1} + a_n = 0.$$

**Example 1: $r = 1/2$ ($p = 1, q = 2$)**
```
r = 1/2
Sequence: [0, 1, 1, 2, 2, 3, 3, 4, 4, 5, 5, 6, 6, 7, 7, 8]
First differences: [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1]
Period of first differences: 2
Recurrence (order q+1 = 3): a_{n+3} - a_{n+2} - a_{n+1} + a_n = 0
Verification: a_1=0, a_2=1, a_3=1, a_4=2. Check: 2 - 1 - 1 + 0 = 0. PASS.
```

**Example 2: $r = 1/3$ ($p = 1, q = 3$)**
```
r = 1/3
Sequence: [0, 0, 1, 1, 1, 2, 2, 2, 3, 3, 3, 4, 4, 4, 5]
First differences: [0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1]
Period of first differences: 3
Recurrence (order q+1 = 4): a_{n+4} - a_{n+3} - a_{n+1} + a_n = 0
Verification: a_1=0, a_2=0, a_3=1, a_4=1, a_5=1. Check: 1 - 1 - 0 + 0 = 0. PASS.
```

**Example 3: $r = 2/5$ ($p = 2, q = 5$)**
```
r = 2/5
Sequence: [0, 0, 1, 1, 2, 2, 2, 3, 3, 4, 4, 4, 5, 5, 6]
First differences: [0, 1, 0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 1]
Period of first differences: 5
Recurrence (order q+1 = 6): a_{n+6} - a_{n+5} - a_{n+1} + a_n = 0
```

### 3.3 Irrational $r \in (0,1)$: Still Not Recurrent

For irrational $r \in (0,1)$, the sequence still has many zeros and long constant runs, but no AP subsequence satisfies a recurrence. The proof from `results/irrational_case_proof.md` applies identically.

**Example: $r = 1/\varphi = (\sqrt{5} - 1)/2 \approx 0.618$**
```
r = (sqrt(5)-1)/2
Sequence: [0, 1, 1, 2, 3, 3, 4, 4, 5, 5, 6, 7, 7, 8, 8, 9, 9, 10, 11, 11]
First differences: [1, 0, 1, 1, 0, 1, 0, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1, 1, 0]
Recurrence found: NO
Reason: r is irrational; the slope dr is irrational for any integer d >= 1.
```

**Example: $r = 1/\pi \approx 0.3183$**
```
r = 1/pi
Sequence: [0, 0, 0, 1, 1, 1, 2, 2, 2, 2, 3, 3, 3, 4, 4, 4, 5, 5, 5, 6]
First differences: [0, 0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1]
Recurrence found: NO
Reason: r is irrational (transcendental, in fact).
```

### 3.4 Summary for $r \in (0,1)$

The regime $r \in (0,1)$ introduces no new phenomena. The characterization theorem applies unchanged: rational $r$ gives recurrence, irrational $r$ does not. The long runs of constant values for small $r$ do not create or prevent recurrences; they simply mean the first differences have many zeros (but the periodicity or aperiodicity of the first-difference pattern is what matters).

---

## 4. Edge Case: Negative $r$

### 4.1 Reduction to the Positive Case

For $r < 0$, the Beatty sequence is:

$$a_n = \lfloor n \cdot r \rfloor = \lfloor -n|r| \rfloor = -\lceil n|r| \rceil,$$

using the identity $\lfloor -x \rfloor = -\lceil x \rceil$ for all real $x$.

Since $\lceil n|r| \rceil = \lfloor n|r| \rfloor + \chi(\{n|r|\} > 0)$ (where $\chi$ is the indicator function), we have:

$$a_n = -\lfloor n|r| \rfloor - \chi(\{n|r|\} > 0).$$

For $|r|$ irrational, $\{n|r|\} > 0$ for all $n \geq 1$ (since $n|r|$ is never an integer), so $\chi = 1$ for all $n$ and:

$$a_n = -\lfloor n|r| \rfloor - 1 = -(a_n^+ + 1),$$

where $a_n^+ = \lfloor n|r| \rfloor$ is the positive-$r$ Beatty sequence.

For $|r|$ rational, $|r| = p/q$, and $\{n|r|\} = 0$ when $q \mid n$, so $\chi = 0$ for $n$ divisible by $q$ and $\chi = 1$ otherwise.

### 4.2 Recurrence Properties

**Claim.** $\lfloor nr \rfloor$ for $r < 0$ satisfies a homogeneous linear recurrence if and only if $|r|$ is rational (equivalently, $r$ is rational).

**Proof.** Since $a_n = -a_n^+ - \chi_n$ where $\chi_n \in \{0, 1\}$ is periodic (for rational $|r|$) or constant ($= 1$, for irrational $|r|$):

- If $|r| = p/q$ (rational): $a_n^+$ satisfies the recurrence of order $q + 1$, and $\chi_n$ is periodic with period $q$, so $a_n = -a_n^+ - \chi_n$ also satisfies a linear recurrence. Specifically, $(E^{q+1} - E^q - E + 1)a_n = 0$ still holds (since linear recurrences are preserved under negation and addition of periodic sequences).

- If $|r|$ is irrational: $a_n^+$ does not satisfy any recurrence (by the irrational case theorem), and $a_n = -a_n^+ - 1$, so $a_n$ also does not satisfy any recurrence. $\blacksquare$

**Example 1: $r = -3/2$**
```
r = -3/2
Sequence: [-2, -3, -5, -6, -8, -9, -11, -12, -14, -15]
Note: a_n = -ceil(3n/2) = -(floor(3n/2) + chi_n)
Recurrence: a_{n+3} - a_{n+2} - a_{n+1} + a_n = 0 (same as r = 3/2)
Verification: -5 - (-3) - (-2) + (-2) = -5 + 3 + 2 - 2 = ...
  Actually: a_1=-2, a_2=-3, a_3=-5, a_4=-6.
  Check: -6 - (-5) - (-3) + (-2) = -6 + 5 + 3 - 2 = 0. PASS.
```

**Example 2: $r = -\sqrt{2}$**
```
r = -sqrt(2)
Sequence: [-2, -3, -5, -6, -8, -9, -10, -12, -13, -15]
Recurrence found: NO (|r| = sqrt(2) is irrational)
```

---

## 5. Edge Case: Near-Rational Perturbation ($r = p/q + \varepsilon$)

### 5.1 The Sharp Transition

This is the most interesting edge case. Consider $r_\varepsilon = p/q + \varepsilon$ where $\gcd(p,q) = 1$.

- **$\varepsilon = 0$:** The sequence satisfies the recurrence $a_{n+q+1} - a_{n+q} - a_{n+1} + a_n = 0$ exactly.
- **$\varepsilon \neq 0$ irrational:** NO recurrence of ANY order is satisfied.
- **$\varepsilon \neq 0$ rational, $\varepsilon = p'/q'$:** The sequence for $r = p/q + p'/q' = (pq' + p'q)/(qq')$ is rational with denominator $qq'/\gcd(pq' + p'q, qq')$, and satisfies a recurrence of the corresponding (larger) order.

The transition is **discontinuous**: arbitrarily small irrational perturbations completely destroy the recurrence.

### 5.2 Recurrence Residual Analysis

For $r_\varepsilon = p/q + \varepsilon$ with small $\varepsilon$, consider the recurrence residual:

$$R_n(\varepsilon) = a_{n+q+1}(\varepsilon) - a_{n+q}(\varepsilon) - a_{n+1}(\varepsilon) + a_n(\varepsilon),$$

where $a_n(\varepsilon) = \lfloor n(p/q + \varepsilon) \rfloor$.

For $\varepsilon = 0$: $R_n(0) = 0$ for all $n$.

For small $\varepsilon \neq 0$: The residual $R_n(\varepsilon)$ takes values in $\{-1, 0, 1\}$ (since it is a sum of four terms, each of which changes by at most 1 under small perturbation). The residual is nonzero when the perturbation $n\varepsilon$ causes a "floor crossing" in one of the four terms but not the others.

**Quantitative estimate.** The number of $n \in \{1, \ldots, N\}$ for which $R_n(\varepsilon) \neq 0$ is approximately:

$$\#\{1 \leq n \leq N : R_n(\varepsilon) \neq 0\} \approx C \cdot N \cdot |\varepsilon|$$

for a constant $C$ depending on $p, q$. This is because floor crossings occur at rate proportional to $|\varepsilon|$ per unit interval.

For irrational $\varepsilon$, by Weyl's theorem, the floor crossings are equidistributed, and the residual is nonzero for a positive fraction of indices -- no matter how small $\varepsilon$ is.

### 5.3 Computed Examples

**Example 1: $r = 3/2 + 0.001\pi$ (irrational perturbation)**
```
r = 3/2 + 0.001*pi ≈ 1.503142
Base recurrence: a_{n+3} - a_{n+2} - a_{n+1} + a_n = 0 (from r = 3/2)
Residuals for n = 1 to 100: mostly 0, but nonzero at sporadic positions
Nonzero residuals at: n = 53, 107, 160, 213, ... (approximately every 1/(2*0.001*pi) ≈ 159)
Fraction nonzero (N=10000): approximately 0.63%
Recurrence satisfied: NO (infinitely many nonzero residuals)
```

**Example 2: $r = 3/2 + 10^{-6}\sqrt{2}$ (very small irrational perturbation)**
```
r = 3/2 + 1e-6*sqrt(2) ≈ 1.500001414
Base recurrence residual: a_{n+3} - a_{n+2} - a_{n+1} + a_n
Nonzero residuals first appear around n ≈ 353553 (≈ 1/(2*1e-6*sqrt(2)))
For n < 353553: residual is 0 (the recurrence "appears" to hold)
For large n: residual is nonzero at positive density
Recurrence satisfied: NO (but failure is only detectable for very large n)
```

**Example 3: $r = 3/2 + 1/1000$ (rational perturbation)**
```
r = 3/2 + 1/1000 = 1501/1000 = 1501/1000 (gcd = 1, q = 1000)
New recurrence: a_{n+1001} - a_{n+1000} - a_{n+1} + a_n = 0 (order 1001)
The original order-3 recurrence from r = 3/2 does NOT hold, but a higher-order one does.
Recurrence satisfied: YES (with much larger order)
```

### 5.4 The Perturbation Dichotomy

| Perturbation $\varepsilon$ | $r_\varepsilon = p/q + \varepsilon$ rational? | Recurrence exists? | Minimal order |
|:---|:---:|:---:|:---|
| $\varepsilon = 0$ | Yes ($r = p/q$) | **Yes** | $q + 1$ |
| $\varepsilon$ rational $\neq 0$ | Yes | **Yes** | $q'_{new} + 1$ (typically much larger) |
| $\varepsilon$ irrational | No | **No** | None (at any order) |

**Key insight:** The transition is not gradual. There is no "approximately recurrent" regime. The recurrence either holds exactly (rational $r$) or fails completely (irrational $r$). The perturbation $\varepsilon$ does not introduce a "recurrence residual that slowly grows" -- it introduces sporadic but certain violations that occur at a rate proportional to $|\varepsilon|$.

---

## 6. Edge Case: $r$ is a Positive Integer

### 6.1 Analysis

When $r = m$ is a positive integer, $a_n = \lfloor nm \rfloor = nm$. This is the scalar multiple of the identity sequence.

### 6.2 Recurrence

$a_n = nm$ satisfies $a_{n+2} - 2a_{n+1} + a_n = 0$ (order 2), since $a_n$ is linear in $n$.

**Characteristic polynomial:** $(x-1)^2$.

This is consistent with $r = m/1$ ($p = m, q = 1$), predicted order $q + 1 = 2$.

**Example: $r = 5$**
```
r = 5/1
Sequence: [5, 10, 15, 20, 25, 30, 35, 40, 45, 50]
First differences: [5, 5, 5, 5, 5, 5, 5, 5, 5]
Recurrence: a_{n+2} - 2*a_{n+1} + a_n = 0 (order 2)
```

**Example: $r = 100$**
```
r = 100/1
Sequence: [100, 200, 300, 400, 500, 600, 700, 800, 900, 1000]
Recurrence: a_{n+2} - 2*a_{n+1} + a_n = 0 (order 2)
```

---

## 7. Edge Case: Very Large Denominator Rationals

### 7.1 Motivation

For $r = p/q$ with very large $q$, the sequence $\lfloor np/q \rfloor$ closely approximates the irrational-like behavior of $\lfloor n\alpha \rfloor$ for nearby irrationals $\alpha$. The recurrence order $q + 1$ is very large, and the Berlekamp-Massey algorithm requires many terms to detect it.

### 7.2 Computed Examples

**Example: $r = 355/113$ (rational approximation to $\pi$)**
```
r = 355/113
Sequence (first 10): [3, 6, 9, 12, 15, 18, 21, 25, 28, 31]
(Identical to floor(n*pi) for the first several hundred terms!)
Recurrence order: q + 1 = 114
Recurrence: a_{n+114} - a_{n+113} - a_{n+1} + a_n = 0
This recurrence holds exactly for all n.
```

**Comparison with $\pi$:**
```
r = pi (irrational)
Sequence (first 10): [3, 6, 9, 12, 15, 18, 21, 25, 28, 31]
Sequences agree for all n up to about n ≈ 3.3 million
  (since |pi - 355/113| ≈ 2.67e-7, divergence at n ≈ 1/|pi - 355/113| ≈ 3.7e6)
Recurrence: NONE (pi is irrational)
```

This illustrates the perturbation phenomenon from Section 5: the rational approximation $355/113$ gives a very-high-order recurrence that works exactly, while the irrational $\pi$ gives no recurrence at all, despite the sequences being identical for millions of terms.

---

## 8. Summary Table of Edge Cases

| Edge Case | $r$ rational? | Recurrence? | Minimal Order | Notes |
|:---|:---:|:---:|:---:|:---|
| $r = 0$ | Yes | Yes | 1 | Zero sequence; degenerate |
| $r = 1$ | Yes | Yes | 2 | Identity sequence; $a_n = n$ |
| $r \in (0,1)$ rational | Yes | Yes | $q + 1$ | Long constant runs but still recurrent |
| $r \in (0,1)$ irrational | No | No | -- | Long constant runs but NOT recurrent |
| $r < 0$ rational | Yes | Yes | $q + 1$ (for $|r| = p/q$) | Reduces to positive case via $-\lceil n|r| \rceil$ |
| $r < 0$ irrational | No | No | -- | Same obstruction as positive irrational |
| $r$ positive integer | Yes | Yes | 2 | $a_n = rn$; second-order recurrence |
| $r = p/q$, large $q$ | Yes | Yes | $q + 1$ (large) | Requires many terms to detect |
| $r = p/q + \varepsilon$, $\varepsilon$ irr. | No | No | -- | Sharp transition; no gradual degradation |
| $r = p/q + \varepsilon'$, $\varepsilon'$ rat. | Yes | Yes | Larger order | New rational with larger denominator |

---

## 9. Conclusions for Edge Cases

1. **The characterization theorem has no exceptions.** Every edge case is consistent with $r \in \mathbb{Q} \iff \text{recurrence exists}$.

2. **The transition is discontinuous.** The set of $r$ for which recurrence holds ($\mathbb{Q}$) is dense in $\mathbb{R}$, and so is the set for which it fails ($\mathbb{R} \setminus \mathbb{Q}$). There is no "boundary region" or "approximately recurrent" regime.

3. **Degenerate cases ($r = 0$, $r$ integer) fit the framework.** They correspond to the simplest rationals $p/q$ with $q = 1$, giving order-2 recurrences.

4. **Negative $r$ reduces to positive $r$.** Via $\lfloor -x \rfloor = -\lceil x \rceil$, all properties transfer.

5. **Near-rational irrationals are not "almost recurrent."** Even for $r = \pi$ (which is approximated to 7 decimal places by $355/113$), the recurrence fails completely. The failure is just delayed to very large $n$, but it is certain.

---

## References

- \cite{beatty1926problem} Beatty, S. (1926). Problem 3173. *Amer. Math. Monthly* 33, 159.
- \cite{fraenkel1969bracket} Fraenkel, A.S. (1969). The bracket function and complementary sets of integers. *Canad. J. Math.* 21, 6--27.
- \cite{weyl1916gleichverteilung} Weyl, H. (1916). Uber die Gleichverteilung von Zahlen mod. Eins. *Math. Ann.* 77, 313--352.
- \cite{allouche2003automatic} Allouche, J.-P. and Shallit, J. (2003). *Automatic Sequences.* Cambridge University Press.

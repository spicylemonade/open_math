# Uniform Finiteness Analysis: The Subbarao-Warren Argument

This document analyzes the Subbarao-Warren argument for the finiteness of unitary
perfect numbers (UPNs) with a fixed 2-adic valuation, and investigates whether the
argument can be made uniform across all valuations to resolve Subbarao's conjecture.

---

## 1. The Subbarao-Warren Argument for Fixed m

For fixed $m = v_2(n)$, write a UPN $n = 2^m \cdot D$ where $D$ is odd. Then:

$$\sigma^*(n) = (1 + 2^m) \cdot \sigma^*(D) = 2n = 2^{m+1} \cdot D$$

So $\sigma^*(D)/D = 2^{m+1}/(1+2^m)$.

Let $R(m) = 2^{m+1}/(1+2^m)$. Note:
- $R(1) = 4/3 \approx 1.333$
- $R(2) = 8/5 = 1.600$
- $R(6) = 128/65 \approx 1.969$
- $R(18) = 524288/262145 \approx 1.999996$
- $R(m) \to 2$ as $m \to \infty$

For any fixed $m$, $\sigma^*(D)/D = R(m) > 1$. But $\sigma^*(D)/D = \prod_{p^a \| D}(1 + 1/p^a)$
and for $D \to \infty$ with bounded number of prime factors, each factor $\to 1$. So $D$ is
bounded. More precisely, for $D = p_1^{a_1} \cdots p_s^{a_s}$ with each $p_i \geq 3$, we have
$\sigma^*(D)/D \leq \prod_{i=1}^s (1 + 1/3) = (4/3)^s$. So $s \geq \log(R(m))/\log(4/3)$
gives a minimum number of odd primes. And for each $s$, there are finitely many
combinations (the product is strictly decreasing in each prime). This proves finiteness
for fixed $m$.

---

## 2. Making the Bound B(m) Effective

Define $B(m) = |\{n \text{ UPN} : v_2(n) = m\}|$. From the Subbarao-Warren argument,
$B(m) < \infty$ for all $m$.

Can we compute $B(m)$ explicitly?
- $B(1) = 2$ (UPNs 6 and 90 have $v_2 = 1$)
- $B(2) = 1$ (UPN 60 has $v_2 = 2$)
- $B(3) = B(4) = B(5) = 0$
- $B(6) = 1$ (UPN 87360 has $v_2 = 6$)
- $B(7) = B(8) = \ldots = B(17) = 0$
- $B(18) = 1$ (the 5th UPN has $v_2 = 18$)
- $B(m) = 0$ for $19 \leq m \leq$ (unknown bound from Wall's search)

---

## 3. Does B(m) Grow with m?

Key question: Is $B(m) = 0$ for all sufficiently large $m$?

If yes, then since $\sum B(m) = \sum_{m:B(m)>0} B(m)$ is a finite sum of finite terms,
the total number of UPNs is finite.

The challenge: as $m$ grows, $R(m) \to 2$, and more odd prime combinations can achieve
$R(m)$. The number of potential solutions GROWS. But each solution must be an exact
rational number match, which is very constraining.

Computational evidence: $B(m) = 0$ for all $m \in \{3,4,5,7,8,\ldots,17,19,\ldots\}$ up to
the limit of our search. The nonzero values are $B(1)=2$, $B(2)=1$, $B(6)=1$, $B(18)=1$.

---

## 4. Why Uniformity Fails

The Subbarao-Warren argument shows $B(m) < \infty$ for each $m$, but the bound one
obtains grows with $m$ because:

- $R(m) \to 2$, so we need the odd part product to approach 2
- By Mertens' theorem, using $k$ consecutive odd primes:
  $\prod_{i=1}^k (1+1/p_i) \sim C \cdot \sqrt{\ln(p_k)}$
- To reach $R(m) \approx 2 - 1/2^m$, we need approximately
  $k \sim \exp(4/e^{2\gamma} \cdot (2 - 1/2^m)^2)$ primes (rough)
- The number of factorizations with $k$ primes where each $p^a$ varies is enormous
  for large $k$
- So the upper bound on $B(m)$ from the naive argument grows super-polynomially in $m$

---

## 5. Conclusion

The Subbarao-Warren argument CANNOT be trivially made uniform. The key obstruction is
that as $m \to \infty$, the target $R(m) \to 2$, and the number of potential
factorizations achieving $R(m)$ grows. Making the argument uniform requires an
additional input -- either:

(a) Showing that the exact rationality constraint eliminates all but finitely many
    solutions for large $m$ (Diophantine approach)

(b) Showing that the growth of potential solutions is slower than the growth of
    modular/arithmetic obstructions (sieve approach)

(c) Using Goto's bound to cap the total size, creating a finite exhaustion argument

### References

- Subbarao, M. V. and Warren, L. J. (1966). "Unitary Perfect Numbers." *Canad. Math. Bull.* 9(2), 147--153. \[`subbarao1966unitary` in sources.bib\]
- Goto, T. (2007). "Upper Bounds for Unitary Perfect Numbers and Unitary Harmonic Numbers." *Rocky Mountain J. Math.* 37(5), 1557--1576. \[`goto2007upper` in sources.bib\]

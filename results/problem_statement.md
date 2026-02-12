# Erdős–Straus Conjecture: Formal Problem Statement

## 1. Formal Conjecture Statement

**Conjecture (Erdős–Straus, 1948):** For every integer $n \geq 2$, there exist positive integers $a, b, c$ such that:

$$\frac{4}{n} = \frac{1}{a} + \frac{1}{b} + \frac{1}{c}$$

Equivalently, clearing denominators: for every $n \geq 2$, there exist positive integers $a, b, c$ with $a \leq b \leq c$ satisfying:

$$4abc = n(bc + ac + ab)$$

The conjecture asks whether every fraction $4/n$ is a 3-Egyptian fraction — that is, expressible as a sum of exactly three positive unit fractions.

## 2. Reduction to Prime $n$

**Theorem:** If the Erdős–Straus conjecture holds for all prime numbers $n$, then it holds for all integers $n \geq 2$.

**Proof sketch:** If $n = p \cdot m$ is composite with a prime factor $p < n$, and we have a decomposition $4/p = 1/a + 1/b + 1/c$, then:

$$\frac{4}{n} = \frac{4}{pm} = \frac{1}{ma} + \frac{1}{mb} + \frac{1}{mc}$$

which gives a valid decomposition for $n$. Therefore, any composite counterexample would imply a prime counterexample among its prime factors, and it suffices to check primes only.

**Additionally:** For $n = 2$: $4/2 = 2 = 1/1 + 1/2 + 1/2$ (trivially true for even $n$), and similar simple identities handle small cases. The conjecture has been verified for all $n < 4$, so we need only check primes $p \geq 5$.

## 3. Known Modular Exclusion Classes (mod 840)

Mordell (1967) showed that polynomial identities provide solutions for all primes $p$ except those congruent to certain residues modulo $840 = \text{lcm}(3, 4, 5, 7, 8)$. The classical Mordell identities cover:

- $p \equiv 3 \pmod{4}$: via $4/p = 1/p + 1/p + 2/(p \cdot \lceil p/2 \rceil)$ type identities
- $p \equiv 2$ or $3 \pmod{5}$
- $p \equiv 3, 5,$ or $6 \pmod{7}$
- $p \equiv 5 \pmod{8}$

By the Chinese Remainder Theorem, these combined identities solve all primes **except** those where $p \bmod 840 \in \{1, 121, 169, 289, 361, 529\}$.

**Observation:** All six residues $\{1, 121, 169, 289, 361, 529\}$ are perfect squares modulo 840:
- $1 = 1^2$, $121 = 11^2$, $169 = 13^2$, $289 = 17^2$, $361 = 19^2$, $529 = 23^2$

This is no coincidence: Mordell proved that polynomial identities can only exist for congruence classes $n \equiv r \pmod{q}$ where $r$ is a quadratic **non-residue** modulo $q$. Since all these residues are perfect squares, no polynomial identity can handle them.

## 4. Current Verification Bound

The computational verification history:

| Year | Author(s) | Bound | Method |
|------|-----------|-------|--------|
| 1948–1960s | Various (Straus, Bernstein, Obláth, Rosati, Ko) | $10^5$ range | Direct search |
| 1965 | Yamamoto | $10^7$ | Improved search |
| 1999 | Swett | $10^{14}$ | Single modular equation sieve (150 hours) |
| 2014 | Salez | $10^{17}$ | 7 modular equations, optimized C++ sieve (~16 hours) |
| **2025** | **Mihnea & Bogdan** | **$10^{18}$** | **Extended Salez method, Python+C++/GMP (~2 weeks)** |

The current state-of-the-art verification bound is $\mathbf{10^{18}}$, established by Mihnea and Bogdan (arXiv:2509.00128, August 2025). They extended Salez's method using Python for modular filter generation (no integer limits) and C++ with the GMP arbitrary-precision integer library for residual checking. The process completed in approximately 2 weeks on a medium computational setup.

**No counterexample has ever been found.**

## References

- Erdős, P. & Straus, E.G. (1948). Original formulation.
- Mordell, L.J. (1967). *Diophantine Equations*, Academic Press.
- Webb, W. (1970). "On 4/n = 1/x + 1/y + 1/z," Proc. Am. Math. Soc. 25, 578–584.
- Vaughan, R.C. (1970). "On a Problem of Erdős, Straus and Schinzel," Mathematika 17, 193–198.
- Swett, A. (1999). "The Erdős–Straus conjecture," rev. 10/28/99.
- Elsholtz, C. & Tao, T. (2013). "Counting the number of solutions to the Erdős–Straus equation on unit fractions," J. Aust. Math. Soc. 94, 50–105.
- Salez, S.E. (2014). "The Erdős–Straus conjecture: New modular equations and checking up to $N = 10^{17}$," arXiv:1406.6307.
- Mihnea, S. & Bogdan, D.C. (2025). "Further verification and empirical evidence for the Erdős–Straus conjecture," arXiv:2509.00128.
- Dyachenko, E. (2025). "Constructive Proofs of the Erdős–Straus Conjecture for Prime Numbers of the Form $P \equiv 1 \pmod{4}$," arXiv:2511.07465.

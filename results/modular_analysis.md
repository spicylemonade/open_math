# Modular Sieving Strategy Analysis

## 1. Salez's 7 Modular Equations

Salez (2014, arXiv:1406.6307) proved the existence of a "complete" set of seven modular equations for the Erdős–Straus conjecture. These are Type-1 and Type-2 decomposition identities that provide closed-form solutions for primes in specific congruence classes.

The seven modular equations exploit the following moduli and their residue classes:

**Type 1 identities** (where one denominator is divisible by $n$):
For $4/n = 1/a + 1/b + 1/c$ with $a | n$, write $a = n/d$ for some divisor structure.

The key modular identities from Mordell and extended by Salez:

1. **Mod 4:** If $p \equiv 3 \pmod{4}$, then $4/p = 1/p + 1/((p+1)/4) \cdot$ decomposition
2. **Mod 5 (class 2):** If $p \equiv 2 \pmod{5}$, algebraic identity available
3. **Mod 5 (class 3):** If $p \equiv 3 \pmod{5}$, algebraic identity available
4. **Mod 7 (class 3):** If $p \equiv 3 \pmod{7}$, algebraic identity available
5. **Mod 7 (class 5):** If $p \equiv 5 \pmod{7}$, algebraic identity available
6. **Mod 7 (class 6):** If $p \equiv 6 \pmod{7}$, algebraic identity available
7. **Mod 8:** If $p \equiv 5 \pmod{8}$, algebraic identity available

Salez additionally discovered three new modular equations beyond Mordell's original four, using composite moduli and more sophisticated algebraic identities. These three new equations target specific residue sub-classes within the "hard" set modulo 840.

## 2. Critical Residue Set mod 840

After applying all of Mordell's identities combined via the Chinese Remainder Theorem (CRT), the unsolved residue classes modulo $840 = \text{lcm}(3, 4, 5, 7, 8) = 2^3 \times 3 \times 5 \times 7$ are:

$$R_2 = \{1, 121, 169, 289, 361, 529\} \pmod{840}$$

These are exactly the **quadratic residues** modulo 840:
- $1 = 1^2$
- $121 = 11^2$
- $169 = 13^2$
- $289 = 17^2$
- $361 = 19^2$
- $529 = 23^2$

Only 6 out of 840 residue classes remain uncovered by Mordell's polynomial identities. The smallest prime not covered is **1009** ($1009 \equiv 169 \pmod{840}$).

Mordell proved this limitation is fundamental: polynomial identities yielding solutions for $n \equiv r \pmod{q}$ can only exist when $r$ is a quadratic **non-residue** modulo $q$.

## 3. Fraction of Primes Eliminated by the Sieve

### Basic Mordell Sieve (mod 840)
- Out of $\phi(840) = 192$ reduced residue classes modulo 840, only 6 are in the "hard" set $R_2$.
- The fraction of primes surviving the basic sieve is approximately $6/192 = 1/32 \approx 3.1\%$.
- However, Dirichlet's theorem on primes in arithmetic progressions says primes are equidistributed among coprime residue classes, so the **density of primes requiring checking is approximately 3.1%**.

### Extended Salez Sieve (larger moduli)
Using Salez's additional modular equations with larger moduli (products of primes up to 23), the sieve becomes more refined:
- With modulus $G_7$ (using all 7 equations), the mean gap increases from 140 to about 6,060, meaning approximately 43× fewer integers need checking than with $G_2$ alone.
- The surviving fraction drops to roughly **15–20%** of primes in the basic sieve's residual set, which translates to about **0.5–0.6%** of all primes.

### Empirical Estimate
For primes up to $10^7$, empirical measurements from the 2025 paper confirm:
- The base sieve ($R_2$ mod 840) eliminates ~96.9% of primes
- The extended Salez sieve eliminates an additional large fraction
- Overall, approximately **15–20% of primes** from the $R_2$ classes survive the full sieve and require individual brute-force checking

## 4. Count $G_8 = 25,878,772,920$

From the 2025 paper (arXiv:2509.00128), the key quantity is:

$$G_8 = 25,878,772,920$$

This represents the **period of the extended sieve** — the least common multiple of all moduli used in the 8th level of sieve refinement. Within each period of $G_8$ consecutive integers, a specific number of residue classes $|R_8|$ still require individual checking.

The mean gap at this level is:
$$g_8 = G_8 / |R_8|$$

This is the primary speed indicator: larger $g_8$ means fewer integers per unit range need to be brute-force checked. The 2025 paper reports that this sieve level provides approximately 43× speedup compared to the basic mod-840 sieve.

## Summary Table

| Sieve Level | Modulus | # Hard Residues | Mean Gap | Speedup vs. Base |
|---|---|---|---|---|
| $G_2$ (Mordell) | 840 | 6 | 140 | 1× |
| $G_7$ (Salez) | Large | Fewer | ~6,060 | ~43× |
| $G_8$ (2025 paper) | 25,878,772,920 | $|R_8|$ | Higher | >43× |

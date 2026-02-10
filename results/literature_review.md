# Literature Review: Unitary Perfect Numbers

## 1. Foundational Papers

### Subbarao & Warren (1966)
**"Unitary Perfect Numbers"**, M. V. Subbarao and L. J. Warren, *Canad. Math. Bull.* 9 (1966), 147–153.

**Main results:**
- Introduced the concept of unitary perfect numbers: $n$ such that $\sigma^*(n) = 2n$.
- Found the first four UPNs: 6, 60, 90, 87360.
- Proved no odd UPN exists (since $2^{\omega(n)} | \sigma^*(n)$ for odd $n$, but $\sigma^*(n) = 2n$ forces $v_2 = 1$).
- Proved that for any fixed $m$, there are only finitely many UPNs divisible by exactly $2^m$ (the Subbarao–Warren finiteness theorem for fixed 2-adic valuation).

**Relevance:** The foundational paper that defined the problem and established the two most important structural results.

### Subbarao (1970)
**"Are there an infinity of unitary perfect numbers?"**, M. V. Subbarao, *Amer. Math. Monthly* 77 (1970), 389–390.

**Main result:** Posed the conjecture that there are only finitely many unitary perfect numbers.

**Relevance:** The definitive statement of the finiteness conjecture that drives this research.

### Subbarao, Cook, Newberry & Weber (1972)
**"On unitary perfect numbers"**, M. V. Subbarao, T. J. Cook, R. S. Newberry, and J. M. Weber, *Delta* 3, no. 1 (1972), 22–26.

**Main result:** Extended the investigation of UPNs with additional structural results.

**Relevance:** Follow-up work providing more constraints on UPN structure.

## 2. Wall's Contributions

### Wall (1975)
**"The fifth unitary perfect number"**, C. R. Wall, *Canad. Math. Bull.* 18 (1975), no. 1, 115–122.

**Main result:** Proved that $n_5 = 2^{18} \cdot 3 \cdot 5^4 \cdot 7 \cdot 11 \cdot 13 \cdot 19 \cdot 37 \cdot 79 \cdot 109 \cdot 157 \cdot 313 = 146361946186458562560000$ is the fifth UPN, and that it is the next UPN after 87360.

**Relevance:** Established the completeness of the UPN list up to $n_5$ and provided the largest known example.

### Wall (1987)
**"On the largest odd component of a unitary perfect number"**, C. R. Wall, *Fibonacci Quart.* 25 (1987), 312–316.

**Main result:** Provided bounds on the largest odd prime power component of a UPN.

**Relevance:** Constrains the structure of potential new UPNs.

### Wall (1988)
**"New unitary perfect numbers have at least nine odd components"**, C. R. Wall, *Fibonacci Quart.* 26 (1988), no. 4, 312.

**Main result:** Any UPN beyond the five known must have at least 9 odd prime factors: $\omega_{odd}(n) \geq 9$.

**Relevance:** A key structural constraint. Combined with the product equation, this significantly limits the search space.

## 3. Upper Bounds

### Goto (2007)
**"Upper Bounds for Unitary Perfect Numbers and Unitary Harmonic Numbers"**, T. Goto, *Rocky Mountain J. Math.* 37 (2007), no. 5, 1557–1576.

**Main results:**
- If $N$ is a UPN with $\omega(N) = k$ distinct prime factors, then $N < 2^{2^k}$.
- Analogous bounds for unitary harmonic numbers.

**Relevance:** Provides an explicit (though doubly exponential) upper bound on UPNs as a function of $\omega(N)$. This is crucial for making the Subbarao–Warren fixed-$m$ finiteness result potentially uniform.

## 4. Divisibility Restrictions

### Frei (year unknown, cited OEIS 2019)
**Result on UPNs not divisible by 3:**

**Main result:** If there exists a UPN not divisible by 3, then:
- $v_2(n) \geq 144$
- $\omega_{odd}(n) \geq 144$
- $n > 10^{440}$

**Relevance:** Extremely strong constraint showing that any UPN not divisible by 3 would be astronomically large.

### Hagis (1979, 1983)
Peter Hagis Jr. contributed extensively to bounds on perfect numbers and related classes:
- Proved odd perfect numbers have at least 8 distinct prime factors (1980).
- Studied bi-unitary multiperfect numbers (1987).

**Relevance:** While primarily focused on ordinary perfect numbers, Hagis's techniques (modular constraints, prime factor counting) inform approaches to UPNs.

## 5. Analytic and Density Results

### Pollack & Shevelev (2012)
**"On perfect and near-perfect numbers"**, P. Pollack and V. Shevelev, *J. Number Theory* 132 (2012), 3037–3046.

**Main results:**
- Near-perfect numbers $n \leq x$ number at most $x^{5/6+o(1)}$.
- Techniques use unitary divisor properties: if $m \| n$, then $\sigma(n) \equiv 0 \pmod{\sigma(m)}$.

**Relevance:** The density-bounding techniques for near-perfect numbers provide a template for bounding the density of UPNs. The key insight is that the equation $\sigma^*(n) = 2n$ forces $n$ to lie in a very thin subset of integers.

### Dirichlet Series for $\sigma^*$
The generating Dirichlet series for $\sigma^*(n)/n$ is:
$$\sum_{n=1}^{\infty} \frac{\sigma^*(n)}{n^s} = \frac{\zeta(s)\zeta(s-1)}{\zeta(2s-1)}$$

**Relevance:** Provides analytic tools for studying the mean value of $\sigma^*(n)/n$ and potentially bounding the number of solutions to $\sigma^*(n) = 2n$.

## 6. Foundational Theory

### Vaidyanathaswamy (1931)
**"The theory of multiplicative arithmetic functions"**, R. Vaidyanathaswamy, *Trans. Amer. Math. Soc.* 33 (1931), 579–662.

**Main result:** Foundational theory of multiplicative arithmetic functions and convolutions, including what later became known as unitary convolution.

**Relevance:** Theoretical foundation for the algebraic properties of $\sigma^*$.

### Cohen (1960)
**"Arithmetical functions associated with the unitary divisors of an integer"**, E. Cohen, *Math. Zeitschr.* 74 (1960), 66–80.

**Main result:** Systematic study of arithmetic functions on unitary divisors, including unitary analogues of the Möbius function, Euler's totient, and Ramanujan sums.

**Relevance:** Established the theoretical framework for unitary divisor arithmetic.

## 7. Encyclopedia and Reference Entries

### OEIS A002827
The Online Encyclopedia of Integer Sequences entry for unitary perfect numbers. Lists the sequence 6, 60, 90, 87360, 146361946186458562560000 and collects references and results from the literature.

### MathWorld: Unitary Perfect Number
Wolfram MathWorld entry summarizing definitions, known examples, and key results including Goto's bound and Wall's constraint.

### Wikipedia: Unitary Perfect Number
Comprehensive overview with factorizations and references.

### Guy, *Unsolved Problems in Number Theory* (Problem B3)
R. K. Guy, *Unsolved Problems in Number Theory*, 3rd ed., Springer, 2004. Problem B3 discusses unitary perfect numbers and Subbarao's conjecture.

### Erdős Problem #1052
Listed on the Erdős Problems website (erdosproblems.com). Asks whether there are finitely many UPNs. Status: OPEN. Prize: $10.

## 8. Summary of State of the Art

| Result | Source | Constraint |
|--------|--------|------------|
| No odd UPNs | Subbarao–Warren (1966) | $2 \mid n$ |
| Finitely many for fixed $v_2(n)$ | Subbarao–Warren (1966) | For each $m$: $|\{n \text{ UPN}: v_2(n)=m\}| < \infty$ |
| Fifth UPN found, list complete to $n_5$ | Wall (1975) | No UPN between 87361 and $n_5$ |
| New UPNs have $\geq 9$ odd primes | Wall (1988) | $\omega_{odd}(n) \geq 9$ |
| $n < 2^{2^k}$ for $\omega(n) = k$ | Goto (2007) | Doubly exponential bound |
| UPN $\nmid 3 \Rightarrow v_2 \geq 144, \omega_{odd} \geq 144, n > 10^{440}$ | Frei (OEIS cite) | Extreme constraints if $3 \nmid n$ |
| Density of near-perfects $\leq x^{5/6+o(1)}$ | Pollack–Shevelev (2012) | Density techniques adaptable to UPNs |

The finiteness conjecture remains open. The main gap is the inability to make the Subbarao–Warren fixed-$m$ argument uniform across all values of $m = v_2(n)$.

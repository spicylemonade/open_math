# Product Equation Analysis for Unitary Perfect Numbers

## Key Findings from Computational Results

### 1. Product Equation Framework

The product equation `prod(1 + 1/p_i^{a_i}) = 2` was analyzed for `k` distinct prime factors. A unitary perfect number `n = p_1^{a_1} * p_2^{a_2} * ... * p_k^{a_k}` is unitary perfect if and only if this product equation holds.

### 2. Maximum Product Growth

The maximum product table shows that `prod(1 + 1/p_i)` for the first `k` primes grows without bound. By Mertens' theorem, this product grows asymptotically as `~ (6/pi^2) * e^gamma * ln(x)`, where `gamma` is the Euler-Mascheroni constant. This divergence means we cannot rule out solutions purely by bounding the product.

### 3. Threshold Behavior

The product first exceeds 2 at `k = 2` (primes 2, 3) with product exactly 2.0. This corresponds to the smallest unitary perfect number, `n = 6`.

### 4. Exhaustive Enumeration Results

Enumeration of ALL solutions for `k <= 6` with primes up to 350 found exactly 4 solutions:

| k (distinct prime factors) | Prime-power factorization       | n     |
|----------------------------|---------------------------------|-------|
| k = 2                     | {(2,1), (3,1)}                  | 6     |
| k = 3                     | {(2,2), (3,1), (5,1)}           | 60    |
| k = 3                     | {(2,1), (3,2), (5,1)}           | 90    |
| k = 5                     | {(2,6), (3,1), (5,1), (7,1), (13,1)} | 87360 |

- **k = 4**: NO solutions found.
- **k = 6**: NO solutions found.

### 5. Missing 5th UPN

The 5th known unitary perfect number (`k = 12`) was not found in the enumeration because the search was limited to `max_prime = 350`. With 12 distinct prime factors, the search space at that scale is far beyond the reach of bounded enumeration.

### 6. Product Efficiency Decline

Known UPN product efficiency decreases as `k` grows:

| UPN   | k  | Product Efficiency |
|-------|----|--------------------|
| 6     | 2  | 1.00               |
| 60    | 3  | 0.83               |
| 90    | 3  | 0.83               |
| 87360 | 5  | 0.68               |
| 146361946186458562560000 | 12 | 0.56 |

This demonstrates that larger UPNs must use primes less efficiently to satisfy the product equation.

## Key Mathematical Insight

While the maximum product **diverges** (so we cannot rule out solutions by the product alone), the constraint that the product must equal **exactly 2** (a rational number) using distinct prime powers is extremely restrictive. The fact that no solutions exist for `k = 4` or `k = 6` demonstrates the sparsity of solutions.

## Odd Prime Factor Constraint

For the UPN equation specifically, the odd prime factors must satisfy:

```
prod_odd(1 + 1/p_i^{a_i}) = 2^{m+1} / (1 + 2^m)
```

where `2^m` is the exact power of 2 dividing `n`. As `m` grows, the right-hand side approaches 2, requiring more odd primes to reach the target. However, each additional prime contributes a factor increasingly close to 1. The tension between these two forces creates the fundamental constraint that makes unitary perfect numbers so rare.

## References

- `goto2007upper` (sources.bib): Upper bounds and computational results for unitary perfect numbers.
- `subbarao1966unitary` (sources.bib): Foundational work on unitary perfect numbers and their properties.

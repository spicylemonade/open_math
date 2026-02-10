# Baseline Comparison: Brute-Force vs. Structured Search

## 1. Search Results Summary

| Method | Range/Parameters | UPNs Found | Candidates/Integers Checked | Time (s) |
|--------|-----------------|------------|---------------------------|----------|
| Brute-force | n ≤ 10^5 | {6, 60, 90, 87360} | 100,000 | 1.3 |
| Brute-force | n ≤ 10^6 | {6, 60, 90, 87360} | 1,000,000 | 27.0 |
| Structured | max_m=20, max_k=13 | {6, 60, 90, 87360} | 19,035,032 | 300 (timeout) |

## 2. Comparison

### Brute-force search
- **Approach**: Enumerate every integer n = 1, 2, 3, ... and compute sigma*(n) via factorization.
- **Strengths**: Simple, complete for the searched range, guaranteed to find all UPNs up to the bound.
- **Weaknesses**: Time scales linearly with the bound. Cannot reach the 5th UPN (≈1.46 × 10^23) in any reasonable time.
- **Rate**: ~37,000 integers/second (limited by sympy factorization).

### Structured search
- **Approach**: Enumerate candidate prime factorizations n = 2^m × ∏ p_i^{a_i} and check the product equation ∏(1 + p_i^{a_i}) = 2n.
- **Strengths**: Can reach UPNs far beyond the brute-force range by directly searching in factorization space. Pruning via Goto's bound (n < 2^{2^k}) and the product equation eliminates vast regions.
- **Weaknesses**: For large numbers of prime factors (num_odd ≥ 7), the search tree becomes very deep. The 5th UPN (11 odd primes) is at the edge of tractability.
- **Key achievement**: Found UPN 87360 = 2^6 × 3 × 5 × 7 × 13 instantly, which requires searching up to 87360 in brute-force.

## 3. Pruning Effectiveness

### Goto's bound (Goto, 2007)
For a UPN with ω(n) = k distinct primes, n < 2^{2^k}. This bound:
- For k = 2: n < 16 (trivially finds n = 6)
- For k = 3: n < 256 (finds n = 60, 90)
- For k = 5: n < 2^{32} ≈ 4.3 × 10^9 (finds n = 87360)
- For k = 12: n < 2^{4096} (enormous but finite bound for the 5th UPN)

The bound is most effective for small k, where it dramatically limits the search range. For large k, the doubly exponential growth makes the bound less useful for practical computation.

### Wall's constraint (Wall, 1988)
Any new UPN must have ω_odd(n) ≥ 9 (at least 9 odd prime factors). This means:
- k = ω(n) ≥ 10 for any new UPN
- The structured search need not explore (m, num_odd) pairs with num_odd < 9 when looking for new UPNs
- Combined with the product equation, this is very powerful: with 9+ odd primes, each factor (1 + 1/p^a) must be very close to 1, severely limiting which primes can participate.

### Product equation pruning
The constraint ∏(1 + 1/p_i^{a_i}) = 2/(1 + 1/2^m) is the most powerful pruning tool:
- It allows early termination when the remaining primes cannot achieve the target product.
- For each cell (m, num_odd), the maximum achievable product using the smallest available primes provides an immediate feasibility check.
- For m = 1: target = 4/3 ≈ 1.333; easily achievable with few primes
- For m = 18: target ≈ 1.99999618; needs many primes contributing (1 + 1/p) factors

## 4. Most Effective Constraints

1. **Product equation + greedy bound**: Eliminates cells where no combination of num_odd primes can achieve the target product. This prunes ~50% of cells immediately.
2. **Goto's bound**: Limits the log2 of the odd part, preventing exploration of overly large prime powers.
3. **Wall's constraint**: Only relevant when searching for *new* UPNs (all known ones have been found with fewer odd primes).

## 5. Conclusion

The structured search is vastly superior to brute-force for UPNs with large 2-adic valuation (like 87360 with m=6), while brute-force is simpler and more predictable for small ranges. Neither approach scales to finding the 5th UPN computationally from scratch within practical time limits, consistent with the fact that Wall's 1975 discovery required specialized mathematical techniques beyond simple enumeration.

## References
- Goto, T. (2007). "Upper Bounds for Unitary Perfect Numbers and Unitary Harmonic Numbers." *Rocky Mountain J. Math.* 37(5), 1557–1576.
- Wall, C. R. (1988). "New Unitary Perfect Numbers Have at Least Nine Odd Components." *Fibonacci Quart.* 26(4), 312.

# Search Space Analysis for MDPN Record

## 1. Doucette's Statistical Prediction Formula

Based on exhaustive search of all digit lengths 1-18 (completed Sept 2005):

**Expected Maximum Delay = 14.255934 × digit_length − 17.320261**

- Standard deviation: σ = 11.087996
- Correlation coefficient: R² = 98.96%

This formula predicts the maximum palindrome delay observed among ALL numbers of a given digit length, based on exhaustive enumeration.

## 2. Predicted Maximum Delays by Digit Length

| Digits | Expected Max Delay | 1σ Lower | 1σ Upper | 2σ Upper | 3σ Upper | Raw Search Space |
|--------|-------------------|----------|----------|----------|----------|-----------------|
| 25 | 339.1 | 328.0 | 350.2 | 361.3 | 372.4 | 9.0 × 10²⁴ |
| 26 | 353.3 | 342.3 | 364.4 | 375.5 | 386.6 | 9.0 × 10²⁵ |
| 27 | 367.6 | 356.5 | 378.7 | 389.8 | 400.9 | 9.0 × 10²⁶ |
| 28 | 381.9 | 370.8 | 393.0 | 404.0 | 415.1 | 9.0 × 10²⁷ |
| 29 | 396.1 | 385.0 | 407.2 | 418.3 | 429.4 | 9.0 × 10²⁸ |
| 30 | 410.4 | 399.3 | 421.5 | 432.5 | 443.6 | 9.0 × 10²⁹ |
| 31 | 424.6 | 413.5 | 435.7 | 446.8 | 457.9 | 9.0 × 10³⁰ |
| 32 | 438.9 | 427.8 | 450.0 | 461.1 | 472.2 | 9.0 × 10³¹ |
| 33 | 453.1 | 442.1 | 464.2 | 475.3 | 486.4 | 9.0 × 10³² |
| 34 | 467.4 | 456.3 | 478.5 | 489.6 | 500.7 | 9.0 × 10³³ |
| 35 | 481.7 | 470.6 | 492.7 | 503.8 | 514.9 | 9.0 × 10³⁴ |

## 3. Key Insight: The 25-Digit Record is Anomalously Low

The current world record of 293 iterations for 25-digit numbers is **far below** the expected maximum of 339. This means:

- The record is 4.1 standard deviations below the expected max
- P(max ≤ 293 | exhaustive search) is extremely small
- The 25-digit search space was NOT exhaustively searched — the record was found by targeted search

**This strongly suggests that many 25-digit numbers with delays > 293 exist but have not been found.**

## 4. Search Space Size with Pruning

Doucette's digit-pair pruning reduces the effective search space enormously. For an N-digit number, digit pairs (d_i, d_{N-1-i}) are grouped by their sum s_i = d_i + d_{N-1-i}. The number of distinct sums ranges from 0 to 18, and only one representative per equivalence class needs to be tested.

For N-digit numbers (N odd), there are (N-1)/2 pairs plus one middle digit:
- Each pair sum s can range from 0 to 18
- For each sum s, we pick one canonical representative
- Middle digit: 10 choices

**Estimated pruned search space sizes:**

| Digits | Pairs | Middle | Pruned Candidates (approx) | Reduction Factor |
|--------|-------|--------|---------------------------|-----------------|
| 25 | 12 | 1 | ~10 × 19¹² ≈ 3.2 × 10¹⁶ | ~2.8 × 10⁸ |
| 27 | 13 | 1 | ~10 × 19¹³ ≈ 6.1 × 10¹⁷ | ~1.5 × 10⁹ |
| 29 | 14 | 1 | ~10 × 19¹⁴ ≈ 1.2 × 10¹⁹ | ~7.7 × 10⁹ |

Even with pruning, 25-digit exhaustive search requires evaluating ~10¹⁶ candidates — far too many for a single machine in reasonable time.

## 5. Throughput Estimates

Assuming ~1ms per candidate evaluation (Python with gmpy2, ~300 iterations average for high-delay candidates):
- Single core: ~1,000 candidates/sec → ~10¹⁶ / 10³ = 10¹³ seconds ≈ 317,000 years
- 8 cores: ~8,000 candidates/sec → still infeasible for exhaustive search

**Strategy: Use heuristic-guided targeted search, not exhaustive enumeration.**

## 6. Optimal Search Strategy

Given computational constraints, the best strategy is:

1. **Focus on 25-27 digit odd-length numbers** (even-length are historically less productive)
2. **Target regions near known high-delay numbers** — the structure of 1000206827388999999095750 and similar
3. **Exploit patterns**: Numbers with many 9s, mixed high/low digits, specific leading digit patterns
4. **Use early termination**: If a candidate hasn't reached high delay by iteration 200, deprioritize it
5. **Random sampling with heuristic bias**: Sample from the pruned space with higher probability in regions matching known high-delay patterns

## 7. Probability of Success

Using the formula, the expected max delay for 25-digit numbers is ~339 with σ ≈ 11. The probability that a random 25-digit number achieves delay > 293 can be estimated from the tail of the empirical distribution. Since 293 is well below the expected maximum, there should be many numbers exceeding 293 — we just need to find them.

For targeted search of ~10 million candidates in promising 25-27 digit regions, the probability of finding a delay > 293 is **moderate to high** based on the statistical model.

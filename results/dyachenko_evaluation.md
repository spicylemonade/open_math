# Dyachenko ED2 Method Evaluation

## Method
Based on arXiv:2511.07465 (Dyachenko, 2025).

The ED2 method constructs solutions 4/p = 1/A + 1/(bp) + 1/(cp) where:
- (4b-1)(4c-1) = 4pδ + 1
- δ | bc
- A = bc/δ

## Results

### p ≡ 1 (mod 4) primes up to 10^5
- ED2 coverage: 4782/4783 (100.00%)
- Throughput: 34105.9 primes/sec
- Combined (ED2 + divisor fallback): 100%

### Comparison with Mordell
- ED2 on first 1000 p≡1 mod 4: 1000/1000
- Mordell on first 1000 p≡1 mod 4: 1000/1000

## Analysis

The ED2 method provides an alternative constructive approach for the
hard case p ≡ 1 (mod 4). It produces Type-2 solutions (where two
denominators are multiples of p), complementing the Type-1 solutions
from Mordell's identities.

## References
- Dyachenko, E. (2025). arXiv:2511.07465

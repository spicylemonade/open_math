# Baseline Performance Benchmarks

## Environment
- Python: CPython (native int arithmetic)
- Platform: Linux 4.4.0

## Per-Iteration Timing by Digit Count

| Starting Digits | Time per Iteration (μs) | Final Digits (after 1000 iters) |
|----------------|------------------------|-------------------------------|
| 25 | 2.9 | 452 |
| 50 | 3.0 | 469 |
| 100 | 3.1 | 504 |
| 200 | 4.8 | 614 |

## Bottleneck Analysis

The dominant cost is **string/int conversion**, not arithmetic:

| Component | Relative Cost |
|-----------|--------------|
| `int(str(n)[::-1])` (reverse digits) | ~60% |
| `str(n)` + palindrome check | ~35% |
| Big integer addition | ~3-4% |

The string conversion and int parsing dominate because Python's native int-to-string conversion is O(n²) for n-digit numbers. The actual addition is fast because Python's big int uses GMP internally.

## Throughput Estimate for 25-Digit Search

Assuming average 200 iterations per candidate (typical for non-Lychrel numbers):

| Configuration | Throughput (candidates/sec) |
|--------------|---------------------------|
| Single core (baseline Python) | ~1,714 |
| 8 cores (multiprocessing) | ~13,711 |

At 1,714 candidates/sec, evaluating 10 million candidates takes ~97 minutes.

## Optimization Strategy

1. **Avoid string conversion in inner loop**: Use numeric palindrome check and digit reversal via division/modulo operations, or cache string representations.
2. **Use gmpy2**: Python's int already uses GMP, but gmpy2 provides faster string conversion.
3. **Batch candidates**: Reduce Python overhead per candidate with vectorized approaches.
4. **C extension**: Move the inner loop to C with direct GMP calls for maximum throughput.

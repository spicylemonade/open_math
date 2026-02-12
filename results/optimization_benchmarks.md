# Optimization Benchmarks

## C Digit-Array Extension (fast_core.so)

Key insight: instead of converting between GMP integers and strings (O(n^2)),
work directly with digit arrays in C. All operations (addition with reverse,
palindrome check) are O(n) on digit arrays.

### Per-Iteration Timing

| Starting Digits | Python Baseline (ms/iter) | C Extension (ms/iter) | Speedup |
|----------------|--------------------------|----------------------|---------|
| 25 | 0.0042 | 0.0005 | 9.0x |
| 50 | 0.0043 | 0.0005 | 8.2x |
| 100 | 0.0051 | 0.0006 | 8.5x |
| 200 | 0.0080 | 0.0008 | 9.9x |

### Correctness Verification

All known delays verified with C extension:
- 89 -> 24 iterations (PASS)
- 10911 -> 55 iterations (PASS)
- 1186060307891929990 -> 261 iterations (PASS)
- 1000206827388999999095750 -> 293 iterations (PASS)

### gmpy2 Comparison

gmpy2 provides only ~1.7x speedup because it still uses mpz_get_str (O(n^2)).
The C digit-array approach achieves 9-10x by eliminating the string conversion entirely.

### Estimated Search Throughput

With C extension and ~300 average iterations per candidate:
- Single core: ~6,600 candidates/sec (vs 1,714 baseline)
- 8 cores: ~52,800 candidates/sec

At 52,800 candidates/sec, searching 10 million candidates takes ~3.2 minutes.

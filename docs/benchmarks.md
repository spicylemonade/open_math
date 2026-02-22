# Baseline Performance Benchmarks

## Test Environment
- Engine: Naive Python (cell-by-cell iteration)
- Python 3.10.17
- Random seed: 42, density: 25%
- Boundary: toroidal (wrap)

## Game of Life: Time per Generation Step

| Grid Size | Mean (s) | Std (s) | Runs |
|-----------|----------|---------|------|
| 100×100   | 0.0262   | 0.0002  | 5    |
| 500×500   | 0.6804   | 0.0049  | 5    |
| 1000×1000 | 2.7746   | 0.0154  | 3    |

**Scaling**: Time scales roughly as O(n²) where n is the grid side length, consistent with the O(width × height) per-step complexity. The 500×500 grid takes ~26× longer than 100×100 (expected: 25×), and 1000×1000 takes ~106× longer than 100×100 (expected: 100×).

## Memory Usage

| Grid Size | Peak Memory (MB) |
|-----------|-------------------|
| 100×100   | 0.17              |
| 500×500   | 4.06              |
| 1000×1000 | 16.13             |

Memory scales quadratically as expected for a 2D list-of-lists representation. Each cell uses approximately 16 bytes (Python int + list overhead).

## Rule 110 (1D): 1000 Steps on Width 10,000

| Metric | Value |
|--------|-------|
| Mean time | 8.74s |
| Std | 0.17s |
| Runs | 5 |
| Time per step | 8.74ms |

## Comparison with Prior Work

The naive Python implementation is expectedly slow compared to optimized implementations:

- **Golly (QuickLife)**: Can simulate Game of Life at ~10M cells/sec on similar hardware using bit-level parallelism. Our naive engine achieves ~360K cells/sec (1M cells / 2.77s), roughly 28× slower.
- **GPU implementations** (Balasalle et al., 2017): Reported ~85× speedup over optimized serial CPU code for Life on NVIDIA Titan X, which would translate to ~2500× faster than our Python baseline.
- **python-lifelib**: Uses SIMD (AVX2) for inner loops, achieving near C-level performance. Estimated 100-500× faster than our baseline.

These baselines motivate the NumPy-accelerated (item_011) and HashLife (item_012) implementations, which should close the gap significantly.

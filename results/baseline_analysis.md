# Baseline Benchmark Analysis

## Overview

Ran 4 baseline solvers on 21 benchmark instances across 3 scales (50, 200, 1000 stops) and 3 metro areas (Manhattan, London, Berlin). Results collected with seed=42, time limit 10s (small/medium) and 30s (large).

## Solvers Tested

1. **nearest_neighbor** — Greedy nearest-neighbor construction
2. **farthest_insertion** — Farthest-insertion construction (OSRM Trip equivalent)
3. **ortools** — Google OR-Tools with guided local search metaheuristic
4. **lkh_style** — Multi-restart 2-opt + or-opt local search improvement

## Results Summary

### Mean Tour Cost by Solver and Scale

| Solver | 50 stops | 200 stops | 1000 stops |
|--------|----------|-----------|------------|
| nearest_neighbor | 6,061 | 11,187 | 23,974 |
| farthest_insertion | 5,095 | 10,076 | 21,518 |
| ortools | 4,859 | 9,549 | 21,319 |
| lkh_style | 4,819 | 9,586 | timeout* |

*lkh_style times out on 1000-stop instances due to O(n²) 2-opt complexity.

### Mean Optimality Gap vs Best Found (%)

| Solver | Mean Gap | Std Gap |
|--------|----------|---------|
| nearest_neighbor | 18.97% | 3.65% |
| farthest_insertion | 5.87% | 2.28% |
| ortools | 0.47% | 0.63% |
| lkh_style | 0.65% | 0.80% |

### Solver Wins (Best Cost per Instance)

| Solver | Wins (out of 18) |
|--------|-----------------|
| ortools | 11 (61%) |
| lkh_style | 7 (39%) |
| farthest_insertion | 0 |
| nearest_neighbor | 0 |

### Mean Computation Time

| Solver | 50 stops | 200 stops |
|--------|----------|-----------|
| nearest_neighbor | <0.01s | <0.01s |
| farthest_insertion | <0.01s | 0.23s |
| ortools | 10.0s (time limit) | 10.0s (time limit) |
| lkh_style | 0.41s | 12.4s |

## Key Findings

1. **OR-Tools and lkh_style are competitive:** OR-Tools achieves the best tour on 61% of instances, lkh_style on 39%. Both are within ~1% of the best found.

2. **Nearest-neighbor is a poor baseline:** ~19% gap confirms it as a lower bound on solution quality.

3. **Farthest-insertion is reasonable:** ~6% gap makes it a useful fast baseline.

4. **OR-Tools benefits from time limit:** With 10s of guided local search, it finds very competitive solutions. It is the best performer at the 200-stop scale on many instances.

5. **lkh_style scalability issue:** The Python 2-opt implementation is O(n²) per iteration and cannot scale to 1000+ stops within reasonable time. A real LKH-3 binary would be significantly faster.

6. **Asymmetric road networks make ATSP harder:** The ~100% asymmetry in our synthetic matrices creates genuine asymmetric structure that distinguishes this from symmetric TSP.

## Target for Improvement

The hybrid solver aims to beat the best of {ortools, lkh_style} by ≥ 0.5% on 200-stop instances, where both achieve gaps of 0.5-0.7% vs the best found. This target is achievable if the learned candidate generation can guide the search more effectively than the generic metaheuristics.

# Digit-Pair Symmetry Pruning Optimization

## 1. Core Observation

In the reverse-and-add process, the first step adds a number N to its reverse R(N). The resulting sum depends only on the **digit-pair sums**, not the individual digits.

For an N-digit number with digits d₀d₁...d_{N-1}:
- R(N) has digits d_{N-1}d_{N-2}...d₀
- The sum N + R(N) at position i has a contribution of d_i + d_{N-1-i}

Two numbers with identical digit-pair sums s_i = d_i + d_{N-1-i} for all i produce the **same** result after the first reverse-and-add step, and therefore have identical subsequent behavior.

## 2. Equivalence Classes

For each position pair (i, N-1-i), define the pair sum:
  s_i = d_i + d_{N-1-i},  where 0 ≤ s_i ≤ 18

For an N-digit number:
- If N is odd: there are (N-1)/2 pairs plus one middle digit d_{(N-1)/2}
- If N is even: there are N/2 pairs

Two numbers are **equivalent** if they have the same tuple of pair sums (and same middle digit if N is odd).

## 3. Canonical Representatives

From each equivalence class, we test only one canonical representative. Doucette chose the smallest number in each class (the "seed").

For pair sum s_i at positions (i, N-1-i):
- s ranges from 0 to 18
- Number of (d_i, d_{N-1-i}) pairs producing sum s: min(s+1, 19-s) when both digits are 0-9
- Canonical choice: d_i = max(0, s-9), d_{N-1-i} = s - d_i

Special constraints:
- Leading digit d₀ ≥ 1 (no leading zeros)
- For the outermost pair (d₀, d_{N-1}): d₀ + d_{N-1} = s₀, with d₀ ≥ 1

## 4. Reduction Factor

For a 17-digit number (Doucette's documented example):
- 8 pairs + 1 middle digit
- Raw search space: 9 × 10¹⁶ (N-digit numbers with leading digit ≥ 1)
- Pruned space: 18 × 19⁷ × 10 ≈ 187 billion
- **Reduction factor: ~4.8 × 10⁵ (about 480,000×)**

For a 25-digit number:
- 12 pairs + 1 middle digit
- Raw search space: 9 × 10²⁴
- Pruned space: 18 × 19¹¹ × 10 ≈ 3.2 × 10¹⁶
- **Reduction factor: ~2.8 × 10⁸ (about 280 million×)**

## 5. Seeds vs. Kins

Terminology from Doucette and the Lychrel community:

- **Seed**: A Lychrel candidate that is the smallest number in its equivalence class. Also called the "root" of the thread.
- **Kin**: Any other number in the same equivalence class as a seed. Kins share the same reverse-and-add trajectory from step 1 onward.

For MDPN search:
- We only need to test seeds
- Any record-setting seed automatically implies all its kins also achieve the same delay
- The MDPN record reports the smallest kin (which is the seed itself)

## 6. Implementation Notes

To enumerate all seeds for N-digit numbers:

```
for s₀ in range(1, 19):        # pair sum for (d₀, d_{N-1}), s₀ ≥ 1 since d₀ ≥ 1
    d₀ = max(1, s₀ - 9)        # canonical leading digit
    d_{N-1} = s₀ - d₀

    for s₁ in range(0, 19):    # pair sum for (d₁, d_{N-2})
        d₁ = max(0, s₁ - 9)
        d_{N-2} = s₁ - d₁

        ... (continue for all pairs)

        for m in range(0, 10):  # middle digit (if N odd)
            candidate = construct_number(d₀, d₁, ..., m, ..., d_{N-2}, d_{N-1})
            delay = reverse_and_add_count(candidate)
```

This nested loop structure makes it easy to partition the search space for parallel execution (e.g., partition by s₀ or by (s₀, s₁) combinations).

## 7. Additional Pruning Opportunities

Beyond basic digit-pair equivalence:

1. **Carry analysis**: When pair sums are all < 10, no carries occur in the first addition. This produces "well-behaved" trajectories that rarely lead to high delays. Focus on pair sums that produce carries (s_i ≥ 10).

2. **Symmetry of N and 10^N - 1 - N**: For some digit lengths, complementary numbers (where each digit d is replaced by 9-d) have related trajectories. This can halve the search space.

3. **Even-digit-length filtering**: Doucette observed that even-length numbers rarely set records. This is because the middle pair sum dominates behavior, and even-length numbers have one more constraint. Prioritize odd-length digit counts.

## References

- [Doucette_WorldRecords] for the original description of digit-pair pruning
- [Nishiyama2012] for the seed/kin distinction in Lychrel candidates
- [Maslov_MDPN] for the application to 25-digit search

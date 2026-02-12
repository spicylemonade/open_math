# Computational Feasibility Assessment: Pushing to $10^{19}$

## 1. Number of Primes Between $10^{18}$ and $10^{19}$

Using exact values of the prime counting function $\pi(x)$ from OEIS A006880:

- $\pi(10^{18}) = 24,739,954,287,740,860$
- $\pi(10^{19}) = 234,057,667,276,344,607$

Therefore, the number of primes in $[10^{18}, 10^{19}]$:

$$\pi(10^{19}) - \pi(10^{18}) = 209,317,712,988,603,747 \approx 2.09 \times 10^{17}$$

That is approximately **209 quadrillion primes** with exactly 19 digits.

## 2. Fraction Surviving the Modular Sieve

### Basic Mordell sieve (mod 840)
- 6 out of 192 coprime residue classes are "hard": $\{1, 121, 169, 289, 361, 529\}$
- Fraction of primes surviving: $6/192 \approx 3.1\%$
- Estimated hard primes in $[10^{18}, 10^{19}]$: $\approx 6.5 \times 10^{15}$

### Extended Salez sieve (7+ equations, period $G_8$)
- The full Salez sieve reduces the surviving fraction by an additional factor of ~43
- Effective fraction: $\approx 3.1\% / 43 \approx 0.072\%$
- Estimated residual primes requiring brute force: $\approx 1.5 \times 10^{14}$

## 3. Per-Prime Verification Cost

For primes $p$ around $10^{18}$–$10^{19}$:

### Brute-force search
For each surviving prime $p$, we need to find $a, b, c$ such that $4abc = p(bc + ac + ab)$.

The search space for a Type-1 decomposition (where $n | a$): iterate $x$ from $\lceil n/4 \rceil$ upward, and for each $x$, check if $4xn - n^2$ has a factorization yielding valid $b, c$.

**Estimated cost per prime:**
- The search depth is typically $O(\sqrt{p})$ in the worst case for brute force
- With optimized parametric search, the average cost is much lower
- For the 2025 paper at $10^{18}$: average per-prime cost was microseconds to milliseconds
- At $10^{19}$: the per-prime cost increases because GMP arbitrary-precision arithmetic is required (integers > 64 bits), incurring a ~10× slowdown vs native arithmetic

**Estimated per-prime cost at $10^{19}$:** ~0.1–1 millisecond (with GMP)

## 4. Total Estimated Compute

### Lower bound estimate
- Residual primes to check: $\approx 1.5 \times 10^{14}$
- Per-prime cost: 0.1 ms
- Total: $1.5 \times 10^{14} \times 10^{-4}$ s $= 1.5 \times 10^{10}$ s $\approx 475$ CPU-years

### Upper bound estimate
- Per-prime cost: 1 ms
- Total: $1.5 \times 10^{14} \times 10^{-3}$ s $= 1.5 \times 10^{11}$ s $\approx 4,750$ CPU-years

### Parallelization
- The problem is embarrassingly parallel (each prime is independent)
- With 1,000 CPU cores: 0.5–5 years wall-clock time
- With 10,000 CPU cores: 17–173 days wall-clock time

## 5. Comparison with 2025 Paper's Runtime

The 2025 paper (arXiv:2509.00128) reports:
- **Bound achieved:** $10^{18}$
- **Runtime:** ~2 weeks on a medium computational setup
- **Method:** Python sieve generation + C++ with GMP for residual checking

### Extrapolation to $10^{19}$
Going from $10^{18}$ to $10^{19}$:
- ~10× more primes to check overall
- Each prime is larger, so arithmetic is slower (GMP overhead)
- Estimated runtime scaling: 10× (more primes) × 1.5× (slower per-prime) = ~15× longer
- From 2 weeks to **~30 weeks** (~7 months) on a comparable setup

### With significant optimization
- Better sieve (larger $G$): could reduce by 2–5×
- Highly optimized C code (avoid GMP where possible using 128-bit integers): 2–3× speedup
- Multi-core parallelism: linear scaling
- **Optimistic estimate with 100 cores and optimizations:** 1–3 weeks

## 6. Feasibility Assessment

### Within our scope (this project)
- **Pushing to $10^{13}$:** Very feasible (minutes to hours with our pipeline)
- **Pushing to $10^{14}$:** Feasible (hours, matching Swett's original result)
- **Pushing to $10^{15}$:** Feasible with optimized C code (days)
- **Pushing to $10^{17}$:** Feasible with full Salez sieve + C (days to weeks)
- **Pushing to $10^{18}$:** Would replicate 2025 paper (weeks)
- **Pushing to $10^{19}$:** Requires significant compute resources (months on single machine)

### Conclusion
Pushing the bound to $10^{19}$ is **computationally feasible** but requires:
1. An optimized C/C++ implementation with 128-bit integer support
2. The full extended Salez sieve
3. Multi-core parallelism or cluster computing
4. Several weeks to months of dedicated compute time

For this project, we target verification up to $10^{13}$ as a demonstration, with infrastructure capable of scaling to $10^{15}+$.

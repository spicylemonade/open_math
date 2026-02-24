# Design Document: Fragmentation-Aware Resource Balance (FARB) Heuristic

## 1. Motivation

Analysis of baseline results reveals two key fragmentation patterns:

**Pattern 1: Resource Dimension Imbalance (Stranded Resources)**
Classical heuristics like BFD and L2 minimize total residual capacity but don't
explicitly balance residual resources across dimensions. This leads to hosts where
one dimension (e.g., CPU) is nearly full while the other (e.g., RAM) has significant
free capacity — the "stranded resource" problem identified by Google Borg engineers
(Verma et al., 2015). Our baselines show 23-36% of active hosts have stranded resources.

**Pattern 2: Workload-Blind Scoring**
DotProduct (Panigrahy et al., 2011) aligns VM demands with host residuals but doesn't
consider the *cost* of creating imbalance. L2 (Panigrahy et al., 2011) minimizes
residual magnitude but treats balanced and imbalanced residuals equally if they have
the same L2 norm. Neither explicitly penalizes creating stranded resources.

## 2. Algorithm Description

### 2.1 Core Idea

FARB scores each candidate host for a VM placement based on three components:
1. **Balance Score**: How well-balanced the host's residual resources would be after placement
2. **Fullness Score**: How full the host would be (prefer filling up hosts)
3. **Residual Score**: L2 norm of residual (tiebreaker)

The key insight is that **balance is weighted most heavily**, directly targeting the
stranded resource problem that other heuristics ignore.

### 2.2 Pseudocode

```
FUNCTION FARB_Place(vm, hosts):
    best_host ← NULL
    best_score ← +∞

    FOR each host h in active_hosts ∪ {few empty hosts}:
        IF NOT h.can_fit(vm.cpu, vm.ram):
            CONTINUE

        // Normalized residual after placement
        cpu_res ← (h.free_cpu - vm.cpu) / h.capacity_cpu
        ram_res ← (h.free_ram - vm.ram) / h.capacity_ram

        // Component 1: Resource balance (lower = more balanced)
        balance ← |cpu_res - ram_res|

        // Component 2: Fullness (lower = fuller host)
        fullness ← (cpu_res + ram_res) / 2

        // Component 3: L2 residual (tiebreaker)
        l2 ← sqrt(cpu_res² + ram_res²)

        // Weighted composite score (minimize)
        score ← w_b * balance + w_f * fullness + w_l * l2

        IF score < best_score:
            best_score ← score
            best_host ← h

    RETURN best_host
```

Default weights: w_b = 2.0, w_f = 1.0, w_l = 0.5

### 2.3 Weight Rationale

- **w_b = 2.0 (balance)**: The most important component. Directly attacks stranded
  resources. A host with residual (0.3, 0.0) has balance = 0.3, while (0.15, 0.15)
  has balance = 0.0. FARB strongly prefers the latter.

- **w_f = 1.0 (fullness)**: Prefer packing hosts tightly, like BFD. This reduces
  the number of active hosts. Equal importance to fullness prevents FARB from
  leaving hosts half-empty just to maintain balance.

- **w_l = 0.5 (L2 residual)**: Tiebreaker that distinguishes between equally
  balanced and equally full hosts. Provides Panigrahy L2 behavior as a fallback.

## 3. Properties

### 3.1 Online Operation
FARB makes decisions based only on the current state of hosts and the arriving VM.
No future information is needed. Each decision is O(k) where k = number of active
hosts + small empty pool ≪ total hosts.

### 3.2 Time Complexity
Per allocation: O(k) where k is the number of candidate hosts (active + pool).
Using the active host tracking optimization, k is typically much smaller than the
total cluster size n. In the worst case (all hosts active), k = n, giving O(n)
per decision. For sorted candidate selection, O(n log n) could be used but is
unnecessary since k is manageable.

### 3.3 Theoretical Argument

**Claim**: FARB reduces fragmentation compared to BFD by reducing the variance
of normalized residual resource ratios across hosts.

**Argument**: BFD minimizes ||residual||₂, which can produce placements where
residual = (ε, δ) with |ε - δ| large. FARB penalizes |ε - δ|, steering toward
residual vectors closer to the diagonal (ε ≈ δ). When residuals are balanced,
any new VM with demand vector (a, b) where a/b is close to the average VM's
ratio will find a feasible host, reducing allocation failures and stranded resources.

More formally: Let R_j = (r_j^cpu, r_j^ram) be the normalized residual of host j.
Define the fragmentation potential as Φ = Σ_j |r_j^cpu - r_j^ram|.
BFD's greedy minimization of ||R_j||₂ does not minimize Φ.
FARB includes |r_j^cpu - r_j^ram| in its scoring, so each placement decision
explicitly reduces Φ on the chosen host.

## 4. Differentiation from Prior Work

| Approach | Scoring Function | Targets Balance? | Targets Fullness? |
|----------|-----------------|-----------------|------------------|
| BFD (baseline) | min ||residual||₂ | No | Yes (implicitly) |
| DotProduct (Panigrahy) | max demand · residual | Partially | No |
| L2 (Panigrahy) | min ||residual||₂ normalized | No | Yes |
| Borg (Google) | Composite with stranded penalty | Ad hoc | Yes |
| FARB (ours) | Weighted: balance + fullness + L2 | **Yes (primary)** | **Yes (explicit)** |

FARB explicitly targets the stranded resource problem that Borg identified but
addresses it as a continuous optimization rather than Borg's rule-based approach.
Unlike DotProduct which aligns demands with residuals (addressing complementarity
but not imbalance), FARB directly minimizes the dimension imbalance of residuals.

## 5. Adaptive Hybrid Extension

The AdaptiveHybrid meta-heuristic monitors cluster state and switches strategies:

```
FUNCTION AdaptiveHybrid_Place(vm, hosts):
    utilization ← compute_cluster_utilization(hosts)
    fragmentation ← compute_fragmentation_index(hosts)

    IF utilization < U_threshold:      // Cluster is sparse
        RETURN DotProduct_Place(vm, hosts)    // Maximize resource alignment
    ELIF fragmentation > F_threshold:  // High fragmentation
        RETURN FARB_Place(vm, hosts)          // Fix imbalance
    ELSE:                              // Normal operation
        RETURN BestFit_Place(vm, hosts)       // Pack tightly
```

Decision tree:
```
         utilization < U?
        /                 \
      YES                  NO
       |                    |
   DotProduct      fragmentation > F?
                  /                   \
                YES                    NO
                 |                      |
              FARB                  BestFit
```

## References

- Panigrahy et al. (2011). Heuristics for Vector Bin Packing. Microsoft Research. [panigrahy2011heuristics]
- Hadary et al. (2020). Protean: VM Allocation Service at Scale. OSDI '20. [hadary2020protean]
- Verma et al. (2015). Large-Scale Cluster Management at Google with Borg. EuroSys '15. [verma2015borg]

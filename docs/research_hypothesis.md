# Research Hypothesis: Tightening the MDS Approximation on Planar Graphs

## 1. Current Best Practical Constant-Factor Ratio

The best known practical constant-factor approximation for MDS on planar graphs comes from the LP-rounding framework of Bansal and Umboh (2017) \cite{BansalUmboh2017}. Since planar graphs have arboricity α ≤ 3, their result yields:

- **Theoretical guarantee:** (2α + 1) = **7-approximation** via LP rounding on bounded-arboricity graphs.
- **LP integrality gap:** At most α + 1 = **4** on planar graphs (Sun 2021 \cite{Sun2021}).

In the distributed setting, the best constant-round ratio is **11 + ε** (Heydt et al. 2025 \cite{HeydtKublenzOdMSiebertzVigny2025}), with a lower bound of **7 − ε** (Hilke et al. 2014 \cite{HilkeLenzenSuomela2014}) for constant-round LOCAL algorithms.

For centralized algorithms, the practical gap is:
- Baker's PTAS at k = 3 gives ratio **1.67** but with high constant overhead (~512n operations).
- Standard greedy gives **O(log n)** ratio — unbounded constant.
- LP rounding (Bansal-Umboh) gives ratio **7** in polynomial time.

**There is no known practical centralized algorithm achieving ratio < 7 while running in near-linear time on planar graphs.**

## 2. Target Ratio

We target an approximation ratio of **≤ 5** on planar graphs, with:
- A provable bound of the form |D| ≤ α · OPT + β · √n (with α ≤ 4, β small)
- Empirical mean ratio ≤ 3.0 on benchmark instances
- Practical running time O(n · polylog(n)) or better

## 3. Proposed Algorithmic Approach

Our hybrid algorithm combines three techniques:

### Stage 1: LP Relaxation with Planarity Constraints
- Solve the LP relaxation of MDS: minimize Σ x_v subject to Σ_{u ∈ N[v]} x_u ≥ 1, 0 ≤ x_v ≤ 1
- Augment with planar-specific valid inequalities derived from:
  - **Euler's formula:** m ≤ 3n − 6 implies average degree < 6, constraining LP solution structure
  - **Face-based constraints:** For each face in a planar embedding, at least ⌈|face|/3⌉ vertices must be in the dominating set
- LP optimal value serves as lower bound for ratio measurement

### Stage 2: Separator-Based Rounding
- Apply the Lipton-Tarjan planar separator theorem: find a separator S of size O(√n) partitioning V into A, B with |A|, |B| ≤ 2n/3
- **Include all separator vertices in the dominating set** — this costs at most O(√n) additive overhead
- Recursively solve MDS on each component A ∪ S and B ∪ S
- Base case: for components of size ≤ threshold T, solve exactly via ILP

### Stage 3: Local Search Refinement
- Apply 1-swap: remove redundant vertices (those whose removal preserves domination)
- Apply 2-swap: try replacing pairs {u, v} with a single vertex w
- Iterate until convergence or iteration limit

### Why Planar Structure Enables Improvement

1. **Bounded treewidth in sub-problems:** k-outerplanar graphs (arising in Baker decomposition) have treewidth ≤ 3k − 1, enabling efficient DP.
2. **Small separators:** Planar separators of size O(√n) mean the overhead of including separator vertices is sublinear, becoming negligible relative to OPT for large graphs.
3. **LP integrality gap:** The LP integrality gap is at most 4 on planar graphs (arboricity 3), so LP-guided rounding can achieve constant-factor approximation.
4. **Bounded density:** By Euler's formula, |E| ≤ 3|V| − 6, so the average degree is < 6. This means each vertex dominates at most ~6 others on average, bounding the greedy gain per step and making local search more effective.

## 4. Falsifiable Predictions

### Prediction 1: Ratio Improvement Over Greedy
> The hybrid algorithm achieves a mean approximation ratio (measured against LP lower bound) at least **20% lower** than standard greedy on planar graphs with n ≥ 100.

**Falsification criterion:** Compute mean ratio for both algorithms on ≥ 50 planar graph instances with n ∈ [100, 10000]. If (mean_greedy_ratio − mean_hybrid_ratio) / mean_greedy_ratio < 0.20, the prediction is falsified.

### Prediction 2: Consistent Bounded Ratio
> The hybrid algorithm never exceeds approximation ratio **5.0** (vs. LP lower bound) on any planar graph instance in our benchmark suite of ≥ 100 instances.

**Falsification criterion:** If any single instance yields ratio > 5.0, the prediction is falsified. We would then investigate whether the bound should be relaxed or the algorithm improved.

### Prediction 3: Near-Linear Scalability
> The hybrid algorithm's running time scales as O(n^{1.2}) or better empirically on planar graphs from n = 1,000 to n = 100,000.

**Falsification criterion:** Fit log(runtime) vs log(n) on ≥ 5 sizes. If the slope exceeds 1.5, the prediction is falsified.

## 5. Risk Assessment

| Risk | Mitigation |
|------|-----------|
| LP solver too slow for large instances | Use LP only for lower bound; round using separator structure |
| Separator overhead dominates for small graphs | Set minimum recursion size; use direct ILP for small instances |
| Local search converges to poor local optimum | Use LP fractional solution to guide initial solution quality |
| Theoretical bound is vacuous for moderate n | Focus on empirical evaluation; accept α·OPT + β·√n form |

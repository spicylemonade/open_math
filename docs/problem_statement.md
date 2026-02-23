# Problem Statement: Minimum Dominating Set on Planar Graphs

## 1. Formal Definitions

**Dominating Set.** Given an undirected graph G = (V, E), a set D ⊆ V is a *dominating set* if every vertex v ∈ V is either in D or adjacent to at least one vertex in D. Formally:

∀v ∈ V : v ∈ D ∨ (∃u ∈ D : {u, v} ∈ E)

**Minimum Dominating Set (MDS).** The Minimum Dominating Set problem asks for a dominating set D* of minimum cardinality:

D* = argmin_{D ⊆ V, D is dominating} |D|

We denote the optimal solution size as γ(G) = |D*|, the *domination number* of G.

**Planar Graphs.** A graph G = (V, E) is *planar* if it can be embedded in the plane without edge crossings. By Euler's formula, any simple planar graph on n vertices has at most m ≤ 3n − 6 edges. Equivalently, a graph is planar if and only if it contains no subdivision of K₅ or K₃,₃ (Kuratowski's theorem).

## 2. NP-Hardness

The Minimum Dominating Set problem is NP-hard, even when restricted to planar graphs. This was established by Garey and Johnson (1979) [garey1979], who showed that DOMINATING SET is NP-complete for general graphs. The restriction to planar graphs was shown to remain NP-complete by Garey, Johnson, and Stockmeyer.

More precisely, MDS on planar graphs is:
- NP-hard (no polynomial-time exact algorithm unless P = NP)
- W[2]-hard in general, but **FPT parameterized by solution size** on planar graphs (Alber, Fellows, Niedermeier 2004 [alber2004])
- Admits a **linear kernel** of size at most 67k on planar graphs (Alber et al. 2004)

## 3. Baker's PTAS

Baker (1994) [baker1994] introduced a technique yielding a Polynomial-Time Approximation Scheme (PTAS) for many NP-hard problems on planar graphs, including MDS:

**Theorem (Baker 1994).** For any fixed integer k ≥ 1, there exists an algorithm that computes a (1 + 2/k)-approximation to MDS on any n-vertex planar graph in time O(2^{O(k)} · n).

The algorithm works by:
1. Computing a BFS-layering of the graph
2. For each offset i ∈ {0, 1, ..., k-1}, partitioning into k-outerplanar subgraphs by deleting every k-th layer
3. Solving MDS exactly on each k-outerplanar piece (treewidth ≤ 3k − 1, enabling DP in time 2^{O(k)} · n)
4. Returning the best solution among the k offsets

The (1 + 2/k) ratio arises because at most 2/k fraction of the optimal vertices are "lost" to deleted layers in the best offset.

**Practical limitation:** While the ratio approaches 1 as k → ∞, the exponential dependence on k (hidden in 2^{O(k)}) makes this impractical for k > 5 on large graphs. For k = 3, the ratio is 1.67 but the constant in 2^{O(k)} makes it slow.

## 4. Greedy Algorithms and Their Limitations

**Standard greedy.** The classical greedy algorithm for Set Cover — repeatedly selecting the vertex that dominates the most undominated vertices — gives an O(log Δ) ≤ O(log n) approximation ratio on general graphs, where Δ is the maximum degree.

On planar graphs, this bound is not improved: the greedy algorithm can produce solutions of size Ω(log n) · γ(G) even on specific planar graph families (e.g., certain grid-like constructions).

**Modified greedy approaches.** Several authors have proposed modified greedy strategies:
- Jones et al. proposed a degree-ratio greedy that considers both the number of newly dominated vertices and the "cost" of adding a vertex
- Dvořák (2013) [dvorak2013] showed that planar graphs have bounded local density properties useful for constant-factor approximations in distributed settings

However, these modified greedy approaches typically achieve only loose constant factors (ratios of 8–20 on planar graphs), far from the optimal PTAS ratios.

## 5. The Approximation Gap

The current state of the art presents a clear gap:

| Approach | Approximation Ratio | Time Complexity | Practical? |
|----------|-------------------|-----------------|------------|
| Baker's PTAS (k=3) | 1.67 | O(2^{9} · n) ≈ O(512n) | Moderate (small k only) |
| Baker's PTAS (k=10) | 1.20 | O(2^{30} · n) ≈ O(10⁹n) | Impractical |
| Standard Greedy | O(log n) | O(n + m) | Yes |
| Modified Greedy | ~10-20 (empirical) | O(n + m) | Yes |
| LP Rounding (general) | O(log n) | O(n² poly) | Moderate |

There is no known practical algorithm that simultaneously achieves:
- A **provable constant-factor** approximation (not dependent on n)
- **Near-linear running time** O(n · polylog(n))
- **Good empirical performance** (ratio ≤ 5 on typical instances)

## 6. Research Question

> **Can we design a practical O(n · polylog(n))-time algorithm achieving approximation ratio ≤ 5 on planar graphs, combining separator decomposition with LP rounding?**

Specifically, we propose an algorithm that:
1. Uses the **Lipton-Tarjan planar separator theorem** to recursively decompose the graph into small pieces
2. Solves MDS **exactly** on small pieces and uses **LP relaxation with planarity-exploiting constraints** for guidance
3. Applies **k-swap local search** to refine the solution

The key insight is that planar separators of size O(√n) allow recursive decomposition where the separator overhead contributes at most an additive O(√n) term, yielding a bound of the form:

|D| ≤ α · OPT + β · √n

For large enough graphs where OPT = Ω(√n), this gives a constant multiplicative ratio.

## References

- [garey1979] Garey, M.R. and Johnson, D.S. (1979). *Computers and Intractability: A Guide to the Theory of NP-Completeness.*
- [baker1994] Baker, B.S. (1994). Approximation algorithms for NP-complete problems on planar graphs. *JACM*, 41(1):153-180.
- [alber2004] Alber, J., Fellows, M.R., and Niedermeier, R. (2004). Polynomial-time data reduction for dominating set. *JACM*, 51(3):363-384.
- [dvorak2013] Dvořák, Z. (2013). Constant-factor approximation of the domination number in sparse graphs.

# Literature Review: Bin Packing Heuristics for Cloud VM Scheduling

## 1. Classical 1D and 2D Online Bin Packing

### 1.1 One-Dimensional Foundations

The classical bin packing problem dates back to the 1970s and has been extensively studied.
Coffman et al. (1996) provide a comprehensive survey of approximation algorithms for 1D
bin packing. The First Fit Decreasing (FFD) algorithm achieves an asymptotic approximation
ratio of 11/9 ≈ 1.222. For online 1D bin packing, the **Harmonic** algorithm family
introduced by Lee and Lee (1985) provides a framework that has been refined over decades.

**Seiden (2002)** introduced the **Super Harmonic** framework and the **Harmonic++**
algorithm, achieving an asymptotic competitive ratio of at most 1.58889 for online 1D
bin packing. This represented a significant advance over previous Harmonic-class algorithms.
Heydrich and van Stee (2016) later refined this to 1.58880 and showed that 1.5884 can be
achieved within the SuperHarmonic framework.

### 1.2 Two-Dimensional Online Bin Packing

For 2D online bin packing (rectangle packing into square bins), **Seiden and van Stee (2003)**
proposed the **H⊗C** algorithm, combining the Harmonic algorithm H with the Improved
Harmonic algorithm C. They proved an asymptotic competitive ratio of at most 2.66013.

**Han et al. (2011)** improved this upper bound to **2.5545** by replacing the Improved
Harmonic algorithm with the Super Harmonic algorithm and developing new weighting functions.
This remains the best known upper bound for 2D online bin packing. The best known lower
bound is 1.907.

### 1.3 Multidimensional Vector Bin Packing

**Christensen et al. (2017)** provide the definitive survey on approximation and online
algorithms for multidimensional bin packing. Key findings include:
- Unlike the 1D case, d-dimensional bin packing for d ≥ 2 does not admit an APTAS
  unless P = NP.
- The vector packing variant (packing d-dimensional vectors into unit-capacity bins) has
  different competitive ratios than the geometric variant (packing rectangles/cuboids).
- For d-dimensional vector packing, the asymptotic approximation ratio is at most
  1 + d·ln(1.5) + ε for any ε > 0 (Bansal et al.).

## 2. Vector Bin Packing Heuristics for VM Placement

### 2.1 DotProduct and L2 Heuristics (Panigrahy et al., 2011)

**Panigrahy et al. (2011)** from Microsoft Research conducted the most systematic study
of heuristics for vector bin packing, motivated by the VM placement problem. Key contributions:

- **FFD variants**: They studied multiple FFD variants using different weight functions
  to convert d-dimensional items to scalars for sorting (sum of coordinates, max coordinate,
  product of coordinates, etc.).

- **DotProduct heuristic**: Score each candidate host by the dot product of the VM's
  demand vector and the host's residual capacity vector. This prefers hosts whose free
  resource profile matches the VM's needs. Formally, for VM demand d and host residual r:
  score(h) = d · r.

- **L2 Norm heuristic**: Place the VM on the host that minimizes the L2 norm of the
  residual capacity vector after placement: score(h) = ||r - d||₂. This aims to balance
  residual resources across dimensions.

- **Results**: DotProduct and L2 outperform FFD-based heuristics on most input classes,
  reducing the number of bins by up to 5-10% on challenging distributions. The improvement
  is largest when item dimensions are uncorrelated.

### 2.2 Nagel et al. (2023) — Recent Heuristic Analysis

Nagel et al. (2023) introduced new heuristics including a local search algorithm, a
game-theoretic approach, and enhanced best-fit heuristics. Their experiments demonstrate
a general trade-off between running time and packing quality. The local search algorithm
outperforms almost all other heuristics while maintaining reasonable running time.

## 3. Production Systems

### 3.1 Google Borg (Verma et al., 2015)

Google's Borg cluster manager handles hundreds of thousands of jobs across clusters of
tens of thousands of machines. Key scheduling insights:
- Borg uses a two-phase approach: feasibility checking followed by scoring.
- The scoring function balances between worst-fit (spreading load) and best-fit (packing
  tightly) to limit **stranded resources**.
- Borg explicitly monitors and minimizes stranded resources — resources on a machine that
  cannot be used because another resource dimension is depleted.
- The cluster traces from Borg (ClusterData2019) provide the most comprehensive public
  dataset for evaluating packing algorithms.

### 3.2 Microsoft Azure Protean (Hadary et al., 2020)

**Protean** is Azure's VM allocation service handling millions of servers globally. Key design:
- Uses a rule-based **Allocation Agent** (AA) with configurable scoring functions.
- Achieves **85-90% utilization** on key metrics through multi-layer caching and concurrent
  allocation agents.
- Separates policy from mechanism, enabling A/B testing of allocation strategies in production.
- The Allocation Agent scores hosts using configurable weighted combinations of features
  including remaining capacity, VM type compatibility, and fault domain spread.
- The Azure Traces for Packing 2020 dataset was released alongside this paper for
  reproducible research on packing algorithms.

### 3.3 Tetris (Grandl et al., 2014)

Tetris is a multi-resource cluster scheduler that explicitly models the multi-dimensional
nature of resource packing. It uses dot-product-based scoring similar to Panigrahy et al.
to align task resource requirements with machine available resources, achieving significantly
better packing than resource-agnostic schedulers.

## 4. ML-Augmented Approaches

### 4.1 Lifetime-Aware Placement (Barbalho et al., MLSys 2023)

**Barbalho et al. (2023)** won the Outstanding Paper Award at MLSys 2023 for their work
on VM allocation with ML-predicted lifetimes. Key contributions:
- Use ML models to predict VM lifetime at allocation time.
- Lifetime-aware algorithms that are **provably robust** to prediction errors.
- Two versions: DPBFR (simple modification of best-fit) and LAR (Lifetime Awareness Rule)
  with explicit use of predicted lifetime.
- Deployed in production at Azure, achieving efficiency improvements consistent with
  simulations.
- Demonstrates that even 1% improvement in packing efficiency saves hundreds of millions
  of dollars at Azure's scale.

### 4.2 VMAgent — RL for VM Scheduling (Sheng et al., 2022)

VMAgent provides a reinforcement learning framework for VM scheduling, built on the
Huawei-East-1 real-world VM trace. It enables training and evaluating RL agents on
practical VM scheduling scenarios including fading and recovering workloads.

## 5. Metaheuristic Approaches

### 5.1 GA+BFD Hybrids

Hybrid genetic algorithms combined with BFD have been proposed for VM placement.
The approach uses BFD to repair infeasible chromosomes in the GA population, combining
the global search capability of evolutionary methods with the fast local optimization
of greedy heuristics. Results show GA+BFD outperforms GA+FFD, suggesting that
hybridizing with stronger base heuristics improves overall solution quality.

### 5.2 Adaptive Online Bin Packing (Song et al., 2014)

Song et al. (2014) proposed adaptive resource provisioning for the cloud using online
bin packing, dynamically adjusting the packing strategy based on observed workload
patterns. This adaptive approach can respond to changing resource demand distributions
that static heuristics cannot exploit.

## 6. Gap Analysis and Research Opportunities

From this review, several gaps and opportunities emerge:

1. **Fragmentation-aware heuristics**: While DotProduct and L2 improve packing efficiency,
   neither explicitly targets the stranded resource problem identified by Google Borg.
   A heuristic that directly minimizes resource imbalance on hosts could further reduce
   fragmentation.

2. **Adaptive heuristic selection**: Most approaches use a single heuristic throughout.
   The observation that different heuristics excel under different workload conditions
   (e.g., DotProduct for balanced loads, L2 for skewed loads) suggests an adaptive
   meta-heuristic could outperform any single approach.

3. **Dynamic departures**: The standard VBP formulation ignores departures. The dynamic
   setting with arrivals and departures creates fragmentation that accumulates over time.
   Periodic defragmentation (VM migration) could recover lost efficiency.

4. **Real-trace evaluation**: Many papers evaluate on synthetic distributions only.
   Evaluation on production traces (Google ClusterData2019, Azure Packing 2020) provides
   more realistic and meaningful comparisons.

## References

See `sources.bib` for complete bibliography.

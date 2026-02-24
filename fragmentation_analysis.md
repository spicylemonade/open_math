# Fragmentation Analysis of Baseline Heuristics

## 1. Distribution of Stranded Resource Types

Analysis of host resource states at the end of simulation reveals distinct stranding patterns between BFD and FARB.

**BFD (Best Fit Decreasing):**
Under BFD, which minimizes L2 residual without regard for dimensional balance, a significant fraction of active hosts develop stranded resources — one dimension nearly full while the other has substantial free capacity. On the Azure-like trace, BFD produces a fragmentation index of 23.4%, meaning nearly one-quarter of active hosts have stranded resources at any given time.

**FARB (Fragmentation-Aware Resource Balance):**
FARB reduces stranded hosts by explicitly penalizing placements that worsen dimensional imbalance. On the same Azure-like trace, FARB achieves a fragmentation index of only 14.0% — a 40% relative reduction in stranded hosts.

See `figures/fig8_stranded_resources.png` for the distribution of stranded CPU, stranded RAM, and balanced hosts under each heuristic.

**Key Finding 1:** BFD creates approximately equal numbers of CPU-stranded and RAM-stranded hosts. This bi-directional stranding is a consequence of BFD's dimension-agnostic L2 scoring — it treats CPU and RAM residuals interchangeably.

## 2. Temporal Patterns

Analysis of fragmentation index over simulation time (see `figures/fig2_fragmentation_timeseries.png`) reveals:

- **BFD fragmentation increases monotonically** during the initial ramp-up phase (first ~30% of events) and then stabilizes at ~32% for Google-like and ~23% for Azure-like traces.
- **FARB fragmentation follows a similar shape but at consistently lower levels**, stabilizing at ~29.5% (Google) and ~14% (Azure).
- **Fragmentation spikes occur after departure bursts**, when departing VMs leave behind partially-used hosts with imbalanced residuals. FARB recovers from these spikes faster due to its balance-preserving placement.
- **The gap between BFD and FARB widens over time**, suggesting FARB's benefits compound as the cluster accumulates more varied host states.

**Key Finding 2:** Fragmentation is not a transient phenomenon — it persists and worsens over time under dimension-agnostic heuristics like BFD. This confirms the need for fragmentation-aware placement.

## 3. VM Size Distribution Analysis

Analysis of the Azure-like VM workload (see `figures/fig9_vm_size_fragmentation.png`):

- VM CPU:RAM demand ratios show a **multi-modal distribution** reflecting Azure's discrete VM types (D-series: balanced, E-series: RAM-heavy, F-series: CPU-heavy).
- **RAM-heavy VMs (E-series, ratio < 0.5)** are the most common, constituting ~40% of requests.
- **CPU-heavy VMs (F-series, ratio > 2.0)** are less common (~15%) but cause disproportionate fragmentation because they leave behind stranded RAM.
- **VM resource imbalance** (|cpu_frac - ram_frac|) ranges from near-zero (balanced VMs) to 0.3+ (highly skewed VMs). VMs with imbalance > 0.15 account for ~60% of all requests.

**Key Finding 3:** The skewed VM size distribution in Azure-like workloads creates natural fragmentation opportunities. Dimension-agnostic heuristics fail to exploit the complementarity between CPU-heavy and RAM-heavy VM types.

## 4. Correlation Between Resource Imbalance and Fragmentation

Quantitative analysis reveals:

| Workload Type   | BFD Frag | FARB Frag | Reduction |
|-----------------|----------|-----------|-----------|
| Azure-like      | 23.4%    | 14.0%     | 40.2%     |
| Google-like     | 32.2%    | 29.5%     | 8.4%      |
| CPU-heavy       | 90.1%    | 82.1%     | 8.9%      |
| RAM-heavy       | 89.5%    | 86.6%     | 3.2%      |
| Bimodal         | 62.6%    | 63.1%     | -0.8%     |

The fragmentation reduction is largest on **Azure-like workloads** where discrete VM types create strong complementarity opportunities. On homogeneous workloads (uniform_small, bimodal), FARB provides minimal fragmentation benefit because all VMs have similar resource ratios.

**Key Finding 4:** FARB's benefit is proportional to the diversity of VM resource ratios in the workload. Workloads with heterogeneous VM types (like production Azure/Google traces) benefit most from fragmentation-aware placement.

## Identified Fragmentation Patterns

### Pattern 1: Cascading Dimensional Imbalance
When BFD places a CPU-heavy VM on a nearly-full host, the remaining capacity becomes RAM-stranded. Subsequent RAM-heavy arrivals cannot use this host, forcing a new host to open. This cascading effect amplifies waste.

**Exploited by FARB:** FARB's balance score term explicitly prevents placements that create extreme dimensional imbalance, breaking the cascade.

### Pattern 2: Departure-Induced Stranding
When VMs depart, they leave behind "holes" in specific dimensions. Under BFD, new arrivals fill these holes based on total residual magnitude, not dimensional fit. This leads to progressive dimensional skew.

**Exploited by FARB:** After departures create imbalanced hosts, FARB steers complementary VMs to those hosts, naturally healing the imbalance.

## Figures

1. `figures/fig8_stranded_resources.png` — Distribution of stranded resource types (BFD vs FARB)
2. `figures/fig2_fragmentation_timeseries.png` — Temporal fragmentation patterns
3. `figures/fig9_vm_size_fragmentation.png` — VM size distribution and imbalance analysis
4. `figures/fig3_utilization_heatmap.png` — CPU vs RAM utilization heatmap showing fragmentation

# Evaluation Metrics and Success Criteria

## 1. Host Utilization Ratio

**Definition**: The average fraction of allocated resources across both dimensions on active hosts.

$$U(t) = \frac{1}{|\mathcal{H}_{\text{active}}(t)|} \sum_{j \in \mathcal{H}_{\text{active}}(t)} \frac{1}{2}\left(\frac{\sum_{v_i \in \mathcal{V}_j(t)} d_i^{\text{cpu}}}{C_j^{\text{cpu}}} + \frac{\sum_{v_i \in \mathcal{V}_j(t)} d_i^{\text{ram}}}{C_j^{\text{ram}}}\right)$$

where $\mathcal{H}_{\text{active}}(t)$ is the set of hosts with at least one VM at time $t$.

- **Range**: [0, 1], higher is better
- **Interpretation**: 1.0 means all active hosts are fully utilized in both dimensions; values below 0.8 indicate significant waste.
- **Benchmark**: Protean achieves 85-90% utilization on Azure (Hadary et al., 2020).

## 2. Fragmentation Index

**Definition**: The fraction of active hosts with **stranded resources** — significant free capacity in one dimension but not the other.

A host $h_j$ has stranded resources at time $t$ if:
$$\min\left(\frac{r_j^{\text{cpu}}(t)}{C_j^{\text{cpu}}}, \frac{r_j^{\text{ram}}(t)}{C_j^{\text{ram}}}\right) < \tau \quad \text{AND} \quad \max\left(\frac{r_j^{\text{cpu}}(t)}{C_j^{\text{cpu}}}, \frac{r_j^{\text{ram}}(t)}{C_j^{\text{ram}}}\right) > \tau$$

where $r_j^{\text{cpu}}(t)$ and $r_j^{\text{ram}}(t)$ are the residual (free) CPU and RAM on host $h_j$, and $\tau = 0.1$ is the stranding threshold (10% of host capacity).

$$F(t) = \frac{|\{j \in \mathcal{H}_{\text{active}}(t) : h_j \text{ has stranded resources}\}|}{|\mathcal{H}_{\text{active}}(t)|}$$

- **Range**: [0, 1], lower is better
- **Interpretation**: 0.0 means no hosts have resource imbalance; values above 0.3 indicate significant fragmentation.

## 3. Number of Active Hosts

**Definition**: The count of hosts with at least one allocated VM at time $t$.

$$N(t) = |\{j : \mathcal{V}_j(t) \neq \emptyset\}|$$

- **Range**: [1, ∞), lower is better (for same total workload)
- **Interpretation**: Directly measures the number of powered-on servers required. The ratio $N(t) / N^*(t)$ (where $N^*$ is the theoretical minimum) gives the packing inefficiency.

## 4. Resource Waste Percentage

**Definition**: The fraction of total capacity on active hosts that is unallocated.

$$W(t) = \frac{\sum_{j \in \mathcal{H}_{\text{active}}(t)} \left[(C_j^{\text{cpu}} - \sum_{v_i \in \mathcal{V}_j(t)} d_i^{\text{cpu}}) + (C_j^{\text{ram}} - \sum_{v_i \in \mathcal{V}_j(t)} d_i^{\text{ram}})\right]}{\sum_{j \in \mathcal{H}_{\text{active}}(t)} (C_j^{\text{cpu}} + C_j^{\text{ram}})} \times 100\%$$

- **Range**: [0%, 100%], lower is better
- **Interpretation**: Represents wasted money — unused resources on powered-on servers. Typical values are 10-20% with current heuristics. Each 1% reduction at hyperscaler scale translates to hundreds of millions in savings.
- **Decomposition**: Can be decomposed into CPU waste and RAM waste separately to identify which dimension is the bottleneck.

## 5. Allocation Failure Rate

**Definition**: The fraction of VM requests that cannot be placed on any host due to insufficient capacity.

$$\text{AFR} = \frac{|\{v_i : \text{no feasible host for } v_i\}|}{|\mathcal{V}|}$$

- **Range**: [0, 1], lower is better (0 is ideal)
- **Interpretation**: Non-zero values indicate the cluster is overloaded or the packing heuristic creates too much fragmentation, preventing placement of VMs that could theoretically fit. A good heuristic maintains low AFR even at high load.

## Success Target

**Primary success criterion**: The novel heuristic must reduce **resource waste percentage** (Metric 4) by at least **2 percentage points** compared to the best baseline heuristic (FFD or BFD) on at least one production trace (Google ClusterData2019 or Azure Packing 2020).

For example, if BFD achieves 15% waste, the novel heuristic must achieve ≤ 13% waste.

**Secondary success criteria**:
- Fragmentation index (Metric 2) reduced by at least 5% relative
- No increase in allocation failure rate (Metric 5) compared to baselines
- Per-allocation decision time ≤ 10ms for clusters up to 10,000 hosts (practical constraint)
- Improvement is statistically significant (p < 0.05) across multiple seeds/runs

## Measurement Protocol

- All metrics are computed at configurable intervals:
  - **Per-event**: After each VM arrival/departure
  - **Per-time-window**: Averaged over configurable time windows (e.g., 5-minute intervals)
  - **End-of-trace**: Aggregate over entire simulation

- Results are stored as:
  - JSON summary (aggregate metrics) in `results/`
  - CSV time-series (per-window metrics) in `results/`

- Statistical robustness:
  - Each experiment is run with 3 random seeds (42, 123, 456) for tie-breaking
  - Reported metrics include mean, standard deviation, min, max across seeds
  - Paired statistical tests (Wilcoxon signed-rank) for comparison between heuristics

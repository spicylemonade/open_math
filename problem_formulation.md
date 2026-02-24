# Formal Problem Definition: 2D Vector Bin Packing for Cloud VM Scheduling

## 1. Problem Overview

Cloud providers allocate virtual machines (VMs) onto physical hosts (servers). Each VM requires
a specific amount of CPU and RAM, and each physical host has fixed CPU and RAM capacities.
The goal is to pack VMs onto the minimum number of hosts while respecting capacity constraints
in both dimensions. This is a 2-dimensional **vector bin packing** (VBP) problem, studied
extensively in the combinatorial optimization literature (Christensen et al., 2017).

## 2. Formal Specification

### 2.1 Bins: Physical Hosts

Let $\mathcal{H} = \{h_1, h_2, \ldots\}$ be a (potentially unbounded) set of physical hosts.
Each host $h_j$ has a **capacity vector**:

$$C_j = (C_j^{\text{cpu}}, C_j^{\text{ram}})$$

where $C_j^{\text{cpu}} > 0$ is the CPU capacity (in cores or normalized units) and
$C_j^{\text{ram}} > 0$ is the RAM capacity (in GB or normalized units).

In the homogeneous case (our primary setting), all hosts share the same capacity:
$C_j = (C^{\text{cpu}}, C^{\text{ram}})$ for all $j$.

### 2.2 Items: VM Requests

Let $\mathcal{V} = \{v_1, v_2, \ldots, v_n\}$ be a sequence of VM requests.
Each VM $v_i$ has a **demand vector**:

$$d_i = (d_i^{\text{cpu}}, d_i^{\text{ram}})$$

where $0 < d_i^{\text{cpu}} \leq C^{\text{cpu}}$ and $0 < d_i^{\text{ram}} \leq C^{\text{ram}}$.

### 2.3 Online Arrival/Departure Model

VMs arrive and depart over time in an **online** fashion:

- **Arrival**: VM $v_i$ arrives at time $a_i$ and must be placed immediately on a host
  (or rejected if no feasible host exists). The scheduler does not know future arrivals.
- **Departure**: VM $v_i$ departs at time $t_i > a_i$, freeing its resources on the
  assigned host. Departure times may or may not be known at arrival (in the general
  online model, they are unknown).

Formally, the input is a sequence of events $\mathcal{E} = \{e_1, e_2, \ldots\}$ where
each event is either:
- $(\text{ARRIVE}, v_i, a_i)$: VM $v_i$ requests placement at time $a_i$
- $(\text{DEPART}, v_i, t_i)$: VM $v_i$ releases resources at time $t_i$

Events are processed in chronological order. Upon an ARRIVE event, the algorithm must
immediately assign $v_i$ to some host $h_j$ or reject it. This assignment is irrevocable
in the standard model (no migration).

### 2.4 Capacity Constraints (No Overcommit)

At any time $t$, let $\mathcal{V}_j(t) \subseteq \mathcal{V}$ be the set of VMs currently
assigned to host $h_j$. The **no-overcommit constraint** requires:

$$\sum_{v_i \in \mathcal{V}_j(t)} d_i^{\text{cpu}} \leq C_j^{\text{cpu}} \quad \forall j, \forall t$$

$$\sum_{v_i \in \mathcal{V}_j(t)} d_i^{\text{ram}} \leq C_j^{\text{ram}} \quad \forall j, \forall t$$

Both dimensions must be satisfied simultaneously — this is what distinguishes vector bin
packing from 1D bin packing.

### 2.5 Optimization Objectives

**Primary objective**: Minimize the number of active hosts at any point in time.
A host $h_j$ is **active** at time $t$ if $\mathcal{V}_j(t) \neq \emptyset$.

$$\text{minimize} \quad |\{j : \mathcal{V}_j(t) \neq \emptyset\}| \quad \forall t$$

**Secondary objective**: Minimize **resource fragmentation**, defined as unused capacity
on active hosts. The **resource waste** at time $t$ is:

$$W(t) = \sum_{j \text{ active}} \left[ \left(C_j^{\text{cpu}} - \sum_{v_i \in \mathcal{V}_j(t)} d_i^{\text{cpu}}\right) + \left(C_j^{\text{ram}} - \sum_{v_i \in \mathcal{V}_j(t)} d_i^{\text{ram}}\right) \right]$$

Fragmentation is particularly problematic when resources are **stranded**: a host has
free CPU but no free RAM (or vice versa), making it unable to accept any new VM despite
having unused capacity in one dimension.

### 2.6 Key Constraints Summary

1. **No overcommit per dimension**: Each host's allocated CPU and RAM must not exceed capacity.
2. **Online decisions**: Placement must be made upon arrival with no knowledge of future requests.
3. **Irrevocable placement**: Once assigned, a VM stays on its host until departure (in the
   base model; migration extensions relax this).
4. **Dynamic departures**: VMs leave at arbitrary times, creating fragmented free space.
5. **Feasibility**: A VM $v_i$ can only be placed on host $h_j$ if there is sufficient
   remaining capacity in **both** dimensions simultaneously.

## 3. Relationship to Standard Formulations

This formulation follows the **d-dimensional vector bin packing** framework from
Christensen et al. (2017), specialized to $d = 2$. In their notation:
- Items are $d$-dimensional vectors in $(0, 1]^d$ (after normalization by host capacity)
- Bins have capacity vector $(1, 1, \ldots, 1) \in \mathbb{R}^d$
- The goal is to partition items into the minimum number of bins such that no bin's
  capacity is exceeded in any dimension

Our formulation extends the standard VBP in two ways relevant to cloud scheduling:
1. **Dynamic/online model**: Items arrive and depart over time, unlike the static offline VBP
2. **Temporal reuse**: When a VM departs, its host capacity becomes available for future VMs

This dynamic variant is sometimes called **Dynamic Vector Bin Packing** (DVBP) in the
literature. The competitive ratio for online 2D bin packing is known to be at most 2.5545
(Han et al., 2011), though this bound applies to the geometric (rectangle packing) variant
rather than the vector packing variant directly.

## 4. Complexity

- The offline 1D bin packing problem is NP-hard (reduction from PARTITION).
- The $d$-dimensional vector bin packing problem is also NP-hard for any $d \geq 1$.
- For $d \geq 2$, no APTAS exists unless P = NP (Woeginger, 1997, as cited in Christensen et al.).
- The best known offline approximation for 2D VBP achieves AAR of $1 + \varepsilon$ for
  any $\varepsilon > 0$ when item sizes are bounded away from 1 (Bansal et al., 2016).
- In the online setting with arrivals and departures, the problem becomes significantly
  harder, motivating the use of heuristic approaches.

## References

- Christensen, H. I., Khan, A., Pokutta, S., & Tetali, P. (2017). Approximation and online
  algorithms for multidimensional bin packing: A survey. *Computer Science Review*, 24, 63-79.
- Han, X., Chin, F. Y. L., Ting, H. F., Zhang, G., & Zhang, Y. (2011). A new upper bound
  2.5545 on 2D online bin packing. *ACM Transactions on Algorithms*, 7(4), Article 50.
- Hadary, O., et al. (2020). Protean: VM Allocation Service at Scale. In *Proc. 14th USENIX
  Symposium on Operating Systems Design and Implementation (OSDI '20)*, pp. 845-861.
- Panigrahy, R., Talwar, K., Uyeda, L., & Wieder, U. (2011). Heuristics for Vector Bin
  Packing. *Microsoft Research Technical Report*.

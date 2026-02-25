# Problem Statement: Learned Heuristics for the Asymmetric TSP on Real Road Networks

## 1. Formal Problem Definition

### 1.1 The Asymmetric Traveling Salesman Problem (ATSP)

Given a complete directed graph G = (V, A) with vertex set V = {1, 2, ..., n} and arc set A = V × V, and a cost function c: A → ℝ≥0, find a Hamiltonian cycle (tour) τ = (v₁, v₂, ..., vₙ, v₁) that minimizes the total cost:

$$\text{minimize} \quad C(\tau) = \sum_{i=1}^{n} c(v_i, v_{i+1 \bmod n})$$

subject to τ visiting each vertex exactly once. The problem is **asymmetric** when c(i,j) ≠ c(j,i) for at least some pairs (i,j).

### 1.2 Road-Network ATSP

In the road-network setting, vertices correspond to physical locations (delivery stops, waypoints) and the cost c(i,j) is the shortest-path travel time (or distance) from location i to location j on the road network. This cost is:

- **Asymmetric:** One-way streets, divided highways, turn restrictions, and differing routes (e.g., highway access ramps) make c(i,j) ≠ c(j,i).
- **Non-metric (in general):** While shortest-path distances satisfy the triangle inequality on static networks, the degree of asymmetry and the relationship between geographic proximity and travel time can be complex.
- **Implicitly defined:** Costs are not given by a simple formula (e.g., Euclidean distance) but computed via shortest-path queries on a large road graph.

### 1.3 Time-Dependent Extension (TD-ATSP)

In the time-dependent variant, edge costs depend on the departure time:

$$c(i, j, t) = f_{ij}(t)$$

where f_{ij}: ℝ≥0 → ℝ≥0 models traffic variation. The tour cost becomes:

$$C(\tau) = \sum_{i=1}^{n} c(v_i, v_{i+1}, T_i)$$

where T_i is the arrival time at node v_i (with T_1 being the departure time). Arrival times propagate: T_{i+1} = T_i + c(v_i, v_{i+1}, T_i) + s_{v_{i+1}}, where s_v is the service time at stop v.

Time-dependent costs violate the FIFO property only under unusual traffic conditions, so we assume FIFO: departing later never leads to earlier arrival.

---

## 2. The Research Gap

### 2.1 Classical Solvers Assume Euclidean/Metric Structure

The two strongest TSP solvers — **Concorde** (exact) and **LKH** (heuristic) — were developed for and primarily tested on Euclidean or metric TSP instances:

1. **Concorde** handles only symmetric TSP. It cannot solve ATSP directly.

2. **LKH-3** handles ATSP via the Jonker-Volgenant transformation (doubling the graph to 2n nodes). However, its core acceleration — the **α-nearness candidate set** — is derived from a 1-tree relaxation that estimates edge quality based on how well an edge fits into a minimum spanning tree structure. This works well for Euclidean instances where spatial proximity correlates with good tour edges. On road networks, the following distortions occur:

   - **One-way streets** create edges where (i→j) exists but (j→i) is much costlier (requires a long detour). The 1-tree cannot capture this directional structure since it operates on the symmetrized transformed graph.
   - **Road hierarchy effects:** A highway segment connecting distant nodes may be faster than a direct local road between nearby nodes. α-nearness, rooted in tree structure, may not rank such edges highly.
   - **Network topology:** Dead ends, bridges, and bottlenecks create non-obvious connectivity patterns that geographic proximity does not predict.

3. **OR-Tools** handles asymmetric matrices natively but uses generic local search without road-network-specific features. Its solution quality on pure TSP instances is typically 2–10% worse than LKH.

### 2.2 Learned Methods Assume Euclidean Coordinates

Most neural combinatorial optimization methods (AM, POMO, NeuroLKH) are trained on random Euclidean instances in the unit square. Key assumptions that break on road networks:

- Node features are (x, y) coordinates — not meaningful as features on a road graph where geographic distance poorly predicts travel time.
- Edge features are Euclidean distances — losing information about road type, speed, one-way status, and traffic.
- Symmetry is assumed — POMO's multiple-optima trick exploits rotational symmetry of TSP tours, which does not hold for ATSP.

### 2.3 The Specific Opportunity

Road-network cost matrices have **rich structural patterns** that current solvers ignore:

- **Asymmetry ratio** a(i,j) = c(i,j)/c(j,i) encodes directional road structure
- **Speed** c_distance(i,j)/c_time(i,j) encodes road type (highway vs. local)
- **Graph topology** (degree, betweenness centrality) encodes network role
- **Traffic patterns** create time-varying but predictable cost variations

A learned model that can extract these features and use them to guide LKH's search — particularly in candidate set generation — could improve upon LKH's α-nearness on road-network instances.

---

## 3. Research Hypotheses

### Hypothesis H1: Learned Candidate Sets Improve LKH on Road-Network ATSP

**Statement:** A GNN-based edge scorer, trained on road-network ATSP instances with directed edge features (duration, distance, speed, asymmetry ratio), will generate candidate sets that contain ≥ 90% of optimal tour edges (candidate recall) with k=5 candidates per node. When used to guide LKH-3, this will reduce mean tour cost by ≥ 0.5% on 200-stop road-network instances compared to LKH-3 with default α-nearness candidates.

**Falsification:** If the learned candidate sets achieve < 90% recall at k=5, or if LKH-3 with learned candidates produces tours with mean cost ≥ 99.5% of LKH-3 default across all 200-stop benchmark instances.

**Rationale:** NeuroLKH demonstrated this paradigm on Euclidean TSP (99.95% recall at k=5 for TSP100). Road networks have even more exploitable structure (edge attributes, topology), but also greater complexity (asymmetry, non-metric distances).

### Hypothesis H2: RL-Guided Local Search Accelerates ATSP Improvement

**Statement:** An RL agent trained to select local search moves (2-opt, or-opt, relocate) on ATSP instances, using current tour state features (edge costs, position, local density), will find tours at least as good as random-restart 2-opt in ≤ 50% of the wall-clock time on 200-stop road-network instances.

**Falsification:** If the RL-guided search requires > 50% of random-restart 2-opt time to reach equivalent solution quality, or if it consistently finds worse tours.

**Rationale:** Random move selection wastes time on unpromising moves. An RL agent can learn which moves are likely to improve the tour based on local structure, avoiding fruitless exploration. The asymmetric setting has richer move structure (directed or-opt, directed relocate) that benefits more from intelligent selection.

### Hypothesis H3: The Hybrid Solver (Learned Candidates + RL Local Search) Outperforms Individual Components

**Statement:** The full hybrid solver combining GNN-based candidate generation with LKH-3 and RL-guided post-processing will achieve strictly lower mean tour cost than either component alone on ≥ 60% of 200-stop and 1000-stop benchmark instances under at least one time budget (1s, 10s, or 60s).

**Falsification:** If the hybrid solver does not outperform both (a) LKH-3 with learned candidates only and (b) LKH-3 with RL local search only on ≥ 60% of instances at any time budget.

**Rationale:** Candidate generation and local search improvement address complementary aspects: better candidates speed up LKH's convergence to good local optima, while RL local search escapes local optima more efficiently. The combination should be synergistic.

### Hypothesis H4: Traffic-Aware Cost Modeling Changes Optimal Tours Significantly

**Statement:** On road-network instances with time-dependent costs (peak vs. off-peak traffic), the optimal departure-time-aware tour cost will differ by ≥ 10% from the tour cost computed with static (average) costs, and the optimal tour ordering will differ on ≥ 20% of edges.

**Falsification:** If tour cost varies by < 10% between peak and off-peak, or if < 20% of edges differ between static-optimal and time-dependent-optimal tours.

**Rationale:** Urban road networks experience 2–4× speed variation between peak and off-peak. This should substantially affect both tour cost and optimal sequencing, especially when tours traverse mixed road types (highway commute corridors vs. local streets).

---

## 4. Success Criteria

### Primary Success Criteria

1. **Tour Quality:** The hybrid solver achieves ≥ 0.5% lower mean tour cost than LKH-3 default on ≥ 60% of 200-stop and 1000-stop road-network benchmark instances.

2. **Statistical Significance:** The improvement is statistically significant (paired Wilcoxon test, p < 0.05) on at least the 200-stop and 1000-stop instance sets.

3. **Scalability:** The hybrid solver remains competitive (gap < 2% vs. LKH-3) on instances up to 2000 stops.

### Secondary Success Criteria

4. **Candidate Set Quality:** Learned candidate sets achieve ≥ 90% recall of optimal tour edges at k=5 candidates per node.

5. **Speed:** GNN inference adds < 20% overhead to total solve time on 200-stop instances.

6. **Generalization:** A model trained on one city's road network achieves at least 80% of its training-city improvement when tested on a different city.

### Minimum Viable Outcome

Even if the primary criteria are not fully met, the project succeeds if:
- We produce a rigorous experimental comparison of classical and hybrid solvers on real road-network ATSP instances
- We demonstrate that road-network-specific features (asymmetry, speed, topology) provide measurable signal for tour edge prediction
- We identify and document the specific conditions under which learned guidance helps or hurts LKH performance

---

## 5. Scope Boundaries

### In Scope
- Single-vehicle ATSP on road networks (no fleet/multi-vehicle)
- Synthetic traffic patterns modeled on realistic time-of-day profiles
- Instances from 50 to 5000 stops
- Cities with OSM data: Manhattan (NYC), central London, Berlin

### Out of Scope
- Real-time dynamic re-routing
- Multi-vehicle CVRP or VRPTW
- Integration with actual OSRM servers (using offline OSMnx-based approximation)
- Hardware-specific optimization (GPU deployment, quantization)
- Customer-facing API or deployment system

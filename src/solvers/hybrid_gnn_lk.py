"""
Hybrid GNN-guided Lin-Kernighan style local search for ATSP.

Uses a trained GNN edge scorer to bias the candidate edge set in a
Lin-Kernighan style local search.  The key idea is that the GNN predicts
which directed edges are most likely to appear in a near-optimal tour,
and the local search restricts its neighborhood exploration to those
high-scoring candidate edges.  This dramatically reduces the search space
while focusing moves on the most promising edges.

Algorithm overview:
  1. Score all directed edges with the GNN (or random scores for ablation).
  2. For each node, keep the top-K highest-scoring outgoing edges as
     candidates (K = min(10, n // 2)).
  3. Construct an initial tour using nearest-neighbor restricted to the
     candidate edge set.
  4. Apply 2-opt improvement restricted to candidate edges.
  5. Apply or-opt improvement (segments of length 1, 2, 3).
  6. If time allows, perturb (double-bridge) and repeat.
  7. Track and return the best tour across all iterations.

The solver handles asymmetric costs correctly: all move evaluations use
directed edge costs, and when ``asymmetry_aware=False`` (ablation mode),
move deltas are computed using symmetrised costs to measure the impact
of ignoring directionality.

Falls back to random candidate scores if the model file does not exist.
"""

import time
import os
import sys

import numpy as np

# ---------------------------------------------------------------------------
# Import the GNN model
# ---------------------------------------------------------------------------
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
from src.models.edge_scorer import build_edge_scorer, AsymmetricEdgeScorer

try:
    import torch
    HAS_TORCH = True
except ImportError:
    HAS_TORCH = False


# ---------------------------------------------------------------------------
# Helper utilities
# ---------------------------------------------------------------------------

def compute_tour_cost(tour, cost_matrix):
    """Compute the total cost of a directed tour.

    Parameters
    ----------
    tour : list[int]
        Ordered sequence of node indices forming a Hamiltonian cycle.
    cost_matrix : np.ndarray
        Asymmetric cost matrix of shape (n, n).

    Returns
    -------
    float
        Total tour cost (sum of directed edge costs along the cycle).
    """
    cost = 0.0
    n = len(tour)
    for i in range(n):
        cost += cost_matrix[tour[i]][tour[(i + 1) % n]]
    return cost


def validate_tour(tour, cost_matrix, reported_cost=None, atol=1e-6):
    """Validate that a tour is a valid Hamiltonian cycle.

    Checks
    ------
    1. Every node in {0, ..., n-1} is visited exactly once.
    2. If ``reported_cost`` is given, it must match the recomputed cost
       within absolute tolerance ``atol``.

    Parameters
    ----------
    tour : list[int]
        The tour to validate.
    cost_matrix : np.ndarray
        Asymmetric cost matrix of shape (n, n).
    reported_cost : float or None
        If not None, the reported cost is checked against the recomputed
        cost.
    atol : float
        Absolute tolerance for cost comparison.

    Returns
    -------
    bool
        True if all checks pass.

    Raises
    ------
    ValueError
        If any validation check fails.
    """
    n = cost_matrix.shape[0]

    if len(tour) != n:
        raise ValueError(
            f"Tour length {len(tour)} does not match number of nodes {n}."
        )

    visited = set(tour)
    if len(visited) != n:
        raise ValueError(
            f"Tour visits {len(visited)} unique nodes, expected {n}."
        )

    if visited != set(range(n)):
        missing = set(range(n)) - visited
        extra = visited - set(range(n))
        raise ValueError(
            f"Tour has missing nodes {missing} and/or invalid nodes {extra}."
        )

    actual_cost = compute_tour_cost(tour, cost_matrix)
    if reported_cost is not None:
        if abs(actual_cost - reported_cost) > atol:
            raise ValueError(
                f"Reported cost {reported_cost} does not match recomputed "
                f"cost {actual_cost} (diff={abs(actual_cost - reported_cost)})."
            )

    return True


# ---------------------------------------------------------------------------
# GNN scoring
# ---------------------------------------------------------------------------

def _load_gnn_model(model_path, device=None):
    """Load a trained GNN edge scorer from a checkpoint file.

    Parameters
    ----------
    model_path : str
        Path to the saved ``state_dict`` (.pt file).
    device : torch.device or None
        Target device.

    Returns
    -------
    AsymmetricEdgeScorer or None
        The loaded model in eval mode, or None if loading fails.
    """
    if not HAS_TORCH:
        return None

    if not os.path.isfile(model_path):
        return None

    if device is None:
        device = torch.device('cpu')

    try:
        model = build_edge_scorer(hidden_dim=64, n_layers=3, dropout=0.1)
        state_dict = torch.load(model_path, map_location=device, weights_only=True)
        model.load_state_dict(state_dict)
        model.to(device)
        model.eval()
        return model
    except Exception:
        return None


def _score_edges_gnn(instance, model, device=None):
    """Score all directed edges of an ATSP instance using the GNN.

    Parameters
    ----------
    instance : dict
        ATSP instance dictionary.
    model : AsymmetricEdgeScorer
        Trained GNN model (already in eval mode).
    device : torch.device or None
        Target device.

    Returns
    -------
    score_matrix : np.ndarray, shape (n, n)
        Matrix of edge scores in [0, 1]; diagonal is zero.
    """
    node_features, edge_features, edge_index = (
        AsymmetricEdgeScorer.instance_to_features(instance, device=device)
    )

    with torch.no_grad():
        scores = model(node_features, edge_features, edge_index)

    cost_matrix = np.asarray(instance["cost_matrix"], dtype=np.float64)
    n = cost_matrix.shape[0]

    score_matrix = np.zeros((n, n), dtype=np.float64)
    src = edge_index[0].cpu().numpy()
    dst = edge_index[1].cpu().numpy()
    score_matrix[src, dst] = scores.cpu().numpy()
    return score_matrix


def _score_edges_random(n, rng):
    """Generate random edge scores (for ablation when use_gnn=False).

    Parameters
    ----------
    n : int
        Number of nodes.
    rng : np.random.RandomState
        Random number generator.

    Returns
    -------
    score_matrix : np.ndarray, shape (n, n)
        Matrix of random scores in [0, 1]; diagonal is zero.
    """
    score_matrix = rng.uniform(0.0, 1.0, size=(n, n))
    np.fill_diagonal(score_matrix, 0.0)
    return score_matrix


# ---------------------------------------------------------------------------
# Candidate edge set construction
# ---------------------------------------------------------------------------

def _build_candidate_set(score_matrix, k):
    """Build a candidate edge set from GNN scores.

    For each node i, keep the top-K highest-scoring outgoing edges.

    Parameters
    ----------
    score_matrix : np.ndarray, shape (n, n)
        Edge scores (higher = more likely to be in optimal tour).
    k : int
        Number of candidate outgoing edges per node.

    Returns
    -------
    candidates : dict
        Mapping from node i to a set of candidate destination nodes.
    candidate_set : set of (int, int)
        Set of all candidate directed edges (i, j).
    """
    n = score_matrix.shape[0]
    candidates = {}
    candidate_set = set()

    for i in range(n):
        row = score_matrix[i].copy()
        row[i] = -1.0  # exclude self-loops
        # Get indices of top-k scores
        if k >= n - 1:
            top_k_indices = [j for j in range(n) if j != i]
        else:
            top_k_indices = np.argpartition(row, -k)[-k:]
            top_k_indices = [j for j in top_k_indices if j != i]
        candidates[i] = set(top_k_indices)
        for j in top_k_indices:
            candidate_set.add((i, j))

    return candidates, candidate_set


# ---------------------------------------------------------------------------
# Construction heuristic: nearest-neighbor on candidate set
# ---------------------------------------------------------------------------

def _nearest_neighbor_candidates(cost_matrix, candidates, start_node):
    """Build a tour using nearest-neighbor restricted to candidate edges.

    If no unvisited candidate neighbour exists, falls back to the
    globally nearest unvisited node.

    Parameters
    ----------
    cost_matrix : np.ndarray
        Asymmetric cost matrix of shape (n, n).
    candidates : dict
        Mapping from node i to set of candidate destination nodes.
    start_node : int
        Starting node.

    Returns
    -------
    list[int]
        A tour visiting all nodes exactly once.
    """
    n = cost_matrix.shape[0]
    visited = np.zeros(n, dtype=bool)
    tour = [start_node]
    visited[start_node] = True

    current = start_node
    for _ in range(n - 1):
        # Try candidate neighbours first
        best_next = -1
        best_cost = np.inf
        for j in candidates.get(current, set()):
            if not visited[j] and cost_matrix[current][j] < best_cost:
                best_cost = cost_matrix[current][j]
                best_next = j

        # Fallback: nearest unvisited node globally
        if best_next == -1:
            row = cost_matrix[current].copy()
            row[visited] = np.inf
            best_next = int(np.argmin(row))

        tour.append(best_next)
        visited[best_next] = True
        current = best_next

    return tour


def _best_nearest_neighbor_candidates(cost_matrix, candidates):
    """Run candidate-restricted nearest-neighbor from every node.

    Parameters
    ----------
    cost_matrix : np.ndarray
        Asymmetric cost matrix.
    candidates : dict
        Candidate edge set per node.

    Returns
    -------
    list[int]
        Best tour found.
    float
        Cost of the best tour.
    """
    n = cost_matrix.shape[0]
    best_tour = None
    best_cost = np.inf

    for start in range(n):
        tour = _nearest_neighbor_candidates(cost_matrix, candidates, start)
        cost = compute_tour_cost(tour, cost_matrix)
        if cost < best_cost:
            best_cost = cost
            best_tour = tour

    return best_tour, best_cost


# ---------------------------------------------------------------------------
# 2-opt local search restricted to candidate edges
# ---------------------------------------------------------------------------

def _two_opt_candidate_improve(tour, cost_matrix, candidate_set,
                               asymmetry_aware=True, time_deadline=None):
    """2-opt improvement restricted to candidate edges.

    A 2-opt move reverses the segment tour[i+1..j].  We only consider
    moves where at least one of the two new edges is in the candidate set.

    When ``asymmetry_aware=True``, move deltas are computed using the
    actual directed costs.  When False, deltas use symmetrised costs
    (average of both directions) as an ablation.

    Uses first-improvement strategy.

    Parameters
    ----------
    tour : list[int]
        Current tour (will be copied).
    cost_matrix : np.ndarray
        Asymmetric cost matrix.
    candidate_set : set of (int, int)
        Set of candidate directed edges.
    asymmetry_aware : bool
        Whether to evaluate moves using directed costs.
    time_deadline : float or None
        Wall-clock deadline.

    Returns
    -------
    list[int]
        Improved tour.
    float
        Cost of the improved tour.
    """
    tour = list(tour)
    n = len(tour)

    if n <= 3:
        return tour, compute_tour_cost(tour, cost_matrix)

    # Precompute the effective cost matrix for move evaluation
    if asymmetry_aware:
        C = cost_matrix
    else:
        # Symmetrised costs for ablation
        C = (cost_matrix + cost_matrix.T) / 2.0

    improved = True
    while improved:
        if time_deadline is not None and time.time() >= time_deadline:
            break
        improved = False

        # Build position lookup
        pos = {tour[k]: k for k in range(n)}

        for i in range(n):
            if time_deadline is not None and time.time() >= time_deadline:
                break

            # Current edge: tour[i] -> tour[(i+1) % n]
            a = tour[i]
            b = tour[(i + 1) % n]
            cost_ab = C[a][b]

            # Try all j such that reversing tour[i+1..j] is beneficial
            # and one of the new edges is a candidate
            for j in range(i + 2, i + n):
                j_mod = j % n
                # Skip trivial case
                if j_mod == i:
                    continue

                c = tour[j_mod]
                d = tour[(j_mod + 1) % n]

                # The 2-opt move replaces edges a->b and c->d with a->c and b->d
                # but with the segment between b and c reversed.
                # Check if at least one new edge is a candidate
                if (a, c) not in candidate_set and (b, d) not in candidate_set:
                    continue

                cost_cd = C[c][d]
                new_cost_ac = C[a][c]
                new_cost_bd = C[b][d]

                # Compute delta from the boundary edges
                delta_boundary = (new_cost_ac + new_cost_bd) - (cost_ab + cost_cd)

                # For the reversed segment, we also need to account for the
                # change in direction of internal edges.
                # In ATSP, reversing a segment [b, ..., c] flips all arcs.
                # Compute exact cost change of internal arcs.
                if asymmetry_aware:
                    # Extract the segment indices
                    seg_indices = []
                    idx = (i + 1) % n
                    while idx != (j_mod + 1) % n:
                        seg_indices.append(idx)
                        idx = (idx + 1) % n

                    if len(seg_indices) >= 2:
                        old_internal = 0.0
                        new_internal = 0.0
                        for s in range(len(seg_indices) - 1):
                            u = tour[seg_indices[s]]
                            v = tour[seg_indices[s + 1]]
                            old_internal += cost_matrix[u][v]
                            new_internal += cost_matrix[v][u]  # reversed
                        delta_internal = new_internal - old_internal
                    else:
                        delta_internal = 0.0

                    delta = delta_boundary + delta_internal
                else:
                    # With symmetrised costs, reversing does not change internal
                    # arc costs (by definition).
                    delta = delta_boundary

                if delta < -1e-10:
                    # Apply the move: reverse segment tour[i+1..j_mod]
                    seg_indices = []
                    idx = (i + 1) % n
                    while idx != (j_mod + 1) % n:
                        seg_indices.append(idx)
                        idx = (idx + 1) % n

                    # Reverse the segment in the tour
                    seg_nodes = [tour[s] for s in seg_indices]
                    seg_nodes.reverse()
                    for k, s in enumerate(seg_indices):
                        tour[s] = seg_nodes[k]

                    improved = True
                    break  # restart scan

            if improved:
                break

    return tour, compute_tour_cost(tour, cost_matrix)


# ---------------------------------------------------------------------------
# Or-opt local search
# ---------------------------------------------------------------------------

def _or_opt_improve(tour, cost_matrix, candidate_set, asymmetry_aware=True,
                    time_deadline=None):
    """Or-opt improvement using candidate edge guidance.

    Removes a segment of length 1, 2, or 3 and reinserts it at a
    position where at least one of the new connecting edges is in the
    candidate set.

    Parameters
    ----------
    tour : list[int]
        Current tour.
    cost_matrix : np.ndarray
        Asymmetric cost matrix.
    candidate_set : set of (int, int)
        Candidate directed edges.
    asymmetry_aware : bool
        Whether to evaluate using directed costs.
    time_deadline : float or None
        Wall-clock deadline.

    Returns
    -------
    list[int]
        Improved tour.
    float
        Cost of the improved tour.
    """
    tour = list(tour)
    n = len(tour)

    if n <= 4:
        return tour, compute_tour_cost(tour, cost_matrix)

    if asymmetry_aware:
        C = cost_matrix
    else:
        C = (cost_matrix + cost_matrix.T) / 2.0

    current_cost = compute_tour_cost(tour, cost_matrix)
    improved = True

    while improved:
        if time_deadline is not None and time.time() >= time_deadline:
            break
        improved = False

        for seg_len in [1, 2, 3]:
            if seg_len >= n - 1:
                continue
            if improved:
                break

            for i in range(n):
                if time_deadline is not None and time.time() >= time_deadline:
                    break

                # Segment: tour[i], tour[i+1], ..., tour[i+seg_len-1]
                seg_indices = [(i + k) % n for k in range(seg_len)]
                segment = [tour[idx] for idx in seg_indices]

                # Predecessor and successor of the segment in the tour
                pred_idx = (i - 1) % n
                succ_idx = (i + seg_len) % n
                pred_node = tour[pred_idx]
                succ_node = tour[succ_idx]

                # Cost of removing the segment
                # Edges removed: pred->seg[0], seg[-1]->succ
                # Edge added: pred->succ
                remove_cost = C[pred_node][segment[0]] + C[segment[-1]][succ_node]
                bridge_cost = C[pred_node][succ_node]
                removal_delta = bridge_cost - remove_cost

                # Internal segment cost (sum of edges within segment)
                seg_internal = 0.0
                for k in range(seg_len - 1):
                    seg_internal += C[segment[k]][segment[k + 1]]

                # Remaining tour after removal
                remaining_indices = [k for k in range(n) if k not in set(seg_indices)]
                remaining = [tour[k] for k in remaining_indices]
                n_rem = len(remaining)

                # Try inserting segment at each position in remaining tour
                for j in range(n_rem):
                    r_node = remaining[j]
                    r_next = remaining[(j + 1) % n_rem]

                    # At least one new edge should be a candidate
                    if ((r_node, segment[0]) not in candidate_set and
                            (segment[-1], r_next) not in candidate_set):
                        continue

                    # Cost of inserting: remove edge r_node->r_next,
                    # add r_node->seg[0] and seg[-1]->r_next
                    old_edge = C[r_node][r_next]
                    new_edges = C[r_node][segment[0]] + C[segment[-1]][r_next]
                    insert_delta = new_edges - old_edge

                    total_delta = removal_delta + insert_delta

                    if total_delta < -1e-10:
                        # Apply: build new tour
                        new_tour = remaining[:j + 1] + segment + remaining[j + 1:]
                        new_cost = compute_tour_cost(new_tour, cost_matrix)

                        if new_cost < current_cost - 1e-10:
                            tour = new_tour
                            current_cost = new_cost
                            improved = True
                            break

                if improved:
                    break
            if improved:
                break

    return tour, current_cost


# ---------------------------------------------------------------------------
# Perturbation: double-bridge
# ---------------------------------------------------------------------------

def _perturb_double_bridge(tour, rng):
    """Apply a double-bridge perturbation.

    Splits the tour into four segments and reconnects them in a different
    order, producing a tour that cannot be reached by 2-opt or 3-opt
    alone.

    Parameters
    ----------
    tour : list[int]
        Current tour.
    rng : np.random.RandomState
        Random number generator.

    Returns
    -------
    list[int]
        Perturbed tour.
    """
    n = len(tour)
    if n < 8:
        new_tour = list(tour)
        i, j = sorted(rng.choice(n, 2, replace=False))
        new_tour[i:j + 1] = rng.permutation(new_tour[i:j + 1]).tolist()
        return new_tour

    cuts = sorted(rng.choice(range(1, n), 3, replace=False))
    a, b, c = cuts

    seg1 = tour[:a]
    seg2 = tour[a:b]
    seg3 = tour[b:c]
    seg4 = tour[c:]

    # Reconnect: seg1 + seg3 + seg2 + seg4
    return seg1 + seg3 + seg2 + seg4


# ---------------------------------------------------------------------------
# Main solver
# ---------------------------------------------------------------------------

def solve_hybrid_gnn_lk(instance, time_limit=60.0, seed=42,
                         model_path='models/edge_scorer_best.pt',
                         use_gnn=True, asymmetry_aware=True):
    """Solve an ATSP instance using GNN-guided LK-style local search.

    The solver uses a trained GNN to score edges and constructs a
    candidate edge set from the highest-scoring edges.  Local search
    (2-opt and or-opt) is then restricted to moves involving candidate
    edges, reducing the neighborhood size while focusing on promising
    moves.

    Parameters
    ----------
    instance : dict
        ATSP instance dict with keys ``cost_matrix`` (list-of-lists or
        2-D array of shape (n, n)), ``coordinates`` (optional), and
        ``metadata`` (optional, with ``n_nodes``).
    time_limit : float
        Maximum wall-clock time in seconds.
    seed : int
        Random seed for reproducibility.
    model_path : str
        Path to the saved GNN model checkpoint (.pt file).
    use_gnn : bool
        If True, use the GNN to score edges.  If False, use random
        scores (ablation mode).
    asymmetry_aware : bool
        If True, evaluate moves using directed (asymmetric) costs.
        If False, use symmetrised costs in move evaluation (ablation).

    Returns
    -------
    dict
        Result dictionary with keys:
        - ``tour`` : list[int] -- the best tour found.
        - ``cost`` : float -- cost of the best tour.
        - ``runtime_seconds`` : float -- elapsed wall-clock time.
        - ``solver_params`` : dict -- parameters used for the solve.
        - ``solver_name`` : str -- ``'hybrid_gnn_lk'``.
    """
    start_time = time.time()
    rng = np.random.RandomState(seed)

    # Parse cost matrix
    cost_matrix = np.asarray(instance["cost_matrix"], dtype=np.float64)
    n = cost_matrix.shape[0]

    # Edge cases: trivial instances
    if n <= 1:
        return {
            "tour": list(range(n)),
            "cost": 0.0,
            "runtime_seconds": time.time() - start_time,
            "solver_params": {
                "time_limit": time_limit,
                "seed": seed,
                "model_path": model_path,
                "use_gnn": use_gnn,
                "asymmetry_aware": asymmetry_aware,
            },
            "solver_name": "hybrid_gnn_lk",
        }

    if n == 2:
        tour = [0, 1]
        cost = compute_tour_cost(tour, cost_matrix)
        return {
            "tour": tour,
            "cost": cost,
            "runtime_seconds": time.time() - start_time,
            "solver_params": {
                "time_limit": time_limit,
                "seed": seed,
                "model_path": model_path,
                "use_gnn": use_gnn,
                "asymmetry_aware": asymmetry_aware,
            },
            "solver_name": "hybrid_gnn_lk",
        }

    time_deadline = start_time + time_limit

    # ------------------------------------------------------------------
    # Step 1: Score edges
    # ------------------------------------------------------------------
    gnn_loaded = False
    if use_gnn and HAS_TORCH:
        device = torch.device('cpu')
        model = _load_gnn_model(model_path, device=device)
        if model is not None:
            try:
                score_matrix = _score_edges_gnn(instance, model, device=device)
                gnn_loaded = True
            except Exception:
                # Fall back to random scores on any GNN failure
                score_matrix = _score_edges_random(n, rng)
        else:
            score_matrix = _score_edges_random(n, rng)
    else:
        score_matrix = _score_edges_random(n, rng)

    # ------------------------------------------------------------------
    # Step 2: Build candidate edge set
    # ------------------------------------------------------------------
    k = min(10, max(2, n // 2))
    candidates, candidate_set = _build_candidate_set(score_matrix, k)

    # ------------------------------------------------------------------
    # Step 3: Construct initial tour using candidate-restricted NN
    # ------------------------------------------------------------------
    best_tour, best_cost = _best_nearest_neighbor_candidates(
        cost_matrix, candidates
    )

    # ------------------------------------------------------------------
    # Step 4: 2-opt improvement restricted to candidates
    # ------------------------------------------------------------------
    if time.time() < time_deadline:
        best_tour, best_cost = _two_opt_candidate_improve(
            best_tour, cost_matrix, candidate_set,
            asymmetry_aware=asymmetry_aware,
            time_deadline=time_deadline,
        )

    # ------------------------------------------------------------------
    # Step 5: Or-opt improvement
    # ------------------------------------------------------------------
    if time.time() < time_deadline:
        best_tour, best_cost = _or_opt_improve(
            best_tour, cost_matrix, candidate_set,
            asymmetry_aware=asymmetry_aware,
            time_deadline=time_deadline,
        )

    iterations_completed = 1

    # ------------------------------------------------------------------
    # Step 6: Iterated local search -- perturb and repeat
    # ------------------------------------------------------------------
    while time.time() < time_deadline:
        iterations_completed += 1

        # Perturb the best tour
        perturbed = _perturb_double_bridge(list(best_tour), rng)

        # 2-opt on perturbed tour
        if time.time() < time_deadline:
            improved_tour, improved_cost = _two_opt_candidate_improve(
                perturbed, cost_matrix, candidate_set,
                asymmetry_aware=asymmetry_aware,
                time_deadline=time_deadline,
            )
        else:
            improved_tour = perturbed
            improved_cost = compute_tour_cost(perturbed, cost_matrix)

        # Or-opt on result
        if time.time() < time_deadline:
            improved_tour, improved_cost = _or_opt_improve(
                improved_tour, cost_matrix, candidate_set,
                asymmetry_aware=asymmetry_aware,
                time_deadline=time_deadline,
            )

        # Update best
        if improved_cost < best_cost - 1e-10:
            best_tour = improved_tour
            best_cost = improved_cost

    elapsed = time.time() - start_time

    # Final validation
    validate_tour(best_tour, cost_matrix, reported_cost=best_cost)

    return {
        "tour": best_tour,
        "cost": best_cost,
        "runtime_seconds": elapsed,
        "solver_params": {
            "time_limit": time_limit,
            "seed": seed,
            "model_path": model_path,
            "use_gnn": use_gnn,
            "asymmetry_aware": asymmetry_aware,
            "k_candidates": k,
            "gnn_loaded": gnn_loaded,
            "iterations_completed": iterations_completed,
        },
        "solver_name": "hybrid_gnn_lk",
    }


# ---------------------------------------------------------------------------
# CLI entry point for quick testing
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    import json

    sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

    try:
        from src.data.instance_generator import generate_synthetic_instance
    except ImportError:
        generate_synthetic_instance = None

    if generate_synthetic_instance is not None:
        print("=== Hybrid GNN-LK ATSP Solver Self-Test ===\n")

        for n_nodes in [10, 20, 50]:
            print(f"--- Instance: n={n_nodes} ---")
            inst = generate_synthetic_instance(n_nodes, seed=42)

            # Test with GNN (will fall back to random if no model)
            result_gnn = solve_hybrid_gnn_lk(
                inst,
                time_limit=10.0,
                seed=42,
                use_gnn=True,
                asymmetry_aware=True,
            )
            print(f"  GNN-guided  : cost={result_gnn['cost']:.2f}, "
                  f"time={result_gnn['runtime_seconds']:.3f}s, "
                  f"iters={result_gnn['solver_params']['iterations_completed']}, "
                  f"gnn_loaded={result_gnn['solver_params']['gnn_loaded']}")

            # Test ablation: random candidates
            result_rnd = solve_hybrid_gnn_lk(
                inst,
                time_limit=10.0,
                seed=42,
                use_gnn=False,
                asymmetry_aware=True,
            )
            print(f"  Random cand : cost={result_rnd['cost']:.2f}, "
                  f"time={result_rnd['runtime_seconds']:.3f}s, "
                  f"iters={result_rnd['solver_params']['iterations_completed']}")

            # Test ablation: no asymmetry awareness
            result_sym = solve_hybrid_gnn_lk(
                inst,
                time_limit=10.0,
                seed=42,
                use_gnn=True,
                asymmetry_aware=False,
            )
            print(f"  Sym. eval   : cost={result_sym['cost']:.2f}, "
                  f"time={result_sym['runtime_seconds']:.3f}s, "
                  f"iters={result_sym['solver_params']['iterations_completed']}")
            print()
    else:
        print("=== Hybrid GNN-LK Minimal Self-Test ===\n")

        n = 10
        cm = np.random.RandomState(42).uniform(10, 100, size=(n, n))
        np.fill_diagonal(cm, 0.0)

        instance = {
            "cost_matrix": cm.tolist(),
            "metadata": {"n_nodes": n},
        }

        result = solve_hybrid_gnn_lk(
            instance, time_limit=5.0, seed=42,
            use_gnn=False, asymmetry_aware=True,
        )
        print(f"Tour: {result['tour']}")
        print(f"Cost: {result['cost']:.2f}")
        print(f"Runtime: {result['runtime_seconds']:.3f}s")
        print(f"Iterations: {result['solver_params']['iterations_completed']}")
        print("Validation: passed")

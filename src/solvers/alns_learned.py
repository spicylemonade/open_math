"""
Adaptive Large Neighborhood Search (ALNS) with learned destroy/repair operators
for the Asymmetric Travelling Salesman Problem (ATSP).

The solver combines classical ALNS with optional GNN-guided repair:

Destroy operators:
  1. Random removal   -- remove random nodes from the tour
  2. Worst removal    -- remove nodes with highest detour cost
  3. Cluster removal  -- remove a cluster of nearby nodes (cost-based proximity)

Repair operators:
  1. Greedy insertion -- insert each removed node at the cheapest position
  2. Regret-2 insertion -- insert the node with highest regret first
  3. GNN-guided insertion -- prefer inserting between high-scoring edges

Adaptive weight mechanism with simulated annealing acceptance criterion.
"""

import math
import os
import time

import numpy as np


# ---------------------------------------------------------------------------
# Helper utilities
# ---------------------------------------------------------------------------

def compute_tour_cost(tour, cost_matrix):
    """Compute total cost of a directed Hamiltonian cycle.

    Parameters
    ----------
    tour : list[int]
        Ordered node indices forming the cycle.
    cost_matrix : array-like
        Square matrix where ``cost_matrix[i][j]`` is the cost from *i* to *j*.

    Returns
    -------
    float
        Sum of directed edge costs along the tour (including the closing edge).
    """
    cost = 0.0
    n = len(tour)
    for i in range(n):
        cost += cost_matrix[tour[i]][tour[(i + 1) % n]]
    return cost


def _nearest_neighbor_tour(cost_matrix, start_node):
    """Build a nearest-neighbor tour starting from *start_node*."""
    n = cost_matrix.shape[0]
    visited = np.zeros(n, dtype=bool)
    tour = [start_node]
    visited[start_node] = True
    current = start_node
    for _ in range(n - 1):
        row = cost_matrix[current].copy()
        row[visited] = np.inf
        next_node = int(np.argmin(row))
        tour.append(next_node)
        visited[next_node] = True
        current = next_node
    return tour


def _best_nearest_neighbor(cost_matrix):
    """Return the best nearest-neighbor tour across all starting nodes."""
    n = cost_matrix.shape[0]
    best_tour = None
    best_cost = np.inf
    for start in range(n):
        tour = _nearest_neighbor_tour(cost_matrix, start)
        cost = compute_tour_cost(tour, cost_matrix)
        if cost < best_cost:
            best_cost = cost
            best_tour = tour
    return best_tour, best_cost


# ---------------------------------------------------------------------------
# Destroy operators
# ---------------------------------------------------------------------------

def random_removal(tour, n_remove, rng):
    """Remove *n_remove* random nodes from the tour.

    Parameters
    ----------
    tour : list[int]
        Current tour.
    n_remove : int
        Number of nodes to remove.
    rng : numpy.random.RandomState
        Random number generator.

    Returns
    -------
    partial_tour : list[int]
        Tour with nodes removed.
    removed : list[int]
        The removed node indices.
    """
    n = len(tour)
    # Never remove all nodes -- keep at least one
    n_remove = min(n_remove, n - 1)
    indices_to_remove = set(rng.choice(n, size=n_remove, replace=False).tolist())
    removed = [tour[i] for i in indices_to_remove]
    partial_tour = [tour[i] for i in range(n) if i not in indices_to_remove]
    return partial_tour, removed


def worst_removal(tour, cost_matrix, n_remove):
    """Remove the *n_remove* nodes that contribute the most detour cost.

    The detour cost of node tour[i] is defined as:
        cost(tour[i-1] -> tour[i]) + cost(tour[i] -> tour[i+1])
        - cost(tour[i-1] -> tour[i+1])

    Nodes with the highest detour cost are the most expensive to keep.

    Parameters
    ----------
    tour : list[int]
        Current tour.
    cost_matrix : numpy.ndarray
        Asymmetric cost matrix.
    n_remove : int
        Number of nodes to remove.

    Returns
    -------
    partial_tour : list[int]
        Tour with expensive nodes removed.
    removed : list[int]
        The removed node indices.
    """
    n = len(tour)
    n_remove = min(n_remove, n - 1)

    # Compute detour cost for each position in the tour
    detour = np.zeros(n)
    for i in range(n):
        prev_node = tour[(i - 1) % n]
        curr_node = tour[i]
        next_node = tour[(i + 1) % n]
        detour[i] = (
            cost_matrix[prev_node][curr_node]
            + cost_matrix[curr_node][next_node]
            - cost_matrix[prev_node][next_node]
        )

    # Greedily remove the node with the highest detour cost, then recompute
    removed = []
    remaining_indices = list(range(n))

    for _ in range(n_remove):
        # Find the position with highest detour among remaining
        best_idx = -1
        best_detour = -np.inf
        for pos, idx in enumerate(remaining_indices):
            if detour[idx] > best_detour:
                best_detour = detour[idx]
                best_idx = pos

        removed_tour_idx = remaining_indices.pop(best_idx)
        removed.append(tour[removed_tour_idx])

    removed_set = set(removed)
    partial_tour = [node for node in tour if node not in removed_set]
    return partial_tour, removed


def cluster_removal(tour, cost_matrix, n_remove, rng):
    """Remove a cluster of nearby nodes based on cost-matrix proximity.

    A seed node is chosen at random, then the closest nodes (by average
    of forward and reverse cost) are added to the removal set.

    Parameters
    ----------
    tour : list[int]
        Current tour.
    cost_matrix : numpy.ndarray
        Asymmetric cost matrix.
    n_remove : int
        Number of nodes to remove.
    rng : numpy.random.RandomState
        Random number generator.

    Returns
    -------
    partial_tour : list[int]
        Tour with cluster removed.
    removed : list[int]
        The removed node indices.
    """
    n = len(tour)
    n_remove = min(n_remove, n - 1)

    # Pick a random seed node from the tour
    seed_pos = rng.randint(0, n)
    seed_node = tour[seed_pos]

    # Compute proximity of every other tour node to the seed node
    # Use average of forward + reverse cost as symmetric distance proxy
    tour_arr = np.array(tour)
    proximity = np.zeros(n)
    for i in range(n):
        node = tour[i]
        if node == seed_node:
            proximity[i] = -1.0  # will be removed first
        else:
            proximity[i] = (
                cost_matrix[seed_node][node] + cost_matrix[node][seed_node]
            ) / 2.0

    # Sort by proximity (ascending = nearest first); seed itself gets -1.0
    sorted_positions = np.argsort(proximity)

    # Take the n_remove nearest positions
    remove_positions = set(sorted_positions[:n_remove].tolist())
    removed = [tour[i] for i in remove_positions]
    partial_tour = [tour[i] for i in range(n) if i not in remove_positions]
    return partial_tour, removed


# ---------------------------------------------------------------------------
# Repair operators
# ---------------------------------------------------------------------------

def _cheapest_insertion_cost(partial_tour, node, cost_matrix):
    """Find the cheapest position to insert *node* into *partial_tour*.

    Returns the insertion cost delta and the position index (insert before
    that index).
    """
    best_delta = np.inf
    best_pos = 0
    m = len(partial_tour)

    if m == 0:
        return 0.0, 0

    if m == 1:
        # Only one position: the tour becomes [partial_tour[0], node]
        delta = (
            cost_matrix[partial_tour[0]][node]
            + cost_matrix[node][partial_tour[0]]
            - cost_matrix[partial_tour[0]][partial_tour[0]]
        )
        return delta, 1

    for i in range(m):
        a = partial_tour[i]
        b = partial_tour[(i + 1) % m]
        delta = cost_matrix[a][node] + cost_matrix[node][b] - cost_matrix[a][b]
        if delta < best_delta:
            best_delta = delta
            best_pos = (i + 1) % m if (i + 1) < m else m
    return best_delta, best_pos


def _insert_at(partial_tour, node, pos):
    """Insert *node* into *partial_tour* at position *pos*."""
    new_tour = list(partial_tour)
    new_tour.insert(pos, node)
    return new_tour


def greedy_insertion(partial_tour, removed, cost_matrix):
    """Repair by greedily inserting each removed node at its cheapest position.

    At each step the removed node whose cheapest insertion cost is lowest
    is inserted first.

    Parameters
    ----------
    partial_tour : list[int]
        Current partial tour.
    removed : list[int]
        Nodes to reinsert.
    cost_matrix : numpy.ndarray
        Asymmetric cost matrix.

    Returns
    -------
    list[int]
        Completed tour with all nodes reinserted.
    """
    tour = list(partial_tour)
    remaining = list(removed)

    while remaining:
        best_node = None
        best_delta = np.inf
        best_pos = 0
        best_idx = 0

        for idx, node in enumerate(remaining):
            delta, pos = _cheapest_insertion_cost(tour, node, cost_matrix)
            if delta < best_delta:
                best_delta = delta
                best_node = node
                best_pos = pos
                best_idx = idx

        tour = _insert_at(tour, best_node, best_pos)
        remaining.pop(best_idx)

    return tour


def regret2_insertion(partial_tour, removed, cost_matrix):
    """Repair using regret-2 insertion.

    For each uninserted node, compute the difference between its second-best
    and best insertion cost (the "regret").  Insert the node with the highest
    regret at its best position first.  This tends to avoid leaving difficult
    insertions for last.

    Parameters
    ----------
    partial_tour : list[int]
        Current partial tour.
    removed : list[int]
        Nodes to reinsert.
    cost_matrix : numpy.ndarray
        Asymmetric cost matrix.

    Returns
    -------
    list[int]
        Completed tour.
    """
    tour = list(partial_tour)
    remaining = list(removed)

    while remaining:
        best_regret = -np.inf
        best_node = None
        best_pos = 0
        best_idx = 0

        m = len(tour)

        for idx, node in enumerate(remaining):
            # Compute insertion cost at every position
            if m == 0:
                # First node to insert
                regret = 0.0
                pos = 0
                greedy_insertion_list = [(0.0, 0)]
            elif m == 1:
                regret = 0.0
                delta = (
                    cost_matrix[tour[0]][node]
                    + cost_matrix[node][tour[0]]
                    - cost_matrix[tour[0]][tour[0]]
                )
                pos = 1
                greedy_insertion_list = [(delta, 1)]
            else:
                deltas = []
                for i in range(m):
                    a = tour[i]
                    b = tour[(i + 1) % m]
                    delta = (
                        cost_matrix[a][node]
                        + cost_matrix[node][b]
                        - cost_matrix[a][b]
                    )
                    insert_pos = (i + 1) % m if (i + 1) < m else m
                    deltas.append((delta, insert_pos))

                deltas.sort(key=lambda x: x[0])
                best_delta_val = deltas[0][0]
                pos = deltas[0][1]

                if len(deltas) >= 2:
                    regret = deltas[1][0] - best_delta_val
                else:
                    regret = 0.0

            if regret > best_regret or (
                regret == best_regret and best_node is None
            ):
                best_regret = regret
                best_node = node
                best_pos = pos
                best_idx = idx

        tour = _insert_at(tour, best_node, best_pos)
        remaining.pop(best_idx)

    return tour


def gnn_guided_insertion(partial_tour, removed, cost_matrix, edge_scores):
    """Repair using GNN edge scores to guide insertion.

    If edge scores are available (not None), insertion positions are ranked
    by a combined metric that blends cheapest-insertion cost with the GNN's
    predicted edge quality.  Specifically, for inserting node *v* between
    nodes *a* and *b*:

        combined_score = delta_cost - alpha * (score(a,v) + score(v,b))

    where ``alpha`` scales the GNN bonus relative to the cost delta.  The
    node/position with the lowest combined score is chosen.

    If *edge_scores* is None, falls back to greedy insertion.

    Parameters
    ----------
    partial_tour : list[int]
        Current partial tour.
    removed : list[int]
        Nodes to reinsert.
    cost_matrix : numpy.ndarray
        Asymmetric cost matrix.
    edge_scores : numpy.ndarray or None
        Matrix of shape (n, n) with GNN edge probabilities, or None.

    Returns
    -------
    list[int]
        Completed tour.
    """
    if edge_scores is None:
        return greedy_insertion(partial_tour, removed, cost_matrix)

    tour = list(partial_tour)
    remaining = list(removed)

    # Determine alpha scaling: use a fraction of the mean cost as bonus scale
    n_total = cost_matrix.shape[0]
    mask = ~np.eye(n_total, dtype=bool)
    mean_cost = np.mean(cost_matrix[mask]) if np.any(mask) else 1.0
    alpha = 0.3 * mean_cost  # tune: 30% of mean edge cost

    while remaining:
        best_score = np.inf
        best_node = None
        best_pos = 0
        best_idx = 0

        m = len(tour)

        for idx, node in enumerate(remaining):
            if m == 0:
                combined = 0.0
                pos = 0
            elif m == 1:
                a = tour[0]
                delta = (
                    cost_matrix[a][node]
                    + cost_matrix[node][a]
                    - cost_matrix[a][a]
                )
                gnn_bonus = edge_scores[a][node] + edge_scores[node][a]
                combined = delta - alpha * gnn_bonus
                pos = 1
            else:
                combined = np.inf
                pos = 0
                for i in range(m):
                    a = tour[i]
                    b = tour[(i + 1) % m]
                    delta = (
                        cost_matrix[a][node]
                        + cost_matrix[node][b]
                        - cost_matrix[a][b]
                    )
                    gnn_bonus = edge_scores[a][node] + edge_scores[node][b]
                    score = delta - alpha * gnn_bonus
                    if score < combined:
                        combined = score
                        pos = (i + 1) % m if (i + 1) < m else m

            if combined < best_score:
                best_score = combined
                best_node = node
                best_pos = pos
                best_idx = idx

        tour = _insert_at(tour, best_node, best_pos)
        remaining.pop(best_idx)

    return tour


# ---------------------------------------------------------------------------
# GNN score loading
# ---------------------------------------------------------------------------

def _load_gnn_scores(instance, model_path):
    """Attempt to load GNN edge scores for the instance.

    Imports torch only when this function is called.  Returns None on any
    failure (missing model, import error, etc.).

    Parameters
    ----------
    instance : dict
        ATSP instance dictionary.
    model_path : str
        Path to the trained model checkpoint (.pt file).

    Returns
    -------
    numpy.ndarray or None
        Edge score matrix of shape (n, n), or None if loading fails.
    """
    if not os.path.isfile(model_path):
        return None

    try:
        import torch
        from src.models.edge_scorer import AsymmetricEdgeScorer, score_instance
    except ImportError:
        try:
            # Try relative import path for when running from repo root
            import sys
            repo_root = os.path.abspath(
                os.path.join(os.path.dirname(__file__), "..", "..")
            )
            if repo_root not in sys.path:
                sys.path.insert(0, repo_root)
            import torch
            from src.models.edge_scorer import AsymmetricEdgeScorer, score_instance
        except ImportError:
            return None

    try:
        device = torch.device("cpu")
        checkpoint = torch.load(model_path, map_location=device, weights_only=False)

        # Determine model hyperparameters from checkpoint
        if isinstance(checkpoint, dict) and "model_state_dict" in checkpoint:
            state_dict = checkpoint["model_state_dict"]
            config = checkpoint.get("config", {})
        elif isinstance(checkpoint, dict) and any(
            k.startswith("node_encoder") for k in checkpoint
        ):
            state_dict = checkpoint
            config = {}
        else:
            state_dict = checkpoint
            config = {}

        hidden_dim = config.get("hidden_dim", 64)
        n_layers = config.get("n_layers", 3)
        dropout = config.get("dropout", 0.1)

        model = AsymmetricEdgeScorer(
            node_dim=8,
            edge_dim=8,
            hidden_dim=hidden_dim,
            n_layers=n_layers,
            dropout=dropout,
        )
        model.load_state_dict(state_dict)
        model.eval()

        score_matrix = score_instance(model, instance, device=device)
        return score_matrix

    except Exception:
        return None


# ---------------------------------------------------------------------------
# Adaptive weight mechanism
# ---------------------------------------------------------------------------

class _AdaptiveWeights:
    """Roulette-wheel selection with adaptive weight updates.

    Each (destroy, repair) operator pair has a weight that is updated
    based on how well solutions produced by that pair performed.

    Parameters
    ----------
    n_destroy : int
        Number of destroy operators.
    n_repair : int
        Number of repair operators.
    rho : float
        Reaction factor for weight updates (learning rate).
    """

    def __init__(self, n_destroy, n_repair, rho=0.1):
        self.n_destroy = n_destroy
        self.n_repair = n_repair
        self.rho = rho
        # Weights for each operator (flattened: destroy_i * n_repair + repair_j)
        self.destroy_weights = np.ones(n_destroy, dtype=np.float64)
        self.repair_weights = np.ones(n_repair, dtype=np.float64)

    def select(self, rng):
        """Select a (destroy_idx, repair_idx) pair via roulette wheel.

        Parameters
        ----------
        rng : numpy.random.RandomState

        Returns
        -------
        destroy_idx : int
        repair_idx : int
        """
        # Select destroy operator
        d_probs = self.destroy_weights / self.destroy_weights.sum()
        destroy_idx = rng.choice(self.n_destroy, p=d_probs)

        # Select repair operator
        r_probs = self.repair_weights / self.repair_weights.sum()
        repair_idx = rng.choice(self.n_repair, p=r_probs)

        return destroy_idx, repair_idx

    def update(self, destroy_idx, repair_idx, reward):
        """Update weights for the selected operators.

        Parameters
        ----------
        destroy_idx : int
        repair_idx : int
        reward : float
            Performance reward (3 = improved best, 1 = accepted, 0 = rejected).
        """
        rho = self.rho
        self.destroy_weights[destroy_idx] = (
            (1.0 - rho) * self.destroy_weights[destroy_idx] + rho * reward
        )
        self.repair_weights[repair_idx] = (
            (1.0 - rho) * self.repair_weights[repair_idx] + rho * reward
        )

        # Clamp weights to a small positive minimum to avoid zero selection probability
        self.destroy_weights = np.maximum(self.destroy_weights, 0.01)
        self.repair_weights = np.maximum(self.repair_weights, 0.01)


# ---------------------------------------------------------------------------
# Main ALNS solver
# ---------------------------------------------------------------------------

def solve_alns(instance, time_limit=60.0, seed=42, max_iterations=1000,
               model_path='models/edge_scorer_best.pt'):
    """Solve an ATSP instance using Adaptive Large Neighborhood Search.

    Combines 3 destroy operators, 3 repair operators, adaptive operator
    selection, and simulated annealing acceptance.  Optionally uses GNN
    edge scores to guide the GNN-guided insertion repair operator.

    Parameters
    ----------
    instance : dict
        ATSP instance with keys ``cost_matrix``, ``metadata``, and optionally
        ``coordinates``.
    time_limit : float
        Maximum wall-clock time in seconds.
    seed : int
        Random seed for reproducibility.
    max_iterations : int
        Maximum number of ALNS iterations.
    model_path : str
        Path to a trained GNN model checkpoint (.pt file).  If the file
        does not exist, the GNN-guided repair operator falls back to
        greedy insertion.

    Returns
    -------
    dict
        Result dictionary with keys:
        - ``tour`` : list[int] -- the best tour found.
        - ``cost`` : float -- cost of the best tour.
        - ``runtime_seconds`` : float -- elapsed wall-clock time.
        - ``solver_params`` : dict -- parameters used for the solve.
        - ``solver_name`` : str -- always ``'alns'``.
    """
    start_time = time.time()
    rng = np.random.RandomState(seed)

    # Prepare cost matrix
    cost_matrix = np.asarray(instance["cost_matrix"], dtype=np.float64)
    n = cost_matrix.shape[0]

    # --- Edge cases ---
    if n <= 1:
        return {
            "tour": list(range(n)),
            "cost": 0.0,
            "runtime_seconds": time.time() - start_time,
            "solver_params": {
                "time_limit": time_limit,
                "seed": seed,
                "max_iterations": max_iterations,
                "model_path": model_path,
                "iterations_completed": 0,
            },
            "solver_name": "alns",
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
                "max_iterations": max_iterations,
                "model_path": model_path,
                "iterations_completed": 0,
            },
            "solver_name": "alns",
        }

    # --- Load GNN edge scores (optional, may be None) ---
    edge_scores = _load_gnn_scores(instance, model_path)

    # --- Construct initial solution via best nearest-neighbor ---
    current_tour, current_cost = _best_nearest_neighbor(cost_matrix)
    best_tour = list(current_tour)
    best_cost = current_cost

    # --- Removal size bounds ---
    min_remove = max(1, n // 10)
    max_remove = max(2, n // 3)

    # --- Simulated annealing parameters ---
    t_start = 0.05 * current_cost
    t_end = 0.0001 * current_cost
    if t_start <= 0:
        t_start = 1.0
    if t_end <= 0:
        t_end = 1e-6
    # Geometric cooling factor
    if max_iterations > 1:
        cooling_factor = (t_end / t_start) ** (1.0 / max_iterations)
    else:
        cooling_factor = 1.0
    temperature = t_start

    # --- Operator definitions ---
    # Destroy operators: index -> function
    destroy_operators = [
        lambda tour, nr, _rng=rng: random_removal(tour, nr, _rng),
        lambda tour, nr, _rng=None: worst_removal(tour, cost_matrix, nr),
        lambda tour, nr, _rng=rng: cluster_removal(tour, cost_matrix, nr, _rng),
    ]

    # Repair operators: index -> function
    repair_operators = [
        lambda pt, rem: greedy_insertion(pt, rem, cost_matrix),
        lambda pt, rem: regret2_insertion(pt, rem, cost_matrix),
        lambda pt, rem: gnn_guided_insertion(pt, rem, cost_matrix, edge_scores),
    ]

    n_destroy = len(destroy_operators)
    n_repair = len(repair_operators)

    # --- Adaptive weights ---
    weights = _AdaptiveWeights(n_destroy, n_repair, rho=0.1)

    # --- Main ALNS loop ---
    time_deadline = start_time + time_limit
    iterations_completed = 0

    for iteration in range(max_iterations):
        if time.time() >= time_deadline:
            break

        # Determine number of nodes to remove
        n_remove = rng.randint(min_remove, max_remove + 1)

        # Select operators
        d_idx, r_idx = weights.select(rng)

        # Destroy
        partial_tour, removed = destroy_operators[d_idx](list(current_tour), n_remove)

        # Repair
        candidate_tour = repair_operators[r_idx](partial_tour, removed)

        # Evaluate candidate
        candidate_cost = compute_tour_cost(candidate_tour, cost_matrix)

        # Determine reward
        reward = 0

        if candidate_cost < best_cost - 1e-10:
            # New global best
            best_tour = list(candidate_tour)
            best_cost = candidate_cost
            current_tour = list(candidate_tour)
            current_cost = candidate_cost
            reward = 3
        elif candidate_cost < current_cost - 1e-10:
            # Improved current solution (but not global best)
            current_tour = list(candidate_tour)
            current_cost = candidate_cost
            reward = 3
        else:
            # Simulated annealing acceptance
            delta = candidate_cost - current_cost
            if temperature > 1e-12:
                acceptance_prob = math.exp(-delta / temperature)
            else:
                acceptance_prob = 0.0

            if rng.random() < acceptance_prob:
                current_tour = list(candidate_tour)
                current_cost = candidate_cost
                reward = 1
            else:
                reward = 0

        # Update adaptive weights
        weights.update(d_idx, r_idx, reward)

        # Cool down
        temperature *= cooling_factor

        iterations_completed += 1

    elapsed = time.time() - start_time

    return {
        "tour": best_tour,
        "cost": best_cost,
        "runtime_seconds": elapsed,
        "solver_params": {
            "time_limit": time_limit,
            "seed": seed,
            "max_iterations": max_iterations,
            "model_path": model_path,
            "iterations_completed": iterations_completed,
            "gnn_scores_loaded": edge_scores is not None,
            "final_destroy_weights": weights.destroy_weights.tolist(),
            "final_repair_weights": weights.repair_weights.tolist(),
        },
        "solver_name": "alns",
    }


# ---------------------------------------------------------------------------
# CLI entry point for quick testing
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    import sys

    # Quick self-test with a small synthetic instance
    repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
    if repo_root not in sys.path:
        sys.path.insert(0, repo_root)

    try:
        from src.data.instance_generator import generate_synthetic_instance
    except ImportError:
        generate_synthetic_instance = None

    if generate_synthetic_instance is not None:
        print("=== ALNS Learned Solver Self-Test ===\n")

        for n_nodes in [10, 20, 50]:
            print(f"--- Instance: n={n_nodes} ---")
            inst = generate_synthetic_instance(n_nodes, seed=42)

            result = solve_alns(
                inst,
                time_limit=30.0,
                seed=42,
                max_iterations=500,
            )

            print(f"  Tour cost        : {result['cost']:.2f}")
            print(f"  Runtime          : {result['runtime_seconds']:.3f}s")
            print(f"  Iterations       : {result['solver_params']['iterations_completed']}")
            print(f"  GNN scores used  : {result['solver_params']['gnn_scores_loaded']}")
            print(f"  Destroy weights  : {result['solver_params']['final_destroy_weights']}")
            print(f"  Repair weights   : {result['solver_params']['final_repair_weights']}")

            # Compare with nearest-neighbor
            cm = np.asarray(inst["cost_matrix"], dtype=np.float64)
            _, nn_cost = _best_nearest_neighbor(cm)
            improvement = (nn_cost - result["cost"]) / nn_cost * 100
            print(f"  NN best cost     : {nn_cost:.2f}")
            print(f"  Improvement      : {improvement:.1f}%\n")
    else:
        # Minimal self-test without instance_generator
        print("=== ALNS Learned Solver Minimal Self-Test ===\n")

        test_rng = np.random.RandomState(42)
        n = 15
        cm = test_rng.uniform(10, 100, size=(n, n))
        np.fill_diagonal(cm, 0.0)

        instance = {
            "cost_matrix": cm.tolist(),
            "metadata": {"n_nodes": n},
        }

        result = solve_alns(instance, time_limit=10.0, seed=42, max_iterations=500)
        print(f"Tour       : {result['tour']}")
        print(f"Cost       : {result['cost']:.2f}")
        print(f"Runtime    : {result['runtime_seconds']:.3f}s")
        print(f"Iterations : {result['solver_params']['iterations_completed']}")

        # Validate tour
        tour_set = set(result["tour"])
        assert len(result["tour"]) == n, "Tour length mismatch"
        assert tour_set == set(range(n)), "Tour does not visit all nodes"
        recomputed = compute_tour_cost(result["tour"], cm)
        assert abs(recomputed - result["cost"]) < 1e-6, "Cost mismatch"
        print("Validation : passed")

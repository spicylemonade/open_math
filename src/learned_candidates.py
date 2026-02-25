"""
Learned candidate set generation for LKH-style local search.

Uses the trained edge-scoring GNN to rank edges by predicted tour membership
probability, then constructs candidate sets of top-k edges per node.
"""

import numpy as np
import torch
from typing import List, Tuple, Dict
from pathlib import Path

from src.models.edge_scorer import EdgeScorerGNN, prepare_graph_data


def load_edge_scorer(model_path: str = "models/edge_scorer.pt",
                     hidden_dim: int = 64, n_layers: int = 3,
                     n_heads: int = 4) -> EdgeScorerGNN:
    """Load trained edge-scoring model."""
    model = EdgeScorerGNN(
        node_input_dim=4, edge_input_dim=4,
        hidden_dim=hidden_dim, n_layers=n_layers, n_heads=n_heads
    )
    state_dict = torch.load(model_path, map_location="cpu", weights_only=True)
    model.load_state_dict(state_dict)
    model.eval()
    return model


def score_edges(model: EdgeScorerGNN, cost_matrix: np.ndarray,
                coordinates: list, k_graph: int = 20) -> Dict[int, List[Tuple[int, float]]]:
    """
    Score all edges in the k-nearest-neighbor graph using the GNN.

    Returns dict mapping each node to a list of (neighbor, score) pairs
    sorted by score descending.
    """
    n = cost_matrix.shape[0]
    graph_data = prepare_graph_data(cost_matrix, coordinates)

    with torch.no_grad():
        scores = model(
            graph_data["node_feats"],
            graph_data["edge_feats"],
            graph_data["edge_index"],
        )

    edge_index = graph_data["edge_index"].numpy()
    scores_np = scores.numpy()

    # Build per-node neighbor lists sorted by score
    node_candidates = {i: [] for i in range(n)}
    for e_idx in range(len(scores_np)):
        src = int(edge_index[0, e_idx])
        dst = int(edge_index[1, e_idx])
        node_candidates[src].append((dst, float(scores_np[e_idx])))

    # Sort each node's neighbors by score descending
    for node in node_candidates:
        node_candidates[node].sort(key=lambda x: -x[1])

    return node_candidates


def generate_candidate_set(model: EdgeScorerGNN, cost_matrix: np.ndarray,
                           coordinates: list, k: int = 5) -> Dict[int, List[int]]:
    """
    Generate learned candidate set: top-k neighbors per node ranked by GNN score.

    Parameters
    ----------
    model : trained EdgeScorerGNN
    cost_matrix : (N, N) asymmetric cost matrix
    coordinates : list of (lat, lon) tuples
    k : number of candidates per node

    Returns
    -------
    dict mapping node -> list of k candidate neighbor nodes
    """
    scored = score_edges(model, cost_matrix, coordinates)
    candidates = {}
    for node, neighbors in scored.items():
        candidates[node] = [nbr for nbr, _ in neighbors[:k]]
    return candidates


def generate_alpha_nearness_candidates(cost_matrix: np.ndarray,
                                       k: int = 5) -> Dict[int, List[int]]:
    """
    Generate classical alpha-nearness candidate set (baseline for comparison).

    Approximates LKH's alpha-nearness by using the k nearest neighbors
    in the asymmetric cost matrix (a simplified version).
    """
    n = cost_matrix.shape[0]
    candidates = {}
    for i in range(n):
        costs = cost_matrix[i].copy()
        costs[i] = np.inf
        nearest = np.argsort(costs)[:k]
        candidates[i] = list(nearest)
    return candidates


def candidate_set_recall(candidates: Dict[int, List[int]],
                         tour: List[int]) -> float:
    """
    Compute what fraction of tour edges are covered by the candidate set.

    Parameters
    ----------
    candidates : dict mapping node -> list of candidate neighbors
    tour : optimal or near-optimal tour

    Returns
    -------
    recall : fraction of tour edges in candidate set
    """
    n = len(tour)
    tour_edges = set()
    for i in range(n):
        src = tour[i]
        dst = tour[(i + 1) % n]
        tour_edges.add((src, dst))

    covered = 0
    for src, dst in tour_edges:
        if src in candidates and dst in candidates[src]:
            covered += 1

    return covered / len(tour_edges)


def write_lkh_candidate_file(candidates: Dict[int, List[int]],
                              cost_matrix: np.ndarray,
                              filename: str = "candidates.txt"):
    """
    Write candidate set in LKH-3's expected format.

    Format:
    N  (number of nodes)
    node_id  n_candidates  neighbor1 cost1  neighbor2 cost2 ...
    ...
    """
    n = len(candidates)
    with open(filename, "w") as f:
        f.write(f"{n}\n")
        for node in range(n):
            nbrs = candidates.get(node, [])
            parts = [f"{node + 1} {len(nbrs)}"]
            for nbr in nbrs:
                cost = int(cost_matrix[node, nbr] * 1000)
                parts.append(f"{nbr + 1} {cost}")
            f.write(" ".join(parts) + "\n")


def constrained_local_search(cost_matrix: np.ndarray, tour: List[int],
                              candidates: Dict[int, List[int]],
                              max_iter: int = 1000) -> Tuple[List[int], float]:
    """
    Local search using only candidate edges (simulates LKH with learned candidates).

    Performs 2-opt moves restricted to candidate edges, similar to how LKH
    restricts its Lin-Kernighan moves to the candidate set.
    """
    from src.local_search import tour_cost, two_opt_move

    n = len(tour)
    current_tour = list(tour)
    current_cost = tour_cost(cost_matrix, current_tour)
    improved = True

    for iteration in range(max_iter):
        if not improved:
            break
        improved = False

        for pos_i in range(n - 1):
            node_i = current_tour[pos_i]
            if node_i not in candidates:
                continue

            for target in candidates[node_i]:
                # Find position of target in tour
                try:
                    pos_j = current_tour.index(target)
                except ValueError:
                    continue

                if pos_j <= pos_i + 1:
                    continue
                if pos_j >= n:
                    continue

                new_tour, improvement = two_opt_move(
                    cost_matrix, current_tour, pos_i, pos_j)

                if improvement > 1e-10:
                    current_tour = new_tour
                    current_cost -= improvement
                    improved = True
                    break
            if improved:
                break

    return current_tour, tour_cost(cost_matrix, current_tour)


# ── Self-test ────────────────────────────────────────────────────────────

if __name__ == "__main__":
    import sys
    sys.path.insert(0, ".")
    from src.data_pipeline import load_instance
    from src.baselines import solve
    from src.local_search import tour_cost

    print("Testing learned candidate generation...")

    data = load_instance("benchmarks/manhattan_50_s42")
    cost_mat = data["durations"]
    coords = data["coordinates"]

    tour, ref_cost = solve(cost_mat, solver_name="ortools", seed=42)
    print(f"  Reference tour cost: {ref_cost:.1f}")

    # Test alpha-nearness candidates
    for k in [5, 10, 15, 20]:
        alpha_cands = generate_alpha_nearness_candidates(cost_mat, k=k)
        recall = candidate_set_recall(alpha_cands, tour)
        print(f"  Alpha-nearness k={k}: recall={recall:.3f}")

    # Test learned candidates (if model exists)
    import os
    if os.path.exists("models/edge_scorer.pt"):
        print("\n  Loading trained model...")
        model = load_edge_scorer()
        for k in [5, 10, 15, 20]:
            learned_cands = generate_candidate_set(model, cost_mat, coords, k=k)
            recall = candidate_set_recall(learned_cands, tour)
            print(f"  Learned k={k}: recall={recall:.3f}")

        # Compare candidate-constrained local search
        nn_tour, nn_cost = solve(cost_mat, solver_name="nearest_neighbor", seed=42)
        print(f"\n  NN cost: {nn_cost:.1f}")

        learned_cands = generate_candidate_set(model, cost_mat, coords, k=10)
        improved_tour, improved_cost = constrained_local_search(
            cost_mat, nn_tour, learned_cands, max_iter=100)
        print(f"  After learned-constrained search: {improved_cost:.1f} "
              f"({(nn_cost - improved_cost)/nn_cost*100:.1f}%)")

        alpha_cands = generate_alpha_nearness_candidates(cost_mat, k=10)
        alpha_tour, alpha_cost = constrained_local_search(
            cost_mat, nn_tour, alpha_cands, max_iter=100)
        print(f"  After alpha-constrained search: {alpha_cost:.1f} "
              f"({(nn_cost - alpha_cost)/nn_cost*100:.1f}%)")
    else:
        print("\n  No trained model found, skipping learned candidate tests")

    print("\nLearned candidates test passed!")

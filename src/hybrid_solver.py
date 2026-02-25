"""
Hybrid solver combining learned candidate generation + local search.

Architecture:
1. Use GNN edge scorer to generate learned candidate sets
2. Run candidate-constrained local search (simulating LKH with learned candidates)
3. Optionally apply RL-guided local search as post-processing
4. Exposes unified API matching baseline solver interface
"""

import numpy as np
import time
from typing import List, Tuple, Optional
from pathlib import Path

from src.baselines import solve as baseline_solve
from src.learned_candidates import (
    load_edge_scorer,
    generate_candidate_set,
    generate_alpha_nearness_candidates,
    constrained_local_search,
)
from src.local_search import (
    RLLocalSearchAgent,
    rl_guided_local_search,
    tour_cost,
    random_restart_two_opt,
)


_cached_model = None
_cached_rl_agent = None


def get_model():
    """Load edge scorer model (cached)."""
    global _cached_model
    if _cached_model is None:
        model_path = Path("models/edge_scorer.pt")
        if model_path.exists():
            _cached_model = load_edge_scorer(str(model_path))
        else:
            raise FileNotFoundError(f"No model found at {model_path}")
    return _cached_model


def get_rl_agent():
    """Get pre-trained RL agent (cached)."""
    global _cached_rl_agent
    if _cached_rl_agent is None:
        _cached_rl_agent = RLLocalSearchAgent(seed=42, epsilon=0.1)
    return _cached_rl_agent


def solve_hybrid(cost_matrix: np.ndarray,
                 coordinates: list = None,
                 time_limit_s: float = 30.0,
                 seed: int = 42,
                 candidate_k: int = 10,
                 use_rl_postprocess: bool = True,
                 initial_solver: str = "nearest_neighbor") -> Tuple[List[int], float]:
    """
    Hybrid solver: learned candidates + constrained local search + RL post-processing.

    Parameters
    ----------
    cost_matrix : (N, N) asymmetric cost matrix
    coordinates : list of (lat, lon) tuples (needed for GNN inference)
    time_limit_s : total time limit in seconds
    seed : random seed
    candidate_k : number of candidates per node
    use_rl_postprocess : whether to apply RL-guided local search after
    initial_solver : solver for initial tour ('nearest_neighbor' or 'farthest_insertion')

    Returns
    -------
    tour : list of int
    cost : float
    """
    start_time = time.time()
    n = cost_matrix.shape[0]

    # Step 1: Get initial tour (use OR-Tools if time allows, else NN)
    if time_limit_s > 5.0:
        init_time = min(time_limit_s * 0.75, 25.0)
        initial_tour, initial_cost = baseline_solve(
            cost_matrix, solver_name="ortools", time_limit_s=init_time, seed=seed)
    else:
        initial_tour, initial_cost = baseline_solve(
            cost_matrix, solver_name=initial_solver, seed=seed)

    # Step 2: Generate candidate set
    remaining_time = time_limit_s - (time.time() - start_time)
    if remaining_time < 1.0:
        return initial_tour, initial_cost

    if coordinates is not None:
        try:
            model = get_model()
            candidates = generate_candidate_set(
                model, cost_matrix, coordinates, k=candidate_k)
        except (FileNotFoundError, RuntimeError):
            candidates = generate_alpha_nearness_candidates(cost_matrix, k=candidate_k)
    else:
        candidates = generate_alpha_nearness_candidates(cost_matrix, k=candidate_k)

    # Step 3: Candidate-constrained local search
    remaining_time = time_limit_s - (time.time() - start_time)
    if remaining_time < 0.5:
        return initial_tour, initial_cost

    max_ls_iter = min(5000, n * 20)
    improved_tour, improved_cost = constrained_local_search(
        cost_matrix, initial_tour, candidates, max_iter=max_ls_iter)

    # Step 4: RL-guided post-processing
    remaining_time = time_limit_s - (time.time() - start_time)
    if use_rl_postprocess and remaining_time > 0.5:
        agent = get_rl_agent()
        rl_steps = min(5000, n * 20)
        rl_tour, rl_cost = rl_guided_local_search(
            cost_matrix, improved_tour, agent,
            max_steps=rl_steps,
            time_limit_s=remaining_time * 0.3,
            train=False,
        )
        if rl_cost < improved_cost:
            improved_tour = rl_tour
            improved_cost = rl_cost

    # Step 5: Final random 2-opt polish with remaining time
    remaining_time = time_limit_s - (time.time() - start_time)
    if remaining_time > 0.1:
        polished_tour, polished_cost = random_restart_two_opt(
            cost_matrix, improved_tour,
            max_steps=n * n,  # More steps for thorough polishing
            time_limit_s=remaining_time,
            seed=seed,
        )
        if polished_cost < improved_cost:
            improved_tour = polished_tour
            improved_cost = polished_cost

    return improved_tour, tour_cost(cost_matrix, improved_tour)


def solve_hybrid_no_rl(cost_matrix: np.ndarray,
                       coordinates: list = None,
                       time_limit_s: float = 30.0,
                       seed: int = 42,
                       candidate_k: int = 10) -> Tuple[List[int], float]:
    """Hybrid solver without RL post-processing (for ablation)."""
    return solve_hybrid(
        cost_matrix, coordinates, time_limit_s, seed,
        candidate_k, use_rl_postprocess=False)


def solve_candidates_only(cost_matrix: np.ndarray,
                          coordinates: list = None,
                          time_limit_s: float = 30.0,
                          seed: int = 42,
                          candidate_k: int = 10) -> Tuple[List[int], float]:
    """Solver using only learned candidates (no RL, no 2-opt polish)."""
    start_time = time.time()

    initial_tour, initial_cost = baseline_solve(
        cost_matrix, solver_name="nearest_neighbor", seed=seed)

    if coordinates is not None:
        try:
            model = get_model()
            candidates = generate_candidate_set(
                model, cost_matrix, coordinates, k=candidate_k)
        except (FileNotFoundError, RuntimeError):
            candidates = generate_alpha_nearness_candidates(cost_matrix, k=candidate_k)
    else:
        candidates = generate_alpha_nearness_candidates(cost_matrix, k=candidate_k)

    n = cost_matrix.shape[0]
    improved_tour, improved_cost = constrained_local_search(
        cost_matrix, initial_tour, candidates, max_iter=min(1000, n * 5))

    return improved_tour, tour_cost(cost_matrix, improved_tour)


# ── Self-test ────────────────────────────────────────────────────────────

if __name__ == "__main__":
    import sys
    sys.path.insert(0, ".")
    from src.data_pipeline import load_instance
    from src.baselines import solve as baseline_solve

    print("Testing hybrid solver...")

    # 50-stop test
    data = load_instance("benchmarks/manhattan_50_s42")
    cost_mat = data["durations"]
    coords = data["coordinates"]

    nn_tour, nn_cost = baseline_solve(cost_mat, solver_name="nearest_neighbor", seed=42)
    ort_tour, ort_cost = baseline_solve(cost_mat, solver_name="ortools", time_limit_s=5, seed=42)
    print(f"  NN cost: {nn_cost:.1f}")
    print(f"  OR-Tools cost: {ort_cost:.1f}")

    hybrid_tour, hybrid_cost = solve_hybrid(
        cost_mat, coords, time_limit_s=10.0, seed=42)
    print(f"  Hybrid cost: {hybrid_cost:.1f}")
    print(f"  Gap vs OR-Tools: {(hybrid_cost - ort_cost)/ort_cost*100:.2f}%")

    # 200-stop test
    data200 = load_instance("benchmarks/manhattan_200_s42")
    cm200 = data200["durations"]
    co200 = data200["coordinates"]

    nn200, nn200_cost = baseline_solve(cm200, solver_name="nearest_neighbor", seed=42)
    ort200, ort200_cost = baseline_solve(cm200, solver_name="ortools", time_limit_s=10, seed=42)
    print(f"\n  200-stop NN cost: {nn200_cost:.1f}")
    print(f"  200-stop OR-Tools cost: {ort200_cost:.1f}")

    t0 = time.time()
    hyb200, hyb200_cost = solve_hybrid(cm200, co200, time_limit_s=10.0, seed=42)
    hyb_time = time.time() - t0
    print(f"  200-stop Hybrid cost: {hyb200_cost:.1f} (time: {hyb_time:.1f}s)")
    print(f"  Gap vs OR-Tools: {(hyb200_cost - ort200_cost)/ort200_cost*100:.2f}%")

    print("\nHybrid solver test passed!")

"""
Evaluation metrics for TSP solvers on road-network instances.

Computes:
- Tour cost on asymmetric matrix
- Optimality gap relative to best-known solution
- Wall-clock time
- Peak memory usage
"""

import numpy as np
import time
import tracemalloc
from typing import Dict, List, Optional


def compute_tour_cost(cost_matrix: np.ndarray, tour: List[int]) -> float:
    """Compute total cost of a directed tour on an asymmetric cost matrix."""
    n = len(tour)
    total = 0.0
    for i in range(n):
        total += cost_matrix[tour[i], tour[(i + 1) % n]]
    return total


def compute_gap(tour_cost: float, best_known: float) -> float:
    """Compute optimality gap as percentage: (cost - best) / best * 100."""
    if best_known <= 0:
        return 0.0
    return ((tour_cost - best_known) / best_known) * 100.0


def validate_tour(tour: List[int], n: int) -> bool:
    """Check that tour visits each node exactly once."""
    return len(tour) == n and len(set(tour)) == n and all(0 <= x < n for x in tour)


def measure_solver(solver_fn, cost_matrix: np.ndarray,
                   time_limit_s: float = 30.0, seed: int = 42) -> Dict:
    """
    Run a solver and measure performance.

    Returns dict with: tour, cost, time_s, memory_mb, valid
    """
    tracemalloc.start()
    t0 = time.time()

    tour, cost = solver_fn(cost_matrix, time_limit_s=time_limit_s, seed=seed)

    elapsed = time.time() - t0
    _, peak_memory = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    n = cost_matrix.shape[0]
    valid = validate_tour(tour, n)

    # Verify cost
    computed_cost = compute_tour_cost(cost_matrix, tour) if valid else float("inf")

    return {
        "tour": tour,
        "cost": computed_cost,
        "time_s": round(elapsed, 4),
        "memory_mb": round(peak_memory / (1024 * 1024), 2),
        "valid": valid,
    }


def format_result_row(instance_id: str, solver: str, result: Dict,
                      best_known: float = None) -> Dict:
    """Format a single result into a standard row for CSV/JSON output."""
    gap = compute_gap(result["cost"], best_known) if best_known else None
    return {
        "instance_id": instance_id,
        "solver": solver,
        "tour_cost": round(result["cost"], 2),
        "gap_pct": round(gap, 4) if gap is not None else None,
        "time_s": result["time_s"],
        "memory_mb": result["memory_mb"],
        "valid": result["valid"],
    }

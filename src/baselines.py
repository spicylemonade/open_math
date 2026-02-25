"""
Baseline solver implementations for asymmetric TSP on road networks.

Provides a uniform solver interface with 4 solvers:
1. LKH-style solver (Python k-opt implementation for ATSP)
2. Google OR-Tools routing solver
3. Greedy nearest-neighbor heuristic for ATSP
4. Farthest-insertion heuristic (OSRM Trip equivalent)

All solvers accept an asymmetric cost matrix and return a tour
(ordered list of node indices) and total cost.
"""

import numpy as np
import time
from typing import Tuple, List, Optional


def tour_cost(cost_matrix: np.ndarray, tour: List[int]) -> float:
    """Compute total cost of a tour on an asymmetric cost matrix."""
    n = len(tour)
    total = 0.0
    for i in range(n):
        total += cost_matrix[tour[i], tour[(i + 1) % n]]
    return total


# ── Solver 1: Nearest Neighbor ──────────────────────────────────────────

def solve_nearest_neighbor(cost_matrix: np.ndarray, start: int = 0,
                           seed: int = 42) -> Tuple[List[int], float]:
    """
    Greedy nearest-neighbor heuristic for ATSP.

    Starting from `start`, greedily visits the nearest unvisited node.
    """
    n = cost_matrix.shape[0]
    visited = set()
    tour = [start]
    visited.add(start)

    current = start
    for _ in range(n - 1):
        # Find nearest unvisited
        costs = cost_matrix[current].copy()
        costs[list(visited)] = np.inf
        next_node = int(np.argmin(costs))
        tour.append(next_node)
        visited.add(next_node)
        current = next_node

    return tour, tour_cost(cost_matrix, tour)


# ── Solver 2: Farthest Insertion ─────────────────────────────────────────

def solve_farthest_insertion(cost_matrix: np.ndarray,
                             seed: int = 42) -> Tuple[List[int], float]:
    """
    Farthest-insertion heuristic for ATSP (similar to OSRM Trip API).

    Builds a tour by repeatedly inserting the farthest unvisited node
    at the position that minimizes the increase in tour cost.
    """
    n = cost_matrix.shape[0]
    rng = np.random.RandomState(seed)

    # Start with the two most distant nodes
    start = rng.randint(n)
    dists_from_start = cost_matrix[start] + cost_matrix[:, start]
    farthest = int(np.argmax(dists_from_start))
    if farthest == start:
        farthest = (start + 1) % n

    tour = [start, farthest]
    in_tour = set(tour)

    while len(tour) < n:
        # Find farthest node from current tour
        best_node = -1
        best_dist = -1
        for node in range(n):
            if node in in_tour:
                continue
            min_dist = min(cost_matrix[t, node] for t in tour)
            if min_dist > best_dist:
                best_dist = min_dist
                best_node = node

        # Find best insertion position
        best_pos = 0
        best_increase = np.inf
        for pos in range(len(tour)):
            i = tour[pos]
            j = tour[(pos + 1) % len(tour)]
            increase = (cost_matrix[i, best_node] +
                       cost_matrix[best_node, j] -
                       cost_matrix[i, j])
            if increase < best_increase:
                best_increase = increase
                best_pos = pos + 1

        tour.insert(best_pos, best_node)
        in_tour.add(best_node)

    return tour, tour_cost(cost_matrix, tour)


# ── Solver 3: OR-Tools ──────────────────────────────────────────────────

def solve_ortools(cost_matrix: np.ndarray, time_limit_s: float = 30.0,
                  seed: int = 42) -> Tuple[List[int], float]:
    """
    Google OR-Tools routing solver for ATSP.

    Uses guided local search metaheuristic with configurable time limit.
    """
    from ortools.constraint_solver import routing_enums_pb2, pywrapcp

    n = cost_matrix.shape[0]

    # Scale to integers (OR-Tools requires integer costs)
    scale = 1000
    int_matrix = (cost_matrix * scale).astype(np.int64)

    manager = pywrapcp.RoutingIndexManager(n, 1, 0)
    routing = pywrapcp.RoutingModel(manager)

    def distance_callback(from_index, to_index):
        from_node = manager.IndexToNode(from_index)
        to_node = manager.IndexToNode(to_index)
        return int(int_matrix[from_node, to_node])

    transit_callback_index = routing.RegisterTransitCallback(distance_callback)
    routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)

    search_parameters = pywrapcp.DefaultRoutingSearchParameters()
    search_parameters.first_solution_strategy = (
        routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC
    )
    search_parameters.local_search_metaheuristic = (
        routing_enums_pb2.LocalSearchMetaheuristic.GUIDED_LOCAL_SEARCH
    )
    search_parameters.time_limit.seconds = int(time_limit_s)

    solution = routing.SolveWithParameters(search_parameters)

    if solution is None:
        # Fallback to nearest neighbor
        return solve_nearest_neighbor(cost_matrix, seed=seed)

    # Extract tour
    tour = []
    index = routing.Start(0)
    while not routing.IsEnd(index):
        node = manager.IndexToNode(index)
        tour.append(node)
        index = solution.Value(routing.NextVar(index))

    return tour, tour_cost(cost_matrix, tour)


# ── Solver 4: Python k-opt (LKH-style) ──────────────────────────────────

def _two_opt_improve_atsp(cost_matrix: np.ndarray, tour: List[int],
                           max_iter: int = 1000) -> List[int]:
    """Apply 2-opt improvement moves for asymmetric TSP."""
    n = len(tour)
    improved = True
    iterations = 0

    while improved and iterations < max_iter:
        improved = False
        iterations += 1
        for i in range(n - 1):
            for j in range(i + 2, n):
                if j == n - 1 and i == 0:
                    continue  # Skip full reversal
                # For ATSP, we need to consider the directed costs
                # Try or-opt: move node j to after node i
                # Current: ... tour[i] -> tour[i+1] -> ... -> tour[j] -> tour[j+1] ...
                # New:     ... tour[i] -> tour[j] -> tour[i+1] -> ... -> tour[j-1] -> tour[j+1] ...
                i_node = tour[i]
                i1_node = tour[(i + 1) % n]
                j_node = tour[j]
                j1_node = tour[(j + 1) % n]

                # Cost of removing edges (i, i+1) and (j, j+1)
                old_cost = (cost_matrix[i_node, i1_node] +
                           cost_matrix[j_node, j1_node])

                # Cost of new edges (i, j) and reversed segment
                # For ATSP 2-opt, we reverse the segment and check directed costs
                new_segment = list(reversed(tour[i + 1:j + 1]))
                new_cost = cost_matrix[i_node, new_segment[0]]
                for k in range(len(new_segment) - 1):
                    new_cost += cost_matrix[new_segment[k], new_segment[k + 1]]
                new_cost += cost_matrix[new_segment[-1], j1_node]

                old_segment_cost = 0
                old_segment = tour[i + 1:j + 1]
                for k in range(len(old_segment) - 1):
                    old_segment_cost += cost_matrix[old_segment[k], old_segment[k + 1]]
                old_segment_cost += cost_matrix[i_node, old_segment[0]]
                old_segment_cost += cost_matrix[old_segment[-1], j1_node]

                if new_cost < old_segment_cost - 1e-10:
                    tour[i + 1:j + 1] = new_segment
                    improved = True

    return tour


def _or_opt_improve_atsp(cost_matrix: np.ndarray, tour: List[int],
                          max_iter: int = 500) -> List[int]:
    """Apply or-opt (relocate) improvement moves for asymmetric TSP."""
    n = len(tour)
    improved = True
    iterations = 0

    while improved and iterations < max_iter:
        improved = False
        iterations += 1
        for i in range(n):
            # Try moving tour[i] to a different position
            node = tour[i]
            prev_i = tour[(i - 1) % n]
            next_i = tour[(i + 1) % n]

            # Cost of removing node from current position
            removal_saving = (cost_matrix[prev_i, node] +
                             cost_matrix[node, next_i] -
                             cost_matrix[prev_i, next_i])

            # Try inserting after each other node
            for j in range(n):
                if j == i or j == (i - 1) % n:
                    continue
                j_node = tour[j]
                j1_node = tour[(j + 1) % n]
                if j1_node == node:
                    continue

                insertion_cost = (cost_matrix[j_node, node] +
                                 cost_matrix[node, j1_node] -
                                 cost_matrix[j_node, j1_node])

                if insertion_cost < removal_saving - 1e-10:
                    # Move is improving
                    tour_new = tour[:i] + tour[i + 1:]
                    # Find new position of j after removal
                    new_j = tour_new.index(j_node)
                    tour_new.insert(new_j + 1, node)
                    tour[:] = tour_new
                    improved = True
                    break
            if improved:
                break

    return tour


def solve_lkh_style(cost_matrix: np.ndarray, time_limit_s: float = 30.0,
                     seed: int = 42, n_restarts: int = 5) -> Tuple[List[int], float]:
    """
    LKH-style solver: multiple random restarts with 2-opt + or-opt improvement.

    For ATSP, uses directed versions of the improvement moves.
    """
    n = cost_matrix.shape[0]
    rng = np.random.RandomState(seed)
    start_time = time.time()

    best_tour = None
    best_cost = np.inf

    for restart in range(n_restarts):
        if time.time() - start_time > time_limit_s:
            break

        # Random starting tour for restarts > 0, nearest-neighbor for restart 0
        if restart == 0:
            initial_tour, _ = solve_nearest_neighbor(cost_matrix, start=0, seed=seed)
        else:
            initial_tour = list(rng.permutation(n))

        # Apply improvement moves
        current_tour = list(initial_tour)
        current_tour = _two_opt_improve_atsp(cost_matrix, current_tour,
                                              max_iter=min(500, n * 5))
        current_tour = _or_opt_improve_atsp(cost_matrix, current_tour,
                                             max_iter=min(300, n * 3))
        # Second round of 2-opt
        current_tour = _two_opt_improve_atsp(cost_matrix, current_tour,
                                              max_iter=min(300, n * 3))

        cost = tour_cost(cost_matrix, current_tour)
        if cost < best_cost:
            best_cost = cost
            best_tour = current_tour

    return best_tour, best_cost


# ── Unified Interface ────────────────────────────────────────────────────

SOLVERS = {
    "nearest_neighbor": solve_nearest_neighbor,
    "farthest_insertion": solve_farthest_insertion,
    "ortools": solve_ortools,
    "lkh_style": solve_lkh_style,
}


def solve(cost_matrix: np.ndarray, solver_name: str,
          time_limit_s: float = 30.0, seed: int = 42) -> Tuple[List[int], float]:
    """
    Unified solver interface.

    Parameters
    ----------
    cost_matrix : np.ndarray, NxN asymmetric cost matrix
    solver_name : str, one of 'nearest_neighbor', 'farthest_insertion', 'ortools', 'lkh_style'
    time_limit_s : float, time limit in seconds
    seed : int, random seed

    Returns
    -------
    tour : list of int, ordered node indices
    cost : float, total tour cost
    """
    if solver_name not in SOLVERS:
        raise ValueError(f"Unknown solver: {solver_name}. Available: {list(SOLVERS.keys())}")

    solver_fn = SOLVERS[solver_name]

    if solver_name in ("ortools", "lkh_style"):
        return solver_fn(cost_matrix, time_limit_s=time_limit_s, seed=seed)
    else:
        return solver_fn(cost_matrix, seed=seed)


def validate_tour(tour: List[int], n: int) -> bool:
    """Check that a tour is valid: visits each node exactly once."""
    return len(tour) == n and len(set(tour)) == n and all(0 <= x < n for x in tour)


# ── Self-test ────────────────────────────────────────────────────────────

if __name__ == "__main__":
    import sys
    sys.path.insert(0, ".")
    from src.data_pipeline import load_instance

    print("Testing all 4 solvers on manhattan_50_s42...")
    data = load_instance("benchmarks/manhattan_50_s42")
    cost_mat = data["durations"]
    n = cost_mat.shape[0]

    for name in SOLVERS:
        t0 = time.time()
        tour, cost = solve(cost_mat, name, time_limit_s=10, seed=42)
        elapsed = time.time() - t0
        valid = validate_tour(tour, n)
        print(f"  {name:25s}: cost={cost:12.1f}  valid={valid}  time={elapsed:.2f}s")
        assert valid, f"Invalid tour from {name}"

    print("\nAll solvers produce valid tours!")

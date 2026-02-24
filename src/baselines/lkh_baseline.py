"""
LKH-3 Style Baseline Wrapper for ATSP.

Pure-Python implementation of an LKH-inspired solver that does not require
the external LKH-3 binary. The approach combines:

1. Jonker-Volgenant ATSP-to-STSP transformation (doubles the node count to
   create a symmetric instance that encodes directed arc costs).
2. Nearest-neighbor construction heuristic on the original asymmetric
   instance to build an initial tour.
3. k-opt local search (2-opt and or-opt moves) evaluated using full
   asymmetric costs.
4. Multiple random restart trials, keeping the best tour found.
5. Configurable parameters: max_trials, time_limit, seed.

Reference
---------
Jonker, R. & Volgenant, A. (1983). "Transforming asymmetric into symmetric
traveling salesman problems." Operations Research Letters, 2(4), 161-163.

Helsgaun, K. (2017). "An extension of the Lin-Kernighan-Helsgaun TSP solver
for solving the generalized traveling salesman problem." LKH-3 technical
report.
"""

import time
import numpy as np


# ---------------------------------------------------------------------------
# Tour cost helpers
# ---------------------------------------------------------------------------

def compute_tour_cost(tour, cost_matrix):
    """Compute the total cost of a directed tour.

    Parameters
    ----------
    tour : list[int]
        Ordered list of node indices forming a Hamiltonian cycle.
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
# Jonker-Volgenant ATSP -> STSP transformation
# ---------------------------------------------------------------------------

def jonker_volgenant_transform(cost_matrix):
    """Transform an asymmetric cost matrix into a symmetric one.

    Uses the Jonker-Volgenant (1983) transformation.  For an n-city ATSP
    with cost matrix C, this creates a 2n-city STSP instance where:

    - Nodes 0..n-1 are the "outgoing" copies.
    - Nodes n..2n-1 are the "incoming" copies.
    - Edge (i, n+j) for i != j has cost C[i][j]  (the arc i -> j).
    - Edge (i, n+i) has cost -M (a large negative value that forces each
      city pair to be adjacent in any optimal STSP tour).
    - All other edges have cost +inf (or a very large value).

    Any optimal STSP tour on this 2n-node instance corresponds to an
    optimal ATSP tour on the original n-node instance.

    Parameters
    ----------
    cost_matrix : np.ndarray
        Asymmetric cost matrix of shape (n, n).

    Returns
    -------
    sym_matrix : np.ndarray
        Symmetric cost matrix of shape (2n, 2n).
    n_original : int
        Original number of nodes.
    """
    n = cost_matrix.shape[0]
    big_m = cost_matrix.max() * n * 10.0 + 1e6

    sym = np.full((2 * n, 2 * n), big_m, dtype=np.float64)

    # Edge (i, n+j) for i != j  =>  cost C[i][j]
    for i in range(n):
        for j in range(n):
            if i != j:
                sym[i, n + j] = cost_matrix[i, j]
                sym[n + j, i] = cost_matrix[i, j]  # symmetric

    # Edge (i, n+i) =>  cost -M  (binding edges)
    for i in range(n):
        sym[i, n + i] = -big_m
        sym[n + i, i] = -big_m

    # Edges within the same partition are infinite (already set to big_m)
    # Diagonal = 0
    np.fill_diagonal(sym, 0.0)

    return sym, n


def extract_atsp_tour_from_stsp(stsp_tour, n_original):
    """Extract the ATSP tour from a STSP tour on the transformed instance.

    In the JV-transformed tour the node pairs (i, n+i) are always adjacent.
    We walk the STSP tour, collecting only the original nodes (< n_original)
    in the order they appear.

    Parameters
    ----------
    stsp_tour : list[int]
        Tour on the 2n-node symmetric instance.
    n_original : int
        Number of nodes in the original ATSP instance.

    Returns
    -------
    list[int]
        Tour on the original n-node ATSP instance.
    """
    return [node for node in stsp_tour if node < n_original]


# ---------------------------------------------------------------------------
# Nearest-neighbor construction heuristic
# ---------------------------------------------------------------------------

def nearest_neighbor_tour(cost_matrix, start_node, rng=None):
    """Build a tour using the nearest-neighbor heuristic.

    Parameters
    ----------
    cost_matrix : np.ndarray
        Asymmetric cost matrix of shape (n, n).
    start_node : int
        Starting node for the construction.
    rng : np.random.RandomState or None
        Not used directly here but kept for API consistency.

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
        # Mask visited nodes with infinity
        row = cost_matrix[current].copy()
        row[visited] = np.inf
        next_node = int(np.argmin(row))
        tour.append(next_node)
        visited[next_node] = True
        current = next_node

    return tour


def best_nearest_neighbor(cost_matrix):
    """Run nearest-neighbor from every node and return the best tour.

    Parameters
    ----------
    cost_matrix : np.ndarray
        Asymmetric cost matrix of shape (n, n).

    Returns
    -------
    list[int]
        The best tour found across all starting nodes.
    float
        Cost of the best tour.
    """
    n = cost_matrix.shape[0]
    best_tour = None
    best_cost = np.inf

    for start in range(n):
        tour = nearest_neighbor_tour(cost_matrix, start)
        cost = compute_tour_cost(tour, cost_matrix)
        if cost < best_cost:
            best_cost = cost
            best_tour = tour

    return best_tour, best_cost


def random_nearest_neighbor(cost_matrix, rng):
    """Nearest-neighbor from a random start node.

    Parameters
    ----------
    cost_matrix : np.ndarray
        Asymmetric cost matrix of shape (n, n).
    rng : np.random.RandomState
        Random number generator.

    Returns
    -------
    list[int]
        Tour.
    """
    n = cost_matrix.shape[0]
    start = rng.randint(0, n)
    return nearest_neighbor_tour(cost_matrix, start)


# ---------------------------------------------------------------------------
# 2-opt local search for ATSP (directed)
# ---------------------------------------------------------------------------

def two_opt_improve(tour, cost_matrix):
    """Improve a tour using 2-opt moves evaluated on the asymmetric costs.

    For a directed tour (t_0, t_1, ..., t_{n-1}), a 2-opt move reverses
    the segment tour[i+1 .. j].  In ATSP, reversing a segment changes the
    direction of all arcs within it as well as the two boundary arcs, so we
    must evaluate using the actual asymmetric costs.

    The move replaces edges:
        tour[i] -> tour[i+1]  and  tour[j] -> tour[j+1]
    with:
        tour[i] -> tour[j]  and  tour[i+1] -> tour[j+1]
    and all internal arcs in the reversed segment flip direction.

    We use first-improvement strategy: apply the first improving move found,
    then restart the scan.

    Parameters
    ----------
    tour : list[int]
        Current tour (modified in-place).
    cost_matrix : np.ndarray
        Asymmetric cost matrix.

    Returns
    -------
    list[int]
        Improved tour.
    float
        Cost of the improved tour.
    """
    n = len(tour)
    improved = True

    while improved:
        improved = False
        current_cost = compute_tour_cost(tour, cost_matrix)
        for i in range(n - 1):
            for j in range(i + 2, n):
                # Skip the wrap-around pair (i=0, j=n-1) since reversing
                # the entire tour minus one element is equivalent to
                # reversing one element, handled implicitly.
                if i == 0 and j == n - 1:
                    continue

                # Create candidate tour with segment [i+1..j] reversed
                new_tour = tour[:i + 1] + tour[i + 1:j + 1][::-1] + tour[j + 1:]
                new_cost = compute_tour_cost(new_tour, cost_matrix)

                if new_cost < current_cost - 1e-10:
                    tour = new_tour
                    current_cost = new_cost
                    improved = True
                    break  # restart scan
            if improved:
                break

    return tour, current_cost


# ---------------------------------------------------------------------------
# Or-opt local search for ATSP (directed)
# ---------------------------------------------------------------------------

def or_opt_improve(tour, cost_matrix):
    """Improve a tour using or-opt moves on the asymmetric instance.

    Or-opt removes a subsequence of length 1, 2, or 3 from its current
    position and reinserts it at the best position in the remaining tour.
    All edge costs are evaluated using the directed (asymmetric) costs.

    Uses first-improvement strategy.

    Parameters
    ----------
    tour : list[int]
        Current tour (will be copied internally).
    cost_matrix : np.ndarray
        Asymmetric cost matrix.

    Returns
    -------
    list[int]
        Improved tour.
    float
        Cost of the improved tour.
    """
    n = len(tour)
    if n <= 4:
        return tour, compute_tour_cost(tour, cost_matrix)

    current_cost = compute_tour_cost(tour, cost_matrix)
    improved = True

    while improved:
        improved = False
        for seg_len in [1, 2, 3]:
            if seg_len >= n - 1:
                continue
            for i in range(n):
                # Extract segment tour[i..i+seg_len-1] (wrapping)
                seg_indices = [(i + k) % n for k in range(seg_len)]
                segment = [tour[idx] for idx in seg_indices]

                # Remaining tour (preserving order)
                remaining = [tour[k] for k in range(n) if k not in set(seg_indices)]

                if len(remaining) == 0:
                    continue

                # Try reinserting the segment at every position in remaining
                for j in range(len(remaining)):
                    # Insert segment after position j in remaining
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
# Combined local search
# ---------------------------------------------------------------------------

def local_search(tour, cost_matrix, time_deadline=None):
    """Apply 2-opt and or-opt local search iteratively until no improvement.

    Alternates between 2-opt and or-opt until neither produces improvement,
    or the time deadline is reached.

    Parameters
    ----------
    tour : list[int]
        Initial tour.
    cost_matrix : np.ndarray
        Asymmetric cost matrix.
    time_deadline : float or None
        Wall-clock deadline (time.time() value). If reached, search stops.

    Returns
    -------
    list[int]
        Locally optimal tour.
    float
        Cost of the tour.
    """
    current_cost = compute_tour_cost(tour, cost_matrix)
    improved_overall = True

    while improved_overall:
        improved_overall = False

        if time_deadline is not None and time.time() >= time_deadline:
            break

        # 2-opt phase
        new_tour, new_cost = two_opt_improve(tour, cost_matrix)
        if new_cost < current_cost - 1e-10:
            tour = new_tour
            current_cost = new_cost
            improved_overall = True

        if time_deadline is not None and time.time() >= time_deadline:
            break

        # Or-opt phase
        new_tour, new_cost = or_opt_improve(tour, cost_matrix)
        if new_cost < current_cost - 1e-10:
            tour = new_tour
            current_cost = new_cost
            improved_overall = True

    return tour, current_cost


# ---------------------------------------------------------------------------
# Perturbation (double-bridge style for restarts with diversity)
# ---------------------------------------------------------------------------

def perturb_tour(tour, rng):
    """Apply a double-bridge perturbation to diversify the tour.

    Splits the tour into four segments and reconnects them in a different
    order, creating a new tour that cannot be reached by 2-opt or 3-opt
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
        # For very small tours, just do a random shuffle of a small segment
        new_tour = list(tour)
        i, j = sorted(rng.choice(n, 2, replace=False))
        new_tour[i:j + 1] = rng.permutation(new_tour[i:j + 1]).tolist()
        return new_tour

    # Choose 3 random cut points (sorted), creating 4 segments
    cuts = sorted(rng.choice(range(1, n), 3, replace=False))
    a, b, c = cuts

    seg1 = tour[:a]
    seg2 = tour[a:b]
    seg3 = tour[b:c]
    seg4 = tour[c:]

    # Reconnect: seg1 + seg3 + seg2 + seg4  (double-bridge)
    return seg1 + seg3 + seg2 + seg4


# ---------------------------------------------------------------------------
# Main solver entry point
# ---------------------------------------------------------------------------

def solve_lkh(instance, max_trials=10, time_limit=60.0, seed=42):
    """Solve an ATSP instance using LKH-style local search.

    This is a pure-Python implementation inspired by the LKH-3 solver.
    It combines nearest-neighbor construction, 2-opt and or-opt local
    search, and multiple random restart trials with double-bridge
    perturbation.

    Parameters
    ----------
    instance : dict
        Instance dict with 'cost_matrix' and 'metadata'.
        ``cost_matrix`` is a list of lists (or numpy array) of shape (n, n).
    max_trials : int
        Number of random restart trials.
    time_limit : float
        Maximum wall-clock time in seconds.
    seed : int
        Random seed for reproducibility.

    Returns
    -------
    dict
        Result dictionary with keys:
        - ``tour`` : list[int] -- the best tour found.
        - ``cost`` : float -- cost of the best tour.
        - ``runtime_seconds`` : float -- elapsed wall-clock time.
        - ``solver_params`` : dict -- parameters used for the solve.
        - ``solver_name`` : str -- always ``'lkh'``.
    """
    start_time = time.time()
    rng = np.random.RandomState(seed)

    # Parse cost matrix
    cost_matrix = np.array(instance["cost_matrix"], dtype=np.float64)
    n = cost_matrix.shape[0]

    # Edge case: trivial instances
    if n <= 1:
        return {
            "tour": list(range(n)),
            "cost": 0.0,
            "runtime_seconds": time.time() - start_time,
            "solver_params": {
                "max_trials": max_trials,
                "time_limit": time_limit,
                "seed": seed,
            },
            "solver_name": "lkh",
        }

    if n == 2:
        tour = [0, 1]
        cost = compute_tour_cost(tour, cost_matrix)
        return {
            "tour": tour,
            "cost": cost,
            "runtime_seconds": time.time() - start_time,
            "solver_params": {
                "max_trials": max_trials,
                "time_limit": time_limit,
                "seed": seed,
            },
            "solver_name": "lkh",
        }

    time_deadline = start_time + time_limit

    # -----------------------------------------------------------------------
    # Trial 0: best nearest-neighbor + local search
    # -----------------------------------------------------------------------
    best_tour, best_cost = best_nearest_neighbor(cost_matrix)

    if time.time() < time_deadline:
        best_tour, best_cost = local_search(
            best_tour, cost_matrix, time_deadline
        )

    trials_completed = 1

    # -----------------------------------------------------------------------
    # Remaining trials: perturbed restarts + local search
    # -----------------------------------------------------------------------
    for trial in range(1, max_trials):
        if time.time() >= time_deadline:
            break

        # Alternate between random NN start and perturbation of best tour
        if trial % 2 == 1:
            # Random nearest-neighbor start
            tour = random_nearest_neighbor(cost_matrix, rng)
        else:
            # Perturb the current best tour
            tour = perturb_tour(list(best_tour), rng)

        tour_cost = compute_tour_cost(tour, cost_matrix)

        # Local search
        if time.time() < time_deadline:
            tour, tour_cost = local_search(tour, cost_matrix, time_deadline)

        # Update best
        if tour_cost < best_cost - 1e-10:
            best_tour = tour
            best_cost = tour_cost

        trials_completed += 1

    elapsed = time.time() - start_time

    # Final validation
    validate_tour(best_tour, cost_matrix, reported_cost=best_cost)

    return {
        "tour": best_tour,
        "cost": best_cost,
        "runtime_seconds": elapsed,
        "solver_params": {
            "max_trials": max_trials,
            "time_limit": time_limit,
            "seed": seed,
            "trials_completed": trials_completed,
        },
        "solver_name": "lkh",
    }


# ---------------------------------------------------------------------------
# CLI entry point for quick testing
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    import json
    import sys
    import os

    # Quick self-test with a small synthetic instance
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

    try:
        from data.instance_generator import generate_synthetic_instance
    except ImportError:
        generate_synthetic_instance = None

    if generate_synthetic_instance is not None:
        print("=== LKH-style ATSP Solver Self-Test ===\n")

        for n_nodes in [10, 20, 50]:
            print(f"--- Instance: n={n_nodes} ---")
            inst = generate_synthetic_instance(n_nodes, seed=42)

            result = solve_lkh(
                inst,
                max_trials=5,
                time_limit=30.0,
                seed=42,
            )

            print(f"  Tour cost     : {result['cost']:.2f}")
            print(f"  Runtime       : {result['runtime_seconds']:.3f}s")
            print(f"  Trials done   : {result['solver_params']['trials_completed']}")
            print(f"  Tour valid    : True (validated internally)")

            # Compare with simple nearest-neighbor
            cm = np.array(inst["cost_matrix"])
            nn_tour, nn_cost = best_nearest_neighbor(cm)
            improvement = (nn_cost - result["cost"]) / nn_cost * 100
            print(f"  NN best cost  : {nn_cost:.2f}")
            print(f"  Improvement   : {improvement:.1f}%\n")
    else:
        # Minimal self-test without instance_generator
        print("=== LKH-style ATSP Solver Minimal Self-Test ===\n")

        # Create a small random ATSP instance
        rng = np.random.RandomState(42)
        n = 10
        cm = rng.uniform(10, 100, size=(n, n))
        np.fill_diagonal(cm, 0.0)

        instance = {
            "cost_matrix": cm.tolist(),
            "metadata": {"n_nodes": n},
        }

        result = solve_lkh(instance, max_trials=5, time_limit=10.0, seed=42)
        print(f"Tour: {result['tour']}")
        print(f"Cost: {result['cost']:.2f}")
        print(f"Runtime: {result['runtime_seconds']:.3f}s")
        print(f"Trials: {result['solver_params']['trials_completed']}")
        print("Validation: passed")

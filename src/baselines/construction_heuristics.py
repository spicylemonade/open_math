"""
Construction heuristics for the Asymmetric Travelling Salesman Problem (ATSP).

Implements three classical construction heuristics:
1. Nearest Neighbor (best of N starts)
2. Greedy Edge Insertion
3. Savings Algorithm (Clarke-Wright)

All solvers accept an instance dict (as produced by src/data/instance_generator.py)
with keys 'metadata', 'coordinates', and 'cost_matrix', and return a result dict:
    {
        'tour': list[int],       # ordered sequence of node indices
        'cost': float,           # total tour cost
        'runtime_seconds': float,
        'solver_params': dict,
        'solver_name': str,
    }
"""

import time

import numpy as np


# ---------------------------------------------------------------------------
# Helper utilities
# ---------------------------------------------------------------------------

def compute_tour_cost(tour, cost_matrix):
    """Compute the total cost of a tour given an asymmetric cost matrix.

    Parameters
    ----------
    tour : list[int]
        Ordered sequence of node indices forming a Hamiltonian cycle.
    cost_matrix : array-like
        Square matrix where cost_matrix[i][j] is the cost of traveling from
        node *i* to node *j*.

    Returns
    -------
    float
        Total tour cost (sum of consecutive edge costs, including the
        closing edge from the last node back to the first).
    """
    cost = 0.0
    n = len(tour)
    for i in range(n):
        cost += cost_matrix[tour[i]][tour[(i + 1) % n]]
    return cost


def _prepare_cost_matrix(instance):
    """Extract the cost matrix from an instance dict as a NumPy array."""
    return np.asarray(instance["cost_matrix"], dtype=np.float64)


# ---------------------------------------------------------------------------
# 1. Nearest Neighbor (best of N starts)
# ---------------------------------------------------------------------------

def solve_nearest_neighbor(instance, seed=42):
    """Nearest-neighbor heuristic trying every possible starting node.

    For each starting node, the heuristic greedily visits the nearest
    unvisited node until all nodes have been visited.  The best tour
    (lowest total cost) across all *N* starting nodes is returned.

    Parameters
    ----------
    instance : dict
        ATSP instance with keys ``metadata``, ``coordinates``,
        ``cost_matrix``.
    seed : int
        Random seed (unused by this deterministic heuristic, kept for
        interface consistency).

    Returns
    -------
    dict
        Result dictionary in the standard format.
    """
    t_start = time.perf_counter()
    C = _prepare_cost_matrix(instance)
    n = C.shape[0]

    # Edge cases
    if n == 1:
        elapsed = time.perf_counter() - t_start
        return {
            "tour": [0],
            "cost": 0.0,
            "runtime_seconds": elapsed,
            "solver_params": {"seed": seed},
            "solver_name": "nearest_neighbor",
        }
    if n == 2:
        tour = [0, 1]
        cost = compute_tour_cost(tour, C)
        elapsed = time.perf_counter() - t_start
        return {
            "tour": tour,
            "cost": cost,
            "runtime_seconds": elapsed,
            "solver_params": {"seed": seed},
            "solver_name": "nearest_neighbor",
        }

    best_tour = None
    best_cost = np.inf

    for start in range(n):
        visited = np.zeros(n, dtype=bool)
        tour = [start]
        visited[start] = True

        for _ in range(n - 1):
            current = tour[-1]
            # Mask already-visited nodes with infinity so they are never chosen
            row = C[current].copy()
            row[visited] = np.inf
            nearest = int(np.argmin(row))
            tour.append(nearest)
            visited[nearest] = True

        cost = compute_tour_cost(tour, C)
        if cost < best_cost:
            best_cost = cost
            best_tour = tour

    elapsed = time.perf_counter() - t_start
    return {
        "tour": best_tour,
        "cost": best_cost,
        "runtime_seconds": elapsed,
        "solver_params": {"seed": seed},
        "solver_name": "nearest_neighbor",
    }


# ---------------------------------------------------------------------------
# 2. Greedy Edge Insertion
# ---------------------------------------------------------------------------

def solve_greedy(instance, seed=42):
    """Greedy edge-insertion heuristic for ATSP.

    Algorithm
    ---------
    1. Enumerate all directed edges (i, j) with i != j and sort by cost
       (ascending).
    2. Iterate through the sorted edges.  Add edge (i, j) to the partial
       solution if:
       - Node *i* has no outgoing edge yet (out-degree < 1).
       - Node *j* has no incoming edge yet (in-degree < 1).
       - Adding the edge does not create a cycle of length < N
         (premature sub-tour).
    3. Continue until exactly *N* edges have been added (forming a
       Hamiltonian cycle).

    Parameters
    ----------
    instance : dict
        ATSP instance.
    seed : int
        Random seed (unused; deterministic heuristic).

    Returns
    -------
    dict
        Result dictionary in the standard format.
    """
    t_start = time.perf_counter()
    C = _prepare_cost_matrix(instance)
    n = C.shape[0]

    # Edge cases
    if n == 1:
        elapsed = time.perf_counter() - t_start
        return {
            "tour": [0],
            "cost": 0.0,
            "runtime_seconds": elapsed,
            "solver_params": {"seed": seed},
            "solver_name": "greedy_edge_insertion",
        }
    if n == 2:
        tour = [0, 1]
        cost = compute_tour_cost(tour, C)
        elapsed = time.perf_counter() - t_start
        return {
            "tour": tour,
            "cost": cost,
            "runtime_seconds": elapsed,
            "solver_params": {"seed": seed},
            "solver_name": "greedy_edge_insertion",
        }

    # Build sorted list of all directed edges (i, j) with cost
    edges = []
    for i in range(n):
        for j in range(n):
            if i != j:
                edges.append((C[i, j], i, j))
    edges.sort(key=lambda x: x[0])

    # Data structures for tracking partial chains
    out_edge = [None] * n   # out_edge[i] = j  means edge i->j selected
    in_edge = [None] * n    # in_edge[j] = i   means edge i->j selected

    # Union-Find to detect premature sub-tours.
    # We track the *successor chain* endpoint reachable from each node.
    # successor[i]: the last node reachable following selected out-edges
    #               starting from i.
    # predecessor[i]: the first node reachable following selected in-edges
    #                 starting from i.
    # These let us quickly check whether adding edge (i, j) would close a
    # cycle shorter than N.
    successor = list(range(n))    # end of the chain starting at i
    predecessor = list(range(n))  # start of the chain ending at i

    num_edges = 0

    for cost_ij, i, j in edges:
        if num_edges == n:
            break

        # Degree constraints
        if out_edge[i] is not None:
            continue
        if in_edge[j] is not None:
            continue

        # Sub-tour check: adding i->j would create a cycle if j's chain
        # eventually leads back to i, i.e. successor[j] == i.
        # That is only acceptable when this would be the N-th edge
        # (completing the Hamiltonian cycle).
        if successor[j] == i and num_edges < n - 1:
            continue

        # Accept edge
        out_edge[i] = j
        in_edge[j] = i
        num_edges += 1

        # Update chain endpoints.
        # Before this edge: the chain ending at i has start predecessor[i],
        # and the chain starting at j has end successor[j].
        # Merging via i->j: the combined chain has start predecessor[i]
        # and end successor[j].
        chain_start = predecessor[i]
        chain_end = successor[j]
        successor[chain_start] = chain_end
        predecessor[chain_end] = chain_start

    # Reconstruct tour from the edge set, starting at node 0
    tour = [0]
    current = 0
    for _ in range(n - 1):
        current = out_edge[current]
        tour.append(current)

    cost = compute_tour_cost(tour, C)
    elapsed = time.perf_counter() - t_start

    return {
        "tour": tour,
        "cost": cost,
        "runtime_seconds": elapsed,
        "solver_params": {"seed": seed},
        "solver_name": "greedy_edge_insertion",
    }


# ---------------------------------------------------------------------------
# 3. Savings Algorithm (Clarke-Wright)
# ---------------------------------------------------------------------------

def solve_savings(instance, seed=42):
    """Clarke-Wright savings algorithm adapted for single-vehicle ATSP.

    Algorithm
    ---------
    Starting configuration: a "star" of routes from the depot (node 0)
    to each customer and back, i.e. routes 0 -> i -> 0 for every
    customer *i*.

    Savings are computed for every pair of customers (i, j):
        s(i, j) = c(i, 0) + c(0, j) - c(i, j)

    Iterating through savings in descending order, two routes are merged
    by replacing edges i->0 and 0->j with i->j if:
      - *i* is currently the last customer in its route (before returning
        to the depot).
      - *j* is currently the first customer in its route (right after
        leaving the depot).
      - *i* and *j* are not already in the same route (would create a
        premature sub-tour).

    The process continues until all customers are in a single tour,
    or no more feasible merges exist.

    Parameters
    ----------
    instance : dict
        ATSP instance.
    seed : int
        Random seed (unused; deterministic heuristic).

    Returns
    -------
    dict
        Result dictionary in the standard format.
    """
    t_start = time.perf_counter()
    C = _prepare_cost_matrix(instance)
    n = C.shape[0]

    # Edge cases
    if n == 1:
        elapsed = time.perf_counter() - t_start
        return {
            "tour": [0],
            "cost": 0.0,
            "runtime_seconds": elapsed,
            "solver_params": {"seed": seed},
            "solver_name": "savings_clarke_wright",
        }
    if n == 2:
        tour = [0, 1]
        cost = compute_tour_cost(tour, C)
        elapsed = time.perf_counter() - t_start
        return {
            "tour": tour,
            "cost": cost,
            "runtime_seconds": elapsed,
            "solver_params": {"seed": seed},
            "solver_name": "savings_clarke_wright",
        }

    depot = 0
    customers = list(range(1, n))

    # Compute savings for all customer pairs
    savings = []
    for i in customers:
        for j in customers:
            if i != j:
                s = C[i, depot] + C[depot, j] - C[i, j]
                savings.append((s, i, j))
    savings.sort(key=lambda x: -x[0])  # descending

    # Each customer starts in its own route: depot -> customer -> depot.
    # We represent routes as doubly-linked lists through dicts:
    #   route_succ[i]: the next customer after i in its route (or None)
    #   route_pred[i]: the previous customer before i in its route (or None)
    # The first customer in a route has route_pred[i] == None,
    # the last has route_succ[i] == None.
    route_succ = {i: None for i in customers}
    route_pred = {i: None for i in customers}

    # Route identity: route_id[i] = id of the route containing customer i.
    # Initially each customer is its own route.
    route_id = {i: i for i in customers}

    # For quick lookup, track the first and last customer in each route.
    route_first = {i: i for i in customers}  # route_id -> first customer
    route_last = {i: i for i in customers}   # route_id -> last customer

    for s_val, i, j in savings:
        if s_val <= 0:
            break

        # i must be the last customer in its route
        if route_succ[i] is not None:
            continue
        # j must be the first customer in its route
        if route_pred[j] is not None:
            continue

        ri = route_id[i]
        rj = route_id[j]

        # Must be different routes (avoid premature sub-tours)
        if ri == rj:
            continue

        # Merge: link i -> j
        route_succ[i] = j
        route_pred[j] = i

        # Update route identity for all nodes in route rj -> set to ri
        node = j
        while node is not None:
            route_id[node] = ri
            node = route_succ[node]

        # Update first/last tracking
        # The merged route starts at route_first[ri] and ends at route_last[rj]
        route_last[ri] = route_last[rj]

        # Clean up the consumed route id
        if rj in route_first:
            del route_first[rj]
        if rj in route_last:
            del route_last[rj]

    # Reconstruct the tour.  There may be multiple disconnected route
    # fragments if some merges were infeasible.  Collect all fragments
    # and connect them through the depot in arbitrary order.
    fragments = []
    visited_customers = set()

    for rid, first_cust in route_first.items():
        fragment = []
        node = first_cust
        while node is not None:
            fragment.append(node)
            visited_customers.add(node)
            node = route_succ[node]
        fragments.append(fragment)

    # Build tour: depot, then concatenated fragments
    tour = [depot]
    for fragment in fragments:
        tour.extend(fragment)

    cost = compute_tour_cost(tour, C)
    elapsed = time.perf_counter() - t_start

    return {
        "tour": tour,
        "cost": cost,
        "runtime_seconds": elapsed,
        "solver_params": {"seed": seed},
        "solver_name": "savings_clarke_wright",
    }

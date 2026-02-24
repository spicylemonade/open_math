"""
Google OR-Tools Routing Baseline for Asymmetric TSP.

Uses the OR-Tools constraint programming routing solver with guided local
search to find high-quality solutions to ATSP instances defined by
asymmetric cost matrices (e.g., derived from real road-network travel times).
"""

import time
import numpy as np

from ortools.constraint_solver import routing_enums_pb2, pywrapcp


def validate_tour(tour, n):
    """Validate that a tour is a valid Hamiltonian cycle.

    Parameters
    ----------
    tour : list[int]
        Ordered list of node indices representing the tour.
    n : int
        Expected number of nodes.

    Returns
    -------
    bool
        True if the tour is valid.

    Raises
    ------
    ValueError
        If the tour is invalid with a description of the problem.
    """
    if len(tour) != n:
        raise ValueError(
            f"Tour has {len(tour)} nodes, expected {n}"
        )
    if set(tour) != set(range(n)):
        missing = set(range(n)) - set(tour)
        extra = set(tour) - set(range(n))
        raise ValueError(
            f"Tour does not visit all nodes exactly once. "
            f"Missing: {missing}, Extra/duplicate: {extra}"
        )
    return True


def solve_ortools(instance, time_limit=60.0, seed=42):
    """Solve an ATSP instance using Google OR-Tools routing solver.

    Parameters
    ----------
    instance : dict
        Instance dict with 'cost_matrix' and 'metadata'.
    time_limit : float
        Maximum wall-clock time in seconds.
    seed : int
        Random seed (unused by OR-Tools but kept for interface consistency).

    Returns
    -------
    dict
        {'tour': list[int], 'cost': float, 'runtime_seconds': float,
         'solver_params': dict, 'solver_name': 'ortools'}

    Raises
    ------
    RuntimeError
        If OR-Tools fails to find a feasible solution within the time limit.
    """
    cost_matrix = np.array(instance["cost_matrix"], dtype=float)
    n = cost_matrix.shape[0]

    # Scale float costs to integers (OR-Tools requires integer costs).
    # Multiply by 100 and round to preserve two decimal places of precision.
    scale_factor = 100
    int_matrix = np.round(cost_matrix * scale_factor).astype(np.int64)

    # Create the routing index manager: one vehicle, depot at node 0.
    manager = pywrapcp.RoutingIndexManager(n, 1, 0)

    # Create the routing model.
    routing = pywrapcp.RoutingModel(manager)

    # Define the transit callback using the integer-scaled cost matrix.
    def transit_callback(from_index, to_index):
        from_node = manager.IndexToNode(from_index)
        to_node = manager.IndexToNode(to_index)
        return int(int_matrix[from_node][to_node])

    transit_callback_index = routing.RegisterTransitCallback(transit_callback)

    # Set the cost evaluator for all vehicles.
    routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)

    # Configure search parameters.
    search_parameters = pywrapcp.DefaultRoutingSearchParameters()

    # First solution strategy: build an initial tour using cheapest arc.
    search_parameters.first_solution_strategy = (
        routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC
    )

    # Local search metaheuristic: guided local search.
    search_parameters.local_search_metaheuristic = (
        routing_enums_pb2.LocalSearchMetaheuristic.GUIDED_LOCAL_SEARCH
    )

    # Set the time limit (in seconds, as an integer for the protobuf field).
    search_parameters.time_limit.FromSeconds(int(max(1, time_limit)))

    # Solve.
    start_time = time.perf_counter()
    solution = routing.SolveWithParameters(search_parameters)
    elapsed = time.perf_counter() - start_time

    if solution is None:
        raise RuntimeError(
            f"OR-Tools found no feasible solution within {time_limit}s "
            f"(status: {routing.status()})"
        )

    # Extract the tour from the solution.
    tour = []
    index = routing.Start(0)
    while not routing.IsEnd(index):
        node = manager.IndexToNode(index)
        tour.append(node)
        index = solution.Value(routing.NextVar(index))

    # Validate the tour.
    validate_tour(tour, n)

    # Compute actual cost using the original float cost matrix (not scaled).
    cost = 0.0
    for i in range(len(tour)):
        from_node = tour[i]
        to_node = tour[(i + 1) % n]
        cost += cost_matrix[from_node][to_node]

    solver_params = {
        "first_solution_strategy": "PATH_CHEAPEST_ARC",
        "local_search_metaheuristic": "GUIDED_LOCAL_SEARCH",
        "time_limit_seconds": time_limit,
        "cost_scale_factor": scale_factor,
        "seed": seed,
    }

    return {
        "tour": tour,
        "cost": float(cost),
        "runtime_seconds": float(elapsed),
        "solver_params": solver_params,
        "solver_name": "ortools",
    }


if __name__ == "__main__":
    # Quick smoke test with a small synthetic instance.
    n = 5
    rng = np.random.RandomState(42)
    matrix = rng.uniform(10, 100, (n, n))
    np.fill_diagonal(matrix, 0.0)

    instance = {
        "metadata": {"n_nodes": n, "city": "test", "source": "synthetic"},
        "cost_matrix": matrix.tolist(),
    }

    result = solve_ortools(instance, time_limit=5.0)
    print(f"Tour: {result['tour']}")
    print(f"Cost: {result['cost']:.2f}")
    print(f"Runtime: {result['runtime_seconds']:.3f}s")
    validate_tour(result["tour"], n)
    print("Tour is valid.")

"""
Ensemble solver for the Asymmetric Travelling Salesman Problem (ATSP).

Combines multiple solver outputs and optionally applies a simplified
EAX-style crossover between the best tours to search for improvements.

Strategy
--------
1. Split the total time budget evenly among all available solvers.
2. Run each solver and collect (tour, cost) pairs.
3. Select the best tour by cost.
4. If *use_crossover* is enabled, attempt a simplified EAX-style crossover
   between the two best tours:
   - Identify edges unique to each tour (symmetric-difference edges).
   - Build AB-cycles by alternating edges from tour A and tour B.
   - Select a random AB-cycle, apply it as a perturbation to tour A.
   - Accept the resulting tour if it improves cost.
5. Return the overall best tour found.

Available solvers are imported with ``try / except`` so that missing
dependencies (e.g. OR-Tools, PyTorch) do not prevent the module from
loading -- unavailable solvers are simply skipped at runtime.
"""

import time
import logging
from typing import Dict, List, Optional, Tuple

import numpy as np

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Solver registry -- each entry maps a short name to a (module_path, func)
# pair.  Imports are deferred and wrapped in try/except so that a missing
# dependency only disables that one solver.
# ---------------------------------------------------------------------------

_SOLVER_FACTORIES: Dict[str, object] = {}


def _register_solvers() -> None:
    """Populate ``_SOLVER_FACTORIES`` with all solver callables that can be
    imported successfully."""

    global _SOLVER_FACTORIES  # noqa: PLW0603

    if _SOLVER_FACTORIES:
        return  # already populated

    # -- Construction heuristics -------------------------------------------
    try:
        from src.baselines.construction_heuristics import solve_nearest_neighbor
        _SOLVER_FACTORIES["nearest_neighbor"] = solve_nearest_neighbor
    except Exception:
        logger.debug("Could not import solve_nearest_neighbor -- skipping")

    try:
        from src.baselines.construction_heuristics import solve_greedy
        _SOLVER_FACTORIES["greedy"] = solve_greedy
    except Exception:
        logger.debug("Could not import solve_greedy -- skipping")

    try:
        from src.baselines.construction_heuristics import solve_savings
        _SOLVER_FACTORIES["savings"] = solve_savings
    except Exception:
        logger.debug("Could not import solve_savings -- skipping")

    # -- LKH baseline ------------------------------------------------------
    try:
        from src.baselines.lkh_baseline import solve_lkh
        _SOLVER_FACTORIES["lkh"] = solve_lkh
    except Exception:
        logger.debug("Could not import solve_lkh -- skipping")

    # -- OR-Tools baseline -------------------------------------------------
    try:
        from src.baselines.ortools_baseline import solve_ortools
        _SOLVER_FACTORIES["ortools"] = solve_ortools
    except Exception:
        logger.debug("Could not import solve_ortools -- skipping")

    # -- Hybrid GNN + LK solver --------------------------------------------
    try:
        from src.solvers.hybrid_gnn_lk import solve_hybrid_gnn_lk
        _SOLVER_FACTORIES["hybrid_gnn_lk"] = solve_hybrid_gnn_lk
    except Exception:
        logger.debug("Could not import solve_hybrid_gnn_lk -- skipping")

    # -- ALNS with learned components --------------------------------------
    try:
        from src.solvers.alns_learned import solve_alns
        _SOLVER_FACTORIES["alns"] = solve_alns
    except Exception:
        logger.debug("Could not import solve_alns -- skipping")


# ---------------------------------------------------------------------------
# Helper utilities
# ---------------------------------------------------------------------------

def compute_tour_cost(tour: List[int], cost_matrix) -> float:
    """Compute the total directed cost of a Hamiltonian cycle.

    Parameters
    ----------
    tour : list[int]
        Ordered node indices forming the cycle.
    cost_matrix : array-like
        Square matrix where ``cost_matrix[i][j]`` is the cost from *i* to *j*.

    Returns
    -------
    float
        Sum of consecutive edge costs including the closing edge.
    """
    total = 0.0
    n = len(tour)
    for i in range(n):
        total += cost_matrix[tour[i]][tour[(i + 1) % n]]
    return float(total)


def validate_tour(tour: List[int], n: int) -> bool:
    """Check that *tour* is a valid Hamiltonian cycle on n nodes.

    Parameters
    ----------
    tour : list[int]
        Tour to validate.
    n : int
        Expected number of nodes.

    Returns
    -------
    bool
        ``True`` if valid.

    Raises
    ------
    ValueError
        With a description of the problem if the tour is invalid.
    """
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
    return True


# ---------------------------------------------------------------------------
# Directed edge-set helpers
# ---------------------------------------------------------------------------

def _tour_edge_set(tour: List[int]) -> set:
    """Return the set of directed edges (i, j) in a tour."""
    n = len(tour)
    return {(tour[i], tour[(i + 1) % n]) for i in range(n)}


def _tour_successor_map(tour: List[int]) -> Dict[int, int]:
    """Return a dict mapping each node to its successor in the tour."""
    n = len(tour)
    return {tour[i]: tour[(i + 1) % n] for i in range(n)}


# ---------------------------------------------------------------------------
# Simplified EAX-style crossover for ATSP
# ---------------------------------------------------------------------------

def _build_ab_cycles(
    tour_a: List[int],
    tour_b: List[int],
) -> List[List[Tuple[int, int, str]]]:
    """Build AB-cycles from two parent tours.

    An AB-cycle is a closed sequence of edges that alternates between edges
    belonging exclusively to tour A and edges belonging exclusively to tour B.

    Parameters
    ----------
    tour_a, tour_b : list[int]
        Two parent tours (same node set).

    Returns
    -------
    list of list of (from_node, to_node, owner)
        Each inner list is one AB-cycle where *owner* is ``'A'`` or ``'B'``.
    """
    edges_a = _tour_edge_set(tour_a)
    edges_b = _tour_edge_set(tour_b)

    # Common edges appear in both tours -- they are irrelevant for AB-cycles
    common = edges_a & edges_b
    only_a = edges_a - common  # edges in A but not B
    only_b = edges_b - common  # edges in B but not A

    if not only_a or not only_b:
        return []

    # Build adjacency for quick lookup:
    #   For A-edges: from_node -> to_node
    #   For B-edges: to_node  -> from_node  (we traverse B-edges in reverse
    #                                        so the cycle alternates direction)
    succ_a: Dict[int, List[int]] = {}
    for u, v in only_a:
        succ_a.setdefault(u, []).append(v)

    # For B-edges we want: given a node that we *arrived at* via an A-edge,
    # find a B-edge that *leaves* that node (going to some other node in B).
    succ_b: Dict[int, List[int]] = {}
    for u, v in only_b:
        succ_b.setdefault(u, []).append(v)

    used_a = set()
    used_b = set()
    cycles: List[List[Tuple[int, int, str]]] = []

    for start_edge in sorted(only_a):  # deterministic iteration order
        if start_edge in used_a:
            continue

        cycle: List[Tuple[int, int, str]] = []
        u, v = start_edge
        current = u

        # We alternate: pick an A-edge from *current*, then a B-edge, etc.
        turn = "A"
        max_steps = 2 * (len(only_a) + len(only_b)) + 2
        step = 0

        while step < max_steps:
            step += 1
            if turn == "A":
                candidates = succ_a.get(current, [])
                # Find an unused A-edge from current
                nxt = None
                for c in candidates:
                    if (current, c) not in used_a:
                        nxt = c
                        break
                if nxt is None:
                    break  # cannot extend
                cycle.append((current, nxt, "A"))
                used_a.add((current, nxt))
                current = nxt
                turn = "B"
            else:
                candidates = succ_b.get(current, [])
                nxt = None
                for c in candidates:
                    if (current, c) not in used_b:
                        nxt = c
                        break
                if nxt is None:
                    break
                cycle.append((current, nxt, "B"))
                used_b.add((current, nxt))
                current = nxt
                turn = "A"

            # Check if cycle is closed
            if current == u and len(cycle) >= 4 and len(cycle) % 2 == 0:
                cycles.append(cycle)
                break

    return cycles


def _apply_ab_cycle(
    tour_a: List[int],
    tour_b: List[int],
    ab_cycle: List[Tuple[int, int, str]],
    cost_matrix,
) -> Optional[List[int]]:
    """Apply a single AB-cycle perturbation to *tour_a*.

    The idea: remove the A-edges of the cycle from tour A and replace them
    with the B-edges of the cycle.  Because this may break the Hamiltonian
    structure, we attempt to reconnect by segment swapping and validate the
    result.

    Parameters
    ----------
    tour_a, tour_b : list[int]
        Parent tours.
    ab_cycle : list of (from, to, owner)
        One AB-cycle.
    cost_matrix : array-like
        Asymmetric cost matrix.

    Returns
    -------
    list[int] or None
        A new valid tour if the crossover succeeds, otherwise ``None``.
    """
    n = len(tour_a)
    succ_a = _tour_successor_map(tour_a)

    # Edges to remove (A-edges in the cycle) and edges to add (B-edges)
    remove_edges = {(u, v) for u, v, owner in ab_cycle if owner == "A"}
    add_edges = {(u, v) for u, v, owner in ab_cycle if owner == "B"}

    # Build a new successor map: start from tour_a, remove A-edges, add B-edges
    new_succ = dict(succ_a)
    for u, v in remove_edges:
        if new_succ.get(u) == v:
            del new_succ[u]

    for u, v in add_edges:
        new_succ[u] = v

    # Try to extract a valid tour from the new successor map
    # There may be multiple fragments -- attempt to stitch them together
    # by finding the best way to connect fragment endpoints.
    if len(new_succ) < n:
        # Some nodes have no outgoing edge -- we need to reconnect
        has_out = set(new_succ.keys())
        has_in = set(new_succ.values())
        missing_out = set(range(n)) - has_out   # nodes needing an outgoing edge
        missing_in = set(range(n)) - has_in      # nodes needing an incoming edge

        # Greedy reconnection: for each node without an outgoing edge, connect
        # it to the cheapest node that still needs an incoming edge.
        missing_out = sorted(missing_out)
        missing_in_list = sorted(missing_in)

        for u in missing_out:
            if not missing_in_list:
                break
            best_v = None
            best_cost = float("inf")
            for v in missing_in_list:
                if v == u:
                    continue
                c = cost_matrix[u][v]
                if c < best_cost:
                    best_cost = c
                    best_v = v
            if best_v is not None:
                new_succ[u] = best_v
                missing_in_list.remove(best_v)

    # Attempt to read tour from new_succ starting at node 0
    try:
        tour = [0]
        visited = {0}
        current = 0
        for _ in range(n - 1):
            nxt = new_succ.get(current)
            if nxt is None or nxt in visited:
                return None  # broken chain
            tour.append(nxt)
            visited.add(nxt)
            current = nxt
        # Verify it closes back to 0
        if new_succ.get(current) != 0:
            return None
        validate_tour(tour, n)
        return tour
    except (ValueError, KeyError):
        return None


def _segment_swap_crossover(
    tour_a: List[int],
    tour_b: List[int],
    cost_matrix,
    rng: np.random.RandomState,
) -> Optional[List[int]]:
    """Fallback crossover: swap a contiguous segment between two tours.

    Picks a random segment from tour_b and inserts it into tour_a at the
    position that minimises insertion cost, removing duplicates.

    Parameters
    ----------
    tour_a, tour_b : list[int]
        Parent tours.
    cost_matrix : array-like
        Asymmetric cost matrix.
    rng : numpy.random.RandomState
        Random number generator.

    Returns
    -------
    list[int] or None
        A valid child tour, or ``None`` if the attempt fails.
    """
    n = len(tour_a)
    if n < 6:
        return None

    # Choose a random segment length (10-40 % of the tour)
    seg_len = rng.randint(max(2, n // 10), max(3, n * 2 // 5))
    seg_start = rng.randint(0, n)
    segment = [tour_b[(seg_start + k) % n] for k in range(seg_len)]
    seg_set = set(segment)

    # Build the remainder of tour_a preserving order, minus the segment nodes
    remainder = [node for node in tour_a if node not in seg_set]
    if not remainder:
        return None

    # Find best insertion position in the remainder
    best_pos = 0
    best_delta = float("inf")
    cm = cost_matrix
    for pos in range(len(remainder)):
        # Inserting segment between remainder[pos] and remainder[(pos+1) % len(remainder)]
        prev_node = remainder[pos]
        next_node = remainder[(pos + 1) % len(remainder)]
        # Cost of removing edge prev->next and adding prev->seg[0], seg[-1]->next
        old_cost = cm[prev_node][next_node]
        new_cost = cm[prev_node][segment[0]] + cm[segment[-1]][next_node]
        delta = new_cost - old_cost
        if delta < best_delta:
            best_delta = delta
            best_pos = pos

    # Build child tour
    child = remainder[: best_pos + 1] + segment + remainder[best_pos + 1 :]

    try:
        validate_tour(child, n)
        return child
    except ValueError:
        return None


def _crossover(
    tour_a: List[int],
    tour_b: List[int],
    cost_matrix,
    rng: np.random.RandomState,
) -> Optional[List[int]]:
    """Attempt EAX-style crossover, falling back to segment swap.

    Parameters
    ----------
    tour_a, tour_b : list[int]
        The two best tours (tour_a is the better one).
    cost_matrix : array-like
        Asymmetric cost matrix.
    rng : numpy.random.RandomState
        Random number generator.

    Returns
    -------
    list[int] or None
        A new tour that is the result of crossover, or ``None`` if all
        attempts fail.
    """
    n = len(tour_a)
    if n < 4:
        return None

    # 1. Try EAX-style AB-cycle crossover
    ab_cycles = _build_ab_cycles(tour_a, tour_b)
    if ab_cycles:
        # Pick a random AB-cycle (prefer shorter ones for less disruption)
        ab_cycles.sort(key=len)
        # Try up to 3 cycles, starting with the shortest
        attempts = min(len(ab_cycles), 3)
        indices = list(range(len(ab_cycles)))
        rng.shuffle(indices)
        for idx in indices[:attempts]:
            child = _apply_ab_cycle(tour_a, tour_b, ab_cycles[idx], cost_matrix)
            if child is not None:
                return child

    # 2. Fallback: segment-swap crossover
    for _ in range(5):
        child = _segment_swap_crossover(tour_a, tour_b, cost_matrix, rng)
        if child is not None:
            return child

    return None


# ---------------------------------------------------------------------------
# Individual solver runner with time limit and error handling
# ---------------------------------------------------------------------------

def _run_solver(
    name: str,
    solver_fn,
    instance: dict,
    time_limit: float,
    seed: int,
) -> Optional[dict]:
    """Run a single solver with error handling.

    Returns the solver result dict on success, or ``None`` on failure.
    """
    try:
        # Construction heuristics do not accept time_limit
        if name in ("nearest_neighbor", "greedy", "savings"):
            result = solver_fn(instance, seed=seed)
        elif name == "lkh":
            result = solver_fn(
                instance,
                max_trials=10,
                time_limit=time_limit,
                seed=seed,
            )
        else:
            # Generic interface assumed for ortools, hybrid_gnn_lk, alns, etc.
            result = solver_fn(instance, time_limit=time_limit, seed=seed)

        # Basic sanity check on result
        if result is None:
            return None
        tour = result.get("tour")
        cost = result.get("cost")
        if tour is None or cost is None:
            return None
        if cost == float("inf"):
            return None

        return result

    except Exception as exc:
        logger.warning("Solver '%s' failed: %s", name, exc)
        return None


# ---------------------------------------------------------------------------
# Main entry point
# ---------------------------------------------------------------------------

def solve_ensemble(
    instance: dict,
    time_limit: float = 60.0,
    seed: int = 42,
    solvers: Optional[List[str]] = None,
    use_crossover: bool = True,
) -> dict:
    """Solve an ATSP instance using an ensemble of multiple solvers.

    Parameters
    ----------
    instance : dict
        ATSP instance with keys ``metadata``, ``coordinates``, and
        ``cost_matrix``.
    time_limit : float
        Total wall-clock time budget (seconds) split among solvers.
    seed : int
        Random seed for reproducibility.
    solvers : list of str or None
        Solver names to use.  If ``None``, all available solvers are used.
    use_crossover : bool
        Whether to try EAX-style crossover on the top-2 tours.

    Returns
    -------
    dict
        Result dictionary in the standard format::

            {
                'tour': list[int],
                'cost': float,
                'runtime_seconds': float,
                'solver_params': dict,
                'solver_name': 'ensemble',
            }
    """
    start_time = time.perf_counter()
    rng = np.random.RandomState(seed)
    cost_matrix = np.asarray(instance["cost_matrix"], dtype=np.float64)
    n = cost_matrix.shape[0]

    # Ensure solver registry is populated
    _register_solvers()

    # Determine which solvers to run
    if solvers is not None:
        requested = []
        for name in solvers:
            if name in _SOLVER_FACTORIES:
                requested.append(name)
            else:
                logger.warning(
                    "Requested solver '%s' is not available -- skipping", name
                )
        solver_names = requested
    else:
        solver_names = list(_SOLVER_FACTORIES.keys())

    if not solver_names:
        # Absolute fallback: return a trivial tour (identity permutation)
        trivial_tour = list(range(n))
        trivial_cost = compute_tour_cost(trivial_tour, cost_matrix)
        elapsed = time.perf_counter() - start_time
        return {
            "tour": trivial_tour,
            "cost": trivial_cost,
            "runtime_seconds": elapsed,
            "solver_params": {
                "seed": seed,
                "solvers_run": [],
                "use_crossover": use_crossover,
                "note": "no solvers available",
            },
            "solver_name": "ensemble",
        }

    # Reserve a small portion of the budget for crossover
    crossover_budget = min(2.0, time_limit * 0.05) if use_crossover else 0.0
    solver_budget = time_limit - crossover_budget

    # Split time budget among solvers.  Construction heuristics are fast, so
    # they get a minimal slice; the rest is distributed evenly among the
    # heavier solvers.
    fast_solvers = {"nearest_neighbor", "greedy", "savings"}
    heavy_names = [s for s in solver_names if s not in fast_solvers]
    fast_names = [s for s in solver_names if s in fast_solvers]

    # Fast solvers share 5 % of the solver budget (or the whole thing if no
    # heavy solvers are present).
    if heavy_names:
        fast_share = solver_budget * 0.05
        heavy_share = solver_budget - fast_share
        per_fast = (fast_share / len(fast_names)) if fast_names else 0.0
        per_heavy = heavy_share / len(heavy_names)
    else:
        per_fast = (solver_budget / len(fast_names)) if fast_names else 0.0
        per_heavy = 0.0

    time_alloc: Dict[str, float] = {}
    for name in fast_names:
        time_alloc[name] = per_fast
    for name in heavy_names:
        time_alloc[name] = per_heavy

    # Run all solvers and collect results
    results: List[Tuple[List[int], float, str]] = []  # (tour, cost, name)
    solvers_run: List[str] = []

    for name in solver_names:
        remaining = time_limit - (time.perf_counter() - start_time)
        if remaining <= 0.0:
            break

        allotted = min(time_alloc[name], remaining)
        solver_fn = _SOLVER_FACTORIES[name]

        result = _run_solver(name, solver_fn, instance, allotted, seed)
        solvers_run.append(name)

        if result is not None:
            tour = result["tour"]
            # Recompute cost with our own helper for consistency
            cost = compute_tour_cost(tour, cost_matrix)
            results.append((tour, cost, name))
            logger.info(
                "Solver '%s' returned tour with cost %.2f", name, cost
            )

    if not results:
        # No solver succeeded -- return identity tour
        trivial_tour = list(range(n))
        trivial_cost = compute_tour_cost(trivial_tour, cost_matrix)
        elapsed = time.perf_counter() - start_time
        return {
            "tour": trivial_tour,
            "cost": trivial_cost,
            "runtime_seconds": elapsed,
            "solver_params": {
                "seed": seed,
                "solvers_run": solvers_run,
                "use_crossover": use_crossover,
                "note": "all solvers failed",
            },
            "solver_name": "ensemble",
        }

    # Sort results by cost (ascending)
    results.sort(key=lambda x: x[1])
    best_tour, best_cost, best_solver = results[0]

    # ------------------------------------------------------------------
    # Optional crossover phase
    # ------------------------------------------------------------------
    crossover_applied = False
    if use_crossover and len(results) >= 2:
        remaining = time_limit - (time.perf_counter() - start_time)
        if remaining > 0.0:
            tour_a = results[0][0]
            tour_b = results[1][0]

            child = _crossover(tour_a, tour_b, cost_matrix, rng)
            if child is not None:
                child_cost = compute_tour_cost(child, cost_matrix)
                if child_cost < best_cost:
                    best_tour = child
                    best_cost = child_cost
                    crossover_applied = True
                    logger.info(
                        "Crossover improved cost: %.2f -> %.2f",
                        results[0][1],
                        child_cost,
                    )

    # Final validation
    try:
        validate_tour(best_tour, n)
    except ValueError as exc:
        # Should not happen, but guard against it
        logger.error("Best tour failed validation: %s -- falling back", exc)
        best_tour = list(range(n))
        best_cost = compute_tour_cost(best_tour, cost_matrix)

    elapsed = time.perf_counter() - start_time

    return {
        "tour": best_tour,
        "cost": float(best_cost),
        "runtime_seconds": float(elapsed),
        "solver_params": {
            "seed": seed,
            "solvers_run": solvers_run,
            "solver_costs": {name: cost for _, cost, name in results},
            "best_component_solver": best_solver if not crossover_applied else f"{best_solver}+crossover",
            "use_crossover": use_crossover,
            "crossover_applied": crossover_applied,
            "time_limit": time_limit,
        },
        "solver_name": "ensemble",
    }


# ---------------------------------------------------------------------------
# CLI entry point for quick testing
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    import sys
    import os

    # Make sure project root is on the path
    project_root = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..", "..")
    )
    if project_root not in sys.path:
        sys.path.insert(0, project_root)

    from src.data.instance_generator import generate_synthetic_instance

    print("=== Ensemble ATSP Solver Self-Test ===\n")

    for n_nodes in [10, 20, 50]:
        print(f"--- Instance: n={n_nodes} ---")
        inst = generate_synthetic_instance(n_nodes, seed=42)

        result = solve_ensemble(
            inst,
            time_limit=30.0,
            seed=42,
            solvers=None,
            use_crossover=True,
        )

        print(f"  Tour cost        : {result['cost']:.2f}")
        print(f"  Runtime          : {result['runtime_seconds']:.3f}s")
        print(f"  Solvers run      : {result['solver_params']['solvers_run']}")
        print(f"  Best component   : {result['solver_params']['best_component_solver']}")
        print(f"  Crossover applied: {result['solver_params']['crossover_applied']}")
        if result['solver_params'].get('solver_costs'):
            for sname, scost in result['solver_params']['solver_costs'].items():
                print(f"    {sname:20s}: {scost:.2f}")
        print()

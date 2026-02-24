"""
Traffic-Aware Iterated Local Search for ATSP with Time-Dependent Edge Weights.

Implements an iterated local search (ILS) solver that accounts for
time-dependent travel costs.  The core idea is that edge traversal costs
vary with the departure time from each node, modelling real-world
phenomena such as rush-hour congestion.

Traffic model
-------------
A Gaussian-shaped rush-hour multiplier is applied to every edge cost:

    f(t) = 1 + (peak_multiplier - 1) * exp(-(t - rush_hour_peak)^2
                                             / (2 * rush_hour_spread^2))

so at the peak hour the cost is scaled by ``peak_multiplier``, and far
from the peak the cost approaches the static baseline.

The time-dependent cost of an edge (i, j) when departed at time t is:

    c_ij(t) = base_cost[i][j] * f(t)

As the vehicle traverses the tour, each successive departure time is
determined by the accumulated travel time so far, making the overall tour
cost depend non-trivially on the ordering.

Key insight for local search
----------------------------
When a 2-opt move changes the early part of the tour, it shifts
departure times for *all* subsequent edges, potentially moving them
into or out of the rush-hour window.  Consequently every candidate move
must be evaluated by recomputing the full time-dependent tour cost from
the affected position onward.

Integration
-----------
This module can be used standalone via ``solve_traffic_aware`` or as an
optional enhancement layer on top of the hybrid GNN-LK solver (item_015).
The function ``add_traffic_weights`` augments any standard instance dict
with a ``traffic_model`` field that the solver consumes.

References
----------
Malandraki, C. & Daskin, M. S. (1992). "Time Dependent Vehicle Routing
Problems: Formulations, Properties and Heuristic Algorithms."
Transportation Science, 26(3), 185-200.

Ichoua, S., Gendreau, M. & Potvin, J.-Y. (2003). "Vehicle Dispatching
with Time-Dependent Travel Times." European Journal of Operational
Research, 144(2), 379-396.
"""

import copy
import time

import numpy as np


# ---------------------------------------------------------------------------
# Traffic model construction
# ---------------------------------------------------------------------------

def add_traffic_weights(instance, rush_hour_peak=8.0, rush_hour_spread=2.0,
                        peak_multiplier=1.5, seed=42):
    """Add synthetic time-dependent weights to an instance.

    Creates a ``traffic_model`` field inside the instance that stores the
    parameters needed by the time-dependent cost evaluator.

    Parameters
    ----------
    instance : dict
        Standard ATSP instance dict with at least a ``cost_matrix`` key.
    rush_hour_peak : float
        Centre of the rush-hour window on a 24-hour clock (hours).
    rush_hour_spread : float
        Standard deviation of the Gaussian rush-hour profile (hours).
    peak_multiplier : float
        Maximum cost multiplier at the peak of rush hour.  Must be >= 1.
    seed : int
        Random seed (reserved for future per-edge noise; currently unused
        but accepted for interface consistency).

    Returns
    -------
    dict
        A *copy* of the instance with an added ``traffic_model`` field
        containing:
        - ``base_cost_matrix`` : np.ndarray -- the original static costs.
        - ``rush_hour_peak`` : float
        - ``rush_hour_spread`` : float
        - ``peak_multiplier`` : float
    """
    if peak_multiplier < 1.0:
        raise ValueError(
            f"peak_multiplier must be >= 1.0, got {peak_multiplier}"
        )

    base_matrix = np.asarray(instance["cost_matrix"], dtype=np.float64)

    inst_out = copy.deepcopy(instance)
    inst_out["traffic_model"] = {
        "base_cost_matrix": base_matrix,
        "rush_hour_peak": float(rush_hour_peak),
        "rush_hour_spread": float(rush_hour_spread),
        "peak_multiplier": float(peak_multiplier),
    }
    return inst_out


# ---------------------------------------------------------------------------
# Time-dependent cost helpers
# ---------------------------------------------------------------------------

def _traffic_multiplier(t, rush_hour_peak, rush_hour_spread, peak_multiplier):
    """Evaluate the Gaussian rush-hour multiplier at time *t* (hours).

    Parameters
    ----------
    t : float or np.ndarray
        Departure time(s) in hours (0-24 scale, but values outside that
        range are handled gracefully).
    rush_hour_peak : float
    rush_hour_spread : float
    peak_multiplier : float

    Returns
    -------
    float or np.ndarray
        Multiplier(s) >= 1.0.
    """
    exponent = -((t - rush_hour_peak) ** 2) / (2.0 * rush_hour_spread ** 2)
    return 1.0 + (peak_multiplier - 1.0) * np.exp(exponent)


def compute_time_dependent_cost(tour, base_matrix, traffic_model,
                                departure_time=8.0):
    """Compute total tour cost accounting for time-dependent edge weights.

    As the vehicle traverses the tour, the departure time at each node
    accumulates based on the travel time of preceding edges.  Each edge
    cost is evaluated at the actual departure time from its origin node.

    Parameters
    ----------
    tour : list[int]
        Ordered sequence of node indices forming a Hamiltonian cycle.
    base_matrix : np.ndarray
        Static asymmetric cost matrix of shape (n, n).  Entries represent
        base travel *times* (in hours for consistency with the traffic
        model clock).
    traffic_model : dict
        Traffic model parameters as produced by ``add_traffic_weights``.
    departure_time : float
        Time (in hours, 0-24) at which the vehicle departs the first
        node of the tour.

    Returns
    -------
    float
        Total time-dependent tour cost.
    """
    rush_peak = traffic_model["rush_hour_peak"]
    rush_spread = traffic_model["rush_hour_spread"]
    peak_mult = traffic_model["peak_multiplier"]

    n = len(tour)
    total_cost = 0.0
    current_time = float(departure_time)

    for k in range(n):
        i = tour[k]
        j = tour[(k + 1) % n]
        base_cost = base_matrix[i, j]
        multiplier = _traffic_multiplier(current_time, rush_peak,
                                         rush_spread, peak_mult)
        edge_cost = base_cost * multiplier
        total_cost += edge_cost
        # The travel time on this edge shifts the departure time for the
        # next edge.  We treat the base cost as travel time in hours.
        current_time += edge_cost

    return total_cost


def _compute_td_cost_from_position(tour, base_matrix, traffic_model,
                                   start_pos, time_at_start_pos):
    """Compute the time-dependent cost of the tour from a given position.

    This is an optimisation helper: when evaluating a local-search move
    that only changes edges from ``start_pos`` onward, we can skip
    re-evaluating the prefix and begin accumulation from
    ``time_at_start_pos``.

    Parameters
    ----------
    tour : list[int]
        Full tour.
    base_matrix : np.ndarray
        Static cost matrix.
    traffic_model : dict
        Traffic model dict.
    start_pos : int
        Index into the tour from which to start cost accumulation.
    time_at_start_pos : float
        The vehicle's clock time when it departs ``tour[start_pos]``.

    Returns
    -------
    float
        Sum of time-dependent edge costs from ``start_pos`` to the end
        of the cycle (including the closing edge back to ``tour[0]``).
    """
    rush_peak = traffic_model["rush_hour_peak"]
    rush_spread = traffic_model["rush_hour_spread"]
    peak_mult = traffic_model["peak_multiplier"]

    n = len(tour)
    cost = 0.0
    current_time = float(time_at_start_pos)

    for k in range(start_pos, n):
        i = tour[k]
        j = tour[(k + 1) % n]
        base_cost = base_matrix[i, j]
        mult = _traffic_multiplier(current_time, rush_peak,
                                   rush_spread, peak_mult)
        edge_cost = base_cost * mult
        cost += edge_cost
        current_time += edge_cost

    return cost


def _compute_prefix_times(tour, base_matrix, traffic_model, departure_time):
    """Compute cumulative departure times at every position in the tour.

    Parameters
    ----------
    tour : list[int]
    base_matrix : np.ndarray
    traffic_model : dict
    departure_time : float

    Returns
    -------
    times : list[float]
        ``times[k]`` is the departure time from ``tour[k]``.
        ``times[0] == departure_time``.
    prefix_costs : list[float]
        ``prefix_costs[k]`` is the cumulative time-dependent cost of
        edges tour[0]->tour[1], ..., tour[k-1]->tour[k].
        ``prefix_costs[0] == 0.0``.
    """
    rush_peak = traffic_model["rush_hour_peak"]
    rush_spread = traffic_model["rush_hour_spread"]
    peak_mult = traffic_model["peak_multiplier"]

    n = len(tour)
    times = [0.0] * n
    prefix_costs = [0.0] * n
    times[0] = float(departure_time)

    for k in range(1, n):
        i = tour[k - 1]
        j = tour[k]
        base_cost = base_matrix[i, j]
        mult = _traffic_multiplier(times[k - 1], rush_peak,
                                   rush_spread, peak_mult)
        edge_cost = base_cost * mult
        prefix_costs[k] = prefix_costs[k - 1] + edge_cost
        times[k] = times[k - 1] + edge_cost

    return times, prefix_costs


# ---------------------------------------------------------------------------
# Static (non-traffic) cost helper for ablation
# ---------------------------------------------------------------------------

def compute_tour_cost(tour, cost_matrix):
    """Compute the static (time-independent) tour cost.

    Provided for interface consistency with other solvers.

    Parameters
    ----------
    tour : list[int]
        Ordered node indices forming a Hamiltonian cycle.
    cost_matrix : np.ndarray
        Asymmetric cost matrix of shape (n, n).

    Returns
    -------
    float
        Total static tour cost.
    """
    cost = 0.0
    n = len(tour)
    for k in range(n):
        cost += cost_matrix[tour[k]][tour[(k + 1) % n]]
    return cost


# ---------------------------------------------------------------------------
# Construction heuristic: nearest-neighbour with time-dependent costs
# ---------------------------------------------------------------------------

def _nn_tour_traffic(base_matrix, traffic_model, departure_time, start_node):
    """Build a nearest-neighbour tour using time-dependent edge costs.

    At each step the cheapest *time-dependent* edge from the current node
    is selected, where the departure time reflects accumulated travel so
    far.

    Parameters
    ----------
    base_matrix : np.ndarray
    traffic_model : dict
    departure_time : float
    start_node : int

    Returns
    -------
    list[int]
        Constructed tour.
    """
    rush_peak = traffic_model["rush_hour_peak"]
    rush_spread = traffic_model["rush_hour_spread"]
    peak_mult = traffic_model["peak_multiplier"]

    n = base_matrix.shape[0]
    visited = np.zeros(n, dtype=bool)
    tour = [start_node]
    visited[start_node] = True
    current_time = float(departure_time)

    for _ in range(n - 1):
        current = tour[-1]
        # Compute time-dependent costs from current node to all others
        row = base_matrix[current].copy()
        mult = _traffic_multiplier(current_time, rush_peak,
                                   rush_spread, peak_mult)
        td_row = row * mult
        td_row[visited] = np.inf
        next_node = int(np.argmin(td_row))
        tour.append(next_node)
        visited[next_node] = True
        current_time += td_row[next_node]

    return tour


def _best_nn_tour_traffic(base_matrix, traffic_model, departure_time):
    """Best-of-all-starts nearest-neighbour with time-dependent costs."""
    n = base_matrix.shape[0]
    best_tour = None
    best_cost = np.inf

    for start in range(n):
        tour = _nn_tour_traffic(base_matrix, traffic_model,
                                departure_time, start)
        cost = compute_time_dependent_cost(tour, base_matrix,
                                           traffic_model, departure_time)
        if cost < best_cost:
            best_cost = cost
            best_tour = tour

    return best_tour, best_cost


# ---------------------------------------------------------------------------
# 2-opt local search with time-dependent cost evaluation
# ---------------------------------------------------------------------------

def _two_opt_td(tour, base_matrix, traffic_model, departure_time,
                time_deadline=None):
    """Improve a tour using 2-opt moves evaluated with time-dependent costs.

    Because reversing a segment in the tour changes the departure times
    for *all* subsequent edges, every candidate move is evaluated by
    recomputing the full time-dependent cost from the earliest affected
    position.

    Uses first-improvement strategy.

    Parameters
    ----------
    tour : list[int]
        Current tour (will be copied).
    base_matrix : np.ndarray
    traffic_model : dict
    departure_time : float
    time_deadline : float or None
        Wall-clock deadline (``time.time()`` value).

    Returns
    -------
    list[int]
        Improved tour.
    float
        Time-dependent cost of the improved tour.
    """
    n = len(tour)
    tour = list(tour)
    current_cost = compute_time_dependent_cost(tour, base_matrix,
                                               traffic_model, departure_time)
    improved = True

    while improved:
        improved = False

        if time_deadline is not None and time.time() >= time_deadline:
            break

        # Precompute prefix departure times for the current tour so we
        # can efficiently evaluate suffix costs after a 2-opt reversal.
        times, prefix_costs = _compute_prefix_times(
            tour, base_matrix, traffic_model, departure_time
        )

        for i in range(n - 1):
            if time_deadline is not None and time.time() >= time_deadline:
                break

            for j in range(i + 2, n):
                if i == 0 and j == n - 1:
                    continue

                # Candidate: reverse segment [i+1 .. j]
                new_tour = tour[:i + 1] + tour[i + 1:j + 1][::-1] + tour[j + 1:]

                # The prefix up to position i is unchanged; the departure
                # time at position i is times[i].  Recompute from i onward.
                suffix_cost = _compute_td_cost_from_position(
                    new_tour, base_matrix, traffic_model, i, times[i]
                )
                new_cost = prefix_costs[i] + suffix_cost

                if new_cost < current_cost - 1e-10:
                    tour = new_tour
                    current_cost = new_cost
                    improved = True
                    break  # restart scan

            if improved:
                break

    return tour, current_cost


# ---------------------------------------------------------------------------
# Or-opt local search with time-dependent cost evaluation
# ---------------------------------------------------------------------------

def _or_opt_td(tour, base_matrix, traffic_model, departure_time,
               time_deadline=None):
    """Improve a tour using or-opt moves with time-dependent evaluation.

    Relocates segments of length 1, 2, or 3 to the best position,
    evaluated under the time-dependent cost model.

    Uses first-improvement strategy.

    Parameters
    ----------
    tour : list[int]
    base_matrix : np.ndarray
    traffic_model : dict
    departure_time : float
    time_deadline : float or None

    Returns
    -------
    list[int]
        Improved tour.
    float
        Time-dependent cost.
    """
    n = len(tour)
    if n <= 4:
        cost = compute_time_dependent_cost(tour, base_matrix,
                                           traffic_model, departure_time)
        return list(tour), cost

    tour = list(tour)
    current_cost = compute_time_dependent_cost(tour, base_matrix,
                                               traffic_model, departure_time)
    improved = True

    while improved:
        improved = False

        if time_deadline is not None and time.time() >= time_deadline:
            break

        for seg_len in [1, 2, 3]:
            if seg_len >= n - 1:
                continue

            if time_deadline is not None and time.time() >= time_deadline:
                break

            for i in range(n):
                if time_deadline is not None and time.time() >= time_deadline:
                    break

                seg_indices = [(i + k) % n for k in range(seg_len)]
                segment = [tour[idx] for idx in seg_indices]
                seg_set = set(seg_indices)
                remaining = [tour[k] for k in range(n) if k not in seg_set]

                if len(remaining) == 0:
                    continue

                for j in range(len(remaining)):
                    new_tour = (remaining[:j + 1] + segment
                                + remaining[j + 1:])
                    new_cost = compute_time_dependent_cost(
                        new_tour, base_matrix, traffic_model, departure_time
                    )
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
# Combined time-dependent local search
# ---------------------------------------------------------------------------

def _local_search_td(tour, base_matrix, traffic_model, departure_time,
                     time_deadline=None):
    """Apply 2-opt and or-opt with time-dependent evaluation until convergence.

    Alternates between the two neighbourhood operators until neither
    yields an improvement or the wall-clock deadline is reached.

    Parameters
    ----------
    tour : list[int]
    base_matrix : np.ndarray
    traffic_model : dict
    departure_time : float
    time_deadline : float or None

    Returns
    -------
    list[int]
        Locally optimal tour.
    float
        Time-dependent cost.
    """
    current_cost = compute_time_dependent_cost(tour, base_matrix,
                                               traffic_model, departure_time)
    any_improved = True

    while any_improved:
        any_improved = False

        if time_deadline is not None and time.time() >= time_deadline:
            break

        # 2-opt phase
        new_tour, new_cost = _two_opt_td(tour, base_matrix, traffic_model,
                                         departure_time, time_deadline)
        if new_cost < current_cost - 1e-10:
            tour = new_tour
            current_cost = new_cost
            any_improved = True

        if time_deadline is not None and time.time() >= time_deadline:
            break

        # Or-opt phase
        new_tour, new_cost = _or_opt_td(tour, base_matrix, traffic_model,
                                        departure_time, time_deadline)
        if new_cost < current_cost - 1e-10:
            tour = new_tour
            current_cost = new_cost
            any_improved = True

    return tour, current_cost


# ---------------------------------------------------------------------------
# Perturbation: double-bridge with traffic-aware bias
# ---------------------------------------------------------------------------

def _perturb_tour_traffic(tour, base_matrix, traffic_model, departure_time,
                          rng):
    """Apply a traffic-aware double-bridge perturbation.

    The standard double-bridge splits the tour into four segments and
    reconnects them in a different order.  The traffic-aware variant
    biases cut-point selection toward positions where the current
    departure time falls near the rush-hour peak, since those are the
    edges most sensitive to reordering.

    Parameters
    ----------
    tour : list[int]
    base_matrix : np.ndarray
    traffic_model : dict
    departure_time : float
    rng : np.random.RandomState

    Returns
    -------
    list[int]
        Perturbed tour.
    """
    n = len(tour)

    if n < 8:
        # For very small tours just shuffle a small segment.
        new_tour = list(tour)
        i, j = sorted(rng.choice(n, 2, replace=False))
        new_tour[i:j + 1] = rng.permutation(new_tour[i:j + 1]).tolist()
        return new_tour

    # Compute departure times at each position.
    times, _ = _compute_prefix_times(tour, base_matrix, traffic_model,
                                     departure_time)

    # Build bias weights: positions closer to rush-hour peak are more
    # likely to be chosen as cut points (higher sensitivity).
    rush_peak = traffic_model["rush_hour_peak"]
    rush_spread = traffic_model["rush_hour_spread"]
    peak_mult = traffic_model["peak_multiplier"]

    # Use the traffic multiplier itself as a weight (higher at peak).
    weights = np.array([
        _traffic_multiplier(times[k], rush_peak, rush_spread, peak_mult)
        for k in range(1, n)
    ])
    # Add a small uniform component so no position has zero probability.
    weights = weights + 0.1
    weights = weights / weights.sum()

    # Choose 3 distinct cut points using the biased distribution.
    candidates = np.arange(1, n)
    cuts = sorted(rng.choice(candidates, size=3, replace=False, p=weights))
    a, b, c = int(cuts[0]), int(cuts[1]), int(cuts[2])

    seg1 = tour[:a]
    seg2 = tour[a:b]
    seg3 = tour[b:c]
    seg4 = tour[c:]

    # Reconnect: seg1 + seg3 + seg2 + seg4  (double-bridge)
    return seg1 + seg3 + seg2 + seg4


# ---------------------------------------------------------------------------
# Tour validation
# ---------------------------------------------------------------------------

def _validate_tour(tour, n):
    """Quick validation that a tour is a valid Hamiltonian cycle.

    Parameters
    ----------
    tour : list[int]
    n : int
        Expected number of nodes.

    Raises
    ------
    ValueError
        If the tour is invalid.
    """
    if len(tour) != n:
        raise ValueError(
            f"Tour length {len(tour)} does not match node count {n}."
        )
    if set(tour) != set(range(n)):
        missing = set(range(n)) - set(tour)
        extra = set(tour) - set(range(n))
        raise ValueError(
            f"Invalid tour. Missing nodes: {missing}, "
            f"extra/duplicate nodes: {extra}."
        )


# ---------------------------------------------------------------------------
# Main solver entry point
# ---------------------------------------------------------------------------

def solve_traffic_aware(instance, time_limit=60.0, seed=42,
                        use_traffic=True, departure_time=8.0):
    """Solve ATSP with time-dependent costs via iterated local search.

    The solver runs an iterated local search (ILS) loop:
    1. Construct an initial tour using time-dependent nearest-neighbour.
    2. Improve the tour with 2-opt and or-opt under time-dependent costs.
    3. Perturb the tour (traffic-biased double-bridge).
    4. Improve again and accept if better.
    5. Repeat until the time limit is exhausted.

    When ``use_traffic=False``, the solver ignores the traffic model and
    evaluates tours using static base costs only.  This mode is provided
    for ablation studies comparing traffic-aware vs traffic-unaware ILS.

    Parameters
    ----------
    instance : dict
        Standard ATSP instance dict.  Must contain a ``traffic_model``
        field (use ``add_traffic_weights`` first) unless
        ``use_traffic=False``, in which case only ``cost_matrix`` is
        required.
    time_limit : float
        Maximum wall-clock time in seconds.
    seed : int
        Random seed for reproducibility.
    use_traffic : bool
        If True, evaluate costs with the time-dependent model.
        If False, use static base costs (ablation mode).
    departure_time : float
        Vehicle departure time in hours (0-24 clock).

    Returns
    -------
    dict
        Result dictionary with keys:
        - ``tour`` : list[int] -- best tour found.
        - ``cost`` : float -- cost of the best tour (static base cost
          for comparability with other solvers).
        - ``traffic_cost`` : float -- time-dependent cost of the best
          tour (only meaningful when ``use_traffic=True``).
        - ``runtime_seconds`` : float -- elapsed wall-clock time.
        - ``solver_params`` : dict -- parameters used.
        - ``solver_name`` : str -- ``'traffic_aware_ils'``.
        - ``iterations`` : int -- number of ILS iterations completed.
    """
    start_time = time.time()
    rng = np.random.RandomState(seed)

    # -----------------------------------------------------------------------
    # Parse and prepare matrices
    # -----------------------------------------------------------------------
    base_matrix = np.asarray(instance["cost_matrix"], dtype=np.float64)
    n = base_matrix.shape[0]

    # Build or retrieve traffic model
    if use_traffic:
        if "traffic_model" not in instance:
            raise ValueError(
                "Instance has no 'traffic_model' field. "
                "Call add_traffic_weights() first, or set use_traffic=False."
            )
        traffic_model = instance["traffic_model"]
        # Ensure base_cost_matrix in the traffic model is a numpy array
        if not isinstance(traffic_model.get("base_cost_matrix"), np.ndarray):
            traffic_model = dict(traffic_model)
            traffic_model["base_cost_matrix"] = np.asarray(
                traffic_model["base_cost_matrix"], dtype=np.float64
            )
    else:
        # Create a dummy traffic model with multiplier == 1 everywhere
        traffic_model = {
            "base_cost_matrix": base_matrix,
            "rush_hour_peak": 0.0,
            "rush_hour_spread": 1.0,
            "peak_multiplier": 1.0,
        }

    # -----------------------------------------------------------------------
    # Trivial instances
    # -----------------------------------------------------------------------
    if n <= 1:
        return {
            "tour": list(range(n)),
            "cost": 0.0,
            "traffic_cost": 0.0,
            "runtime_seconds": time.time() - start_time,
            "solver_params": {
                "time_limit": time_limit,
                "seed": seed,
                "use_traffic": use_traffic,
                "departure_time": departure_time,
            },
            "solver_name": "traffic_aware_ils",
            "iterations": 0,
        }

    if n == 2:
        tour = [0, 1]
        static_cost = compute_tour_cost(tour, base_matrix)
        td_cost = compute_time_dependent_cost(tour, base_matrix,
                                              traffic_model, departure_time)
        return {
            "tour": tour,
            "cost": static_cost,
            "traffic_cost": td_cost,
            "runtime_seconds": time.time() - start_time,
            "solver_params": {
                "time_limit": time_limit,
                "seed": seed,
                "use_traffic": use_traffic,
                "departure_time": departure_time,
            },
            "solver_name": "traffic_aware_ils",
            "iterations": 0,
        }

    time_deadline = start_time + time_limit

    # -----------------------------------------------------------------------
    # Phase 1: Construct initial tour
    # -----------------------------------------------------------------------
    if use_traffic:
        best_tour, best_td_cost = _best_nn_tour_traffic(
            base_matrix, traffic_model, departure_time
        )
    else:
        # Deterministic nearest-neighbour (best of all starts), static costs
        best_tour = None
        best_td_cost = np.inf
        for start in range(n):
            visited = np.zeros(n, dtype=bool)
            tour = [start]
            visited[start] = True
            current = start
            for _ in range(n - 1):
                row = base_matrix[current].copy()
                row[visited] = np.inf
                nxt = int(np.argmin(row))
                tour.append(nxt)
                visited[nxt] = True
                current = nxt
            td = compute_time_dependent_cost(tour, base_matrix,
                                             traffic_model, departure_time)
            if td < best_td_cost:
                best_td_cost = td
                best_tour = tour

    # -----------------------------------------------------------------------
    # Phase 2: Initial local search
    # -----------------------------------------------------------------------
    if time.time() < time_deadline:
        best_tour, best_td_cost = _local_search_td(
            best_tour, base_matrix, traffic_model, departure_time,
            time_deadline
        )

    iterations = 1

    # -----------------------------------------------------------------------
    # Phase 3: Iterated local search loop
    # -----------------------------------------------------------------------
    while time.time() < time_deadline:
        iterations += 1

        # Perturb
        if use_traffic:
            candidate = _perturb_tour_traffic(
                list(best_tour), base_matrix, traffic_model,
                departure_time, rng
            )
        else:
            # Standard double-bridge perturbation without traffic bias
            candidate = _perturb_double_bridge(list(best_tour), rng)

        # Local search on the perturbed tour
        if time.time() < time_deadline:
            candidate, cand_cost = _local_search_td(
                candidate, base_matrix, traffic_model, departure_time,
                time_deadline
            )
        else:
            cand_cost = compute_time_dependent_cost(
                candidate, base_matrix, traffic_model, departure_time
            )

        # Accept if improving
        if cand_cost < best_td_cost - 1e-10:
            best_tour = candidate
            best_td_cost = cand_cost

    # -----------------------------------------------------------------------
    # Final results
    # -----------------------------------------------------------------------
    elapsed = time.time() - start_time

    _validate_tour(best_tour, n)

    static_cost = compute_tour_cost(best_tour, base_matrix)
    td_cost = compute_time_dependent_cost(best_tour, base_matrix,
                                          traffic_model, departure_time)

    return {
        "tour": best_tour,
        "cost": static_cost,
        "traffic_cost": td_cost,
        "runtime_seconds": elapsed,
        "solver_params": {
            "time_limit": time_limit,
            "seed": seed,
            "use_traffic": use_traffic,
            "departure_time": departure_time,
            "rush_hour_peak": traffic_model["rush_hour_peak"],
            "rush_hour_spread": traffic_model["rush_hour_spread"],
            "peak_multiplier": traffic_model["peak_multiplier"],
        },
        "solver_name": "traffic_aware_ils",
        "iterations": iterations,
    }


# ---------------------------------------------------------------------------
# Helper: plain double-bridge for non-traffic mode
# ---------------------------------------------------------------------------

def _perturb_double_bridge(tour, rng):
    """Standard (non-traffic-biased) double-bridge perturbation.

    Parameters
    ----------
    tour : list[int]
    rng : np.random.RandomState

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
    return tour[:a] + tour[b:c] + tour[a:b] + tour[c:]


# ---------------------------------------------------------------------------
# Integration hook for the hybrid GNN-LK solver
# ---------------------------------------------------------------------------

def enhance_with_traffic(hybrid_result, instance, departure_time=8.0,
                         time_limit=30.0, seed=42):
    """Post-process a hybrid solver result with traffic-aware refinement.

    Takes the tour produced by any solver (e.g., the hybrid GNN-LK from
    ``src/solvers/hybrid_gnn_lk.py``) and refines it under the
    time-dependent cost model.

    This function is the integration point described in item_016: it
    accepts an existing tour, re-evaluates it under traffic conditions,
    and runs the traffic-aware ILS to search for improvements.

    Parameters
    ----------
    hybrid_result : dict
        Result dict from any solver with at least a ``tour`` key.
    instance : dict
        Instance dict with ``cost_matrix`` and ``traffic_model`` fields.
    departure_time : float
        Departure time in hours (0-24).
    time_limit : float
        Additional wall-clock seconds to spend on refinement.
    seed : int
        Random seed.

    Returns
    -------
    dict
        Updated result dict.  If the traffic-aware refinement improves
        the time-dependent cost, the tour is replaced; otherwise the
        original is returned with traffic cost annotations.
    """
    if "traffic_model" not in instance:
        raise ValueError(
            "Instance has no 'traffic_model'. "
            "Call add_traffic_weights() first."
        )

    base_matrix = np.asarray(instance["cost_matrix"], dtype=np.float64)
    traffic_model = instance["traffic_model"]
    if not isinstance(traffic_model.get("base_cost_matrix"), np.ndarray):
        traffic_model = dict(traffic_model)
        traffic_model["base_cost_matrix"] = np.asarray(
            traffic_model["base_cost_matrix"], dtype=np.float64
        )

    original_tour = hybrid_result["tour"]
    n = len(original_tour)

    # Evaluate the original tour under time-dependent costs
    original_td_cost = compute_time_dependent_cost(
        original_tour, base_matrix, traffic_model, departure_time
    )

    # Run traffic-aware ILS starting from the given tour
    start_time = time.time()
    time_deadline = start_time + time_limit
    rng = np.random.RandomState(seed)

    # Local search on the provided tour
    best_tour, best_td_cost = _local_search_td(
        original_tour, base_matrix, traffic_model, departure_time,
        time_deadline
    )

    # ILS loop
    iterations = 1
    while time.time() < time_deadline:
        iterations += 1

        candidate = _perturb_tour_traffic(
            list(best_tour), base_matrix, traffic_model,
            departure_time, rng
        )

        if time.time() < time_deadline:
            candidate, cand_cost = _local_search_td(
                candidate, base_matrix, traffic_model, departure_time,
                time_deadline
            )
        else:
            cand_cost = compute_time_dependent_cost(
                candidate, base_matrix, traffic_model, departure_time
            )

        if cand_cost < best_td_cost - 1e-10:
            best_tour = candidate
            best_td_cost = cand_cost

    _validate_tour(best_tour, n)

    static_cost = compute_tour_cost(best_tour, base_matrix)

    result = dict(hybrid_result)
    result["tour"] = best_tour
    result["cost"] = static_cost
    result["traffic_cost"] = best_td_cost
    result["traffic_refinement"] = {
        "original_traffic_cost": original_td_cost,
        "refined_traffic_cost": best_td_cost,
        "improvement_pct": (
            (original_td_cost - best_td_cost) / original_td_cost * 100.0
            if original_td_cost > 0 else 0.0
        ),
        "refinement_iterations": iterations,
        "refinement_time_seconds": time.time() - start_time,
    }
    result["solver_name"] = (
        result.get("solver_name", "unknown") + "+traffic_refinement"
    )

    return result


# ---------------------------------------------------------------------------
# CLI entry point for quick testing
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    import sys
    import os

    print("=== Traffic-Aware ILS Solver Self-Test ===\n")

    for n_nodes in [10, 20, 50]:
        print(f"--- Instance: n={n_nodes} ---")

        # Create a synthetic ATSP instance
        rng = np.random.RandomState(42)
        # Use travel times in hours (small values for realism).
        # E.g., inter-city distances that take 0.1 to 1.0 hours.
        cm = rng.uniform(0.1, 1.0, size=(n_nodes, n_nodes))
        np.fill_diagonal(cm, 0.0)

        instance = {
            "cost_matrix": cm.tolist(),
            "metadata": {"n_nodes": n_nodes, "source": "synthetic"},
        }

        # Add traffic weights
        instance = add_traffic_weights(
            instance,
            rush_hour_peak=8.0,
            rush_hour_spread=2.0,
            peak_multiplier=1.5,
        )

        # Solve with traffic
        result_traffic = solve_traffic_aware(
            instance, time_limit=5.0, seed=42,
            use_traffic=True, departure_time=8.0,
        )

        # Solve without traffic (ablation)
        result_static = solve_traffic_aware(
            instance, time_limit=5.0, seed=42,
            use_traffic=False, departure_time=8.0,
        )

        print(f"  Traffic-aware:")
        print(f"    Static cost   : {result_traffic['cost']:.4f}")
        print(f"    Traffic cost  : {result_traffic['traffic_cost']:.4f}")
        print(f"    Iterations    : {result_traffic['iterations']}")
        print(f"    Runtime       : {result_traffic['runtime_seconds']:.3f}s")
        print(f"  Static (ablation):")
        print(f"    Static cost   : {result_static['cost']:.4f}")
        print(f"    Traffic cost  : {result_static['traffic_cost']:.4f}")
        print(f"    Iterations    : {result_static['iterations']}")
        print(f"    Runtime       : {result_static['runtime_seconds']:.3f}s")

        # Test enhance_with_traffic integration
        mock_hybrid_result = {
            "tour": result_static["tour"],
            "cost": result_static["cost"],
            "solver_name": "mock_hybrid",
        }
        enhanced = enhance_with_traffic(
            mock_hybrid_result, instance,
            departure_time=8.0, time_limit=3.0, seed=42,
        )
        print(f"  Enhanced (from static tour):")
        print(f"    Traffic cost  : {enhanced['traffic_cost']:.4f}")
        print(f"    Improvement   : "
              f"{enhanced['traffic_refinement']['improvement_pct']:.2f}%")
        print(f"    Solver name   : {enhanced['solver_name']}")
        print()

    print("All tests passed.")

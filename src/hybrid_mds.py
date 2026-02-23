"""
Hybrid MDS algorithm combining separator decomposition, LP rounding, and local search.

Pipeline:
1. Planar LP for lower bound and initial fractional solution
2. Separator-based rounding using decomposition
3. Local search refinement
4. Best-of-all selection among individual algorithms
"""

import time
from src.graph import Graph
from src.greedy import greedy_dominating_set, modified_greedy_dominating_set
from src.lp_solver import solve_lp_relaxation, lp_rounding_dominating_set
from src.planar_lp import planar_lp_rounding
from src.separator_mds import separator_mds
from src.local_search import local_search


def hybrid_mds(graph, separator_threshold=200, local_search_depth=100,
               use_lp=True, use_separator=True, use_local_search=True):
    """Hybrid MDS algorithm.

    Runs multiple strategies and returns the best solution:
    1. Greedy + local search
    2. Separator-based + local search
    3. Planar LP rounding + local search
    4. Best of all

    Args:
        graph: Planar graph
        separator_threshold: Base case size for separator ILP
        local_search_depth: Max iterations for local search
        use_lp: Whether to include LP-based methods
        use_separator: Whether to include separator method
        use_local_search: Whether to apply local search refinement

    Returns:
        (best_ds, lp_lower_bound, metadata)
    """
    if graph.n == 0:
        return set(), 0.0, {'algorithm': 'empty', 'candidates': {}}

    candidates = {}

    # Strategy 1: Greedy + local search
    ds_greedy = greedy_dominating_set(graph)
    if use_local_search:
        ds_greedy = local_search(graph, ds_greedy,
                                 max_iterations=local_search_depth,
                                 use_2swap=(graph.n <= 2000))
    candidates['greedy+ls'] = ds_greedy

    # Strategy 2: Modified greedy + local search
    if graph.n <= 5000:
        ds_mod = modified_greedy_dominating_set(graph)
        if use_local_search:
            ds_mod = local_search(graph, ds_mod,
                                  max_iterations=local_search_depth,
                                  use_2swap=(graph.n <= 2000))
        candidates['modified_greedy+ls'] = ds_mod

    # Strategy 3: Separator-based + local search
    if use_separator:
        ds_sep = separator_mds(graph, threshold=separator_threshold)
        if use_local_search:
            ds_sep = local_search(graph, ds_sep,
                                  max_iterations=local_search_depth,
                                  use_2swap=(graph.n <= 2000))
        candidates['separator+ls'] = ds_sep

    # Strategy 4: Planar LP rounding + local search
    lp_lower_bound = 0.0
    if use_lp and graph.n <= 5000:
        try:
            ds_plp, lp_lb = planar_lp_rounding(graph)
            lp_lower_bound = lp_lb
            if use_local_search:
                ds_plp = local_search(graph, ds_plp,
                                      max_iterations=local_search_depth,
                                      use_2swap=(graph.n <= 2000))
            candidates['planar_lp+ls'] = ds_plp
        except Exception:
            pass

    # Get LP lower bound if not computed yet
    if lp_lower_bound == 0.0 and graph.n <= 5000:
        try:
            lp_val, _ = solve_lp_relaxation(graph)
            lp_lower_bound = lp_val
        except Exception:
            pass

    # Select best candidate
    best_name = None
    best_ds = None
    best_size = float('inf')

    for name, ds in candidates.items():
        if graph.is_dominating_set(ds) and len(ds) < best_size:
            best_size = len(ds)
            best_ds = ds
            best_name = name

    if best_ds is None:
        # Fallback
        best_ds = set(graph.nodes)
        best_name = 'fallback'

    metadata = {
        'algorithm': best_name,
        'candidates': {name: len(ds) for name, ds in candidates.items()},
    }

    return best_ds, lp_lower_bound, metadata

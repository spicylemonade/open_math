"""
k-swap local search post-processing to reduce dominating set size.

Implements:
1. 1-swap: try removing each vertex and check if domination maintained
2. 2-swap: try replacing pairs with single vertices
"""


def one_swap_reduce(graph, ds, max_iterations=100):
    """1-swap local search: remove redundant vertices.

    Repeatedly scan the dominating set and remove any vertex whose
    removal does not break domination.

    Returns improved dominating set.
    """
    ds = set(ds)
    improved = True
    iteration = 0

    while improved and iteration < max_iterations:
        improved = False
        iteration += 1

        # Sort by degree (remove low-degree first — more likely redundant)
        for v in sorted(ds, key=lambda u: graph.degree(u)):
            candidate = ds - {v}
            if graph.is_dominating_set(candidate):
                ds = candidate
                improved = True
                break  # Restart scan after each removal

    return ds


def two_swap_reduce(graph, ds, max_iterations=50):
    """2-swap local search: replace pairs with single vertices.

    For each pair (u, v) in the dominating set, try removing both and
    adding a single vertex w not in ds that covers their combined
    contribution.

    Returns improved dominating set.
    """
    ds = set(ds)
    all_nodes = graph.nodes
    improved = True
    iteration = 0

    while improved and iteration < max_iterations:
        improved = False
        iteration += 1

        ds_list = sorted(ds, key=lambda u: graph.degree(u))
        for i in range(len(ds_list)):
            if improved:
                break
            u = ds_list[i]
            for j in range(i + 1, min(i + 20, len(ds_list))):
                v = ds_list[j]
                # Try removing both u and v
                candidate = ds - {u, v}

                # Check if some single vertex w can replace them
                # w must dominate everything that u and v were uniquely covering
                dominated_by_uv_only = set()
                for node in graph.closed_neighbors(u) | graph.closed_neighbors(v):
                    if node not in candidate:
                        # Check if node is dominated by rest of candidate
                        is_dominated = False
                        for nb in graph.closed_neighbors(node):
                            if nb in candidate:
                                is_dominated = True
                                break
                        if not is_dominated:
                            dominated_by_uv_only.add(node)

                if not dominated_by_uv_only:
                    # Both u and v are redundant; just remove them
                    ds = candidate
                    improved = True
                    break

                # Try to find a single vertex w that dominates all of dominated_by_uv_only
                for w in all_nodes:
                    if w in candidate:
                        continue
                    w_covers = graph.closed_neighbors(w)
                    if dominated_by_uv_only <= w_covers:
                        test = candidate | {w}
                        if graph.is_dominating_set(test):
                            ds = test
                            improved = True
                            break

                if improved:
                    break

    return ds


def local_search(graph, ds, max_iterations=100, use_2swap=True):
    """Combined local search: 1-swap then optionally 2-swap.

    Args:
        graph: Graph instance
        ds: Initial dominating set
        max_iterations: Max iterations per phase
        use_2swap: Whether to also apply 2-swap

    Returns:
        Improved dominating set.
    """
    ds = set(ds)
    original_size = len(ds)

    # Phase 1: 1-swap reduction
    ds = one_swap_reduce(graph, ds, max_iterations)

    # Phase 2: 2-swap reduction (if enabled and worthwhile)
    if use_2swap and len(ds) > 2:
        ds = two_swap_reduce(graph, ds, max_iterations=max_iterations // 2)

    # Phase 3: Final 1-swap cleanup
    ds = one_swap_reduce(graph, ds, max_iterations=20)

    return ds

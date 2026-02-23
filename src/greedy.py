"""
Baseline greedy and modified-greedy MDS algorithms.

Implements:
1. Standard greedy: repeatedly pick highest-degree undominated vertex
2. Modified greedy: degree-ratio selection (Jones et al. variant)
"""


def greedy_dominating_set(graph):
    """Standard greedy dominating set.

    Repeatedly selects the vertex that dominates the most new vertices
    (including itself if undominated). This is equivalent to the greedy
    algorithm for weighted set cover applied to MDS.

    Returns a set of vertices forming a dominating set.
    """
    dominated = set()
    ds = set()
    all_nodes = graph.nodes

    while dominated != all_nodes:
        best_v = None
        best_gain = -1
        for v in all_nodes:
            if v in ds:
                continue
            # Count how many new vertices v would dominate
            gain = len(graph.closed_neighbors(v) - dominated)
            if gain > best_gain:
                best_gain = gain
                best_v = v
        if best_v is None or best_gain == 0:
            # All remaining vertices are isolated and undominated
            for v in all_nodes - dominated:
                ds.add(v)
                dominated.add(v)
            break
        ds.add(best_v)
        dominated |= graph.closed_neighbors(best_v)

    return ds


def modified_greedy_dominating_set(graph):
    """Modified greedy with degree-ratio selection (Jones et al. variant).

    Instead of selecting the vertex with maximum new-domination gain,
    selects based on the ratio: gain / (1 + number of already-selected
    neighbors), favoring vertices that contribute more new coverage
    relative to their overlap with existing selections.

    Returns a set of vertices forming a dominating set.
    """
    dominated = set()
    ds = set()
    all_nodes = graph.nodes

    while dominated != all_nodes:
        best_v = None
        best_score = -1
        for v in all_nodes:
            if v in ds:
                continue
            gain = len(graph.closed_neighbors(v) - dominated)
            if gain == 0:
                continue
            # Penalize vertices with many already-selected neighbors
            overlap = len(graph.neighbors(v) & ds)
            score = gain / (1.0 + overlap)
            if score > best_score:
                best_score = score
                best_v = v
        if best_v is None:
            for v in all_nodes - dominated:
                ds.add(v)
                dominated.add(v)
            break
        ds.add(best_v)
        dominated |= graph.closed_neighbors(best_v)

    return ds

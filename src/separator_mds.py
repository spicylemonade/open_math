"""
Separator-based MDS algorithm for planar graphs.

Uses the Lipton-Tarjan planar separator theorem to decompose the graph,
includes separator vertices in the dominating set, solves sub-problems
exactly (small) or via greedy (large), then removes redundant vertices.
"""

from collections import deque
import networkx as nx
from src.graph import Graph
from src.lp_solver import solve_ilp_exact
from src.greedy import greedy_dominating_set


def compute_planar_separator(graph):
    """Compute a planar separator using BFS-based approach.

    Returns (separator, comp_a, comp_b) where separator is a set of vertices
    whose removal splits the remaining vertices into comp_a and comp_b,
    each with at most 2/3 of total vertices.
    """
    nxG = graph.to_networkx()

    if graph.n <= 10:
        # Too small to separate meaningfully
        return set(graph.nodes), set(), set()

    # Use NetworkX's node connectivity for a simple separator approach
    # We use BFS-layering based separator (practical Lipton-Tarjan)
    # Pick a BFS root and find a balanced layer cut

    # Find a vertex with reasonable centrality
    nodes = sorted(graph.nodes)
    root = nodes[0]

    # BFS to get layers
    dist = {root: 0}
    queue = deque([root])
    layers = {}
    max_layer = 0
    while queue:
        v = queue.popleft()
        d = dist[v]
        if d not in layers:
            layers[d] = []
        layers[d].append(v)
        max_layer = max(max_layer, d)
        for u in graph.neighbors(v):
            if u not in dist:
                dist[u] = d + 1
                queue.append(u)

    # Handle disconnected vertices
    for v in graph.nodes:
        if v not in dist:
            dist[v] = max_layer + 1
            if max_layer + 1 not in layers:
                layers[max_layer + 1] = []
            layers[max_layer + 1].append(v)
            max_layer += 1

    # Find best layer to cut: the one closest to n/2 cumulative
    n = graph.n
    target = n / 2
    cumulative = 0
    best_cut_layer = 0
    best_diff = n
    for d in range(max_layer + 1):
        cumulative += len(layers.get(d, []))
        diff = abs(cumulative - target)
        if diff < best_diff:
            best_diff = diff
            best_cut_layer = d

    # Separator = vertices at the cut layer
    separator = set(layers.get(best_cut_layer, []))

    # Also include adjacent layers if separator is too small for balance
    # This approximates the Lipton-Tarjan separator
    comp_a = set()
    comp_b = set()
    for d in range(max_layer + 1):
        for v in layers.get(d, []):
            if v in separator:
                continue
            if d < best_cut_layer:
                comp_a.add(v)
            else:
                comp_b.add(v)

    # If heavily imbalanced, include more layers in separator
    while max(len(comp_a), len(comp_b)) > 2 * n / 3 and len(separator) < n / 2:
        if len(comp_a) > len(comp_b):
            # Move the outermost layer of comp_a into separator
            max_d_a = max(dist[v] for v in comp_a) if comp_a else -1
            to_move = [v for v in comp_a if dist[v] == max_d_a]
            for v in to_move:
                comp_a.discard(v)
                separator.add(v)
        else:
            min_d_b = min(dist[v] for v in comp_b) if comp_b else max_layer + 1
            to_move = [v for v in comp_b if dist[v] == min_d_b]
            for v in to_move:
                comp_b.discard(v)
                separator.add(v)

    return separator, comp_a, comp_b


def separator_mds(graph, threshold=200):
    """Separator-based MDS algorithm.

    Args:
        graph: Planar graph
        threshold: Base-case size for exact ILP solve

    Returns:
        Set of vertices forming a dominating set.
    """
    if graph.n == 0:
        return set()

    # Handle connected components independently
    components = graph.connected_components()
    if len(components) > 1:
        result = set()
        for comp in components:
            if len(comp) == 1:
                result.update(comp)
                continue
            sg = graph.subgraph(comp)
            result |= separator_mds(sg, threshold)
        return result

    # Base case: solve exactly
    if graph.n <= threshold:
        opt_set, opt_val = solve_ilp_exact(graph, time_limit=60)
        if opt_set is not None:
            return opt_set
        return greedy_dominating_set(graph)

    # Compute separator
    separator, comp_a, comp_b = compute_planar_separator(graph)

    # Include all separator vertices
    ds = set(separator)

    # Find what's already dominated
    dominated = set(ds)
    for v in ds:
        dominated |= graph.closed_neighbors(v)

    # Solve sub-problems
    for comp in [comp_a, comp_b]:
        if not comp:
            continue

        # Check if component is fully dominated
        undom = comp - dominated
        if not undom:
            continue

        sg = graph.subgraph(comp)

        if sg.n <= threshold:
            opt_set, _ = solve_ilp_exact(sg, time_limit=60)
            if opt_set is not None:
                ds |= opt_set
            else:
                ds |= greedy_dominating_set(sg)
        else:
            ds |= greedy_dominating_set(sg)

        # Update dominated set
        for v in ds:
            dominated |= graph.closed_neighbors(v)

    # Fix any remaining undominated vertices
    for v in graph.nodes:
        if v not in dominated:
            ds.add(v)
            dominated |= graph.closed_neighbors(v)

    # Redundancy removal: try to remove each vertex
    ds_list = sorted(ds, key=lambda v: graph.degree(v))
    for v in ds_list:
        candidate = ds - {v}
        if graph.is_dominating_set(candidate):
            ds = candidate

    return ds

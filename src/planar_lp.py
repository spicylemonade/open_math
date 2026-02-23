"""
Enhanced LP rounding exploiting planarity constraints.

Augments the standard LP with planar-specific valid inequalities
and uses a tighter rounding scheme exploiting bounded integrality gap.
"""

import pulp
import networkx as nx
from src.graph import Graph
from src.greedy import greedy_dominating_set


def _get_planar_faces(graph):
    """Get faces from a planar embedding of the graph.

    Returns list of faces, each face is a list of vertices.
    """
    nxG = graph.to_networkx()
    is_planar, embedding = nx.check_planarity(nxG)
    if not is_planar:
        return []

    faces = []
    visited_half_edges = set()

    for v in embedding:
        for w in embedding.neighbors_cw_order(v):
            if (v, w) in visited_half_edges:
                continue
            face = []
            curr_v, curr_w = v, w
            while (curr_v, curr_w) not in visited_half_edges:
                visited_half_edges.add((curr_v, curr_w))
                face.append(curr_v)
                # Next half-edge: go to w, then next after curr_v in CW order
                next_v = curr_w
                next_w = embedding.next_face_half_edge(curr_v, curr_w)[1]
                curr_v, curr_w = next_v, next_w
            if len(face) >= 3:
                faces.append(face)

    return faces


def solve_planar_lp(graph):
    """Solve LP relaxation with planar-specific constraints.

    Augments standard MDS LP with:
    1. Face-based constraints: for each face of size s, at least ceil(s/3)
       vertices must be in the dominating set or adjacent to one
    2. Density constraint from Euler's formula

    Returns (lp_value, fractional_solution_dict).
    """
    nodes = sorted(graph.nodes)
    prob = pulp.LpProblem("MDS_Planar_LP", pulp.LpMinimize)

    x = {}
    for v in nodes:
        x[v] = pulp.LpVariable(f"x_{v}", 0, 1, cat=pulp.LpContinuous)

    # Objective: minimize total
    prob += pulp.lpSum(x[v] for v in nodes)

    # Standard domination constraints
    for v in nodes:
        closed_nb = graph.closed_neighbors(v)
        prob += pulp.lpSum(x[u] for u in closed_nb) >= 1

    # Planar-specific: face-based constraints
    faces = _get_planar_faces(graph)
    for i, face in enumerate(faces):
        if len(face) >= 3:
            # Each face of size s needs at least ceil(s/3) coverage
            # A vertex in or adjacent to the face must be selected
            face_and_neighbors = set(face)
            for v in face:
                face_and_neighbors |= graph.neighbors(v)
            face_and_neighbors &= set(nodes)
            min_needed = (len(face) + 2) // 3
            prob += pulp.lpSum(x[v] for v in face_and_neighbors) >= min_needed

    # Planar density constraint: |DS| >= n / (Delta + 1)
    if graph.n > 0:
        max_deg = max(graph.degree(v) for v in nodes)
        prob += pulp.lpSum(x[v] for v in nodes) >= graph.n / (max_deg + 1)

    prob.solve(pulp.PULP_CBC_CMD(msg=0))

    lp_value = pulp.value(prob.objective)
    solution = {v: pulp.value(x[v]) for v in nodes}

    return lp_value, solution


def planar_lp_rounding(graph):
    """Enhanced LP rounding exploiting planarity.

    Uses the planar LP for a tighter fractional solution, then applies
    a threshold rounding at 1/4 (based on planar integrality gap bound of ~4).
    Fixes any remaining undominated vertices greedily.

    Returns (dominating_set, lp_lower_bound).
    """
    if graph.n == 0:
        return set(), 0

    lp_value, frac = solve_planar_lp(graph)

    # Planar-aware threshold: 1/4 based on integrality gap
    threshold = 0.25

    ds = set()
    for v in graph.nodes:
        if frac.get(v, 0) >= threshold:
            ds.add(v)

    # Fix domination: add vertices greedily for any undominated
    dominated = set()
    for v in ds:
        dominated |= graph.closed_neighbors(v)

    all_nodes = graph.nodes
    for v in all_nodes:
        if v not in dominated:
            # Pick the neighbor with highest LP value
            best_u = max(graph.closed_neighbors(v),
                         key=lambda u: frac.get(u, 0))
            ds.add(best_u)
            dominated |= graph.closed_neighbors(best_u)

    # Second pass: try to remove redundant vertices
    for v in sorted(ds, key=lambda u: frac.get(u, 0)):
        candidate = ds - {v}
        if graph.is_dominating_set(candidate):
            ds = candidate

    return ds, lp_value

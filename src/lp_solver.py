"""
LP/ILP relaxation-based MDS solver with rounding.

Provides:
1. LP relaxation for lower bound
2. Deterministic threshold rounding
3. ILP exact solver for small instances
"""

import pulp


def solve_lp_relaxation(graph):
    """Solve LP relaxation of MDS.

    minimize sum x_v
    subject to: for all v: sum_{u in N[v]} x_u >= 1
                0 <= x_v <= 1

    Returns (lp_value, fractional_solution_dict).
    """
    nodes = sorted(graph.nodes)
    prob = pulp.LpProblem("MDS_LP", pulp.LpMinimize)

    x = {}
    for v in nodes:
        x[v] = pulp.LpVariable(f"x_{v}", 0, 1, cat=pulp.LpContinuous)

    # Objective
    prob += pulp.lpSum(x[v] for v in nodes)

    # Domination constraints
    for v in nodes:
        closed_nb = graph.closed_neighbors(v)
        prob += pulp.lpSum(x[u] for u in closed_nb) >= 1

    prob.solve(pulp.PULP_CBC_CMD(msg=0))

    lp_value = pulp.value(prob.objective)
    solution = {v: pulp.value(x[v]) for v in nodes}

    return lp_value, solution


def lp_rounding_dominating_set(graph, threshold=None):
    """LP rounding for MDS.

    Solves LP relaxation then rounds: include v if x_v >= threshold.
    Default threshold is 1/(max_degree + 1).
    If rounding leaves undominated vertices, add them greedily.

    Returns (dominating_set, lp_lower_bound).
    """
    lp_value, frac = solve_lp_relaxation(graph)

    if threshold is None:
        max_deg = max(graph.degree(v) for v in graph.nodes)
        threshold = 1.0 / (max_deg + 1)

    ds = set()
    for v in graph.nodes:
        if frac[v] >= threshold:
            ds.add(v)

    # Fix: ensure domination by adding missing vertices greedily
    dominated = set()
    for v in ds:
        dominated |= graph.closed_neighbors(v)

    for v in graph.nodes:
        if v not in dominated:
            # Add the vertex from N[v] with highest LP value
            best_u = max(graph.closed_neighbors(v),
                         key=lambda u: frac.get(u, 0))
            ds.add(best_u)
            dominated |= graph.closed_neighbors(best_u)

    return ds, lp_value


def solve_ilp_exact(graph, time_limit=300):
    """Solve MDS exactly via ILP.

    minimize sum x_v
    subject to: for all v: sum_{u in N[v]} x_u >= 1
                x_v in {0, 1}

    Returns (optimal_set, optimal_value) or (None, None) if infeasible/timeout.
    """
    nodes = sorted(graph.nodes)
    prob = pulp.LpProblem("MDS_ILP", pulp.LpMinimize)

    x = {}
    for v in nodes:
        x[v] = pulp.LpVariable(f"x_{v}", 0, 1, cat=pulp.LpBinary)

    prob += pulp.lpSum(x[v] for v in nodes)

    for v in nodes:
        closed_nb = graph.closed_neighbors(v)
        prob += pulp.lpSum(x[u] for u in closed_nb) >= 1

    solver = pulp.PULP_CBC_CMD(msg=0, timeLimit=time_limit)
    prob.solve(solver)

    if prob.status != pulp.constants.LpStatusOptimal:
        return None, None

    opt_set = {v for v in nodes if pulp.value(x[v]) > 0.5}
    opt_value = len(opt_set)

    return opt_set, opt_value

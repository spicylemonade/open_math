"""Tests for src/lp_solver.py — LP/ILP MDS solver."""

import pytest
from src.graph import (
    Graph, generate_path_graph, generate_cycle_graph, generate_grid_graph,
    generate_random_planar_graph, generate_delaunay_planar_graph,
)
from src.lp_solver import solve_lp_relaxation, lp_rounding_dominating_set, solve_ilp_exact


class TestLPRelaxation:
    def test_path_5_lower_bound(self):
        g = generate_path_graph(5)
        lp_val, frac = solve_lp_relaxation(g)
        # OPT for P_5 is 2, LP should give <= 2
        assert lp_val <= 2.0 + 0.01
        assert lp_val > 0

    def test_cycle_6_lower_bound(self):
        g = generate_cycle_graph(6)
        lp_val, frac = solve_lp_relaxation(g)
        # OPT for C_6 is 2, LP should give <= 2
        assert lp_val <= 2.0 + 0.01

    def test_grid_3x3(self):
        g = generate_grid_graph(3, 3)
        lp_val, frac = solve_lp_relaxation(g)
        assert lp_val > 0
        assert all(0 <= v <= 1 for v in frac.values())


class TestLPRounding:
    def test_path_5_valid(self):
        g = generate_path_graph(5)
        ds, lb = lp_rounding_dominating_set(g)
        assert g.is_dominating_set(ds)

    def test_cycle_10_valid(self):
        g = generate_cycle_graph(10)
        ds, lb = lp_rounding_dominating_set(g)
        assert g.is_dominating_set(ds)

    def test_grid_3x3_valid(self):
        g = generate_grid_graph(3, 3)
        ds, lb = lp_rounding_dominating_set(g)
        assert g.is_dominating_set(ds)

    def test_grid_5x5_valid(self):
        g = generate_grid_graph(5, 5)
        ds, lb = lp_rounding_dominating_set(g)
        assert g.is_dominating_set(ds)

    def test_random_planar_50_valid(self):
        g = generate_random_planar_graph(50, seed=42)
        ds, lb = lp_rounding_dominating_set(g)
        assert g.is_dominating_set(ds)

    def test_random_planar_100_valid(self):
        g = generate_random_planar_graph(100, seed=42)
        ds, lb = lp_rounding_dominating_set(g)
        assert g.is_dominating_set(ds)

    def test_delaunay_50_valid(self):
        g = generate_delaunay_planar_graph(50, seed=42)
        ds, lb = lp_rounding_dominating_set(g)
        assert g.is_dominating_set(ds)


class TestILPExact:
    def test_path_5_optimal(self):
        g = generate_path_graph(5)
        opt_set, opt_val = solve_ilp_exact(g)
        assert opt_val == 2
        assert g.is_dominating_set(opt_set)

    def test_cycle_6_optimal(self):
        g = generate_cycle_graph(6)
        opt_set, opt_val = solve_ilp_exact(g)
        assert opt_val == 2
        assert g.is_dominating_set(opt_set)

    def test_star_optimal(self):
        g = Graph()
        for i in range(6):
            g.add_node(i)
        for i in range(1, 6):
            g.add_edge(0, i)
        opt_set, opt_val = solve_ilp_exact(g)
        assert opt_val == 1
        assert g.is_dominating_set(opt_set)

    def test_grid_3x3_optimal(self):
        g = generate_grid_graph(3, 3)
        opt_set, opt_val = solve_ilp_exact(g)
        assert g.is_dominating_set(opt_set)
        assert opt_val <= 3  # known optimal for 3x3 grid

    def test_lp_bound_leq_ilp(self):
        g = generate_grid_graph(4, 4)
        lp_val, _ = solve_lp_relaxation(g)
        _, ilp_val = solve_ilp_exact(g)
        assert lp_val <= ilp_val + 0.01

    def test_random_planar_30(self):
        g = generate_random_planar_graph(30, seed=42)
        opt_set, opt_val = solve_ilp_exact(g)
        assert g.is_dominating_set(opt_set)
        assert opt_val > 0

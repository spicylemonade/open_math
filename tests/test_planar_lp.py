"""Tests for src/planar_lp.py — enhanced planar LP rounding."""

import pytest
from src.graph import (
    Graph, generate_path_graph, generate_cycle_graph, generate_grid_graph,
    generate_random_planar_graph, generate_delaunay_planar_graph,
)
from src.planar_lp import planar_lp_rounding, solve_planar_lp
from src.lp_solver import lp_rounding_dominating_set


class TestPlanarLP:
    def test_lb_at_least_standard(self):
        """Planar LP should give at least as tight a bound as standard LP."""
        g = generate_grid_graph(5, 5)
        planar_val, _ = solve_planar_lp(g)
        from src.lp_solver import solve_lp_relaxation
        std_val, _ = solve_lp_relaxation(g)
        # Planar LP has more constraints, so its value should be >= standard
        assert planar_val >= std_val - 0.01


class TestPlanarLPRoundingValidity:
    def test_path_5(self):
        g = generate_path_graph(5)
        ds, lb = planar_lp_rounding(g)
        assert g.is_dominating_set(ds)

    def test_cycle_10(self):
        g = generate_cycle_graph(10)
        ds, lb = planar_lp_rounding(g)
        assert g.is_dominating_set(ds)

    def test_grid_3x3(self):
        g = generate_grid_graph(3, 3)
        ds, lb = planar_lp_rounding(g)
        assert g.is_dominating_set(ds)

    def test_grid_5x5(self):
        g = generate_grid_graph(5, 5)
        ds, lb = planar_lp_rounding(g)
        assert g.is_dominating_set(ds)

    def test_random_planar_50(self):
        g = generate_random_planar_graph(50, seed=42)
        ds, lb = planar_lp_rounding(g)
        assert g.is_dominating_set(ds)

    def test_random_planar_100(self):
        g = generate_random_planar_graph(100, seed=42)
        ds, lb = planar_lp_rounding(g)
        assert g.is_dominating_set(ds)

    def test_delaunay_50(self):
        g = generate_delaunay_planar_graph(50, seed=42)
        ds, lb = planar_lp_rounding(g)
        assert g.is_dominating_set(ds)

    def test_delaunay_100(self):
        g = generate_delaunay_planar_graph(100, seed=42)
        ds, lb = planar_lp_rounding(g)
        assert g.is_dominating_set(ds)

    def test_empty(self):
        g = Graph()
        ds, lb = planar_lp_rounding(g)
        assert len(ds) == 0


class TestPlanarLPImprovement:
    def test_better_than_standard_on_some(self):
        """Planar LP rounding should be better than standard on most instances."""
        better_count = 0
        total = 0
        for seed in range(42, 52):
            g = generate_delaunay_planar_graph(100, seed=seed)
            std_ds, std_lb = lp_rounding_dominating_set(g)
            planar_ds, planar_lb = planar_lp_rounding(g)

            assert g.is_dominating_set(planar_ds)
            total += 1
            if len(planar_ds) <= len(std_ds):
                better_count += 1

        # Should be better on at least 80% of instances
        assert better_count >= 8, f"Only better on {better_count}/{total} instances"

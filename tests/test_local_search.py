"""Tests for src/local_search.py — local search post-processing."""

import pytest
from src.graph import (
    Graph, generate_path_graph, generate_cycle_graph, generate_grid_graph,
    generate_random_planar_graph, generate_delaunay_planar_graph,
)
from src.local_search import one_swap_reduce, two_swap_reduce, local_search
from src.greedy import greedy_dominating_set


class TestOneSwap:
    def test_reduces_redundant(self):
        g = generate_path_graph(5)
        # Start with all vertices as DS (very redundant)
        ds = set(g.nodes)
        reduced = one_swap_reduce(g, ds)
        assert g.is_dominating_set(reduced)
        assert len(reduced) < len(ds)

    def test_preserves_validity(self):
        g = generate_grid_graph(5, 5)
        ds = greedy_dominating_set(g)
        reduced = one_swap_reduce(g, ds)
        assert g.is_dominating_set(reduced)
        assert len(reduced) <= len(ds)


class TestTwoSwap:
    def test_preserves_validity(self):
        g = generate_grid_graph(4, 4)
        ds = greedy_dominating_set(g)
        reduced = two_swap_reduce(g, ds)
        assert g.is_dominating_set(reduced)
        assert len(reduced) <= len(ds)


class TestLocalSearch:
    def test_improves_greedy_on_grid(self):
        g = generate_grid_graph(5, 5)
        ds = greedy_dominating_set(g)
        improved = local_search(g, ds)
        assert g.is_dominating_set(improved)
        assert len(improved) <= len(ds)

    def test_improves_greedy_on_delaunay(self):
        g = generate_delaunay_planar_graph(100, seed=42)
        ds = greedy_dominating_set(g)
        improved = local_search(g, ds)
        assert g.is_dominating_set(improved)
        assert len(improved) <= len(ds)

    def test_average_improvement(self):
        """Test that local search improves greedy by >= 2% on average."""
        total_improvement = 0
        count = 0
        for seed in range(42, 92):
            g = generate_delaunay_planar_graph(100, seed=seed)
            ds = greedy_dominating_set(g)
            improved = local_search(g, ds)
            assert g.is_dominating_set(improved)
            if len(ds) > 0:
                pct = (len(ds) - len(improved)) / len(ds) * 100
                total_improvement += pct
                count += 1

        avg_improvement = total_improvement / count if count > 0 else 0
        assert avg_improvement >= 2.0, f"Average improvement only {avg_improvement:.1f}%"

    def test_path_optimal(self):
        g = generate_path_graph(10)
        ds = set(g.nodes)  # start with all
        improved = local_search(g, ds)
        assert g.is_dominating_set(improved)
        # Should reduce significantly from n=10
        assert len(improved) <= 5

    def test_no_worse_than_input(self):
        for seed in [42, 43, 44]:
            g = generate_random_planar_graph(100, seed=seed)
            ds = greedy_dominating_set(g)
            improved = local_search(g, ds)
            assert g.is_dominating_set(improved)
            assert len(improved) <= len(ds)

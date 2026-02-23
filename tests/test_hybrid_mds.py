"""Tests for src/hybrid_mds.py — hybrid MDS algorithm."""

import time
import pytest
from src.graph import (
    Graph, generate_path_graph, generate_cycle_graph, generate_grid_graph,
    generate_random_planar_graph, generate_delaunay_planar_graph,
)
from src.hybrid_mds import hybrid_mds
from src.greedy import greedy_dominating_set
from src.lp_solver import lp_rounding_dominating_set
from src.separator_mds import separator_mds


class TestHybridValidity:
    def test_path_5(self):
        g = generate_path_graph(5)
        ds, lb, meta = hybrid_mds(g)
        assert g.is_dominating_set(ds)

    def test_cycle_10(self):
        g = generate_cycle_graph(10)
        ds, lb, meta = hybrid_mds(g)
        assert g.is_dominating_set(ds)

    def test_grid_5x5(self):
        g = generate_grid_graph(5, 5)
        ds, lb, meta = hybrid_mds(g)
        assert g.is_dominating_set(ds)

    def test_random_planar_100(self):
        g = generate_random_planar_graph(100, seed=42)
        ds, lb, meta = hybrid_mds(g)
        assert g.is_dominating_set(ds)

    def test_delaunay_100(self):
        g = generate_delaunay_planar_graph(100, seed=42)
        ds, lb, meta = hybrid_mds(g)
        assert g.is_dominating_set(ds)

    def test_empty(self):
        g = Graph()
        ds, lb, meta = hybrid_mds(g)
        assert len(ds) == 0


class TestHybridQuality:
    def test_at_least_as_good_as_greedy(self):
        """Hybrid should be at least as good as greedy on ≥95% of instances."""
        better_or_equal = 0
        total = 20
        for seed in range(42, 42 + total):
            g = generate_delaunay_planar_graph(100, seed=seed)
            greedy_ds = greedy_dominating_set(g)
            hybrid_ds, _, _ = hybrid_mds(g)
            assert g.is_dominating_set(hybrid_ds)
            if len(hybrid_ds) <= len(greedy_ds):
                better_or_equal += 1

        pct = better_or_equal / total
        assert pct >= 0.95, f"Only better/equal on {pct*100:.0f}% of instances"

    def test_at_least_as_good_as_lp(self):
        """Hybrid should be at least as good as standard LP on ≥95% of instances."""
        better_or_equal = 0
        total = 20
        for seed in range(42, 42 + total):
            g = generate_delaunay_planar_graph(100, seed=seed)
            lp_ds, _ = lp_rounding_dominating_set(g)
            hybrid_ds, _, _ = hybrid_mds(g)
            assert g.is_dominating_set(hybrid_ds)
            if len(hybrid_ds) <= len(lp_ds):
                better_or_equal += 1

        pct = better_or_equal / total
        assert pct >= 0.95, f"Only better/equal on {pct*100:.0f}% of instances"

    def test_at_least_as_good_as_separator(self):
        """Hybrid should be at least as good as separator on ≥95% of instances."""
        better_or_equal = 0
        total = 20
        for seed in range(42, 42 + total):
            g = generate_delaunay_planar_graph(100, seed=seed)
            sep_ds = separator_mds(g, threshold=50)
            hybrid_ds, _, _ = hybrid_mds(g, separator_threshold=50)
            assert g.is_dominating_set(hybrid_ds)
            if len(hybrid_ds) <= len(sep_ds):
                better_or_equal += 1

        pct = better_or_equal / total
        assert pct >= 0.95, f"Only better/equal on {pct*100:.0f}% of instances"


class TestHybridRuntime:
    def test_reasonable_runtime(self):
        g = generate_delaunay_planar_graph(500, seed=42)
        start = time.time()
        ds, lb, meta = hybrid_mds(g)
        elapsed = time.time() - start
        assert g.is_dominating_set(ds)
        assert elapsed < 60

    def test_metadata(self):
        g = generate_grid_graph(5, 5)
        ds, lb, meta = hybrid_mds(g)
        assert 'algorithm' in meta
        assert 'candidates' in meta
        assert len(meta['candidates']) >= 3

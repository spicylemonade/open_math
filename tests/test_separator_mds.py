"""Tests for src/separator_mds.py — separator-based MDS algorithm."""

import time
import pytest
from src.graph import (
    Graph, generate_path_graph, generate_cycle_graph, generate_grid_graph,
    generate_random_planar_graph, generate_delaunay_planar_graph,
)
from src.separator_mds import separator_mds, compute_planar_separator
from src.greedy import greedy_dominating_set


class TestSeparator:
    def test_separator_splits(self):
        g = generate_grid_graph(10, 10)
        sep, a, b = compute_planar_separator(g)
        assert len(sep) > 0
        assert len(sep) + len(a) + len(b) == g.n
        # No vertex in both a and b
        assert len(a & b) == 0

    def test_separator_balance(self):
        g = generate_grid_graph(10, 10)
        n = g.n
        sep, a, b = compute_planar_separator(g)
        assert max(len(a), len(b)) <= 2 * n / 3 + len(sep)


class TestSeparatorMDSValidity:
    def test_path_10(self):
        g = generate_path_graph(10)
        ds = separator_mds(g, threshold=20)
        assert g.is_dominating_set(ds)

    def test_cycle_10(self):
        g = generate_cycle_graph(10)
        ds = separator_mds(g, threshold=20)
        assert g.is_dominating_set(ds)

    def test_grid_3x3(self):
        g = generate_grid_graph(3, 3)
        ds = separator_mds(g, threshold=20)
        assert g.is_dominating_set(ds)

    def test_grid_5x5(self):
        g = generate_grid_graph(5, 5)
        ds = separator_mds(g, threshold=50)
        assert g.is_dominating_set(ds)

    def test_grid_10x10(self):
        g = generate_grid_graph(10, 10)
        ds = separator_mds(g, threshold=50)
        assert g.is_dominating_set(ds)

    def test_random_planar_50(self):
        g = generate_random_planar_graph(50, seed=42)
        ds = separator_mds(g, threshold=60)
        assert g.is_dominating_set(ds)

    def test_random_planar_100(self):
        g = generate_random_planar_graph(100, seed=42)
        ds = separator_mds(g, threshold=50)
        assert g.is_dominating_set(ds)

    def test_delaunay_100(self):
        g = generate_delaunay_planar_graph(100, seed=42)
        ds = separator_mds(g, threshold=50)
        assert g.is_dominating_set(ds)

    def test_random_planar_500(self):
        g = generate_random_planar_graph(500, seed=42)
        ds = separator_mds(g, threshold=100)
        assert g.is_dominating_set(ds)

    def test_empty(self):
        g = Graph()
        ds = separator_mds(g)
        assert len(ds) == 0


class TestSeparatorMDSPerformance:
    def test_runtime_reasonable(self):
        g = generate_random_planar_graph(500, seed=42)
        start = time.time()
        ds = separator_mds(g, threshold=100)
        elapsed = time.time() - start
        assert g.is_dominating_set(ds)
        assert elapsed < 60  # should be much faster

    def test_not_much_worse_than_greedy(self):
        g = generate_delaunay_planar_graph(200, seed=42)
        greedy_ds = greedy_dominating_set(g)
        sep_ds = separator_mds(g, threshold=100)
        assert g.is_dominating_set(sep_ds)
        # Separator should not be more than 10x worse
        assert len(sep_ds) < 10 * len(greedy_ds)

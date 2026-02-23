"""Tests for src/greedy.py — greedy MDS algorithms."""

import pytest
from src.graph import (
    Graph, generate_path_graph, generate_cycle_graph, generate_grid_graph,
    generate_random_planar_graph, generate_delaunay_planar_graph,
)
from src.greedy import greedy_dominating_set, modified_greedy_dominating_set


class TestGreedyValidity:
    """Test that greedy produces valid dominating sets."""

    def test_path_5(self):
        g = generate_path_graph(5)
        ds = greedy_dominating_set(g)
        assert g.is_dominating_set(ds)

    def test_path_10(self):
        g = generate_path_graph(10)
        ds = greedy_dominating_set(g)
        assert g.is_dominating_set(ds)

    def test_cycle_6(self):
        g = generate_cycle_graph(6)
        ds = greedy_dominating_set(g)
        assert g.is_dominating_set(ds)

    def test_cycle_10(self):
        g = generate_cycle_graph(10)
        ds = greedy_dominating_set(g)
        assert g.is_dominating_set(ds)

    def test_grid_3x3(self):
        g = generate_grid_graph(3, 3)
        ds = greedy_dominating_set(g)
        assert g.is_dominating_set(ds)

    def test_grid_5x5(self):
        g = generate_grid_graph(5, 5)
        ds = greedy_dominating_set(g)
        assert g.is_dominating_set(ds)

    def test_random_planar_50(self):
        g = generate_random_planar_graph(50, seed=42)
        ds = greedy_dominating_set(g)
        assert g.is_dominating_set(ds)

    def test_random_planar_100(self):
        g = generate_random_planar_graph(100, seed=42)
        ds = greedy_dominating_set(g)
        assert g.is_dominating_set(ds)

    def test_delaunay_50(self):
        g = generate_delaunay_planar_graph(50, seed=42)
        ds = greedy_dominating_set(g)
        assert g.is_dominating_set(ds)

    def test_single_node(self):
        g = Graph()
        g.add_node(0)
        ds = greedy_dominating_set(g)
        assert g.is_dominating_set(ds)
        assert len(ds) == 1


class TestModifiedGreedyValidity:
    """Test that modified greedy produces valid dominating sets."""

    def test_path_5(self):
        g = generate_path_graph(5)
        ds = modified_greedy_dominating_set(g)
        assert g.is_dominating_set(ds)

    def test_path_10(self):
        g = generate_path_graph(10)
        ds = modified_greedy_dominating_set(g)
        assert g.is_dominating_set(ds)

    def test_cycle_6(self):
        g = generate_cycle_graph(6)
        ds = modified_greedy_dominating_set(g)
        assert g.is_dominating_set(ds)

    def test_grid_3x3(self):
        g = generate_grid_graph(3, 3)
        ds = modified_greedy_dominating_set(g)
        assert g.is_dominating_set(ds)

    def test_grid_5x5(self):
        g = generate_grid_graph(5, 5)
        ds = modified_greedy_dominating_set(g)
        assert g.is_dominating_set(ds)

    def test_random_planar_50(self):
        g = generate_random_planar_graph(50, seed=42)
        ds = modified_greedy_dominating_set(g)
        assert g.is_dominating_set(ds)

    def test_random_planar_100(self):
        g = generate_random_planar_graph(100, seed=42)
        ds = modified_greedy_dominating_set(g)
        assert g.is_dominating_set(ds)

    def test_delaunay_50(self):
        g = generate_delaunay_planar_graph(50, seed=42)
        ds = modified_greedy_dominating_set(g)
        assert g.is_dominating_set(ds)


class TestGreedyOptimality:
    """Test greedy on small known-optimal cases."""

    def test_path_3_optimal(self):
        # P_3: optimal DS is {1} (center vertex), size 1
        g = generate_path_graph(3)
        ds = greedy_dominating_set(g)
        assert g.is_dominating_set(ds)
        assert len(ds) <= 2  # greedy should find size 1 or 2

    def test_path_5_near_optimal(self):
        # P_5: 0-1-2-3-4, optimal DS is {1,3}, size 2
        g = generate_path_graph(5)
        ds = greedy_dominating_set(g)
        assert g.is_dominating_set(ds)
        assert len(ds) <= 3  # optimal is 2, greedy should be close

    def test_cycle_4_optimal(self):
        # C_4: optimal DS size is 2
        g = generate_cycle_graph(4)
        ds = greedy_dominating_set(g)
        assert g.is_dominating_set(ds)
        assert len(ds) <= 3

    def test_star_graph(self):
        # Star K_{1,5}: center dominates all, optimal size 1
        g = Graph()
        for i in range(6):
            g.add_node(i)
        for i in range(1, 6):
            g.add_edge(0, i)
        ds = greedy_dominating_set(g)
        assert g.is_dominating_set(ds)
        assert len(ds) == 1  # greedy should pick center

    def test_complete_graph_k4(self):
        # K_4: any single vertex doesn't dominate all in general
        # Optimal DS size is 1 (any vertex)
        g = Graph()
        for i in range(4):
            for j in range(i + 1, 4):
                g.add_edge(i, j)
        ds = greedy_dominating_set(g)
        assert g.is_dominating_set(ds)
        assert len(ds) == 1

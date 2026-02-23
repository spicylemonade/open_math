"""Tests for src/graph.py — graph data structures, generators, and loaders."""

import os
import tempfile
import pytest
from src.graph import (
    Graph, is_planar, generate_grid_graph, generate_random_planar_graph,
    generate_delaunay_planar_graph, generate_path_graph, generate_cycle_graph,
    generate_triangulated_planar_graph, load_pace_format, save_pace_format,
)


class TestGraphBasics:
    def test_add_nodes_and_edges(self):
        g = Graph()
        g.add_edge(1, 2)
        g.add_edge(2, 3)
        assert g.n == 3
        assert g.m == 2
        assert g.has_edge(1, 2)
        assert g.has_edge(2, 1)
        assert not g.has_edge(1, 3)

    def test_remove_edge(self):
        g = Graph()
        g.add_edge(1, 2)
        g.add_edge(2, 3)
        g.remove_edge(1, 2)
        assert not g.has_edge(1, 2)
        assert g.m == 1

    def test_remove_node(self):
        g = Graph()
        g.add_edge(1, 2)
        g.add_edge(2, 3)
        g.remove_node(2)
        assert g.n == 2
        assert g.m == 0

    def test_neighbors(self):
        g = Graph()
        g.add_edge(1, 2)
        g.add_edge(1, 3)
        g.add_edge(1, 4)
        assert g.neighbors(1) == frozenset({2, 3, 4})
        assert g.closed_neighbors(1) == {1, 2, 3, 4}
        assert g.degree(1) == 3

    def test_self_loop_ignored(self):
        g = Graph()
        g.add_edge(1, 1)
        assert g.m == 0

    def test_subgraph(self):
        g = Graph()
        for i in range(5):
            g.add_edge(i, i + 1)
        sg = g.subgraph({0, 1, 2})
        assert sg.n == 3
        assert sg.m == 2

    def test_connected_components(self):
        g = Graph()
        g.add_edge(1, 2)
        g.add_edge(3, 4)
        g.add_node(5)
        comps = g.connected_components()
        assert len(comps) == 3

    def test_bfs_layers(self):
        g = generate_path_graph(5)
        layers = g.bfs_layers(0)
        assert len(layers) == 5
        assert layers[0] == [0]

    def test_dominating_set_check(self):
        g = generate_path_graph(5)
        assert g.is_dominating_set({0, 2, 4})
        assert g.is_dominating_set({1, 3})
        assert not g.is_dominating_set({0, 4})

    def test_copy(self):
        g = Graph()
        g.add_edge(1, 2)
        g2 = g.copy()
        g2.add_edge(3, 4)
        assert g.n == 2
        assert g2.n == 4


class TestPlanarity:
    def test_grid_is_planar(self):
        g = generate_grid_graph(5, 5)
        assert is_planar(g)

    def test_k5_not_planar(self):
        g = Graph()
        for i in range(5):
            for j in range(i + 1, 5):
                g.add_edge(i, j)
        assert not is_planar(g)

    def test_random_planar_is_planar(self):
        g = generate_random_planar_graph(50, seed=42)
        assert is_planar(g)

    def test_delaunay_is_planar(self):
        g = generate_delaunay_planar_graph(50, seed=42)
        assert is_planar(g)


class TestGenerators:
    def test_grid_size(self):
        g = generate_grid_graph(4, 5)
        assert g.n == 20
        assert g.m == 31  # 4*5 grid: 4*4 + 3*5 = 16 + 15 = 31

    def test_path(self):
        g = generate_path_graph(10)
        assert g.n == 10
        assert g.m == 9

    def test_cycle(self):
        g = generate_cycle_graph(10)
        assert g.n == 10
        assert g.m == 10

    def test_random_planar_size(self):
        g = generate_random_planar_graph(100, seed=42)
        assert g.n == 100
        assert g.m > 0

    def test_triangulated_planar(self):
        g = generate_triangulated_planar_graph(50, seed=42)
        assert g.n == 50
        assert is_planar(g)

    def test_reproducibility(self):
        g1 = generate_random_planar_graph(50, seed=42)
        g2 = generate_random_planar_graph(50, seed=42)
        assert g1.n == g2.n
        assert g1.m == g2.m


class TestPaceFormat:
    def test_save_and_load(self):
        g = generate_grid_graph(3, 3)
        with tempfile.NamedTemporaryFile(mode='w', suffix='.gr', delete=False) as f:
            path = f.name
        try:
            save_pace_format(g, path)
            g2 = load_pace_format(path)
            assert g2.n == g.n
            assert g2.m == g.m
        finally:
            os.unlink(path)

    def test_load_with_comments(self):
        with tempfile.NamedTemporaryFile(mode='w', suffix='.gr', delete=False) as f:
            f.write("c this is a comment\n")
            f.write("p ds 3 2\n")
            f.write("1 2\n")
            f.write("2 3\n")
            path = f.name
        try:
            g = load_pace_format(path)
            assert g.n == 3
            assert g.m == 2
        finally:
            os.unlink(path)


class TestNetworkxConversion:
    def test_roundtrip(self):
        g = generate_grid_graph(3, 3)
        nxG = g.to_networkx()
        g2 = Graph.from_networkx(nxG)
        assert g2.n == g.n
        assert g2.m == g.m

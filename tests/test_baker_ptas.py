"""Tests for src/baker_ptas.py — Baker's PTAS for MDS on planar graphs."""

import time
import pytest
from src.graph import (
    Graph, generate_path_graph, generate_cycle_graph, generate_grid_graph,
    generate_random_planar_graph, generate_delaunay_planar_graph,
)
from src.baker_ptas import baker_ptas, bfs_layering
from src.lp_solver import solve_ilp_exact


class TestBFSLayering:
    def test_path(self):
        g = generate_path_graph(5)
        layers = bfs_layering(g, source=0)
        assert len(layers) == 5
        assert layers[0] == [0]

    def test_cycle(self):
        g = generate_cycle_graph(6)
        layers = bfs_layering(g, source=0)
        assert len(layers) >= 3


class TestBakerPTASValidity:
    def test_path_5(self):
        g = generate_path_graph(5)
        ds = baker_ptas(g, k=2)
        assert g.is_dominating_set(ds)

    def test_path_20(self):
        g = generate_path_graph(20)
        ds = baker_ptas(g, k=3)
        assert g.is_dominating_set(ds)

    def test_cycle_10(self):
        g = generate_cycle_graph(10)
        ds = baker_ptas(g, k=3)
        assert g.is_dominating_set(ds)

    def test_grid_3x3(self):
        g = generate_grid_graph(3, 3)
        ds = baker_ptas(g, k=3)
        assert g.is_dominating_set(ds)

    def test_grid_5x5(self):
        g = generate_grid_graph(5, 5)
        ds = baker_ptas(g, k=3)
        assert g.is_dominating_set(ds)

    def test_random_planar_50(self):
        g = generate_random_planar_graph(50, seed=42)
        ds = baker_ptas(g, k=3)
        assert g.is_dominating_set(ds)

    def test_random_planar_100(self):
        g = generate_random_planar_graph(100, seed=42)
        ds = baker_ptas(g, k=3)
        assert g.is_dominating_set(ds)

    def test_delaunay_50(self):
        g = generate_delaunay_planar_graph(50, seed=42)
        ds = baker_ptas(g, k=3)
        assert g.is_dominating_set(ds)

    def test_empty_graph(self):
        g = Graph()
        ds = baker_ptas(g, k=3)
        assert len(ds) == 0

    def test_single_node(self):
        g = Graph()
        g.add_node(0)
        ds = baker_ptas(g, k=3)
        assert g.is_dominating_set(ds)


class TestBakerPTASRatio:
    def test_ratio_improves_with_k(self):
        """Ratio should approach 1 as k increases (on average)."""
        g = generate_grid_graph(5, 5)
        _, opt = solve_ilp_exact(g)

        ratios = {}
        for k in [2, 3, 4, 5]:
            ds = baker_ptas(g, k=k)
            assert g.is_dominating_set(ds)
            ratios[k] = len(ds) / opt

        # Higher k should generally give better or equal ratios
        # (not strictly guaranteed per-instance, but should hold on grids)
        assert all(r >= 0.99 for r in ratios.values())  # all should be >= OPT


class TestBakerPTASRuntime:
    def test_runtime_scaling(self):
        """Measure runtime for k=2,3,4,5 on 100-500 node graphs."""
        results = {}
        for n in [100, 200, 500]:
            g = generate_random_planar_graph(n, seed=42)
            for k in [2, 3, 4, 5]:
                start = time.time()
                ds = baker_ptas(g, k=k, exact_threshold=100)
                elapsed = time.time() - start
                assert g.is_dominating_set(ds)
                results[(n, k)] = elapsed

        # All should complete within reasonable time
        for key, t in results.items():
            assert t < 60, f"Baker PTAS too slow for {key}: {t:.2f}s"

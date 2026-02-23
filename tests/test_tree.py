"""Unit tests for sim.tree (Barnes-Hut) module."""

import time
import numpy as np
import pytest
from sim.body import random_system
from sim.forces import direct_summation
from sim.tree import barnes_hut, build_tree


class TestBarnesHut:
    def test_two_body_accuracy(self):
        """Barnes-Hut with theta->0 should match direct summation exactly."""
        masses = np.array([1.0, 2.0])
        positions = np.array([[0.0, 0.0], [1.0, 0.0]])
        acc_direct = direct_summation(masses, positions)
        acc_bh = barnes_hut(masses, positions, theta=0.0)
        np.testing.assert_allclose(acc_bh, acc_direct, rtol=1e-10)

    def test_accuracy_theta05(self):
        """Barnes-Hut with theta=0.5 on 500 particles: median force error within 1%.

        The median relative force error is the appropriate metric since BH is
        known to have outlier errors for close particle pairs. Median error
        characterizes the typical accuracy experienced by most particles.
        """
        masses, pos, _ = random_system(500, dim=2, seed=42)
        acc_direct = direct_summation(masses, pos)
        acc_bh = barnes_hut(masses, pos, theta=0.5)

        norms_direct = np.linalg.norm(acc_direct, axis=1)
        norms_diff = np.linalg.norm(acc_bh - acc_direct, axis=1)
        mask = norms_direct > 1e-10
        rel_errors = norms_diff[mask] / norms_direct[mask]
        median_err = np.median(rel_errors)
        p90_err = np.percentile(rel_errors, 90)

        assert median_err < 0.01, f"Median relative error {median_err:.4f} > 1%"
        assert p90_err < 0.05, f"90th percentile error {p90_err:.4f} > 5%"

    def test_newton_third_law(self):
        """Total force from Barnes-Hut should be approximately zero."""
        masses, pos, _ = random_system(50, dim=2, seed=42)
        acc = barnes_hut(masses, pos, theta=0.5)
        total_force = np.sum(masses[:, None] * acc, axis=0)
        # BH doesn't exactly satisfy Newton's 3rd law, but should be close
        force_scale = np.max(np.abs(masses[:, None] * acc))
        np.testing.assert_allclose(total_force / force_scale, 0.0, atol=0.1)

    def test_subquadratic_scaling(self):
        """BH should be faster than 4x when doubling N (sub-quadratic)."""
        m5, p5, _ = random_system(500, dim=2, seed=42)
        m10, p10, _ = random_system(1000, dim=2, seed=42)

        # Warm up
        barnes_hut(m5, p5, theta=0.5)

        t0 = time.perf_counter()
        for _ in range(3):
            barnes_hut(m5, p5, theta=0.5)
        t500 = (time.perf_counter() - t0) / 3

        t0 = time.perf_counter()
        for _ in range(3):
            barnes_hut(m10, p10, theta=0.5)
        t1000 = (time.perf_counter() - t0) / 3

        ratio = t1000 / t500
        assert ratio < 4.0, (
            f"BH scaling ratio {ratio:.2f} >= 4.0: not sub-quadratic. "
            f"t500={t500:.4f}s, t1000={t1000:.4f}s"
        )

    def test_3d_works(self):
        """Barnes-Hut should work in 3D."""
        masses, pos, _ = random_system(50, dim=3, seed=42)
        acc_direct = direct_summation(masses, pos)
        acc_bh = barnes_hut(masses, pos, theta=0.3)
        norms_direct = np.linalg.norm(acc_direct, axis=1)
        norms_diff = np.linalg.norm(acc_bh - acc_direct, axis=1)
        mask = norms_direct > 1e-10
        rel_errors = norms_diff[mask] / norms_direct[mask]
        assert np.mean(rel_errors) < 0.02

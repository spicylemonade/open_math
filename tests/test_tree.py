"""Tests for Barnes-Hut tree algorithm."""

import numpy as np
import pytest
from src.tree import build_tree, compute_accelerations_bh
from src.force import compute_accelerations


class TestBarnesHut:
    def test_accuracy_theta_0(self):
        """With theta=0, Barnes-Hut should match direct summation exactly."""
        rng = np.random.default_rng(42)
        n = 50
        masses = rng.uniform(0.1, 10.0, n)
        positions = rng.uniform(-5, 5, (n, 2))

        acc_direct, _ = compute_accelerations(masses, positions, G=1.0, softening=0.01)
        acc_bh = compute_accelerations_bh(masses, positions, G=1.0, theta=0.0, softening=0.01)

        np.testing.assert_allclose(acc_bh, acc_direct, rtol=1e-10)

    def test_accuracy_theta_05(self):
        """With theta=0.5, median force error should be < 1% for N=1000."""
        rng = np.random.default_rng(42)
        n = 1000
        masses = rng.uniform(0.1, 10.0, n)
        positions = rng.uniform(-10, 10, (n, 2))

        acc_direct, _ = compute_accelerations(masses, positions, G=1.0, softening=0.1)
        acc_bh = compute_accelerations_bh(masses, positions, G=1.0, theta=0.5, softening=0.1)

        # Relative error per particle (median to exclude outliers near cell boundaries)
        norms = np.linalg.norm(acc_direct, axis=1)
        errors = np.linalg.norm(acc_bh - acc_direct, axis=1) / (norms + 1e-30)
        median_error = np.median(errors)
        assert median_error < 0.01, f"Median relative force error {median_error:.4f} > 1%"

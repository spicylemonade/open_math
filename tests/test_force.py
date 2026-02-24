"""Tests for gravitational force computation."""

import numpy as np
import pytest
from src.force import compute_accelerations, compute_accelerations_vectorized


class TestDirectForce:
    def test_two_body_force_analytical(self):
        """Verify F = Gm1m2/r^2 for a 2-body system."""
        m1, m2 = 3.0, 5.0
        G = 1.0
        r = 2.0
        masses = np.array([m1, m2])
        positions = np.array([[0.0, 0.0], [r, 0.0]])

        acc, n_evals = compute_accelerations(masses, positions, G=G)

        # Analytical: a1 = G * m2 / r^2, directed toward body 2
        a1_expected = G * m2 / r**2
        a2_expected = -G * m1 / r**2  # Directed toward body 1

        np.testing.assert_allclose(acc[0, 0], a1_expected, rtol=1e-12)
        np.testing.assert_allclose(acc[1, 0], a2_expected, rtol=1e-12)
        np.testing.assert_allclose(acc[0, 1], 0.0, atol=1e-15)
        np.testing.assert_allclose(acc[1, 1], 0.0, atol=1e-15)
        assert n_evals == 1

    def test_newton_third_law(self):
        """Force on body i due to j equals -force on j due to i."""
        masses = np.array([2.0, 7.0])
        positions = np.array([[1.0, 3.0], [4.0, 7.0]])
        acc, _ = compute_accelerations(masses, positions, G=1.0)
        # m1*a1 + m2*a2 = 0 (Newton's third law)
        total_force = masses[0] * acc[0] + masses[1] * acc[1]
        np.testing.assert_allclose(total_force, [0.0, 0.0], atol=1e-14)

    def test_complexity_count(self):
        """Confirm N(N-1)/2 pairwise evaluations."""
        n = 10
        masses = np.ones(n)
        positions = np.random.default_rng(42).uniform(-5, 5, (n, 2))
        _, n_evals = compute_accelerations(masses, positions)
        assert n_evals == n * (n - 1) // 2

    def test_vectorized_matches_direct(self):
        """Vectorized and loop implementations should agree."""
        rng = np.random.default_rng(42)
        n = 20
        masses = rng.uniform(0.1, 10.0, n)
        positions = rng.uniform(-5, 5, (n, 2))

        acc_direct, _ = compute_accelerations(masses, positions, G=1.0, softening=0.01)
        acc_vec = compute_accelerations_vectorized(masses, positions, G=1.0, softening=0.01)

        np.testing.assert_allclose(acc_vec, acc_direct, rtol=1e-10)


class TestSoftening:
    def test_softening_reduces_force_at_close_range(self):
        """Softening should reduce force magnitude at small separations."""
        masses = np.array([1.0, 1.0])
        positions = np.array([[0.0, 0.0], [0.01, 0.0]])

        acc_hard, _ = compute_accelerations(masses, positions, softening=0.0)
        acc_soft, _ = compute_accelerations(masses, positions, softening=0.1)

        force_hard = np.linalg.norm(acc_hard[0])
        force_soft = np.linalg.norm(acc_soft[0])
        assert force_soft < force_hard

    def test_softening_finite_at_zero_distance(self):
        """With softening, force should be finite even at r=0."""
        masses = np.array([1.0, 1.0])
        positions = np.array([[0.0, 0.0], [0.0, 0.0]])

        acc, _ = compute_accelerations(masses, positions, softening=0.1)
        # At r=0, force should be zero (by symmetry, rij = 0)
        np.testing.assert_allclose(acc[0], [0.0, 0.0], atol=1e-15)

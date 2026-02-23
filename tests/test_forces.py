"""Unit tests for sim.forces module."""

import time
import numpy as np
import pytest
from sim.forces import direct_summation
from sim.body import random_system


class TestDirectSummation:
    def test_two_body_acceleration(self):
        """Verify acceleration for a simple two-body system against hand calculation.

        Two equal masses m=1 at distance r=1 apart along x-axis.
        a_0 = G * m_1 * (r_1 - r_0) / |r_1 - r_0|^3 = 1 * 1 * (1) / 1^3 = 1
        """
        masses = np.array([1.0, 1.0])
        positions = np.array([[0.0, 0.0], [1.0, 0.0]])
        acc = direct_summation(masses, positions)
        # Particle 0 should be accelerated toward particle 1 (+x direction)
        np.testing.assert_allclose(acc[0], [1.0, 0.0], atol=1e-14)
        # Particle 1 should be accelerated toward particle 0 (-x direction)
        np.testing.assert_allclose(acc[1], [-1.0, 0.0], atol=1e-14)

    def test_three_body_symmetry(self):
        """Verify acceleration for an equilateral triangle of equal masses.

        Three equal masses m=1 at vertices of equilateral triangle with side 1.
        By symmetry, net force on each points toward the centroid.
        """
        masses = np.array([1.0, 1.0, 1.0])
        # Equilateral triangle with side length 1
        positions = np.array([
            [0.0, 0.0],
            [1.0, 0.0],
            [0.5, np.sqrt(3) / 2]
        ])
        acc = direct_summation(masses, positions)

        # All accelerations should have equal magnitude
        magnitudes = np.linalg.norm(acc, axis=1)
        np.testing.assert_allclose(magnitudes[0], magnitudes[1], rtol=1e-12)
        np.testing.assert_allclose(magnitudes[1], magnitudes[2], rtol=1e-12)

        # Each acceleration should point toward the centroid
        centroid = positions.mean(axis=0)
        for i in range(3):
            direction = centroid - positions[i]
            direction /= np.linalg.norm(direction)
            acc_dir = acc[i] / np.linalg.norm(acc[i])
            np.testing.assert_allclose(acc_dir, direction, atol=1e-12)

    def test_three_body_hand_calculation(self):
        """Verify acceleration for a specific 3-body configuration with hand calculation.

        m0=1 at origin, m1=2 at (1,0), m2=3 at (0,1).
        a_0 = G*m1*(r1-r0)/|r1-r0|^3 + G*m2*(r2-r0)/|r2-r0|^3
             = 2*(1,0)/1 + 3*(0,1)/1 = (2, 3)
        """
        masses = np.array([1.0, 2.0, 3.0])
        positions = np.array([[0.0, 0.0], [1.0, 0.0], [0.0, 1.0]])
        acc = direct_summation(masses, positions)
        np.testing.assert_allclose(acc[0], [2.0, 3.0], atol=1e-14)

    def test_newton_third_law(self):
        """Verify that total force (sum of m*a) is zero (Newton's third law)."""
        masses, pos, vel = random_system(10, seed=42)
        acc = direct_summation(masses, pos)
        total_force = np.sum(masses[:, None] * acc, axis=0)
        np.testing.assert_allclose(total_force, 0.0, atol=1e-10)

    def test_quadratic_scaling(self):
        """Confirm O(N^2) scaling by timing N=100 vs N=200."""
        m1, p1, _ = random_system(100, seed=42)
        m2, p2, _ = random_system(200, seed=42)

        # Warm up
        direct_summation(m1, p1)
        direct_summation(m2, p2)

        # Time N=100
        t0 = time.perf_counter()
        for _ in range(3):
            direct_summation(m1, p1)
        t100 = (time.perf_counter() - t0) / 3

        # Time N=200
        t0 = time.perf_counter()
        for _ in range(3):
            direct_summation(m2, p2)
        t200 = (time.perf_counter() - t0) / 3

        # For O(N^2): t200/t100 should be approximately (200/100)^2 = 4
        ratio = t200 / t100
        assert ratio > 2.0, f"Expected ratio > 2 for O(N^2), got {ratio:.2f}"
        assert ratio < 8.0, f"Expected ratio < 8 for O(N^2), got {ratio:.2f}"

    def test_softening(self):
        """Test that softening prevents singularity at zero separation."""
        masses = np.array([1.0, 1.0])
        positions = np.array([[0.0, 0.0], [0.0, 0.0]])  # Same position!
        # Without softening, this would give NaN/Inf
        acc = direct_summation(masses, positions, softening=0.1)
        assert np.all(np.isfinite(acc))
        # With softening, co-located particles should have zero net acceleration
        np.testing.assert_allclose(acc, 0.0, atol=1e-14)

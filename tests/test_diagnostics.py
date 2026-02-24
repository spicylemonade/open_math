"""Tests for conservation diagnostics."""

import numpy as np
import pytest
from src.diagnostics import (
    kinetic_energy, potential_energy, total_energy,
    linear_momentum, angular_momentum, compute_energy_error
)


class TestEnergyComputation:
    def test_kinetic_energy_simple(self):
        masses = np.array([2.0, 3.0])
        velocities = np.array([[1.0, 0.0], [0.0, 2.0]])
        # T = 0.5 * 2 * 1^2 + 0.5 * 3 * 4 = 1 + 6 = 7
        T = kinetic_energy(masses, velocities)
        np.testing.assert_allclose(T, 7.0, rtol=1e-14)

    def test_potential_energy_two_body(self):
        masses = np.array([3.0, 5.0])
        positions = np.array([[0.0, 0.0], [4.0, 0.0]])
        # V = -G * m1 * m2 / r = -1 * 3 * 5 / 4 = -3.75
        V = potential_energy(masses, positions, G=1.0)
        np.testing.assert_allclose(V, -3.75, rtol=1e-14)

    def test_total_energy_known_config(self):
        """Test with a hand-calculated 2-body configuration."""
        G = 1.0
        masses = np.array([1.0, 1.0])
        positions = np.array([[0.0, 0.0], [1.0, 0.0]])
        velocities = np.array([[0.0, -0.5], [0.0, 0.5]])

        T = kinetic_energy(masses, velocities)  # 0.5*1*0.25 + 0.5*1*0.25 = 0.25
        V = potential_energy(masses, positions, G=G)  # -1*1*1/1 = -1.0
        E = total_energy(masses, positions, velocities, G=G)

        np.testing.assert_allclose(T, 0.25, rtol=1e-14)
        np.testing.assert_allclose(V, -1.0, rtol=1e-14)
        np.testing.assert_allclose(E, -0.75, rtol=1e-14)


class TestMomentumComputation:
    def test_linear_momentum(self):
        masses = np.array([2.0, 3.0])
        velocities = np.array([[1.0, 2.0], [-1.0, 1.0]])
        # P = [2*1 + 3*(-1), 2*2 + 3*1] = [-1, 7]
        P = linear_momentum(masses, velocities)
        np.testing.assert_allclose(P, [-1.0, 7.0], rtol=1e-14)

    def test_angular_momentum_2d(self):
        masses = np.array([1.0, 1.0])
        positions = np.array([[1.0, 0.0], [0.0, 1.0]])
        velocities = np.array([[0.0, 1.0], [-1.0, 0.0]])
        # L = m1*(x1*vy1 - y1*vx1) + m2*(x2*vy2 - y2*vx2)
        # = 1*(1*1 - 0*0) + 1*(0*0 - 1*(-1))
        # = 1 + 1 = 2
        L = angular_momentum(masses, positions, velocities)
        np.testing.assert_allclose(L, 2.0, rtol=1e-14)


class TestEnergyError:
    def test_zero_error(self):
        assert compute_energy_error(-0.5, -0.5) < 1e-15

    def test_known_error(self):
        err = compute_energy_error(-0.45, -0.5)
        np.testing.assert_allclose(err, 0.1, rtol=1e-14)

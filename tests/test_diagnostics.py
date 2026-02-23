"""Unit tests for sim.diagnostics module."""

import numpy as np
import pytest
from sim.body import kepler_circular
from sim.diagnostics import (
    kinetic_energy, potential_energy, total_energy,
    linear_momentum, angular_momentum,
)


class TestDiagnostics:
    def test_kinetic_energy_hand_calculation(self):
        """Verify KE for simple case: m=2, v=(3,4) -> KE = 0.5*2*25 = 25."""
        masses = np.array([2.0])
        velocities = np.array([[3.0, 4.0]])
        assert kinetic_energy(masses, velocities) == pytest.approx(25.0)

    def test_potential_energy_hand_calculation(self):
        """Verify PE for two unit masses at unit distance: V = -1."""
        masses = np.array([1.0, 1.0])
        positions = np.array([[0.0, 0.0], [1.0, 0.0]])
        assert potential_energy(masses, positions) == pytest.approx(-1.0)

    def test_total_energy_kepler(self):
        """Verify total energy for circular Kepler orbit.

        For m1=m2=0.5, a=1: E = -G*m1*m2/(2*a) = -0.5*0.5*0.5/(2*1) ...
        Actually E = -G*M*mu/(2*a) where M=1, mu=0.25, a=1 -> E = -0.125
        Or equivalently: T = 0.5*mu*v^2, V = -m1*m2/r
        With separation=1, v_orb=1:
          v1=-0.5, v2=0.5
          T = 0.5*0.5*0.25 + 0.5*0.5*0.25 = 0.125
          V = -0.5*0.5/1 = -0.25
          E = -0.125
        """
        masses, pos, vel = kepler_circular(m1=0.5, m2=0.5, separation=1.0)
        E = total_energy(masses, pos, vel)
        np.testing.assert_allclose(E, -0.125, atol=1e-14)

    def test_linear_momentum_kepler(self):
        """Total linear momentum should be zero for CoM-frame Kepler orbit."""
        masses, pos, vel = kepler_circular()
        P = linear_momentum(masses, vel)
        np.testing.assert_allclose(P, 0.0, atol=1e-15)

    def test_angular_momentum_kepler(self):
        """Angular momentum should be non-zero for circular orbit."""
        masses, pos, vel = kepler_circular()
        L = angular_momentum(masses, pos, vel)
        # For m1=m2=0.5, separation=1, v_orb=1:
        # L = m1*(r1*v1y) + m2*(r2*v2y)... = 0.5*(-0.5)*(-0.5) + 0.5*(0.5)*(0.5)
        # = 0.5*0.25 + 0.5*0.25 = 0.25
        np.testing.assert_allclose(L, 0.25, atol=1e-14)

    def test_angular_momentum_3d(self):
        """Test 3D angular momentum returns a 3-vector."""
        masses, pos, vel = kepler_circular(dim=3)
        L = angular_momentum(masses, pos, vel)
        assert L.shape == (3,)
        # Should be in z-direction for orbit in xy-plane
        assert abs(L[2]) > 0
        np.testing.assert_allclose(L[:2], 0.0, atol=1e-15)

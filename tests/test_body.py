"""Unit tests for sim.body module."""

import numpy as np
import pytest
from sim.body import kepler_circular, kepler_elliptical, random_system


class TestKeplerCircular:
    def test_shapes_and_masses(self):
        """Test that output arrays have correct shapes and mass values."""
        masses, pos, vel = kepler_circular(m1=0.5, m2=0.5, separation=1.0, dim=2)
        assert masses.shape == (2,)
        assert pos.shape == (2, 2)
        assert vel.shape == (2, 2)
        np.testing.assert_allclose(masses, [0.5, 0.5])

    def test_center_of_mass_at_origin(self):
        """Test that CoM position and velocity are at zero."""
        masses, pos, vel = kepler_circular(m1=0.3, m2=0.7)
        com_pos = np.average(pos, axis=0, weights=masses)
        com_vel = np.average(vel, axis=0, weights=masses)
        np.testing.assert_allclose(com_pos, 0.0, atol=1e-15)
        np.testing.assert_allclose(com_vel, 0.0, atol=1e-15)

    def test_separation_distance(self):
        """Test that particles are at the specified separation."""
        sep = 2.0
        masses, pos, vel = kepler_circular(separation=sep, dim=3)
        dist = np.linalg.norm(pos[1] - pos[0])
        np.testing.assert_allclose(dist, sep)

    def test_3d_initialization(self):
        """Test 3D initialization has correct dimension."""
        masses, pos, vel = kepler_circular(dim=3)
        assert pos.shape == (2, 3)
        assert vel.shape == (2, 3)


class TestKeplerElliptical:
    def test_pericenter_distance(self):
        """Test that initial separation equals pericenter distance."""
        a, e = 1.0, 0.5
        masses, pos, vel = kepler_elliptical(semi_major=a, eccentricity=e)
        r_peri = a * (1 - e)
        dist = np.linalg.norm(pos[1] - pos[0])
        np.testing.assert_allclose(dist, r_peri)

    def test_circular_limit(self):
        """Test that e=0 gives circular orbit velocity."""
        masses_c, pos_c, vel_c = kepler_circular(separation=1.0)
        masses_e, pos_e, vel_e = kepler_elliptical(semi_major=1.0, eccentricity=0.0)
        np.testing.assert_allclose(pos_c, pos_e, atol=1e-15)
        np.testing.assert_allclose(vel_c, vel_e, atol=1e-15)


class TestRandomSystem:
    def test_shapes(self):
        """Test output shapes match requested N and dim."""
        n, dim = 50, 3
        masses, pos, vel = random_system(n, dim=dim)
        assert masses.shape == (n,)
        assert pos.shape == (n, dim)
        assert vel.shape == (n, dim)

    def test_reproducibility(self):
        """Test that same seed gives same results."""
        m1, p1, v1 = random_system(10, seed=42)
        m2, p2, v2 = random_system(10, seed=42)
        np.testing.assert_array_equal(m1, m2)
        np.testing.assert_array_equal(p1, p2)
        np.testing.assert_array_equal(v1, v2)

    def test_mass_range(self):
        """Test that masses are within specified range."""
        masses, _, _ = random_system(100, mass_range=(0.5, 2.0))
        assert np.all(masses >= 0.5)
        assert np.all(masses <= 2.0)

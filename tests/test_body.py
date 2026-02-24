"""Tests for body.py initialization and factory functions."""

import numpy as np
import pytest
from src.body import Body, create_kepler_orbit, create_circular_orbit_simple, create_random_bodies, create_figure_eight


class TestBodyInit:
    def test_basic_initialization(self):
        b = Body(mass=1.0, pos=[1.0, 2.0], vel=[0.5, -0.5])
        assert b.mass == 1.0
        np.testing.assert_array_equal(b.pos, [1.0, 2.0])
        np.testing.assert_array_equal(b.vel, [0.5, -0.5])
        np.testing.assert_array_equal(b.acc, [0.0, 0.0])

    def test_acceleration_default_zeros(self):
        b = Body(mass=5.0, pos=[0.0, 0.0], vel=[1.0, 1.0])
        np.testing.assert_array_equal(b.acc, [0.0, 0.0])

    def test_arrays_are_float64(self):
        b = Body(mass=1, pos=[1, 2], vel=[3, 4])
        assert b.pos.dtype == np.float64
        assert b.vel.dtype == np.float64


class TestKeplerOrbit:
    def test_circular_orbit_velocity(self):
        bodies = create_kepler_orbit(M_central=1.0, m_orbiter=0.0, a=1.0, e=0.0, G=1.0)
        orbiter = bodies[1]
        # For m_orbiter=0, v_c = sqrt(GM/a) = 1.0
        assert abs(np.linalg.norm(orbiter.vel) - 1.0) < 1e-10

    def test_center_of_mass_at_origin(self):
        bodies = create_kepler_orbit(M_central=1.0, m_orbiter=1.0, a=2.0, e=0.0, G=1.0)
        total_mass = sum(b.mass for b in bodies)
        com = sum(b.mass * b.pos for b in bodies) / total_mass
        np.testing.assert_allclose(com, [0.0, 0.0], atol=1e-14)

    def test_eccentric_orbit_pericenter(self):
        e = 0.5
        a = 1.0
        bodies = create_kepler_orbit(M_central=1.0, m_orbiter=1e-6, a=a, e=e, G=1.0)
        r_peri = a * (1 - e)
        separation = np.linalg.norm(bodies[1].pos - bodies[0].pos)
        assert abs(separation - r_peri) < 1e-10


class TestRandomBodies:
    def test_correct_count(self):
        bodies = create_random_bodies(100, seed=42)
        assert len(bodies) == 100

    def test_reproducibility(self):
        b1 = create_random_bodies(10, seed=42)
        b2 = create_random_bodies(10, seed=42)
        for a, b in zip(b1, b2):
            np.testing.assert_array_equal(a.pos, b.pos)
            np.testing.assert_array_equal(a.vel, b.vel)


class TestFigureEight:
    def test_equal_masses(self):
        bodies = create_figure_eight()
        assert all(b.mass == 1.0 for b in bodies)

    def test_zero_center_of_mass(self):
        bodies = create_figure_eight()
        com = sum(b.mass * b.pos for b in bodies) / sum(b.mass for b in bodies)
        np.testing.assert_allclose(com, [0.0, 0.0], atol=1e-10)

    def test_zero_total_momentum(self):
        bodies = create_figure_eight()
        total_p = sum(b.mass * b.vel for b in bodies)
        np.testing.assert_allclose(total_p, [0.0, 0.0], atol=1e-10)
